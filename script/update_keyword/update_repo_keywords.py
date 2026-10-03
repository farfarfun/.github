#!/usr/bin/env python3
"""
GitHub仓库关键词批量更新脚本
用于更新farfarfun组织下所有仓库的关键词(topics)

使用方法:
1. 设置GitHub Personal Access Token环境变量: GITHUB_TOKEN
2. 运行脚本: python update_repo_keywords.py
"""

import json
import os
import sys
import time
from dataclasses import dataclass
from typing import Any

import requests
from farlog import getLogger
from funsecret import read_secret

logger = getLogger("farfarfun")


@dataclass
class RepoConfig:
    """表示单个仓库的待同步元信息。

    属性：name 为仓库名；description 为描述；keywords 为 topics；homepage 为主页，
    传入 ``None`` 时表示清空主页。
    """

    name: str
    description: str
    keywords: list[str]
    homepage: str | None = None


class GitHubRepoUpdater:
    """同步一个 GitHub 组织内仓库的描述、主页和 topics。"""

    def __init__(
        self,
        org_name: str = "farfarfun",
        token: str | None = None,
        config_file: str | None = None,
        dry_run: bool = True,
        replace_topics: bool = False,
    ) -> None:
        """初始化更新器。

        参数：org_name 为组织名；token 为 GitHub token；config_file 为配置路径，省略时
        使用脚本同目录的 ``repo_config.json``；dry_run 控制是否写入；replace_topics
        控制 topics 是否整体替换。返回：无。
        """
        # 默认 dry-run：这套脚本会批量改 100+ 个仓库的元信息，误跑一次的代价很高，
        # 必须显式 --apply 才真正写入。
        self.dry_run_mode = dry_run
        self.replace_topics = replace_topics
        self.config_file = config_file or os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "repo_config.json"
        )
        self.config = self.load_config()
        settings = self.config.get("settings", {})
        self.api_delay_seconds = float(settings.get("api_delay_seconds", 1))
        self.max_retries = max(1, int(settings.get("max_retries", 3)))

        self.org_name = org_name or self.config.get("organization", "farfarfun")
        self.token = (
            token or os.environ.get("GITHUB_TOKEN") or read_secret("github", "token")
        )
        self.base_url = "https://api.github.com"
        self.session = requests.Session()

        if not self.token:
            raise ValueError(
                "GitHub token is required. Set GITHUB_TOKEN environment variable."
            )

        self.session.headers.update(
            {
                "Authorization": f"token {self.token}",
                "Accept": "application/vnd.github.v3+json",
                "User-Agent": "farfarfun-repo-updater/1.0",
            }
        )

    def request(self, method: str, url: str, **kwargs: Any) -> requests.Response:
        """执行可重试的 GitHub API 请求。

        参数：method 为 HTTP 方法；url 为请求地址；kwargs 传给 requests。返回：HTTP
        响应。网络错误、限流或服务端错误在重试耗尽后抛出 RuntimeError。
        """
        last_response = None
        for attempt in range(1, self.max_retries + 1):
            try:
                response = self.session.request(method, url, **kwargs)
            except requests.RequestException as exc:
                if attempt == self.max_retries:
                    raise RuntimeError(
                        f"GitHub API 请求失败: {method} {url}: {exc}"
                    ) from exc
                time.sleep(self.api_delay_seconds)
                continue
            last_response = response
            if response.status_code < 500 and response.status_code != 429:
                return response
            if attempt < self.max_retries:
                time.sleep(self.api_delay_seconds)
        assert last_response is not None
        raise RuntimeError(
            f"GitHub API 请求失败: {method} {url}: "
            f"HTTP {last_response.status_code} {last_response.text[:500]}"
        )

    def load_config(self) -> dict[str, Any]:
        """读取配置文件。

        参数：无。返回：配置文件的 JSON 对象；文件不存在时返回空字典。读取或解析失败时
        抛出 RuntimeError。
        """
        if not os.path.exists(self.config_file):
            return {}
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.error(f"配置文件 {self.config_file} 读取/解析失败: {e}")
            raise RuntimeError(f"无法加载配置文件 {self.config_file}") from e

    def get_repo_configs(self) -> dict[str, RepoConfig]:
        """将配置文件中的仓库条目转换为配置对象。

        参数：无。返回：以仓库名为键的 RepoConfig 字典。
        """
        configs = {}

        # 从配置文件读取
        if self.config and "repositories" in self.config:
            for repo_name, repo_data in self.config["repositories"].items():
                configs[repo_name] = RepoConfig(
                    name=repo_name,
                    description=repo_data.get("description", ""),
                    keywords=repo_data.get("keywords", []),
                    homepage=repo_data.get("homepage"),
                )
        return configs

    def get_org_repos(self) -> list[str]:
        """分页获取组织下全部仓库名称。

        参数：无。返回：仓库名称列表。API 返回非 200 状态时抛出 RuntimeError。
        """
        url = f"{self.base_url}/orgs/{self.org_name}/repos"
        repos = []
        page = 1

        while True:
            response = self.request("GET", url, params={"page": page, "per_page": 100})
            if response.status_code != 200:
                raise RuntimeError(
                    f"获取组织仓库失败: {url}: HTTP {response.status_code} "
                    f"{response.text[:500]}"
                )

            data = response.json()
            if not data:
                break

            repos.extend([repo["name"] for repo in data])
            page += 1

        logger.info(f"Found {len(repos)} repositories in {self.org_name} organization")
        return repos

    def get_repo_info(self, repo_name: str) -> dict[str, Any]:
        """获取指定仓库的当前元信息。

        参数：repo_name 为仓库名。返回：GitHub 返回的仓库信息。API 返回非 200 状态时
        抛出 RuntimeError。
        """
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}"
        response = self.request("GET", url)

        if response.status_code == 200:
            return response.json()
        else:
            raise RuntimeError(
                f"获取仓库信息失败: {url}: HTTP {response.status_code} "
                f"{response.text[:500]}"
            )

    def update_repo_topics(
        self,
        repo_name: str,
        topics: list[str],
        current_topics: list[str] | None = None,
        replace: bool = False,
    ) -> bool:
        """更新仓库的 topics。

        参数：repo_name 为仓库名；topics 为目标 topics；current_topics 为线上已有
        topics；replace 为是否整体替换。返回：请求成功或 dry-run 时为 True，否则为
        False。默认将 topics 与线上值取并集，避免覆盖手工添加的值。
        """
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}/topics"

        # GitHub API要求topics必须是小写，且不能包含空格
        cleaned_topics = [topic.lower().replace(" ", "-") for topic in topics]

        if not replace:
            merged = [t.lower().replace(" ", "-") for t in (current_topics or [])]
            for topic in cleaned_topics:
                if topic not in merged:
                    merged.append(topic)
            cleaned_topics = merged

        if self.dry_run_mode:
            logger.info(f"[dry-run] 将把 {repo_name} 的 topics 设为: {cleaned_topics}")
            return True

        data = {"names": cleaned_topics}

        response = self.request("PUT", url, json=data)

        if response.status_code == 200:
            logger.success(
                f"Successfully updated topics for {repo_name}: {cleaned_topics}"
            )
            return True
        else:
            logger.error(
                f"Failed to update topics for {repo_name}: {response.status_code} - {response.text}"
            )
            return False

    def update_repo_description(
        self, repo_name: str, description: str, homepage: str | None = None
    ) -> bool:
        """更新仓库描述和主页。

        参数：repo_name 为仓库名；description 为描述；homepage 为主页，传入 None
        会清空主页。返回：请求成功或 dry-run 时为 True，否则为 False。
        """
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}"

        # homepage 传 None 表示「清空」，要显式发空串；只用 `if homepage:` 会导致
        # 清空请求被静默丢掉，于是每次跑都判定为「有差异」但永远改不掉。
        data = {"description": description, "homepage": homepage or ""}

        if self.dry_run_mode:
            logger.info(f"[dry-run] 将把 {repo_name} 的描述改为: {description!r}")
            return True

        response = self.request("PATCH", url, json=data)

        if response.status_code == 200:
            logger.success(f"Successfully updated description for {repo_name}")
            return True
        else:
            logger.error(
                f"Failed to update description for {repo_name}: {response.status_code} - {response.text}"
            )
            return False

    def update_single_repo(
        self,
        repo_name: str,
        config: RepoConfig,
        update_description: bool = True,
        update_topics: bool = True,
    ) -> bool:
        """按配置更新单个仓库。

        参数：repo_name 为仓库名；config 为目标配置；update_description 和
        update_topics 控制更新项目。返回：所有请求成功时为 True，否则为 False。
        """
        logger.info(f"Updating repository: {repo_name}")

        # 获取当前仓库信息
        repo_info = self.get_repo_info(repo_name)
        if not repo_info:
            return False

        success = True
        changes_made = False

        # 更新描述和主页
        if update_description and (
            repo_info.get("description") != config.description
            or repo_info.get("homepage") != config.homepage
        ):
            logger.info(f"Updating description for {repo_name}")
            logger.info(f"  Current: {repo_info.get('description', 'None')}")
            logger.info(f"  New: {config.description}")
            if repo_info.get("homepage") != config.homepage:
                logger.info(
                    f"  Homepage: {repo_info.get('homepage', 'None')} -> {config.homepage}"
                )

            if not self.update_repo_description(
                repo_name, config.description, config.homepage
            ):
                success = False
            else:
                changes_made = True

        # 更新关键词
        if update_topics:
            current_topics = repo_info.get("topics", [])
            new_topics = [topic.lower().replace(" ", "-") for topic in config.keywords]

            if self.replace_topics:
                needs_update = set(current_topics) != set(new_topics)
            else:
                # 追加模式下，配置里的 topics 已经全在线上就无需动作；
                # 线上多出来的（手工加的）不算差异，不能因此触发覆盖。
                needs_update = not set(new_topics) <= set(current_topics)

            if needs_update:
                logger.info(f"Updating topics for {repo_name}")
                logger.info(f"  Current: {current_topics}")
                logger.info(f"  New: {new_topics}")

                if not self.update_repo_topics(
                    repo_name,
                    config.keywords,
                    current_topics=current_topics,
                    replace=self.replace_topics,
                ):
                    success = False
                else:
                    changes_made = True
            else:
                logger.info(f"Topics for {repo_name} are already up to date")

        if not changes_made and success:
            logger.info(f"No changes needed for {repo_name}")

        # 添加延迟以避免API限制
        time.sleep(self.api_delay_seconds)

        return success

    def update_all_repos(
        self, update_description: bool = True, update_topics: bool = True
    ) -> dict[str, bool]:
        """批量更新配置中存在的仓库。

        参数：update_description 和 update_topics 控制更新项目。返回：以仓库名为键、
        更新是否成功为值的结果字典。
        """
        configs = self.get_repo_configs()
        org_repos = self.get_org_repos()
        results = {}

        update_types = []
        if update_description:
            update_types.append("descriptions")
        if update_topics:
            update_types.append("topics")

        logger.info(f"Starting batch update for {len(configs)} repositories")
        logger.info(
            f"Will update: {', '.join(update_types) if update_types else 'nothing (dry run only)'}"
        )

        for repo_name, config in configs.items():
            if repo_name not in org_repos:
                logger.warning(
                    f"Repository {repo_name} not found in organization {self.org_name}"
                )
                results[repo_name] = False
                continue

            results[repo_name] = self.update_single_repo(
                repo_name, config, update_description, update_topics
            )

        # 输出结果摘要
        successful = sum(1 for success in results.values() if success)
        total = len(results)

        logger.success(
            f"Update completed: {successful}/{total} repositories updated successfully"
        )

        return results

    def dry_run(self) -> None:
        """显示配置与线上现状的对比，不写入 GitHub。

        参数：无。返回：无。
        """
        configs = self.get_repo_configs()
        org_repos = self.get_org_repos()

        logger.info("=== DRY RUN MODE - No changes will be made ===")

        for repo_name, config in configs.items():
            if repo_name not in org_repos:
                logger.warning(f"Repository {repo_name} not found in organization")
                continue

            logger.info(f"\nRepository: {repo_name}")
            logger.info(f"  Description: {config.description}")
            logger.info(f"  Homepage: {config.homepage}")
            logger.info(f"  Keywords: {config.keywords}")

            # 获取当前信息进行对比
            repo_info = self.get_repo_info(repo_name)
            if repo_info:
                current_topics = repo_info.get("topics", [])
                logger.info(f"  Current topics: {current_topics}")


