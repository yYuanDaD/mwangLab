"""Per-tool-call token accounting for the 45-paper Claude large run.

Reads Claude Code session transcripts (~/.claude/projects/**/*.jsonl), keeps the ones that
worked on runs_claude papers, and writes two CSVs next to this script:

- transcripts.csv: one row per kept transcript (paper, turns, final context, summed usage).
- calls.csv: one row per tool call, with the tokens it added to the context.

Attribution: for assistant turn i, context(i) = input + cache_creation + cache_read tokens.
Tokens added by the tool results of turn i = context(i+1) - context(i) - output(i). When a
turn has several tool calls, that delta is split by tool-result length. Output tokens are split
between tool-call input (chars / 3.5, capped) and thinking/text. The first turn's context is
the baseline (system prompt, task brief, loaded skill). Summed over a transcript, the
attributed tokens equal its final context, which is what the run reported as subagent_tokens.

Only metadata leaves the transcript: tool names, file paths, the first 300 characters of each
command, and token counts. No tool output text is written.

Stdlib only:  python extract_usage.py [--projects DIR] [--progress PATH]
"""

import argparse
import csv
import json
import os
import re
from collections import OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_PROGRESS = (HERE.parent / "large_run_pilot_20261019" / "runs_claude" / "progress.csv")


