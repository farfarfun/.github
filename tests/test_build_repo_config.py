import importlib
import sys
import types
import unittest
from pathlib import Path
from unittest.mock import mock_open, patch

SCRIPT_DIR = Path(__file__).parents[1] / "script" / "update_keyword"
sys.path.insert(0, str(SCRIPT_DIR))

fake_funshell = types.ModuleType("funshell")
fake_funshell.run_shell = lambda *args, **kwargs: (_ for _ in ()).throw(
    AssertionError("import must not execute gh")
)
sys.modules.setdefault("funshell", fake_funshell)

build_repo_config = importlib.import_module("build_repo_config")


class BuildConfigTests(unittest.TestCase):
    def test_import_has_no_command_or_file_side_effects(self):
        self.assertTrue(callable(build_repo_config.main))

    def test_build_config_skips_forks(self):
        config, skipped = build_repo_config.build_config(
            [
                {
                    "name": "main-repo",
                    "description": None,
                    "homepageUrl": "",
                    "repositoryTopics": [{"name": "python"}],
                    "isFork": False,
                },
                {
                    "name": "fork-repo",
                    "description": "fork",
                    "homepageUrl": None,
                    "repositoryTopics": [],
                    "isFork": True,
                },
            ]
        )

        self.assertEqual(skipped, ["fork-repo"])
        self.assertEqual(
            config["repositories"]["main-repo"],
            {"description": "", "keywords": ["python"], "homepage": None},
        )

    def test_fetch_repositories_returns_gh_json(self):
        with patch.object(
            build_repo_config, "run_shell", return_value='[{"name": "main-repo"}]'
        ) as run_shell:
            self.assertEqual(
                build_repo_config.fetch_repositories(), [{"name": "main-repo"}]
            )

        self.assertIn("gh repo list farfarfun", run_shell.call_args.args[0])

    def test_fetch_repositories_rejects_command_error_and_invalid_json(self):
        with (
            patch.object(
                build_repo_config, "run_shell", return_value="run shell error: fail"
            ),
            self.assertRaisesRegex(RuntimeError, "gh 命令执行失败"),
        ):
            build_repo_config.fetch_repositories()

        with (
            patch.object(build_repo_config, "run_shell", return_value="not json"),
            self.assertRaisesRegex(RuntimeError, "有效 JSON"),
        ):
            build_repo_config.fetch_repositories()

    def test_main_propagates_config_write_error(self):
        with (
            patch.object(build_repo_config, "fetch_repositories", return_value=[]),
            patch("builtins.open", mock_open()) as open_file,
        ):
            open_file.side_effect = OSError("disk full")
            with self.assertRaisesRegex(OSError, "disk full"):
                build_repo_config.main()


if __name__ == "__main__":
    unittest.main()
