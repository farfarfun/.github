import importlib
import logging
import sys
import tempfile
import types
import unittest
from pathlib import Path
from unittest.mock import patch

import requests


SCRIPT_DIR = Path(__file__).parents[1] / "script" / "update_keyword"
sys.path.insert(0, str(SCRIPT_DIR))

fake_secret = types.ModuleType("funsecret")
fake_secret.read_secret = lambda *args, **kwargs: "dummy-token"
sys.modules.setdefault("funsecret", fake_secret)

fake_log = types.ModuleType("farlog")


def get_logger(name):
    logger = logging.getLogger(name)
    logger.success = logger.info
    return logger


fake_log.getLogger = get_logger
sys.modules.setdefault("farlog", fake_log)

update_repo_keywords = importlib.import_module("update_repo_keywords")


class FakeUpdater:
    preview_called = False
    update_all_called = False
    init_kwargs = {}
    batch_results = {"funread": True}

    def __init__(self, **kwargs):
        type(self).init_kwargs = kwargs

    def dry_run(self):
        type(self).preview_called = True

    def get_repo_configs(self):
        return {}

    def update_all_repos(self, *args):
        type(self).update_all_called = True
        return type(self).batch_results


class CliTests(unittest.TestCase):
    def test_dry_run_executes_preview(self):
        FakeUpdater.preview_called = False
        with patch.object(update_repo_keywords, "GitHubRepoUpdater", FakeUpdater), patch.object(
            sys, "argv", ["update_repo_keywords.py", "--dry-run"]
        ):
            self.assertEqual(update_repo_keywords.main(), 0)
        self.assertTrue(FakeUpdater.preview_called)

    def test_unknown_repository_returns_nonzero(self):
        with patch.object(update_repo_keywords, "GitHubRepoUpdater", FakeUpdater), patch.object(
            sys, "argv", ["update_repo_keywords.py", "--repo", "missing"]
        ):
            self.assertEqual(update_repo_keywords.main(), 1)

    def test_apply_executes_batch_update(self):
        FakeUpdater.update_all_called = False
        FakeUpdater.batch_results = {"funread": True}
        with patch.object(update_repo_keywords, "GitHubRepoUpdater", FakeUpdater), patch.object(
            sys, "argv", ["update_repo_keywords.py", "--apply"]
        ):
            self.assertEqual(update_repo_keywords.main(), 0)

        self.assertTrue(FakeUpdater.update_all_called)
        self.assertFalse(FakeUpdater.init_kwargs["dry_run"])

    def test_apply_returns_nonzero_when_batch_has_failure(self):
        FakeUpdater.batch_results = {"funread": False}
        with patch.object(update_repo_keywords, "GitHubRepoUpdater", FakeUpdater), patch.object(
            sys, "argv", ["update_repo_keywords.py", "--apply"]
        ):
            self.assertEqual(update_repo_keywords.main(), 1)


class TopicUpdateTests(unittest.TestCase):
    def setUp(self):
        self.updater = update_repo_keywords.GitHubRepoUpdater.__new__(
            update_repo_keywords.GitHubRepoUpdater
        )
        self.updater.org_name = "farfarfun"
        self.updater.base_url = "https://api.github.com"
        self.updater.dry_run_mode = False
        self.updater.replace_topics = False

    def test_topics_are_merged_by_default(self):
        response = types.SimpleNamespace(status_code=200)
        self.updater.request = unittest.mock.Mock(return_value=response)

        result = self.updater.update_repo_topics(
            "funread", ["python", "farfarfun"], current_topics=["legado"]
        )

        self.assertTrue(result)
        self.updater.request.assert_called_once_with(
            "PUT",
            "https://api.github.com/repos/farfarfun/funread/topics",
            json={"names": ["legado", "python", "farfarfun"]},
        )

    def test_dry_run_does_not_write(self):
        self.updater.dry_run_mode = True
        self.updater.request = unittest.mock.Mock()

        self.assertTrue(self.updater.update_repo_topics("funread", ["python"]))
        self.updater.request.assert_not_called()


