#!/usr/bin/env python3
"""farfarfun 组织、uTools 插件与独立应用的 logo 生成器。

生成全部格式与尺寸的 SVG、PNG 与 favicon：

    uv run python brand/gen_logos.py

每个主体沿用主组织的折叠 F 和笑脸，在上横线放入各自的小符号。

除 farfarfun 的原版矢量源 ``farfarfun-original.svg`` 外，这个文件是图形产物的来源。
要改图形就改源文件再重跑，不要手工动
``svg/`` ``png/`` ``favicon/``——每次运行都会先清空再整体重建。
"""

from __future__ import annotations

import colorsys
import shutil
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable
from xml.etree import ElementTree as ET

BRAND = Path(__file__).resolve().parent
SVG_DIR = BRAND / "svg"
PNG_DIR = BRAND / "png"
ICO_DIR = BRAND / "favicon"
ORIGINAL_SVG = BRAND / "farfarfun-original.svg"

S = 1024  # 画布边长
RX = 232  # 圆角方形的圆角半径
MOTIF_TRANSFORM = "translate(780,336) scale(0.23) translate(-512,-512)"
PLUGIN_MOTIF_TRANSFORM = "translate(780,336) scale(0.30) translate(-512,-512)"


# --------------------------------------------------------------------------- #
# 主图形
# --------------------------------------------------------------------------- #
CLASH_LETTERS = (
    "M 215 390 C 180 360 125 375 110 420 C 95 465 95 555 110 600 "
    "C 125 645 180 660 215 630 "
    "M 285 375 V 645 H 390 "
    "M 455 645 L 510 375 L 565 645 M 470 565 H 550 "
    "M 735 395 C 705 365 635 365 625 425 C 615 485 735 485 735 555 "
    "C 735 630 665 665 620 625 "
    "M 805 375 V 645 M 805 510 H 915 M 915 375 V 645"
)


def stroked(d: str, color: str, width: float) -> str:
    return (
        f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}" '
        'stroke-linecap="round" stroke-linejoin="round"/>'
    )


def ff_mark(color: str, eye_color: str = "#0c1b65") -> str:
    """Use the original SVG's silhouette in monochrome formats."""
    root = ET.parse(ORIGINAL_SVG).getroot()
    ns = "{http://www.w3.org/2000/svg}"
    shapes = ("upper-shape", "face-shape", "foot-shape")
    paths = [root.find(f"{ns}path[@id='{name}']") for name in shapes]
    eye_element = root.find(f"{ns}path[@id='eyes']")
    assert all(path is not None for path in paths) and eye_element is not None
    fill_paths = "".join(f'<path fill="{color}" d="{path.get("d")}"/>' for path in paths)
    eye_path = (
        f'<path fill="none" stroke="{eye_color}" stroke-width="22" stroke-linecap="round" '
        f'd="{eye_element.get("d")}"/>'
    )
    return f'<g transform="scale({S / 1254})">{fill_paths}{eye_path}</g>'


