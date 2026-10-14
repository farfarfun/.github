#!/usr/bin/env python3
"""farfarfun 组织与 uTools 插件的 logo 生成器。

生成全部格式与尺寸的 SVG、PNG 与 favicon：

    uv run python brand/gen_logos.py

图形是 ``ff`` 连字——两个 f 共享一道横杠，笔画在底部连成微笑弧：``ff`` 取自
**far far**，底部的弧线是 **fun**。主组织用纯 ff，子组织在右下角挂一枚角标
区分产品线；四个 uTools 插件再往下挂一层，共用同一套 ff 与角标机制。

这个文件是所有图形产物的唯一来源。要改图形就改这里再重跑，不要手工动
``svg/`` ``png/`` ``favicon/``——每次运行都会先清空再整体重建。
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

BRAND = Path(__file__).resolve().parent
SVG_DIR = BRAND / "svg"
PNG_DIR = BRAND / "png"
ICO_DIR = BRAND / "favicon"

S = 1024  # 画布边长
RX = 232  # 圆角方形的圆角半径


# --------------------------------------------------------------------------- #
# 主体与色板
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Subject:
    """一个要出图的主体：一个组织，或一个 uTools 插件。"""

    key: str  # 文件名
    name: str  # 组合标上的名字
    label: str  # 中文定位
    c0: str  # 渐变起点
    c1: str  # 渐变终点
    deep: str  # 角标里图形用的深色
    badge: str | None  # 角标图形，None 表示主组织不挂角标


ORGS: tuple[Subject, ...] = (
    Subject("farfarfun", "farfarfun", "主组织 / Python 工具链", "#06B6D4", "#7C3AED", "#6D28D9", None),
    Subject("drive", "farfarfun-drive", "网盘 / 云存储", "#0EA5E9", "#1D4ED8", "#1D4ED8", "cloud"),
    Subject("skill", "farfarfun-skill", "自研 AI Agent Skill", "#8B5CF6", "#6D28D9", "#6D28D9", "spark"),
    Subject("skills", "farfarfun-skills", "Skill 聚合镜像", "#6366F1", "#4338CA", "#4338CA", "stack"),
    Subject("utools", "farfarfun-utools", "uTools 插件", "#14B8A6", "#0F766E", "#0F766E", "puzzle"),
    Subject("action", "farfarfun-action", "GitHub Action", "#F97316", "#C2410C", "#C2410C", "play"),
)

# 四个 uTools 插件。家族感由 ff 图形和角标机制保证，所以这里不把色相锁在
# utools 组织的青绿里——插件是在启动器里四个排一行被人扫一眼认出来的，
# 色相拉开比凑成一家更要紧。尤其 fundoc 不能再用组织那支青绿：
# 它和 utools 的头像会同时出现在 farfarfun-utools 的 README 里。
PLUGINS: tuple[Subject, ...] = (
    Subject("funchat", "funchat", "AI 好友聊天", "#06B6D4", "#0E7490", "#0E7490", "bubble"),
    Subject("fundoc", "fundoc", "FunDoc 文档", "#4F46E5", "#3730A3", "#3730A3", "doc"),
    Subject("funlink", "funlink", "网址收藏", "#22C55E", "#15803D", "#15803D", "bookmark"),
    Subject("funotp", "funotp", "FunOTP 两步验证", "#F43F5E", "#BE123C", "#BE123C", "shield"),
)

SUBJECTS: tuple[Subject, ...] = ORGS + PLUGINS

INK = "#FFFFFF"  # 深色底上的图形色
PAPER = "#F8FAFC"  # 反白版的底色
PAPER_EDGE = "#E2E8F0"  # 反白版的描边，防止在白色页面上糊掉


# --------------------------------------------------------------------------- #
# 图形几何
# --------------------------------------------------------------------------- #
# f1 顶钩 → f1 竖 → 底部笑弧 → f2 竖 → f2 顶钩，一笔到底。
# 底部用扁椭圆弧而非正圆，弧线才读作「微笑」而不是「碗」。
FF = (
    "M 464 250 A 92 92 0 0 0 372 342 L 372 596 "
    "A 140 104 0 0 0 652 596 L 652 342 A 92 92 0 0 1 744 250"
)
FF_BAR = "M 290 452 L 734 452"  # 两个 f 共享的横杠
FF_STROKE = 86
FF_SHIFT = "translate(-5,37)"  # 把图形光学居中到画布中心

BADGE_CX = BADGE_CY = 806
BADGE_R = 150
BADGE_GAP = 26  # 角标与主图形之间挖出的空隙
GLYPH_SCALE = 1.52


def glyph(kind: str, fg: str, bg: str) -> str:
    """角标内部的图形，画在 ±52 的局部坐标系里。"""
    if kind == "cloud":
        return (
            f'<g fill="{fg}" transform="translate(-1,8)">'
            '<circle cx="-22" cy="4" r="22"/>'
            '<circle cx="2" cy="-14" r="28"/>'
            '<circle cx="26" cy="4" r="20"/>'
            '<rect x="-22" y="2" width="48" height="24" rx="12"/>'
            "</g>"
        )
    if kind == "spark":
        return (
            f'<path fill="{fg}" d="M 0 -50 C 7 -21 21 -7 50 0 C 21 7 7 21 0 50 '
            'C -7 21 -21 7 -50 0 C -21 -7 -7 -21 0 -50 Z"/>'
        )
    if kind == "stack":
        return (
            '<g transform="translate(-4,-4)">'
            f'<rect x="-46" y="-46" width="60" height="60" rx="14" fill="none" '
            f'stroke="{fg}" stroke-width="15"/>'
            f'<rect x="-23" y="-23" width="78" height="78" rx="23" fill="{bg}"/>'
            f'<rect x="-14" y="-14" width="60" height="60" rx="14" fill="{fg}"/>'
            "</g>"
        )
    if kind == "puzzle":
        return (
            f'<path fill="{fg}" stroke="{fg}" stroke-width="13" stroke-linejoin="round" '
            'transform="translate(0,4)" '
            'd="M -44 -44 L -16 -44 A 19 19 0 1 1 16 -44 L 44 -44 L 44 44 L -44 44 '
            'L -44 16 A 19 19 0 1 0 -44 -16 Z"/>'
        )
    if kind == "play":
        return (
            f'<path fill="{fg}" stroke="{fg}" stroke-width="20" stroke-linejoin="round" '
            'transform="translate(-7,0)" d="M -30 -44 L 44 0 L -30 44 Z"/>'
        )
    # 以下四个是 uTools 插件的角标。
    if kind == "bubble":
        # 对话气泡。三个点在小尺寸下会并成一道，但那时整枚角标也只剩一个点了。
        return (
            f'<g transform="translate(0,-11)">'
            f'<path fill="{fg}" d="M -22 30 L -28 64 L 10 33 Z"/>'
            f'<rect x="-48" y="-40" width="96" height="74" rx="26" fill="{fg}"/>'
            f'<g fill="{bg}"><circle cx="-24" cy="-3" r="9.5"/>'
            '<circle cx="0" cy="-3" r="9.5"/><circle cx="24" cy="-3" r="9.5"/></g>'
            "</g>"
        )
    if kind == "doc":
        return (
            f'<rect x="-38" y="-52" width="76" height="104" rx="14" fill="{fg}"/>'
            f'<g fill="{bg}"><rect x="-20" y="-30" width="40" height="12" rx="6"/>'
            '<rect x="-20" y="-6" width="40" height="12" rx="6"/>'
            '<rect x="-20" y="18" width="24" height="12" rx="6"/></g>'
        )
    if kind == "bookmark":
        return (
            f'<path fill="{fg}" stroke="{fg}" stroke-width="16" stroke-linejoin="round" '
            'd="M -32 -44 L 32 -44 L 32 44 L 0 20 L -32 44 Z"/>'
        )
    if kind == "shield":
        # 盾 + 对勾：读作「验证通过」，比光一个盾更说得清 OTP。
        return (
            f'<g transform="translate(0,-2)">'
            f'<path fill="{fg}" d="M 0 -52 L 44 -33 L 44 4 C 44 33 24 49 0 56 '
            'C -24 49 -44 33 -44 4 L -44 -33 Z"/>'
            f'<path fill="none" stroke="{bg}" stroke-width="13" stroke-linecap="round" '
            'stroke-linejoin="round" d="M -19 0 L -5 15 L 20 -14"/>'
            "</g>"
        )
    raise ValueError(f"unknown glyph: {kind}")


def badge(s: Subject, *, bg: str, fg: str, cx: float = BADGE_CX, cy: float = BADGE_CY,
          r: float = BADGE_R) -> str:
    if s.badge is None:
        return ""
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>'
        f'<g transform="translate({cx},{cy}) scale({GLYPH_SCALE})">'
        f"{glyph(s.badge, fg, bg)}</g>"
    )


def knockout(s: Subject, mark: str, *, cx: float = BADGE_CX, cy: float = BADGE_CY,
             r: float = BADGE_R) -> str:
    """在主图形上挖掉角标占的那一圈，角标才会读作「盖在上面」。"""
    if s.badge is None:
        return mark
    mid = f"k-{s.key}"
    return (
        f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">'
        f'<rect width="{S}" height="{S}" fill="white"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r + BADGE_GAP}" fill="black"/></mask>'
        f'<g mask="url(#{mid})">{mark}</g>'
    )


def stroked(d: str, color: str, width: float) -> str:
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )


def ff_mark(color: str) -> str:
    return (
        f'<g transform="{FF_SHIFT}">'
        f"{stroked(FF, color, FF_STROKE)}{stroked(FF_BAR, color, FF_STROKE)}</g>"
    )


def squircle(fill: str, edge: str | None = None) -> str:
    stroke = f' stroke="{edge}" stroke-width="4"' if edge else ""
    return f'<rect x="0" y="0" width="{S}" height="{S}" rx="{RX}" fill="{fill}"{stroke}/>'


# --------------------------------------------------------------------------- #
# 格式
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Fmt:
    key: str
    title: str
    note: str
    sizes: tuple[int, ...]
    body: Callable[[Subject], str] = field(repr=False)


def f_icon(s: Subject) -> str:
    """主图标：渐变圆角方。组织头像、应用图标、favicon 都用它。"""
    return squircle("url(#g)") + knockout(s, ff_mark(INK)) + badge(s, bg=INK, fg=s.deep)


def f_inverse(s: Subject) -> str:
    """反白：浅底配渐变图形。深色页眉、贴纸、印刷物用。"""
    return (
        squircle(PAPER, PAPER_EDGE)
        + knockout(s, ff_mark("url(#g)"))
        + badge(s, bg=s.deep, fg=INK)
    )


def f_circle(s: Subject) -> str:
    """圆形容器：头像被裁成圆形的平台上不会切角。"""
    scaled = (
        '<g transform="translate(512,512) scale(0.86) translate(-512,-512)">'
        f"{ff_mark(INK)}</g>"
    )
    return (
        '<circle cx="512" cy="512" r="512" fill="url(#g)"/>'
        + knockout(s, scaled, cx=752, cy=752, r=142)
        + badge(s, bg=INK, fg=s.deep, cx=752, cy=752, r=142)
    )


def f_mark(s: Subject) -> str:
    """无容器：透明底的纯图形。README 页眉、水印用。"""
    return knockout(s, ff_mark("url(#g)")) + badge(s, bg=s.deep, fg=INK)


# 尺寸取自实际用途：
#   16/32/48  favicon      64/96     GitHub 列表与 PR 头像
#   128/180   桌面与 iOS   192/256   PWA、uTools 插件
#   384/512   组织头像（GitHub 要求 ≥500）   1024  母版
ICON_SIZES = (16, 32, 48, 64, 96, 128, 180, 192, 256, 384, 512, 1024)
ALT_SIZES = (64, 128, 256, 512, 1024)
MARK_SIZES = (32, 64, 128, 256, 512, 1024)

FORMATS: tuple[Fmt, ...] = (
    Fmt("icon", "主图标", "渐变圆角方。组织头像、应用图标、favicon 的来源。", ICON_SIZES, f_icon),
    Fmt("icon-inverse", "反白", "浅底配渐变图形。深色页眉、贴纸与印刷物上用。", ALT_SIZES, f_inverse),
    Fmt("icon-circle", "圆形容器", "头像被裁成圆形的平台上不会切角。", ALT_SIZES, f_circle),
    Fmt("mark", "无容器", "透明底的纯图形。README 页眉、文档水印用。", MARK_SIZES, f_mark),
)


# --------------------------------------------------------------------------- #
# 横版组合标
# --------------------------------------------------------------------------- #
LOCKUP_H = 320  # 母版画布高
LOCKUP_MARK = 248  # 图形边长
LOCKUP_GAP = 56  # 图形与文字之间的间距
LOCKUP_FONT = 132
LOCKUP_SIZES = (80, 160, 320)
FONT_FILE = Path.home() / ".fonts" / "NotoSansSC-Medium.ttf"
FONT_STACK = "'Noto Sans SC','Source Sans 3','DejaVu Sans',sans-serif"


def _measure(text: str) -> tuple[float, float]:
    """返回 (文字宽度, SVG 基线 y)，让文字在画布上视觉居中。"""
    from PIL import ImageFont

    font = ImageFont.truetype(str(FONT_FILE), LOCKUP_FONT)
    x0, y0, x1, y1 = font.getbbox(text)
    ascent, _ = font.getmetrics()
    return x1 - x0, LOCKUP_H / 2 + ascent - (y0 + y1) / 2


def render_lockup(s: Subject, *, on_dark: bool) -> str:
    text_w, baseline = _measure(s.name)
    text_x = LOCKUP_MARK + LOCKUP_GAP
    width = round(text_x + text_w)
    # 图形画在 1024 的局部坐标系里再整体缩放，userSpaceOnUse 的渐变
    # 必须按同一套坐标给，否则只覆盖左上角一小块。
    grad = (
        f'<linearGradient id="g" x1="0" y1="0" x2="{S}" y2="{S}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{s.c0}"/>'
        f'<stop offset="1" stop-color="{s.c1}"/></linearGradient>'
    )
    mark = knockout(s, ff_mark("url(#g)")) + badge(
        s, bg=INK if on_dark else s.deep, fg=s.deep if on_dark else INK
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {LOCKUP_H}" '
        f'width="{width}" height="{LOCKUP_H}" role="img" aria-label="{s.name}">'
        f"<defs>{grad}</defs>"
        f'<g transform="translate(0,{(LOCKUP_H - LOCKUP_MARK) / 2}) '
        f'scale({LOCKUP_MARK / S})">{mark}</g>'
        f'<text x="{text_x}" y="{baseline:.1f}" font-family="{FONT_STACK}" '
        f'font-size="{LOCKUP_FONT}" font-weight="500" '
        f'fill="{INK if on_dark else "#0F172A"}">{s.name}</text></svg>'
    )


# --------------------------------------------------------------------------- #
# 输出
# --------------------------------------------------------------------------- #
def render_icon(fmt: Fmt, s: Subject) -> str:
    grad = (
        f'<linearGradient id="g" x1="0" y1="0" x2="{S}" y2="{S}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{s.c0}"/>'
        f'<stop offset="1" stop-color="{s.c1}"/></linearGradient>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" '
        f'width="{S}" height="{S}" role="img" aria-label="{s.name} logo">'
        f"<defs>{grad}</defs>{fmt.body(s)}</svg>"
    )


def main() -> None:
    import cairosvg

    for d in (SVG_DIR, PNG_DIR, ICO_DIR):
        shutil.rmtree(d, ignore_errors=True)
    ICO_DIR.mkdir(parents=True, exist_ok=True)

    n_png = 0
    for fmt in FORMATS:
        (SVG_DIR / fmt.key).mkdir(parents=True, exist_ok=True)
        (PNG_DIR / fmt.key).mkdir(parents=True, exist_ok=True)
        for s in SUBJECTS:
            svg = render_icon(fmt, s)
            (SVG_DIR / fmt.key / f"{s.key}.svg").write_text(svg, encoding="utf-8")
            for size in fmt.sizes:
                cairosvg.svg2png(
                    bytestring=svg.encode(),
                    write_to=str(PNG_DIR / fmt.key / f"{s.key}-{size}.png"),
                    output_width=size,
                    output_height=size,
                )
                n_png += 1

    for suffix, on_dark in (("lockup", False), ("lockup-on-dark", True)):
        (SVG_DIR / suffix).mkdir(parents=True, exist_ok=True)
        (PNG_DIR / suffix).mkdir(parents=True, exist_ok=True)
        for s in SUBJECTS:
            svg = render_lockup(s, on_dark=on_dark)
            (SVG_DIR / suffix / f"{s.key}.svg").write_text(svg, encoding="utf-8")
            for h in LOCKUP_SIZES:
                cairosvg.svg2png(
                    bytestring=svg.encode(),
                    write_to=str(PNG_DIR / suffix / f"{s.key}-{h}.png"),
                    output_height=h,
                )
                n_png += 1

    # 多尺寸 .ico，直接丢进任意 Web 项目当 favicon
    from PIL import Image

    for s in SUBJECTS:
        src = Image.open(PNG_DIR / "icon" / f"{s.key}-256.png").convert("RGBA")
        src.save(ICO_DIR / f"{s.key}.ico", format="ICO",
                 sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])

    n_fmt = len(FORMATS) + 2
    print(
        f"{n_fmt} 种格式 × {len(SUBJECTS)} 个主体（{len(ORGS)} 组织 + {len(PLUGINS)} 插件）："
        f"{n_png} 张 PNG、{n_fmt * len(SUBJECTS)} 个 SVG、"
        f"{len(SUBJECTS)} 个 .ico 已写入 {BRAND}"
    )


if __name__ == "__main__":
    main()
