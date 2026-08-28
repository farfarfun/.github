"""从 GitHub 线上真实状态重建 repo_config.json。

原来的 repo_config.json 存的是 2025 年批量生成的模板文案（「XX工具包 - 提供XX功能」），
和仓库实际内容对不上；脚本按它跑一遍，就会把手工修正过的描述和 topics 全部覆盖回错的。

线上状态才是当前的准确基线，所以直接以线上为准重建。
"""

import json
import os
import subprocess

FIELDS = "name,description,homepageUrl,repositoryTopics,isFork,isArchived,isPrivate"

raw = subprocess.run(
    ["gh", "repo", "list", "farfarfun", "--limit", "300", "--json", FIELDS],
    capture_output=True, text=True, check=True,
).stdout
repos = json.loads(raw)

out = {}
skipped_fork = []
for r in sorted(repos, key=lambda x: x["name"]):
    if r["isFork"]:
        skipped_fork.append(r["name"])
        continue
    topics = [t["name"] for t in (r.get("repositoryTopics") or [])]
    out[r["name"]] = {
        "description": r.get("description") or "",
        "keywords": topics,
        "homepage": r.get("homepageUrl") or None,
    }

config = {
    "organization": "farfarfun",
    "_comment": (
        "本文件由 build_repo_config.py 从 GitHub 线上状态生成，是仓库元信息的基线快照。"
        "手工改完线上元信息后请重新生成，否则 update_repo_keywords.py 会把线上改动覆盖回旧值。"
    ),
    "repositories": out,
    "default_keywords": ["python", "farfarfun"],
    "settings": {"api_delay_seconds": 1, "max_retries": 3},
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "repo_config.json")
with open(out_path, "w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)
    f.write("\n")

no_desc = [k for k, v in out.items() if not v["description"]]
no_topic = [k for k, v in out.items() if not v["keywords"]]
print(f"写入 {len(out)} 个仓库（跳过 {len(skipped_fork)} 个 fork: {', '.join(skipped_fork)}）")
print(f"仍无描述 {len(no_desc)} 个: {', '.join(no_desc)}")
print(f"仍无 topics {len(no_topic)} 个: {', '.join(no_topic)}")
