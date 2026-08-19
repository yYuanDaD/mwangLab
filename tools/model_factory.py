"""Central LLM provider configuration for the bioinformatics agent.

The evaluated deployment selects DeepSeek V4 Pro in ``.env``.  The library
fallback remains Claude Sonnet 4.6 when no provider is configured, so a fresh
environment without a DeepSeek key fails neither implicitly nor ambiguously.
"""

from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Mapping
from urllib.parse import urlsplit, urlunsplit

from dotenv import load_dotenv
from langchain_anthropic import ChatAnthropic


DEFAULT_PROVIDER = "anthropic"
DEFAULT_MODELS = {
    "anthropic": "claude-sonnet-4-6",
    "deepseek": "deepseek-v4-pro",
}
DEEPSEEK_MODELS = frozenset({"deepseek-v4-pro", "deepseek-v4-flash"})
_ANTHROPIC_NO_TEMPERATURE_PREFIXES = (
    "claude-fable-5", "claude-mythos-5", "claude-opus-5", "claude-sonnet-5",
)


@dataclass(frozen=True)
class ModelConfig:
    provider: str
    model: str
    api_key_env: str
    base_url: str | None = None
    effort: str | None = None

    @property
    def label(self) -> str:
        effort = f" effort={self.effort}" if self.effort else ""
        return f"{self.provider}:{self.model}{effort}"


def _normalize_provider(value: str) -> str:
    normalized = value.strip().lower()
    aliases = {"claude": "anthropic", "sonnet": "anthropic"}
    normalized = aliases.get(normalized, normalized)
    if normalized not in DEFAULT_MODELS:
        supported = ", ".join(sorted(DEFAULT_MODELS))
        raise ValueError(f"Unsupported BIOAGENT_LLM_PROVIDER={value!r}; choose one of: {supported}")
    return normalized


def _deepseek_anthropic_url(value: str) -> str:
    base = (value or "https://api.deepseek.com").rstrip("/")
    parsed = urlsplit(base)
    if parsed.netloc.lower() == "api.deepseek.com":
        # Older local configs may contain obsolete suffixes such as /v4.
        # The current official Anthropic endpoint is rooted at /anthropic.
        return urlunsplit((parsed.scheme or "https", parsed.netloc, "/anthropic", "", ""))
    return base if base.endswith("/anthropic") else base + "/anthropic"


def resolve_model_config(
    *,
    provider: str | None = None,
    model: str | None = None,
    effort: str | None = None,
    environment: Mapping[str, str] | None = None,
) -> ModelConfig:
    """Resolve provider settings without reading or retaining any secret value."""
    load_dotenv()
    env = environment if environment is not None else os.environ
    resolved_provider = _normalize_provider(
        provider or env.get("BIOAGENT_LLM_PROVIDER", DEFAULT_PROVIDER)
    )
    resolved_model = (model or env.get("BIOAGENT_LLM_MODEL") or
                      DEFAULT_MODELS[resolved_provider]).strip()

    requested_effort = effort if effort is not None else env.get("BIOAGENT_LLM_EFFORT")
    if requested_effort:
        requested_effort = requested_effort.strip().lower()
        if requested_effort not in {"low", "medium", "high", "xhigh", "max"}:
            raise ValueError(
                "BIOAGENT_LLM_EFFORT must be one of: low, medium, high, xhigh, max"
            )

    if resolved_provider == "deepseek":
        # DeepSeek silently maps unsupported names to V4 Flash on its Anthropic
        # endpoint. Fail locally so an A/B cannot unknowingly test the wrong model.
        if resolved_model not in DEEPSEEK_MODELS:
            allowed = ", ".join(sorted(DEEPSEEK_MODELS))
            raise ValueError(f"Unsupported DeepSeek model {resolved_model!r}; choose one of: {allowed}")
        return ModelConfig(
            provider="deepseek",
            model=resolved_model,
            api_key_env="DEEPSEEK_API_KEY",
            base_url=_deepseek_anthropic_url(env.get("DEEPSEEK_BASE_URL", "")),
            effort=requested_effort or "max",
        )

    return ModelConfig(
        provider="anthropic",
        model=resolved_model,
        api_key_env="CLAUDE_API_KEY",
        base_url=None,
        effort=requested_effort,
    )


def create_chat_model(
    config: ModelConfig | None = None,
    *,
    required: bool = True,
    thinking: bool | None = None,
    max_tokens: int | None = None,
    environment: Mapping[str, str] | None = None,
):
    """Create a ChatAnthropic client for Anthropic or DeepSeek's compatible API.

    ``required=False`` preserves the existing fail-soft behavior of optional LLM
    hooks: a missing provider key returns ``None`` instead of aborting the run.
    """
    load_dotenv()
    env = environment if environment is not None else os.environ
    resolved = config or resolve_model_config(environment=env)
    api_key = env.get(resolved.api_key_env)
    if not api_key:
        if not required:
            return None
        raise ValueError(
            f"API key not found for {resolved.label}; set {resolved.api_key_env} in .env"
        )

    kwargs = {
        "model": resolved.model,
        "api_key": api_key,
    }
    # Claude 5 models use adaptive reasoning controls and reject the legacy temperature field.
    # Keep temperature=0 for older Claude models and DeepSeek's Anthropic-compatible endpoint.
    if (resolved.provider != "anthropic" or
            not resolved.model.startswith(_ANTHROPIC_NO_TEMPERATURE_PREFIXES)):
        kwargs["temperature"] = 0
    if max_tokens is not None:
        if max_tokens < 1:
            raise ValueError("max_tokens must be a positive integer")
        kwargs["max_tokens"] = max_tokens
    if resolved.base_url:
        kwargs["base_url"] = resolved.base_url
    if resolved.provider == "deepseek":
        thinking_enabled = True if thinking is None else thinking
        kwargs["thinking"] = {"type": "enabled" if thinking_enabled else "disabled"}
    else:
        thinking_enabled = thinking
    if resolved.effort and thinking_enabled is not False:
        kwargs["effort"] = resolved.effort
    return ChatAnthropic(**kwargs)


def create_structured_chat_model(
    config: ModelConfig | None = None,
    *,
    required: bool = True,
    max_tokens: int | None = None,
    environment: Mapping[str, str] | None = None,
):
    """Create a client compatible with forced-schema structured output.

    DeepSeek thinking mode rejects the forced ``tool_choice`` used by
    ``with_structured_output``. Structured hooks therefore use the same V4
    model with thinking disabled, while the main agent keeps thinking enabled.
    """
    env = environment if environment is not None else os.environ
    resolved = config or resolve_model_config(environment=env)
    if max_tokens is None and resolved.provider == "deepseek":
        raw_limit = env.get("BIOAGENT_STRUCTURED_MAX_TOKENS", "16384")
        try:
            max_tokens = int(raw_limit)
        except (TypeError, ValueError) as exc:
            raise ValueError("BIOAGENT_STRUCTURED_MAX_TOKENS must be a positive integer") from exc
        if max_tokens < 1:
            raise ValueError("BIOAGENT_STRUCTURED_MAX_TOKENS must be a positive integer")
    return create_chat_model(
        resolved,
        required=required,
        thinking=False,
        max_tokens=max_tokens,
        environment=environment,
    )
