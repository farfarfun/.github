"""离线验证 update_repo_keywords.py 的两处关键改动：

1. topics 默认并集追加，不再抹掉线上手工加的
2. 默认 dry-run，不加 --apply 不写入
"""

import os
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# 打桩掉 funsecret / farlog，避免为了跑测试去装一堆依赖
fake_secret = types.ModuleType("funsecret")
fake_secret.read_secret = lambda *a, **k: "dummy-token"
sys.modules["funsecret"] = fake_secret

fake_log = types.ModuleType("farlog")
import logging

logging.basicConfig(level=logging.CRITICAL)


def _get_logger(name):
    lg = logging.getLogger(name)
    lg.success = lg.info
    return lg


fake_log.getLogger = _get_logger
sys.modules["farlog"] = fake_log

import update_repo_keywords as m  # noqa: E402

u = m.GitHubRepoUpdater.__new__(m.GitHubRepoUpdater)
u.org_name = "farfarfun"
u.base_url = "https://api.github.com"

captured = {}


class FakeSession:
    def put(self, url, json):
        captured["names"] = json["names"]

        class R:
            status_code = 200

        return R()


u.session = FakeSession()

# --- 场景 1：默认追加模式，线上有手工加的 topic ---
u.dry_run = False
u.replace_topics = False
u.update_repo_topics(
    "funread", ["python", "farfarfun"], current_topics=["legado", "手工加的"]
)
got = captured["names"]
assert "legado" in got, f"手工加的 topic 被抹掉了: {got}"
assert "python" in got and "farfarfun" in got, got
print("✅ 追加模式: 线上手工 topic 保留 ->", got)

# --- 场景 2：显式 replace，整体替换 ---
captured.clear()
u.replace_topics = True
u.update_repo_topics(
    "funread", ["python", "farfarfun"], current_topics=["legado"], replace=True
)
got = captured["names"]
assert got == ["python", "farfarfun"], got
print("✅ 替换模式: 按配置整体替换 ->", got)

# --- 场景 3：dry-run 不发任何请求 ---
captured.clear()
u.dry_run = True
u.replace_topics = False
u.update_repo_topics("funread", ["python"], current_topics=["legado"])
assert captured == {}, f"dry-run 竟然发出了写请求: {captured}"
print("✅ dry-run: 未发出任何写请求")

# --- 场景 4：needs_update 判定 —— 线上是配置的超集时不该触发 ---
new = {"python", "farfarfun"}
cur = {"python", "farfarfun", "legado"}
assert not (not new <= cur), "追加模式下不该判定为需要更新"
print("✅ 线上 topics 是配置超集时，不再触发覆盖")

print("\n全部通过")
