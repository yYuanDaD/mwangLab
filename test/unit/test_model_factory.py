import unittest
import os
from unittest.mock import patch

from tools.model_factory import (
    ModelConfig,
    create_chat_model,
    create_structured_chat_model,
    resolve_model_config,
)


class ModelFactoryTests(unittest.TestCase):
    def test_default_preserves_sonnet(self):
        config = resolve_model_config(environment={"CLAUDE_API_KEY": "secret"})
        self.assertEqual(config.provider, "anthropic")
        self.assertEqual(config.model, "claude-sonnet-4-6")
        self.assertEqual(config.api_key_env, "CLAUDE_API_KEY")
        self.assertIsNone(config.effort)

    def test_deepseek_uses_anthropic_endpoint_and_max_effort(self):
        config = resolve_model_config(
            provider="deepseek",
            environment={"DEEPSEEK_BASE_URL": "https://api.deepseek.com/"},
        )
        self.assertEqual(config.model, "deepseek-v4-pro")
        self.assertEqual(config.base_url, "https://api.deepseek.com/anthropic")
        self.assertEqual(config.effort, "max")

    def test_deepseek_does_not_duplicate_anthropic_suffix(self):
        config = resolve_model_config(
            provider="deepseek",
            environment={"DEEPSEEK_BASE_URL": "https://example.test/anthropic"},
        )
        self.assertEqual(config.base_url, "https://example.test/anthropic")

    def test_deepseek_removes_obsolete_official_version_suffix(self):
        config = resolve_model_config(
            provider="deepseek",
            environment={"DEEPSEEK_BASE_URL": "https://api.deepseek.com/v4"},
        )
        self.assertEqual(config.base_url, "https://api.deepseek.com/anthropic")

    def test_rejects_unknown_deepseek_model_to_prevent_silent_downgrade(self):
        with self.assertRaisesRegex(ValueError, "Unsupported DeepSeek model"):
            resolve_model_config(provider="deepseek", model="deepseek-v4-pr0", environment={})

    def test_missing_optional_key_returns_none(self):
        config = ModelConfig("deepseek", "deepseek-v4-pro", "DEEPSEEK_API_KEY",
                             "https://api.deepseek.com/anthropic", "max")
        self.assertIsNone(create_chat_model(config, required=False, environment={}))

    @patch("tools.model_factory.ChatAnthropic")
    def test_constructor_receives_provider_specific_settings(self, constructor):
        config = resolve_model_config(provider="deepseek", environment={})
        create_chat_model(
            config,
            environment={"DEEPSEEK_API_KEY": "not-exposed"},
        )
        constructor.assert_called_once_with(
            model="deepseek-v4-pro",
            api_key="not-exposed",
            temperature=0,
            base_url="https://api.deepseek.com/anthropic",
            thinking={"type": "enabled"},
            effort="max",
        )

    @patch("tools.model_factory.ChatAnthropic")
    def test_structured_deepseek_disables_thinking_and_omits_effort(self, constructor):
        config = resolve_model_config(provider="deepseek", environment={})
        create_structured_chat_model(
            config,
            environment={"DEEPSEEK_API_KEY": "not-exposed"},
        )
        constructor.assert_called_once_with(
            model="deepseek-v4-pro",
            api_key="not-exposed",
            temperature=0,
            max_tokens=16384,
            base_url="https://api.deepseek.com/anthropic",
            thinking={"type": "disabled"},
        )

    @patch("tools.model_factory.ChatAnthropic")
    def test_structured_deepseek_honors_explicit_output_budget(self, constructor):
        config = resolve_model_config(provider="deepseek", environment={})
        create_structured_chat_model(
            config,
            max_tokens=24576,
            environment={"DEEPSEEK_API_KEY": "not-exposed"},
        )
        self.assertEqual(constructor.call_args.kwargs["max_tokens"], 24576)

    @patch("tools.model_factory.ChatAnthropic")
    def test_structured_opus5_omits_deprecated_temperature(self, constructor):
        config = resolve_model_config(
            provider="anthropic", model="claude-opus-5", effort="medium", environment={}
        )
        create_structured_chat_model(
            config, max_tokens=4096, environment={"CLAUDE_API_KEY": "not-exposed"}
        )
        constructor.assert_called_once_with(
            model="claude-opus-5", api_key="not-exposed", max_tokens=4096,
        )

    def test_structured_deepseek_rejects_invalid_output_budget(self):
        config = resolve_model_config(provider="deepseek", environment={})
        with self.assertRaisesRegex(ValueError, "positive integer"):
            create_structured_chat_model(
                config,
                environment={
                    "DEEPSEEK_API_KEY": "not-exposed",
                    "BIOAGENT_STRUCTURED_MAX_TOKENS": "0",
                },
            )

    @patch("tools.model_factory.create_structured_chat_model")
    def test_seacdm_defaults_to_anthropic_when_main_agent_is_deepseek(self, constructor):
        from tools.seacdm_tools import _get_llm

        with patch.dict(os.environ, {"BIOAGENT_LLM_PROVIDER": "deepseek"}, clear=True):
            _get_llm()
        config = constructor.call_args.args[0]
        self.assertEqual(config.provider, "anthropic")
        self.assertEqual(config.model, "claude-sonnet-4-6")

    @patch("tools.model_factory.create_structured_chat_model")
    def test_seacdm_provider_can_be_explicitly_overridden(self, constructor):
        from tools.seacdm_tools import _get_llm

        with patch.dict(os.environ, {"BIOAGENT_SEACDM_LLM_PROVIDER": "deepseek"}, clear=True):
            _get_llm()
        config = constructor.call_args.args[0]
        self.assertEqual(config.provider, "deepseek")
        self.assertEqual(config.model, "deepseek-v4-pro")


if __name__ == "__main__":
    unittest.main()
