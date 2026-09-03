#!/usr/bin/env python3
"""
GitHub仓库关键词批量更新脚本
用于更新farfarfun组织下所有仓库的关键词(topics)

使用方法:
1. 设置GitHub Personal Access Token环境变量: GITHUB_TOKEN
2. 运行脚本: python update_repo_keywords.py
"""

import os
import json
import time
import requests
from dataclasses import dataclass

from funsecret import read_secret
from farlog import getLogger

logger = getLogger("farfarfun")


@dataclass
class RepoConfig:
    """仓库配置类"""

    name: str
    description: str
    keywords: list[str]
    homepage: str | None = None


class GitHubRepoUpdater:
    """GitHub仓库关键词更新器"""

    def __init__(
        self,
        org_name: str = "farfarfun",
        token: str | None = None,
        config_file: str = "repo_config.json",
        dry_run: bool = True,
        replace_topics: bool = False,
    ):
        # 默认 dry-run：这套脚本会批量改 100+ 个仓库的元信息，误跑一次的代价很高，
        # 必须显式 --apply 才真正写入。
        self.dry_run = dry_run
        self.replace_topics = replace_topics
        self.config_file = config_file
        self.config = self.load_config()

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

    def load_config(self) -> dict:
        """加载配置文件"""
        if not os.path.exists(self.config_file):
            return {}
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                return json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            logger.error(f"配置文件 {self.config_file} 读取/解析失败: {e}")
            raise RuntimeError(f"无法加载配置文件 {self.config_file}") from e

    def get_repo_configs(self) -> dict[str, RepoConfig]:
        """获取仓库配置"""
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
        """获取组织下的所有仓库"""
        url = f"{self.base_url}/orgs/{self.org_name}/repos"
        repos = []
        page = 1

        while True:
            response = self.session.get(url, params={"page": page, "per_page": 100})
            if response.status_code != 200:
                logger.error(
                    f"Failed to fetch repos: {response.status_code} - {response.text}"
                )
                break

            data = response.json()
            if not data:
                break

            repos.extend([repo["name"] for repo in data])
            page += 1

        logger.info(f"Found {len(repos)} repositories in {self.org_name} organization")
        return repos

    def get_repo_info(self, repo_name: str) -> dict | None:
        """获取仓库信息"""
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}"
        response = self.session.get(url)

        if response.status_code == 200:
            return response.json()
        else:
            logger.error(
                f"Failed to get repo info for {repo_name}: {response.status_code}"
            )
            return None

    def update_repo_topics(
        self,
        repo_name: str,
        topics: list[str],
        current_topics: list[str] | None = None,
        replace: bool = False,
    ) -> bool:
        """更新仓库的topics(关键词)。

        默认是**并集追加**。GitHub 的 `PUT /topics` 语义是整体替换，直接拿配置里的
        列表去调，会把线上手工补的 topics 全部抹掉——这正是这套脚本以前会撤销修复的原因
        之一。只有显式传 replace=True 才走整体替换。
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

        if self.dry_run:
            logger.info(f"[dry-run] 将把 {repo_name} 的 topics 设为: {cleaned_topics}")
            return True

        data = {"names": cleaned_topics}

        response = self.session.put(url, json=data)

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
        """更新仓库描述和主页"""
        url = f"{self.base_url}/repos/{self.org_name}/{repo_name}"

        # homepage 传 None 表示「清空」，要显式发空串；只用 `if homepage:` 会导致
        # 清空请求被静默丢掉，于是每次跑都判定为「有差异」但永远改不掉。
        data = {"description": description, "homepage": homepage or ""}

        if self.dry_run:
            logger.info(f"[dry-run] 将把 {repo_name} 的描述改为: {description!r}")
            return True

        response = self.session.patch(url, json=data)

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
        """更新单个仓库的所有信息"""
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
        time.sleep(1)

        return success

    def update_all_repos(
        self, update_description: bool = True, update_topics: bool = True
    ) -> dict[str, bool]:
        """批量更新所有配置的仓库"""
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
        """预览模式 - 显示将要进行的更改但不实际执行"""
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


def main():
    """主函数"""
    import argparse

    parser = argparse.ArgumentParser(
        description="Update GitHub repository keywords and metadata"
    )
    parser.add_argument("--org", default="farfarfun", help="GitHub organization name")
    parser.add_argument(
        "--dry-run", action="store_true", help="只打印配置与线上现状的对比，不做任何写入"
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
            else:
                print(f"Repository {args.repo} not found in configuration")
        else:
            results = updater.update_all_repos(update_description, update_topics)

            # 输出最终结果
            print("\n=== Update Results ===")
            for repo, success in results.items():
                status = "✅ Success" if success else "❌ Failed"
                print(f"{repo}: {status}")

    except Exception as e:
        logger.error(f"Script execution failed: {e}")
        return 1

    return 0


if __name__ == "__main__":
    exit(main())