class FailureAndMetadataTests(unittest.TestCase):
    def test_default_config_is_resolved_from_script_directory(self):
        session = types.SimpleNamespace(headers={})
        with patch.object(update_repo_keywords.requests, "Session", return_value=session):
            updater = update_repo_keywords.GitHubRepoUpdater(token="test-token")

        self.assertEqual(
            Path(updater.config_file), SCRIPT_DIR / "repo_config.json"
        )

    def test_invalid_config_raises_runtime_error(self):
        with tempfile.TemporaryDirectory() as directory:
            config_path = Path(directory) / "repo_config.json"
            config_path.write_text("{invalid", encoding="utf-8")
            updater = update_repo_keywords.GitHubRepoUpdater.__new__(
                update_repo_keywords.GitHubRepoUpdater
            )
            updater.config_file = str(config_path)

            with self.assertRaises(RuntimeError):
                updater.load_config()

    @patch.object(update_repo_keywords.time, "sleep")
    def test_request_raises_after_retrying_network_errors(self, sleep):
        updater = update_repo_keywords.GitHubRepoUpdater.__new__(
            update_repo_keywords.GitHubRepoUpdater
        )
        updater.max_retries = 3
        updater.api_delay_seconds = 0
        updater.session = types.SimpleNamespace(
            request=unittest.mock.Mock(side_effect=requests.ConnectionError("offline"))
        )

        with self.assertRaisesRegex(RuntimeError, "GitHub API 请求失败"):
            updater.request("GET", "https://api.github.com/example")

        self.assertEqual(updater.session.request.call_count, 3)
        self.assertEqual(sleep.call_count, 2)

    def test_description_update_sends_homepage(self):
        updater = update_repo_keywords.GitHubRepoUpdater.__new__(
            update_repo_keywords.GitHubRepoUpdater
        )
        updater.org_name = "farfarfun"
        updater.base_url = "https://api.github.com"
        updater.dry_run_mode = False
        updater.request = unittest.mock.Mock(
            return_value=types.SimpleNamespace(status_code=200)
        )

        self.assertTrue(
            updater.update_repo_description(
                "funread", "Reader utilities", "https://example.test/funread"
            )
        )
        updater.request.assert_called_once_with(
            "PATCH",
            "https://api.github.com/repos/farfarfun/funread",
            json={
                "description": "Reader utilities",
                "homepage": "https://example.test/funread",
            },
        )

    def test_description_update_clears_homepage(self):
        updater = update_repo_keywords.GitHubRepoUpdater.__new__(
            update_repo_keywords.GitHubRepoUpdater
        )
        updater.org_name = "farfarfun"
        updater.base_url = "https://api.github.com"
        updater.dry_run_mode = False
        updater.request = unittest.mock.Mock(
            return_value=types.SimpleNamespace(status_code=200)
        )

        self.assertTrue(updater.update_repo_description("funread", "Reader utilities"))
        self.assertEqual(updater.request.call_args.kwargs["json"]["homepage"], "")

    def test_get_org_repos_fetches_all_pages(self):
        updater = update_repo_keywords.GitHubRepoUpdater.__new__(
            update_repo_keywords.GitHubRepoUpdater
        )
        updater.org_name = "farfarfun"
        updater.base_url = "https://api.github.com"
        updater.request = unittest.mock.Mock(
            side_effect=[
                types.SimpleNamespace(status_code=200, json=lambda: [{"name": "one"}]),
                types.SimpleNamespace(status_code=200, json=lambda: [{"name": "two"}]),
                types.SimpleNamespace(status_code=200, json=lambda: []),
            ]
        )

        self.assertEqual(updater.get_org_repos(), ["one", "two"])
        self.assertEqual(updater.request.call_count, 3)

    def test_get_org_repos_raises_for_http_error(self):
        updater = update_repo_keywords.GitHubRepoUpdater.__new__(
            update_repo_keywords.GitHubRepoUpdater
        )
        updater.org_name = "farfarfun"
        updater.base_url = "https://api.github.com"
        updater.request = unittest.mock.Mock(
            return_value=types.SimpleNamespace(status_code=403, text="forbidden")
        )

        with self.assertRaisesRegex(RuntimeError, "HTTP 403"):
            updater.get_org_repos()

    def test_get_repo_info_raises_for_http_error(self):
        updater = update_repo_keywords.GitHubRepoUpdater.__new__(
            update_repo_keywords.GitHubRepoUpdater
        )
        updater.org_name = "farfarfun"
        updater.base_url = "https://api.github.com"
        updater.request = unittest.mock.Mock(
            return_value=types.SimpleNamespace(status_code=404, text="not found")
        )

        with self.assertRaisesRegex(RuntimeError, "HTTP 404"):
            updater.get_repo_info("missing")

    def test_update_all_repos_marks_missing_repository_as_failed(self):
        updater = update_repo_keywords.GitHubRepoUpdater.__new__(
            update_repo_keywords.GitHubRepoUpdater
        )
        updater.org_name = "farfarfun"
        updater.get_repo_configs = unittest.mock.Mock(
            return_value={"missing": update_repo_keywords.RepoConfig("missing", "", [])}
        )
        updater.get_org_repos = unittest.mock.Mock(return_value=[])

        self.assertEqual(updater.update_all_repos(), {"missing": False})


if __name__ == "__main__":
    unittest.main()
