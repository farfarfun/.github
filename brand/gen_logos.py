#!/usr/bin/env python3
"""farfarfun 组织 logo 生成器。

生成全部候选方案的 SVG 与 PNG：

    uv run python brand/gen_logos.py

核心图形是 ``ff`` 连字——两个 f 共享一道横杠，笔画在底部连成微笑弧。
主组织用纯 ff，子组织在右下角挂一枚角标区分产品线。
"""

from __future__ import annotations

import shutil
from dataclasses import dataclass, field
from pathlib import Path

BRAND = Path(__file__).resolve().parent
SVG_DIR = BRAND / "svg"
PNG_DIR = BRAND / "png"

S = 1024  # 画布边长
RX = 232  # 圆角方形的圆角半径


# --------------------------------------------------------------------------- #
# 组织与色板
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Org:
    key: str  # 文件名
    name: str  # GitHub 组织名
    label: str  # 中文定位
    c0: str  # 渐变起点
    c1: str  # 渐变终点
    deep: str  # 角标图形用的深色
    badge: str | None  # 角标图形，None 表示主组织不挂角标


ORGS: tuple[Org, ...] = (
    Org("farfarfun", "farfarfun", "主组织 / Python 工具链", "#06B6D4", "#7C3AED", "#6D28D9", None),
    Org("drive", "farfarfun-drive", "网盘 / 云存储", "#0EA5E9", "#1D4ED8", "#1D4ED8", "cloud"),
    Org("skill", "farfarfun-skill", "自研 AI Agent Skill", "#8B5CF6", "#6D28D9", "#6D28D9", "spark"),
    Org("skills", "farfarfun-skills", "Skill 聚合镜像", "#6366F1", "#4338CA", "#4338CA", "stack"),
    Org("utools", "farfarfun-utools", "uTools 插件", "#14B8A6", "#0F766E", "#0F766E", "puzzle"),
    Org("action", "farfarfun-action", "GitHub Action", "#F97316", "#C2410C", "#C2410C", "play"),
)

INK = "#FFFFFF"  # 深色底上的图形色
PAPER = "#F8FAFC"  # 反白方案的底色
PAPER_EDGE = "#E2E8F0"  # 反白方案的描边，防止在白色页面上糊掉


# --------------------------------------------------------------------------- #
# 图形几何
# --------------------------------------------------------------------------- #
# ff 单笔连字：f1 顶钩 → f1 竖 → 底部笑弧 → f2 竖 → f2 顶钩，一笔到底。
# 底部用扁椭圆弧而非正圆，弧线才读作「微笑」而不是「碗」。
FF_MONO = (
    "M 464 250 A 92 92 0 0 0 372 342 L 372 596 "
    "A 140 104 0 0 0 652 596 L 652 342 A 92 92 0 0 1 744 250"
)
FF_BAR = "M 290 452 L 734 452"  # 两个 f 共享的横杠
FF_STROKE = 86
FF_SHIFT = "translate(-5,37)"  # 把图形光学居中到画布中心

# ff 字母式：两个规规矩矩的 f，不加任何修饰，只靠字形本身
FF_LETTER_F1 = "M 464 262 A 92 92 0 0 0 372 354 L 372 700"
FF_LETTER_F2 = "M 744 262 A 92 92 0 0 0 652 354 L 652 700"
FF_LETTER_BAR = "M 290 468 L 734 468"
FF_LETTER_SHIFT = "translate(-5,31)"

# ff 表情版：两个 f 的顶钩当眉毛，竖画之间嵌一道小笑弧
FF_FACE_SMILE = "M 452 574 A 76 90 0 0 0 572 574"
FF_FACE_SMILE_STROKE = 54

# 备选概念：三连 chevron（far·far·fun ≈ Python REPL 的 >>>）
CHEV_W, CHEV_H, CHEV_STROKE = 104, 148, 84
CHEV_XS = (340, 512, 684)

# 角标
BADGE_CX = BADGE_CY = 806
BADGE_R = 150
GLYPH_SCALE = 1.52


def chevrons() -> str:
    half = CHEV_W / 2
    return " ".join(
        f"M {cx - half} {512 - CHEV_H} L {cx + half} 512 L {cx - half} {512 + CHEV_H}"
        for cx in CHEV_XS
    )


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
    raise ValueError(f"unknown glyph: {kind}")


BADGE_GAP = 26  # 角标与主图形之间挖出的空隙


def badge(org: Org, *, bg: str, fg: str, cx: float = BADGE_CX, cy: float = BADGE_CY,
          r: float = BADGE_R) -> str:
    if org.badge is None:
        return ""
    return (
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>'
        f'<g transform="translate({cx},{cy}) scale({GLYPH_SCALE})">'
        f"{glyph(org.badge, fg, bg)}</g>"
    )


