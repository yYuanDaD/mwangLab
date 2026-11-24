"""Run the remaining papers of the 211-paper run, one fresh headless Claude session per paper.

Owner 2026-11-24: "一篇文章就用一个会话跑完，然后把结果汇总". Each paper gets its own `claude -p`
session (Opus, prompt from PROMPT_211.md via prompt_for.py); then finish_paper.py, a fresh Sonnet
review session (review_paper.py prepare/record), FIX ITEMS sent once back to the analysis session
(`--resume`), and a commit + push of that paper. No orchestrator context accumulates.

When a session hits the usage limit the worker sleeps and resumes the same session after the reset.
Rows whose run folder already exists but are not in progress.csv are skipped (in flight elsewhere or
interrupted: handle by hand per RESUME_211.md).

    python test/experiments/large_run_pilot_20261019/run_211_driver.py --workers 5 [--limit N] [--dry-run]
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
import threading
import time
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
RUNS = os.path.join(HERE, "runs_claude")
PY = sys.executable
LOG = os.path.join(RUNS, "driver_log.csv")
TOOLS = ["Bash", "Read", "Write", "Edit", "Glob", "Grep", "Skill"]
LIMIT_WAIT_S = 15 * 60
LOCK = threading.Lock()


def log(msg):
    line = f"{datetime.now():%Y-%m-%d %H:%M:%S} {msg}"
    with LOCK:
        print(line, flush=True)
        with open(os.path.join(RUNS, "driver.out"), "a", encoding="utf-8") as f:
            f.write(line + "\n")


def run_py(args):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([PY] + args, cwd=REPO, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env)
    return p.stdout + p.stderr


def claude(prompt, model, resume=None):
    """One headless session call; retries the same session after a usage-limit stop."""
    session = resume
    text = prompt
    t0 = time.time()
    tokens = 0
    while True:
        cmd = ["claude", "-p", "--model", model, "--output-format", "json",
               "--permission-mode", "acceptEdits", "--allowedTools", *TOOLS]
        if session:
            cmd += ["--resume", session]
        p = subprocess.run(cmd, input=text, cwd=REPO, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=4 * 3600)
        try:
            out = json.loads(p.stdout.strip().splitlines()[-1])
        except Exception:
            out = {"is_error": True, "result": (p.stdout + p.stderr)[-2000:]}
        session = out.get("session_id") or session
        u = out.get("usage") or {}
        tokens += sum(int(u.get(k) or 0) for k in ("input_tokens", "output_tokens",
                                                     "cache_creation_input_tokens",
                                                     "cache_read_input_tokens"))
        result = str(out.get("result") or "")
        low = result.lower()
        if out.get("is_error") and ("not logged in" in low or "/login" in low):
            raise RuntimeError("claude CLI is not logged in; run `claude` then /login once, and restart the driver")
        if out.get("is_error") and ("limit" in low or "429" in low or "overloaded" in low):
            log(f"usage limit/overload ({model}); sleeping {LIMIT_WAIT_S // 60} min then resuming {session}")
            time.sleep(LIMIT_WAIT_S)
            text = "The usage limit has reset. Continue from where you stopped (do not restart) and finish as originally asked."
            if not session:
                text = prompt
            continue
        return result, session, (time.time() - t0) / 60, tokens, bool(out.get("is_error"))


def field(text, name):
    m = re.search(rf"^{name}:\s*(.*)$", text, re.M)
    return m.group(1).strip() if m else ""


def pending():
    q = {r["n"]: r for r in csv.DictReader(open(os.path.join(HERE, "queue_211.csv"), encoding="utf-8"))}
    done = {r["paper_id"] for r in csv.DictReader(open(os.path.join(RUNS, "progress.csv"), encoding="utf-8"))}
    order = open(os.path.join(HERE, "run_order_211.txt")).read().strip().split(",")
    out = []
    for n in order:
        pid = q[n]["paper_id"]
        if pid in done or os.path.isdir(os.path.join(RUNS, pid)):
            continue
        out.append((n, pid, q[n]["gse"]))
    return out


def commit(pid, what):
    with LOCK:
        rel = os.path.relpath(RUNS, REPO).replace("\\", "/")
        subprocess.run(["git", "add", f"{rel}/{pid}", f"{rel}/progress.csv", f"{rel}/PROBLEMS.md",
                        f"{rel}/REVIEW_QUEUE.md", f"{rel}/driver_log.csv"], cwd=REPO, capture_output=True)
        subprocess.run(["git", "commit", "-q", "-m",
                        f"211-paper run: {what}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"],
                       cwd=REPO, capture_output=True)
        for _ in range(4):
            if subprocess.run(["git", "push", "-q", "origin", "HEAD"], cwd=REPO,
                              capture_output=True).returncode == 0:
                break
            time.sleep(20)


def do_paper(n, pid, gse):
    prompt = run_py([os.path.join(HERE, "prompt_for.py"), n]).split("\n", 1)[1].strip()
    log(f"start row {n} {pid}")
    res, sid, mins, toks, err = claude(prompt, "claude-opus-5-5")
    status = field(res, "STATUS") or ("failed" if err else "failed")
    vs = field(res, "VS_PAPER") or res.strip().replace("\n", " ")[:200]
    probs = field(res, "PROBLEMS") or "none"
    with LOCK:
        val = run_py([os.path.join(HERE, "finish_paper.py"), pid, gse, f"{mins:.1f}", str(toks),
                      status, vs, probs]).strip().splitlines()[-1:]
    log(f"row {n} {pid}: {status} | {vs[:120]} | {val}")
    review = "none"
    if os.path.isdir(os.path.join(RUNS, pid)):
        prep = run_py([os.path.join(HERE, "review_paper.py"), "prepare", pid])
        rprompt = "\n".join(l for l in prep.splitlines() if not l.startswith("# ")).strip()
        if "Cases to review" in rprompt:
            rres, _, rmins, rtoks, _ = claude(rprompt, "claude-sonnet-5-5")
            with LOCK:
                rec = run_py([os.path.join(HERE, "review_paper.py"), "record", pid, f"{rmins:.1f}", str(rtoks)])
            review = " ".join(l.strip() for l in rec.splitlines() if ": " in l and "FIX" not in l)[:200]
            if "FIX ITEMS" in rec:
                items = rec.split("FIX ITEMS", 1)[1].split("\n", 1)[1].strip()
                msg = ("The review of your run came back \"fix\". Apply these items once, or answer in writing why "
                       "not, then update HANDBACK.md:\n\n" + items + "\n\nRun `execute` again if the run changes. "
                       "Same rules as before (no commit/push, no tool code changes). Reply with exactly two lines:\n"
                       "RESOLUTION: applied | rebutted | skipped — <one line>\nVS_PAPER: <updated one line of at most 200 characters>")
                fres, _, fmins, ftoks, _ = claude(msg, "claude-opus-5-5", resume=sid)
                resol = field(fres, "RESOLUTION")
                kind = next((k for k in ("applied", "rebutted", "skipped") if resol.lower().startswith(k)), "skipped")
                with LOCK:
                    run_py([os.path.join(HERE, "review_paper.py"), "resolve", pid, kind, resol[:200] or kind])
                    if kind == "applied":
                        run_py([os.path.join(HERE, "record_run.py"), pid, gse, f"{mins + fmins:.1f}",
                                str(toks + ftoks), status, field(fres, "VS_PAPER") or vs])
                review += f" | fix {kind}"
    with LOCK:
        new = not os.path.exists(LOG)
        with open(LOG, "a", encoding="utf-8", newline="") as f:
            w = csv.writer(f)
            if new:
                w.writerow(["time", "row", "paper_id", "status", "minutes", "tokens", "review", "vs_paper"])
            w.writerow([f"{datetime.now():%Y-%m-%d %H:%M}", n, pid, status, f"{mins:.1f}", toks, review, vs])
    commit(pid, f"row {n} ({pid}) via driver")
    log(f"done row {n} {pid}: review {review}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--limit", type=int, default=0)
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    todo = pending()
    if a.limit:
        todo = todo[:a.limit]
    log(f"driver start: {len(todo)} rows, {a.workers} workers: {[t[0] for t in todo][:20]}")
    if a.dry_run:
        return
    it = iter(todo)

    def worker():
        while True:
            with LOCK:
                nxt = next(it, None)
            if nxt is None:
                return
            try:
                do_paper(*nxt)
            except RuntimeError as e:  # not logged in: stop this worker, leave the row unrecorded
                log(f"row {nxt[0]} {nxt[1]} stopped: {e}")
                return
            except Exception as e:  # keep the batch going
                log(f"row {nxt[0]} {nxt[1]} crashed: {type(e).__name__}: {e}")

    ths = [threading.Thread(target=worker) for _ in range(a.workers)]
    for t in ths:
        t.start()
    for t in ths:
        t.join()
    log("driver finished")


if __name__ == "__main__":
    main()
