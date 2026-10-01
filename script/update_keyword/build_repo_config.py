"""从 GitHub 线上真实状态重建 repo_config.json。

原来的 repo_config.json 存的是 2025 年批量生成的模板文案（「XX工具包 - 提供XX功能」），
和仓库实际内容对不上；脚本按它跑一遍，就会把手工修正过的描述和 topics 全部覆盖回错的。

线上状态才是当前的准确基线，所以直接以线上为准重建。
"""

import json
import os
import shlex

from funshell import run_shell

FIELDS = "name,description,homepageUrl,repositoryTopics,isFork,isArchived,isPrivate"


def fetch_repositories() -> list[dict]:
    """查询组织仓库并返回 GitHub CLI 的结构化结果。"""
    command = shlex.join(
        ["gh", "repo", "list", "farfarfun", "--limit", "300", "--json", FIELDS]
    )
    raw = run_shell(command, printf=False)
    if raw.startswith("run shell error:"):
        raise RuntimeError(f"gh 命令执行失败: {raw}")
    try:
        return json.loads(raw)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"gh 命令未返回有效 JSON: {raw[:500]!r}") from exc


def build_config(repos: list[dict]) -> tuple[dict, list[str]]:
    """把 GitHub 仓库数据转换为配置文件内容。"""
    repositories = {}
    skipped_forks = []
    for repo in sorted(repos, key=lambda item: item["name"]):
        if repo["isFork"]:
            skipped_forks.append(repo["name"])
            continue
        topics = [topic["name"] for topic in (repo.get("repositoryTopics") or [])]
        repositories[repo["name"]] = {
            "description": repo.get("description") or "",
            "keywords": topics,
            "homepage": repo.get("homepageUrl") or None,
        }

    config = {
        "organization": "farfarfun",
        "_comment": (
            "本文件由 build_repo_config.py 从 GitHub 线上状态生成，是仓库元信息的基线快照。"
            "手工改完线上元信息后请重新生成，否则 update_repo_keywords.py 会把线上改动覆盖回旧值。"
        ),
        "repositories": repositories,
        "default_keywords": ["python", "farfarfun"],
        "settings": {"api_delay_seconds": 1, "max_retries": 3},
    }
    return config, skipped_forks


def main() -> int:
    config, skipped_forks = build_config(fetch_repositories())
    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "repo_config.json")
    with open(out_path, "w", encoding="utf-8") as file:
        json.dump(config, file, ensure_ascii=False, indent=2)
        file.write("\n")

    repositories = config["repositories"]
    no_desc = [name for name, data in repositories.items() if not data["description"]]
    no_topic = [name for name, data in repositories.items() if not data["keywords"]]
    print(
        f"写入 {len(repositories)} 个仓库（跳过 {len(skipped_forks)} 个 fork: "
        f"{', '.join(skipped_forks)}）"
    )
    print(f"仍无描述 {len(no_desc)} 个: {', '.join(no_desc)}")
    print(f"仍无 topics {len(no_topic)} 个: {', '.join(no_topic)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