def load_papers(progress_csv):
    papers = {}
    with open(progress_csv, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            ids = [row["paper_id"]] + [g for g in row["gse"].split(";") if g]
            papers[row["paper_id"]] = ids
    return papers


def text_of(content):
    if isinstance(content, str):
        return content
    parts = []
    for block in content or []:
        if isinstance(block, dict):
            if block.get("type") == "text":
                parts.append(block.get("text", ""))
            elif block.get("type") == "tool_result":
                parts.append(text_of(block.get("content")))
    return "\n".join(parts)


def match_paper(prompt, papers):
    hits = []
    for pid, ids in papers.items():
        pos = [prompt.find(i) for i in ids if i and prompt.find(i) >= 0]
        if pos:
            hits.append((min(pos), pid))
    hits.sort()
    return [pid for _, pid in hits]


def describe(tool, inp):
    if not isinstance(inp, dict):
        return ""
    if tool == "Bash":
        return (inp.get("command") or "")[:300]
    for key in ("file_path", "notebook_path", "path", "pattern", "skill", "url", "description"):
        if inp.get(key):
            extra = inp.get("path") if key == "pattern" else None
            return f"{inp[key]}" + (f" @ {extra}" if extra else "")
    return json.dumps(inp, ensure_ascii=False)[:200]


def parse(path):
    """Return (meta, turns, results). turns: ordered assistant messages with usage and tool uses."""
    turns = OrderedDict()
    results = {}
    first_user = None
    meta = {"cwd": None, "sidechain": None, "first_ts": None, "last_ts": None}
    with open(path, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            try:
                rec = json.loads(line)
            except ValueError:
                continue
            ts = rec.get("timestamp")
            if ts:
                meta["first_ts"] = meta["first_ts"] or ts
                meta["last_ts"] = ts
            meta["cwd"] = meta["cwd"] or rec.get("cwd")
            if meta["sidechain"] is None and "isSidechain" in rec:
                meta["sidechain"] = rec.get("isSidechain")
            msg = rec.get("message") or {}
            if rec.get("type") == "user":
                content = msg.get("content")
                if first_user is None and not (isinstance(content, list) and any(
                        isinstance(b, dict) and b.get("type") == "tool_result" for b in content)):
                    first_user = text_of(content)
                if isinstance(content, list):
                    for b in content:
                        if isinstance(b, dict) and b.get("type") == "tool_result":
                            results[b.get("tool_use_id")] = len(text_of(b.get("content")))
            elif rec.get("type") == "assistant" and msg.get("usage"):
                mid = msg.get("id") or rec.get("uuid")
                t = turns.setdefault(mid, {"blocks": [], "usage": None})
                t["blocks"].extend(b for b in msg.get("content") or [] if isinstance(b, dict))
                t["usage"] = msg["usage"]
                t["model"] = msg.get("model") or t.get("model")
    meta["prompt"] = first_user or ""
    return meta, list(turns.values()), results


def ctx(u):
    return (u.get("input_tokens", 0) + u.get("cache_creation_input_tokens", 0)
            + u.get("cache_read_input_tokens", 0))


def analyse(path, paper, meta, turns, results):
    rows = []
    for i, t in enumerate(turns):
        u = t["usage"]
        out = u.get("output_tokens", 0)
        nxt = ctx(turns[i + 1]["usage"]) if i + 1 < len(turns) else None
        added = max(nxt - ctx(u) - out, 0) if nxt is not None else 0
        uses = [b for b in t["blocks"] if b.get("type") == "tool_use"]
        talk = sum(len(b.get("text") or b.get("thinking") or "") for b in t["blocks"]
                   if b.get("type") in ("text", "thinking"))
        if i == 0:
            rows.append({"turn": -1, "tool": "(baseline)", "desc": "system prompt + brief + skill",
                         "result_tokens": ctx(u), "output_tokens": 0, "result_chars": 0,
                         "input_chars": 0})
        in_chars = [len(json.dumps(b.get("input"), ensure_ascii=False)) for b in uses]
        tool_out = [min(c / 3.5, out) for c in in_chars]
        scale = min(1.0, out / sum(tool_out)) if sum(tool_out) else 0
        tool_out = [x * scale for x in tool_out]
        res_chars = [results.get(b.get("id"), 0) for b in uses]
        total_res = sum(res_chars)
        for j, b in enumerate(uses):
            share = (res_chars[j] / total_res) if total_res else 1 / len(uses)
            rows.append({"turn": i, "tool": b.get("name"), "desc": describe(b.get("name"), b.get("input")),
                         "result_tokens": round(added * share), "output_tokens": round(tool_out[j]),
                         "result_chars": res_chars[j], "input_chars": in_chars[j]})
        rest = out - round(sum(tool_out))
        if not uses:
            rest, extra = out, added
        else:
            extra = 0
        if rest > 0 or extra > 0:
            rows.append({"turn": i, "tool": "(thinking/text)", "desc": f"{talk} chars",
                         "result_tokens": extra, "output_tokens": rest, "result_chars": 0,
                         "input_chars": talk})
    summary = {
        "file": str(path), "paper_id": paper, "sidechain": meta["sidechain"], "cwd": meta["cwd"],
        "first_ts": meta["first_ts"], "last_ts": meta["last_ts"], "turns": len(turns),
        "final_context": ctx(turns[-1]["usage"]) + turns[-1]["usage"].get("output_tokens", 0),
        "sum_output": sum(t["usage"].get("output_tokens", 0) for t in turns),
        "sum_cache_read": sum(t["usage"].get("cache_read_input_tokens", 0) for t in turns),
        "sum_cache_creation": sum(t["usage"].get("cache_creation_input_tokens", 0) for t in turns),
        "sum_input": sum(t["usage"].get("input_tokens", 0) for t in turns),
        "models": ";".join(sorted({t.get("model") or "" for t in turns} - {""})),
    }
    return summary, rows


def main():
    ap = argparse.ArgumentParser()
    root = Path(os.environ.get("CLAUDE_CONFIG_DIR", Path.home() / ".claude")) / "projects"
    ap.add_argument("--projects", default=str(root))
    ap.add_argument("--progress", default=str(DEFAULT_PROGRESS))
    ap.add_argument("--out", default=str(HERE))
    ap.add_argument("--match", default="runs_claude|large_run",
                    help="regex the first prompt must contain (default: the 45-paper run)")
    args = ap.parse_args()
    papers = load_papers(args.progress)
    out = Path(args.out)
    summaries, calls = [], []
    scanned = 0
    for path in sorted(Path(args.projects).rglob("*.jsonl")):
        scanned += 1
        try:
            meta, turns, results = parse(path)
        except OSError:
            continue
        if not turns:
            continue
        prompt = meta["prompt"]
        if not re.search(args.match, prompt):
            continue
        hits = match_paper(prompt, papers)
        if not hits:
            paper = "(none)"
        elif len(hits) == 1:
            paper = hits[0]
        else:
            paper = "(multi:" + ";".join(hits[:5]) + ")"
        summary, rows = analyse(path, paper, meta, turns, results)
        summary["prompt_head"] = re.sub(r"\s+", " ", prompt)[:200]
        summaries.append(summary)
        for r in rows:
            calls.append({"file": path.name, "paper_id": paper, **r})
    for name, rows in (("transcripts.csv", summaries), ("calls.csv", calls)):
        with open(out / name, "w", newline="", encoding="utf-8") as fh:
            if rows:
                w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
                w.writeheader()
                w.writerows(rows)
    print(f"scanned {scanned} transcripts, kept {len(summaries)}, {len(calls)} call rows -> {out}")


if __name__ == "__main__":
    main()