def main() -> int:
    """运行仓库元信息更新命令行程序。

    参数：通过命令行接收组织、仓库和更新选项。返回：成功为 0，配置、请求或更新失败为 1。
    """
    import argparse

    parser = argparse.ArgumentParser(
        description="Update GitHub repository keywords and metadata"
    )
    parser.add_argument("--org", default="farfarfun", help="GitHub organization name")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="只打印配置与线上现状的对比，不做任何写入",
    )
    parser.add_argument(
        "--apply",
        action="store_true",
        help="真正写入 GitHub。不加这个参数一律只打印将要做的改动（默认安全）",
    )
    parser.add_argument(
        "--replace-topics",
        action="store_true",
        help="用配置里的 topics 整体替换线上（会抹掉线上手工加的）。默认是并集追加",
    )
    parser.add_argument("--repo", help="Update specific repository only")
    parser.add_argument(
        "--no-description",
        action="store_true",
        help="Skip updating repository descriptions",
    )
    parser.add_argument(
        "--no-topics",
        action="store_true",
        help="Skip updating repository topics/keywords",
    )
    parser.add_argument(
        "--description-only",
        action="store_true",
        help="Only update descriptions, skip topics",
    )
    parser.add_argument(
        "--topics-only",
        action="store_true",
        help="Only update topics, skip descriptions",
    )

    args = parser.parse_args()

    # 确定更新选项
    update_description = True
    update_topics = True

    if args.description_only:
        update_topics = False
    elif args.topics_only:
        update_description = False
    else:
        if args.no_description:
            update_description = False
        if args.no_topics:
            update_topics = False

    try:
        updater = GitHubRepoUpdater(
            org_name=args.org,
            dry_run=not args.apply,
            replace_topics=args.replace_topics,
        )
        if not args.apply:
            logger.warning("未加 --apply，本次只打印将要做的改动，不会写入 GitHub")

        if args.dry_run:
            updater.dry_run()
        elif args.repo:
            configs = updater.get_repo_configs()
            if args.repo in configs:
                result = updater.update_single_repo(
                    args.repo, configs[args.repo], update_description, update_topics
                )
                print(
                    f"Repository {args.repo} update: {'Success' if result else 'Failed'}"
                )
                if not result:
                    return 1
            else:
                print(f"Repository {args.repo} not found in configuration")
                return 1
        else:
            results = updater.update_all_repos(update_description, update_topics)

            # 输出最终结果
            print("\n=== Update Results ===")
            for repo, success in results.items():
                status = "✅ Success" if success else "❌ Failed"
                print(f"{repo}: {status}")
            if not all(results.values()):
                return 1

    except (OSError, RuntimeError, ValueError) as e:
        logger.error(f"Script execution failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