def shifted_color(value: str, delta: float) -> str:
    rgb = [int(value[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    hue, lightness, saturation = colorsys.rgb_to_hls(*rgb)
    rgb = colorsys.hls_to_rgb((hue + delta) % 1, lightness, saturation)
    return "#" + "".join(f"{round(channel * 255):02x}" for channel in rgb)


def family_root(s: Subject) -> ET.Element:
    root = ET.parse(ORIGINAL_SVG).getroot()
    if s.key == "farfarfun":
        return root
    base_hue = colorsys.rgb_to_hls(24 / 255, 85 / 255, 232 / 255)[0]
    rgb = [int(s.c0[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    delta = colorsys.rgb_to_hls(*rgb)[0] - base_hue
    for element in root.iter():
        for attribute in ("fill", "stroke", "stop-color"):
            value = element.get(attribute)
            if value and value.startswith("#"):
                element.set(attribute, shifted_color(value, delta))
    accent = shifted_color("#0c1b65", delta)
    motif_transform = PLUGIN_MOTIF_TRANSFORM if s in PLUGINS else MOTIF_TRANSFORM
    motif = ET.fromstring(f'<g xmlns="http://www.w3.org/2000/svg" transform="{motif_transform}">{s.mark(accent)}</g>')
    root.append(motif)
    if s in PLUGINS:
        group = ET.SubElement(root, "{http://www.w3.org/2000/svg}g", {
            "transform": "translate(627,627) scale(1.30) translate(-627,-627)",
        })
        for element in list(root):
            if element.tag == "{http://www.w3.org/2000/svg}path" or element is motif:
                root.remove(element)
                group.append(element)
    root.set("aria-label", f"{s.name} logo")
    return root


def family_flat_mark(s: Subject, color: str, accent: str) -> str:
    if s.key == "farfarfun":
        return ff_mark(color)
    motif_transform = PLUGIN_MOTIF_TRANSFORM if s in PLUGINS else MOTIF_TRANSFORM
    mark = (
        ff_mark(color, accent)
        + f'<g transform="scale({S / 1254}) {motif_transform}">{s.mark(accent)}</g>'
    )
    if s in PLUGINS:
        # 启动器里的透明图标保留约 4% 上下留白，避免主体显小。
        return f'<g transform="translate(512,512) scale(1.45) translate(-512,-512)">{mark}</g>'
    return mark


def cloud_mark(color: str) -> str:
    return stroked(
        "M 348 668 H 706 C 784 668 822 619 822 556 C 822 492 772 446 705 444 "
        "C 675 354 606 310 522 310 C 438 310 373 360 354 436 "
        "C 273 439 215 486 215 552 C 215 617 267 668 348 668 Z", color, 86
    )


def spark_mark(color: str) -> str:
    return (
        f'<path fill="{color}" d="M 512 200 C 552 390 634 472 824 512 '
        'C 634 552 552 634 512 824 C 472 634 390 552 200 512 '
        'C 390 472 472 390 512 200 Z"/>'
    )


def stack_mark(color: str) -> str:
    return (
        f'<path fill="{color}" d="M 512 248 L 777 374 L 512 500 L 247 374 Z"/>'
        + stroked("M 255 520 L 512 642 L 769 520", color, 78)
        + stroked("M 255 668 L 512 790 L 769 668", color, 78)
    )


def puzzle_mark(color: str) -> str:
    return (
        '<g transform="translate(512,512) scale(5.2)">'
        f'<path fill="{color}" stroke="{color}" stroke-width="13" stroke-linejoin="round" '
        'd="M -44 -44 L -16 -44 A 19 19 0 1 1 16 -44 L 44 -44 L 44 44 L -44 44 '
        'L -44 16 A 19 19 0 1 0 -44 -16 Z"/></g>'
    )


def play_mark(color: str) -> str:
    return (
        f'<path fill="{color}" d="M 354 283 Q 354 245 393 268 L 753 476 '
        'Q 795 500 753 525 L 393 757 Q 354 780 354 741 Z"/>'
    )


def game_mark(color: str) -> str:
    return (
        stroked(
            "M 318 360 H 706 C 772 360 810 402 828 468 L 874 649 "
            "C 893 726 827 771 762 730 L 666 669 H 358 L 262 730 "
            "C 197 771 131 726 150 649 L 196 468 C 214 402 252 360 318 360 Z",
            color, 68
        )
        + stroked("M 300 514 H 456 M 378 436 V 592", color, 58)
        + f'<g fill="{color}"><circle cx="650" cy="488" r="39"/>'
        '<circle cx="740" cy="576" r="39"/></g>'
    )


def bubble_mark(color: str) -> str:
    return (
        stroked(
            "M 385 285 H 639 C 739 285 790 340 790 435 V 542 "
            "C 790 641 733 695 640 695 H 465 L 318 790 L 344 680 "
            "C 269 652 230 602 230 542 V 435 C 230 340 286 285 385 285 Z", color, 76
        )
        + f'<g fill="{color}"><circle cx="390" cy="490" r="37"/>'
        '<circle cx="512" cy="490" r="37"/><circle cx="634" cy="490" r="37"/></g>'
    )


def doc_mark(color: str) -> str:
    return (
        f'<rect x="310" y="250" width="404" height="524" rx="50" fill="none" '
        f'stroke="{color}" stroke-width="96"/>'
        + stroked("M 410 424 H 614 M 410 528 H 614 M 410 632 H 554", color, 80)
    )


def bookmark_mark(color: str) -> str:
    return (
        f'<path fill="{color}" d="M 330 260 H 694 Q 740 260 740 305 V 770 '
        'L 512 623 L 284 770 V 305 Q 284 260 330 260 Z"/>'
    )


def shield_mark(color: str) -> str:
    return (
        stroked(
            "M 512 239 L 748 331 V 515 C 748 655 649 749 512 797 "
            "C 375 749 276 655 276 515 V 331 Z", color, 76
        )
        + stroked("M 390 510 L 480 605 L 650 425", color, 76)
    )


def clash_mark(color: str) -> str:
    return stroked(CLASH_LETTERS, color, 48)


def calendar_mark(color: str) -> str:
    return (
        f'<rect x="260" y="300" width="504" height="464" rx="60" fill="none" '
        f'stroke="{color}" stroke-width="72"/>'
        + stroked("M 380 240 V 360 M 644 240 V 360 M 270 450 H 754", color, 72)
        + stroked("M 410 594 L 482 666 L 626 540", color, 72)
    )


def qr_mark(color: str) -> str:
    return stroked(
        "M 250 250 H 440 V 440 H 250 Z M 584 250 H 774 V 440 H 584 Z "
        "M 250 584 H 440 V 774 H 250 Z M 584 584 H 656 V 656 H 584 Z "
        "M 774 544 V 656 M 544 774 H 656 V 702 M 774 774 H 712", color, 48
    )


def calculator_mark(color: str) -> str:
    return stroked("M 730 280 H 300 L 520 512 L 300 744 H 730", color, 76)


# --------------------------------------------------------------------------- #
# 主体与色板
# --------------------------------------------------------------------------- #
@dataclass(frozen=True)
class Subject:
    """一个要出图的主体：一个组织、一个 uTools 插件，或一个独立应用。"""

    key: str  # 文件名
    name: str  # 组合标上的名字
    label: str  # 中文定位
    c0: str  # 渐变起点
    c1: str  # 渐变终点
    deep: str  # 单色场景用的深色
    mark: Callable[[str], str] = ff_mark


ORGS: tuple[Subject, ...] = (
    Subject("farfarfun", "farfarfun", "主组织 / Python 工具链", "#1855E8", "#19C6F4", "#07133F", ff_mark),
    Subject("drive", "farfarfun-drive", "网盘 / 云存储", "#0EA5E9", "#1D4ED8", "#1D4ED8", cloud_mark),
    Subject("skill", "farfarfun-skill", "自研 AI Agent Skill", "#8B5CF6", "#6D28D9", "#6D28D9", spark_mark),
    Subject("skills", "farfarfun-skills", "Skill 聚合镜像", "#6366F1", "#4338CA", "#4338CA", stack_mark),
    Subject("utools", "farfarfun-utools", "uTools 插件", "#14B8A6", "#0F766E", "#0F766E", puzzle_mark),
    Subject("action", "farfarfun-action", "GitHub Action", "#F97316", "#C2410C", "#C2410C", play_mark),
    Subject("game", "farfarfun-game", "游戏 / FunGame", "#84CC16", "#4D7C0F", "#4D7C0F", game_mark),
)

# 插件会在 uTools 启动器里并排出现，因此保留彼此区分明显的色相。
PLUGINS: tuple[Subject, ...] = (
    Subject("funchat", "funchat", "AI 好友聊天", "#06B6D4", "#0E7490", "#0E7490", bubble_mark),
    Subject("fundoc", "fundoc", "FunDoc 文档", "#4F46E5", "#3730A3", "#3730A3", doc_mark),
    Subject("funlink", "funlink", "网址收藏", "#22C55E", "#15803D", "#15803D", bookmark_mark),
    Subject("funotp", "funotp", "FunOTP 两步验证", "#F43F5E", "#BE123C", "#BE123C", shield_mark),
    Subject("funcalendar", "FunCalendar", "时光常伴 / 双历与黄历", "#F59E0B", "#B45309", "#B45309", calendar_mark),
    Subject("funqr", "FunQR", "码上生花 / 二维码互转", "#9874CF", "#654092", "#654092", qr_mark),
    Subject("funcalc", "FunCalc", "算有所得 / 计算笔记本", "#3B82F6", "#1D4ED8", "#1D4ED8", calculator_mark),
)

APPS: tuple[Subject, ...] = (
    Subject("funclash", "FunClash", "代理客户端 / mihomo 内核", "#D946EF", "#7E22CE",
            "#7E22CE", clash_mark),
)

SUBJECTS: tuple[Subject, ...] = ORGS + PLUGINS + APPS

INK = "#FFFFFF"  # 深色底上的图形色
PAPER = "#F8FAFC"  # 反白版的底色
PAPER_EDGE = "#E2E8F0"  # 反白版的描边，防止在白色页面上糊掉


# --------------------------------------------------------------------------- #
# 容器
# --------------------------------------------------------------------------- #
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
    """主图标由 render_icon() 中的原版 SVG 家族造型生成。"""
    return squircle("url(#g)") + s.mark(INK)


def f_inverse(s: Subject) -> str:
    """反白：浅底配渐变图形。深色页眉、贴纸、印刷物用。"""
    return squircle(PAPER, PAPER_EDGE) + family_flat_mark(s, "url(#g)", INK)


def f_circle(s: Subject) -> str:
    """圆形容器：头像被裁成圆形的平台上不会切角。"""
    scaled = (
        '<g transform="translate(512,512) scale(0.86) translate(-512,-512)">'
        f"{family_flat_mark(s, INK, s.deep)}</g>"
    )
    circle_fill = "url(#bg)" if s.key == "farfarfun" else "url(#g)"
    return (
        f'<circle cx="512" cy="512" r="512" fill="{circle_fill}"/>'
        + scaled
    )


def f_mark(s: Subject) -> str:
    """无容器：透明底的纯图形。README 页眉、水印用。"""
    return family_flat_mark(s, "url(#g)", INK)


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
    grad = (
        f'<linearGradient id="g" x1="0" y1="0" x2="{S}" y2="{S}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{s.c0}"/>'
        f'<stop offset="1" stop-color="{s.c1}"/></linearGradient>'
    )
    mark = family_flat_mark(s, "url(#g)", INK)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {LOCKUP_H}" '
        f'width="{width}" height="{LOCKUP_H}" role="img" aria-label="{s.name}">'
        f'<defs>{grad}</defs>'
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
    if fmt.key == "icon":
        return (ORIGINAL_SVG.read_text(encoding="utf-8") if s.key == "farfarfun"
                else ET.tostring(family_root(s), encoding="unicode"))
    grad = (
        f'<linearGradient id="g" x1="0" y1="0" x2="{S}" y2="{S}" '
        f'gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{s.c0}"/>'
        f'<stop offset="1" stop-color="{s.c1}"/></linearGradient>'
    )
    bg = (
        '<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
        '<stop offset="0" stop-color="#1745D1"/>'
        '<stop offset=".28" stop-color="#09A7F5"/>'
        '<stop offset=".55" stop-color="#0756C7"/>'
        '<stop offset=".78" stop-color="#101C60"/>'
        '<stop offset="1" stop-color="#050B30"/></linearGradient>'
    )
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {S} {S}" '
        f'width="{S}" height="{S}" role="img" aria-label="{s.name} logo">'
        f'<defs>{grad}{bg if s.key == "farfarfun" and fmt.key == "icon-circle" else ""}</defs>'
        f'{fmt.body(s)}</svg>'
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
        f"{n_fmt} 种格式 × {len(SUBJECTS)} 个主体（{len(ORGS)} 组织 + {len(PLUGINS)} 插件"
        f" + {len(APPS)} 应用）："
        f"{n_png} 张 PNG、{n_fmt * len(SUBJECTS)} 个 SVG、"
        f"{len(SUBJECTS)} 个 .ico 已写入 {BRAND}"
    )


if __name__ == "__main__":
    main()