def knockout(org: Org, mark: str, *, cx: float = BADGE_CX, cy: float = BADGE_CY,
             r: float = BADGE_R) -> str:
    """在主图形上挖掉角标占的那一圈，角标才会读作「盖在上面」。"""
    if org.badge is None:
        return mark
    mid = f"k-{org.key}"
    return (
        f'<mask id="{mid}" maskUnits="userSpaceOnUse" x="0" y="0" width="{S}" height="{S}">'
        f'<rect width="{S}" height="{S}" fill="white"/>'
        f'<circle cx="{cx}" cy="{cy}" r="{r + BADGE_GAP}" fill="black"/></mask>'
        f'<g mask="url(#{mid})">{mark}</g>'
    )


def stroked(d: str, color: str, width: float, extra: str = "") -> str:
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
        f'stroke-linecap="round" stroke-linejoin="round" {extra}/>'
    )


# --------------------------------------------------------------------------- #
# 方案
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Variant:
    key: str
    title: str
    note: str
    body: object = field(repr=False)  # (org) -> svg 片段


def _mark_mono(color: str, shift: str = FF_SHIFT) -> str:
    return (
        f'<g transform="{shift}">'
        f"{stroked(FF_MONO, color, FF_STROKE)}{stroked(FF_BAR, color, FF_STROKE)}</g>"
    )


def _mark_letter(color: str, *, face: bool = False) -> str:
    smile = stroked(FF_FACE_SMILE, color, FF_FACE_SMILE_STROKE) if face else ""
    return (
        f'<g transform="{FF_LETTER_SHIFT}">'
        f"{stroked(FF_LETTER_F1, color, FF_STROKE)}"
        f"{stroked(FF_LETTER_F2, color, FF_STROKE)}"
        f"{stroked(FF_LETTER_BAR, color, FF_STROKE)}{smile}</g>"
    )


def _squircle(fill: str, edge: str | None = None) -> str:
    stroke = f' stroke="{edge}" stroke-width="4"' if edge else ""
    return f'<rect x="0" y="0" width="{S}" height="{S}" rx="{RX}" fill="{fill}"{stroke}/>'


def v1(org: Org) -> str:  # 单笔连字 · 圆角方 · 渐变
    return _squircle("url(#g)") + knockout(org, _mark_mono(INK)) + badge(
        org, bg=INK, fg=org.deep
    )


def v2(org: Org) -> str:  # 纯字母式双 f
    return _squircle("url(#g)") + knockout(org, _mark_letter(INK)) + badge(
        org, bg=INK, fg=org.deep
    )


def v3(org: Org) -> str:  # 表情版：顶钩当眉毛，中间嵌笑弧
    return _squircle("url(#g)") + knockout(org, _mark_letter(INK, face=True)) + badge(
        org, bg=INK, fg=org.deep
    )


def v4(org: Org) -> str:  # 反白：浅底 + 渐变图形
    return (
        _squircle(PAPER, PAPER_EDGE)
        + knockout(org, _mark_mono("url(#g)"))
        + badge(org, bg=org.deep, fg=INK)
    )


def v5(org: Org) -> str:  # 圆形容器
    scaled = (
        '<g transform="translate(512,512) scale(0.86) translate(-512,-512)">'
        f"{_mark_mono(INK)}</g>"
    )
    return (
        '<circle cx="512" cy="512" r="512" fill="url(#g)"/>'
        + knockout(org, scaled, cx=752, cy=752, r=142)
        + badge(org, bg=INK, fg=org.deep, cx=752, cy=752, r=142)
    )


def v6(org: Org) -> str:  # 无容器，透明底
    return knockout(org, _mark_mono("url(#g)")) + badge(org, bg=org.deep, fg=INK)


def v7(org: Org) -> str:  # 备选概念：>>> 三连 chevron
    mark = stroked(chevrons(), INK, CHEV_STROKE)
    return _squircle("url(#g)") + knockout(org, mark) + badge(org, bg=INK, fg=org.deep)


VARIANTS: tuple[Variant, ...] = (
    Variant("v1-ff-mono", "单笔连字", "一笔画完 ff 与底部笑弧，再加一道共享横杠。结构最简，16px 下仍然成立。", v1),
    Variant("v2-ff-letter", "纯字母式", "两个规规矩矩的 f 共享横杠，不加任何修饰。最克制，也最像一个字体厂牌。", v2),
    Variant("v3-ff-face", "表情版", "在 v2 的两道竖画之间嵌一道小笑弧，顶钩顺势成了眉毛。最外向的一版。", v3),
    Variant("v4-ff-inverse", "反白", "浅底配渐变图形。用在深色页眉、贴纸与印刷物上。", v4),
    Variant("v5-ff-circle", "圆形容器", "同样的连字放进正圆。头像被裁成圆形的平台上不会切角。", v5),
    Variant("v6-ff-bare", "无容器", "透明底的纯图形，供 README 页眉、favicon 与水印使用。", v6),
    Variant("v7-chevron", "备选概念 · 三连 chevron", "far·far·fun 三个词对应三个尖角，也是 Python REPL 的 >>> 提示符。", v7),
)


