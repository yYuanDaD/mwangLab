"""Persistent run status plus an optional single-line terminal renderer."""

from __future__ import annotations

from datetime import datetime
import json
import os
import sys
from threading import RLock
import time
from typing import Literal, TextIO

from pydantic import BaseModel, Field


RunState = Literal["pending", "running", "waiting_approval", "completed", "partial", "failed"]


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


class RunStatus(BaseModel):
    schema_version: str = "1.0"
    run_id: str
    profile: str
    status: RunState = "pending"
    accession: str | None = None
    study_index: int = 0
    study_total: int = 0
    stage: str = "pending"
    stage_index: int = 0
    stage_total: int = 0
    completed_stages: list[str] = Field(default_factory=list)
    current_tool: str | None = None
    elapsed_seconds: float = 0.0
    llm_calls: int = 0
    estimated_cost_usd: float = 0.0
    warning_count: int = 0
    failure_count: int = 0
    message: str = ""
    evidence_ids: list[str] = Field(default_factory=list)
    started_at: str = Field(default_factory=_now)
    updated_at: str = Field(default_factory=_now)
    finished_at: str | None = None


class ConsoleStatusRenderer:
    """Render one compact ASCII line; avoids Windows console emoji/encoding issues."""

    def __init__(self, stream: TextIO | None = None):
        self.stream = stream or sys.stdout
        self._last_width = 0

    def render(self, status: RunStatus, *, final: bool = False) -> None:
        if hasattr(self.stream, "isatty") and not self.stream.isatty():
            return
        study = f" [{status.accession} {status.study_index}/{status.study_total}]" if status.accession else ""
        stages = f" {status.stage_index}/{status.stage_total} stages" if status.stage_total else ""
        tool = f" tool={status.current_tool}" if status.current_tool else ""
        counters = f" warn={status.warning_count} fail={status.failure_count}"
        line = (f"[RUN {status.run_id}] [{status.status}]" + study
                + f" [{status.stage}]" + stages + tool
                + f" {status.elapsed_seconds:.0f}s" + counters)
        padded = line.ljust(self._last_width)
        self.stream.write("\r" + padded + ("\n" if final else ""))
        self.stream.flush()
        self._last_width = len(line)


class RunStatusTracker:
    def __init__(self, path: str, *, run_id: str, profile: str,
                 stages: list[str] | tuple[str, ...] = (), study_total: int = 0,
                 renderer: ConsoleStatusRenderer | None = None):
        self.path = path
        self.stages = tuple(stages)
        self.state = RunStatus(
            run_id=run_id, profile=profile, stage_total=len(self.stages),
            study_total=study_total,
        )
        self.renderer = renderer
        self._started_monotonic = time.monotonic()
        self._lock = RLock()
        self._write()

    def _write(self, *, final: bool = False) -> None:
        self.state.elapsed_seconds = round(time.monotonic() - self._started_monotonic, 2)
        self.state.updated_at = _now()
        os.makedirs(os.path.dirname(self.path) or ".", exist_ok=True)
        tmp_path = self.path + ".tmp"
        with open(tmp_path, "w", encoding="utf-8") as fh:
            json.dump(self.state.model_dump(mode="json"), fh, indent=2, ensure_ascii=False)
        os.replace(tmp_path, self.path)
        if self.renderer:
            self.renderer.render(self.state, final=final)

    def start(self, message: str = "") -> None:
        with self._lock:
            self.state.status = "running"
            self.state.message = message
            self._write()

    def set_profile(self, profile: str) -> None:
        with self._lock:
            self.state.profile = profile
            self._write()

    def snapshot(self) -> dict:
        with self._lock:
            return self.state.model_dump(mode="json")

    def begin_study(self, accession: str, index: int, total: int | None = None) -> None:
        with self._lock:
            self.state.accession = accession
            self.state.study_index = index
            if total is not None:
                self.state.study_total = total
            self.state.stage = "pending"
            self.state.stage_index = 0
            self.state.completed_stages = []
            self.state.current_tool = None
            self.state.message = ""
            self._write()

    def set_stage(self, stage: str, *, message: str = "", current_tool: str | None = None,
                  evidence_ids: list[str] | None = None) -> None:
        with self._lock:
            previous = self.state.stage
            if previous not in ("pending", stage) and previous not in self.state.completed_stages:
                self.state.completed_stages.append(previous)
            self.state.stage = stage
            self.state.stage_index = self.stages.index(stage) + 1 if stage in self.stages else 0
            self.state.current_tool = current_tool
            self.state.message = message
            if evidence_ids:
                self.state.evidence_ids = list(dict.fromkeys(self.state.evidence_ids + evidence_ids))
            self._write()

    def waiting_approval(self, message: str) -> None:
        with self._lock:
            self.state.status = "waiting_approval"
            self.state.message = message
            self._write()

    def resume(self, message: str = "") -> None:
        with self._lock:
            self.state.status = "running"
            self.state.message = message
            self._write()

    def add_warning(self, message: str = "") -> None:
        with self._lock:
            self.state.warning_count += 1
            if message:
                self.state.message = message
            self._write()

    def add_failure(self, message: str = "") -> None:
        with self._lock:
            self.state.failure_count += 1
            if message:
                self.state.message = message
            self._write()

    def set_usage(self, *, llm_calls: int | None = None, estimated_cost_usd: float | None = None) -> None:
        with self._lock:
            if llm_calls is not None:
                self.state.llm_calls = llm_calls
            if estimated_cost_usd is not None:
                self.state.estimated_cost_usd = round(float(estimated_cost_usd), 6)
            self._write()

    def finish(self, status: Literal["completed", "partial", "failed"], message: str = "") -> None:
        with self._lock:
            if self.state.stage not in ("pending", "completed") and self.state.stage not in self.state.completed_stages:
                self.state.completed_stages.append(self.state.stage)
            self.state.status = status
            self.state.stage = "completed" if status != "failed" else "failed"
            self.state.stage_index = self.state.stage_total if status != "failed" else self.state.stage_index
            self.state.current_tool = None
            self.state.message = message
            self.state.finished_at = _now()
            self._write(final=True)
