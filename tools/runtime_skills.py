"""Repository-local runtime skills for the LangChain bioinformatics agent.

This is intentionally separate from Codex's `.agents/skills` discovery. The
bioinformatics agent only sees compact metadata until it explicitly calls the
bounded loader tool for one relevant skill.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from langchain_core.tools import tool


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SKILL_ROOT = PROJECT_ROOT / "agent_skills"
REFERENCE_EXTENSIONS = {".md", ".txt", ".json"}
MAX_SKILL_CHARS = 60_000


@dataclass(frozen=True)
class RuntimeSkill:
    name: str
    description: str
    path: Path
    instructions: str


def _parse_skill(path: Path) -> RuntimeSkill:
    text = path.read_text(encoding="utf-8")
    match = re.match(r"\A---\s*\n(.*?)\n---\s*\n?(.*)\Z", text, flags=re.DOTALL)
    if not match:
        raise ValueError(f"Skill frontmatter is missing or malformed: {path}")
    metadata: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip().strip('"\'')
    name = metadata.get("name", "")
    description = metadata.get("description", "")
    if not re.fullmatch(r"[a-z0-9-]{1,63}", name):
        raise ValueError(f"Invalid runtime skill name in {path}: {name!r}")
    if not description:
        raise ValueError(f"Runtime skill description is required: {path}")
    return RuntimeSkill(name=name, description=description, path=path, instructions=match.group(2).strip())


def discover_runtime_skills(skill_root: str | Path = DEFAULT_SKILL_ROOT) -> tuple[RuntimeSkill, ...]:
    root = Path(skill_root).resolve()
    if not root.is_dir():
        return ()
    skills = [_parse_skill(path) for path in sorted(root.glob("*/SKILL.md"))]
    names = [skill.name for skill in skills]
    if len(names) != len(set(names)):
        raise ValueError("Runtime skill registry contains duplicate names.")
    return tuple(skills)


def render_runtime_skill_catalog(skills: tuple[RuntimeSkill, ...]) -> str:
    if not skills:
        return ""
    lines = [
        "RUNTIME SKILLS (progressive disclosure):",
        "The following trusted project workflows are available. When one clearly matches the "
        "request, call load_runtime_skill once before planning or calling scientific tools. "
        "Do not load unrelated skills.",
    ]
    lines.extend(f"- {skill.name}: {skill.description}" for skill in skills)
    return "\n".join(lines)


def load_runtime_skill_bundle(
    skill_name: str,
    skill_root: str | Path = DEFAULT_SKILL_ROOT,
    *,
    include_references: bool = True,
) -> str:
    skills = {skill.name: skill for skill in discover_runtime_skills(skill_root)}
    if skill_name not in skills:
        available = ", ".join(sorted(skills)) or "none"
        raise ValueError(f"Unknown runtime skill {skill_name!r}. Available: {available}")
    skill = skills[skill_name]
    parts = [
        f"RUNTIME SKILL LOADED: {skill.name}",
        f"Description: {skill.description}",
        "",
        skill.instructions,
    ]
    if include_references:
        reference_root = skill.path.parent / "references"
        if reference_root.is_dir():
            for path in sorted(reference_root.rglob("*")):
                if path.is_file() and path.suffix.lower() in REFERENCE_EXTENSIONS:
                    relative = path.relative_to(skill.path.parent)
                    parts.extend(["", f"REFERENCE: {relative.as_posix()}", path.read_text(encoding="utf-8")])
    bundle = "\n".join(parts)
    if len(bundle) > MAX_SKILL_CHARS:
        raise ValueError(f"Runtime skill {skill_name!r} exceeds {MAX_SKILL_CHARS} characters.")
    return bundle


@tool
def load_runtime_skill(skill_name: str) -> str:
    """Load one trusted project workflow by exact name before planning relevant analysis.

    Use only a name listed under RUNTIME SKILLS in the system prompt. The loader is read-only,
    only reads repository-local SKILL.md and text/JSON references, and never executes skill scripts.
    """
    try:
        return load_runtime_skill_bundle(skill_name)
    except Exception as exc:
        return f"Runtime skill load failed. Error: {type(exc).__name__}: {exc}"