# --------------------------------------------------------------------------- #
# 横版组合标
# --------------------------------------------------------------------------- #
LOCKUP_H = 320  # 画布高
LOCKUP_MARK = 248  # 图形边长
LOCKUP_GAP = 56  # 图形与文字之间的间距
LOCKUP_FONT = 132
FONT_FILE = Path.home() / ".fonts" / "NotoSansSC-Medium.ttf"
FONT_STACK = "'Noto Sans SC','Source Sans 3','DejaVu Sans',sans-serif"


def _measure(text: str) -> tuple[float, float]:
    """返回 (文字宽度, SVG 基线 y)，让文字在画布上视觉居中。"""
    from PIL import ImageFont

    font = ImageFont.truetype(str(FONT_FILE), LOCKUP_FONT)
    x0, y0, x1, y1 = font.getbbox(text)
    ascent, _ = font.getmetrics()
    return x1 - x0, LOCKUP_H / 2 + ascent - (y0 + y1) / 2


def render_lockup(org: Org, *, on_dark: bool) -> str:
    text_w, baseline = _measure(org.name)
    text_x = LOCKUP_MARK + LOCKUP_GAP
    width = round(text_x + text_w)
    # 图形画在 1024 的局部坐标系里再整体缩放，userSpaceOnUse 的渐变
    # 必须按同一套坐标给，否则只覆盖左上角一小块。
    grad = (
        f'<linearGradient id="g" x1="0" y1="0" x2="{S}" y2="{S}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{org.c0}"/>'
        f'<stop offset="1" stop-color="{org.c1}"/></linearGradient>'
    )
    scale = LOCKUP_MARK / S
    mark = knockout(org, _mark_mono("url(#g)")) + badge(
        org, bg=org.deep if not on_dark else INK, fg=INK if not on_dark else org.deep
    )
    fill = INK if on_dark else "#0F172A"
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {LOCKUP_H}" '
        f'width="{width}" height="{LOCKUP_H}" role="img" '
        f'aria-label="{org.name}">'
        f"<defs>{grad}</defs>"
        f'<g transform="translate(0,{(LOCKUP_H - LOCKUP_MARK) / 2}) scale({scale})">'
        f"{mark}</g>"
        f'<text x="{text_x}" y="{baseline:.1f}" font-family="{FONT_STACK}" '
        f'font-size="{LOCKUP_FONT}" font-weight="500" fill="{fill}">{org.name}</text>'
        f"</svg>"
    )


# --------------------------------------------------------------------------- #
# 输出
# --------------------------------------------------------------------------- #
def render_svg(variant: Variant, org: Org) -> str:
    grad = (
        f'<linearGradient id="g" x1="0" y1="0" x2="{S}" y2="{S}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{org.c0}"/>'
        f'<stop offset="1" stop-color="{org.c1}"/></linearGradient>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" '
        f'width="{S}" height="{S}" role="img" '
        f'aria-label="{org.name} logo">'
        f"<defs>{grad}</defs>{variant.body(org)}</svg>"
    )


def main() -> None:
    import cairosvg

    for d in (SVG_DIR, PNG_DIR):
        shutil.rmtree(d, ignore_errors=True)

    for variant in VARIANTS:
        svg_dir = SVG_DIR / variant.key
        png_dir = PNG_DIR / variant.key
        svg_dir.mkdir(parents=True, exist_ok=True)
        png_dir.mkdir(parents=True, exist_ok=True)

        for org in ORGS:
            svg = render_svg(variant, org)
            (svg_dir / f"{org.key}.svg").write_text(svg, encoding="utf-8")
            for size in (512, 64):
                cairosvg.svg2png(
                    bytestring=svg.encode(),
                    write_to=str(png_dir / f"{org.key}-{size}.png"),
                    output_width=size,
                    output_height=size,
                )

    # 横版组合标：浅色底与深色底各一套
    lock_svg = SVG_DIR / "lockup"
    lock_png = PNG_DIR / "lockup"
    lock_svg.mkdir(parents=True, exist_ok=True)
    lock_png.mkdir(parents=True, exist_ok=True)
    for org in ORGS:
        for suffix, on_dark in (("", False), ("-on-dark", True)):
            svg = render_lockup(org, on_dark=on_dark)
            name = f"{org.key}{suffix}"
            (lock_svg / f"{name}.svg").write_text(svg, encoding="utf-8")
            cairosvg.svg2png(
                bytestring=svg.encode(),
                write_to=str(lock_png / f"{name}.png"),
                output_height=160,
            )

    n = len(VARIANTS) * len(ORGS)
    print(f"{n} 套图标 + {len(ORGS) * 2} 套横版组合标已写入 {SVG_DIR.parent}")


if __name__ == "__main__":
    main()
