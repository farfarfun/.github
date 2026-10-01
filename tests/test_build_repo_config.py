import importlib
import sys
import types
import unittest
from pathlib import Path


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


if __name__ == "__main__":
    unittest.main()
