#!/usr/bin/env python3
"""Generate the real WBS image for the TAMEO-IA project.

The WBS content is curated from:
- Réalisation/dossier/dossierRéalisation.tex
- RapportFinal/rapport.tex

The SVG renderer intentionally uses only Python's standard library so the image
can be regenerated without Graphviz, Inkscape, or online services. If Pillow is
available, the script also writes a PNG copy for LaTeX inclusion.
"""

from __future__ import annotations

import argparse
import html
import textwrap
from dataclasses import dataclass
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[2]
REPORT_DIR = Path(__file__).resolve().parents[1]
LOGO_PATH = REPORT_DIR / "assets" / "tameo-logo.png"
SVG_LOGO_HREF = "../assets/tameo-logo.png"
DEFAULT_OUTPUT = REPORT_DIR / "img" / "wbs-reel-tameo.svg"
DEFAULT_PNG_OUTPUT = DEFAULT_OUTPUT.with_suffix(".png")
PNG_SCALE = 2
WIDTH = 1800
HEIGHT = 1275
MARGIN_X = 70
CARD_W = 520
CARD_H = 410
GAP_X = 50
ROW_1_Y = 275
ROW_2_Y = 735
ROOT_X = 520
ROOT_Y = 125
ROOT_W = 760
ROOT_H = 88
TRUNK_Y = 242
LOWER_TRUNK_Y = 702


@dataclass(frozen=True)
class Task:
    code: str
    title: str
    status: str = "Réalisé"


@dataclass(frozen=True)
class WorkPackage:
    code: str
    title: str
    accent: str
    tasks: tuple[Task, ...]


WBS: tuple[WorkPackage, ...] = (
    WorkPackage(
        "1",
        "Plateforme BlueBoat/banc d'essai",
        "#2E6F95",
        (
            Task("1.1", "Prise en main BlueOS, ArduPilot, MAVLink et QGroundControl"),
            Task("1.2", "Architecture réseau avec switch, Jetson et station à terre"),
            Task("1.3", "Accès distants SSH/VNC et endpoints MAVLink vers la Jetson"),
            Task("1.4", "Intégration physique Jetson, caméras, alimentation et boîte étanche"),
            Task("1.5", "Manuel d'utilisation du BlueBoat modifié"),
        ),
    ),
    WorkPackage(
        "2",
        "Vision et perception",
        "#3A8F7B",
        (
            Task("2.1", "Environnement reproductible Linux, Windows et Jetson"),
            Task("2.2", "Collecte, tri et préparation d'images maritimes"),
            Task("2.3", "Annotation CVAT des bouées et préparation des repères de docking"),
            Task("2.4", "Entraînements YOLO26 avec augmentations adaptées aux scènes maritimes"),
            Task("2.5", "Tests d'inférence, mesures de performance et préparation de l'export"),
            Task("2.6", "Documentation de configuration du module Vision"),
        ),
    ),
    WorkPackage(
        "3",
        "Embarqué et contrôle",
        "#7C6FB0",
        (
            Task("3.1", "Benchmark contrôleurs et choix BlueOS/ArduPilot"),
            Task("3.2", "Tests de communication BlueBoat, moteurs et firmware"),
            Task("3.3", "Interface VESC par script Lua, PWM fictif, UART et MAVLink"),
            Task("3.4", "Préparation de l'intégration des capteurs et actionneurs réels", "Engagé"),
            Task("3.5", "Procédures de tests, étalonnage et validation technique"),
        ),
    ),
    WorkPackage(
        "4",
        "Tests et intégration système",
        "#C46A4A",
        (
            Task("4.1", "Fixation des caméras, de la Jetson, du switch et de l'alimentation"),
            Task("4.2", "Support mobile pour essais GPS et validations à terre"),
            Task("4.3", "Tests du code IA sur plateforme réelle"),
            Task("4.4", "Supervision QGroundControl et capacité de reprise en main"),
            Task("4.5", "Validation des communications MAVLink, station sol et Jetson"),
        ),
    ),
    WorkPackage(
        "5",
        "Bateau réel et bancs de test",
        "#B28A2E",
        (
            Task("5.1", "Choix Hobie Cat 14 et conception du châssis aluminium"),
            Task("5.2", "Architecture électrique cohérente avec les sous-systèmes"),
            Task("5.3", "Architecture de direction brushless et évolution du safran"),
            Task("5.4", "Bancs de test moteur principal, direction, GPS et radiocommande"),
            Task("5.5", "Suivi conformité MEBC et choix système hybride pilote/radiocommande"),
        ),
    ),
    WorkPackage(
        "6",
        "Gestion, livrables et passation",
        "#4F7F52",
        (
            Task("6.1", "Coordination des pôles et séances de travail au FabLab"),
            Task("6.2", "Suivi budget, sponsors, achats, commandes et réception des composants"),
            Task("6.3", "Matrice RACI finale et suivi des risques techniques"),
            Task("6.4", "Rapport PIE, dossier de réalisation et documentation de continuité"),
            Task("6.5", "Manuels BlueBoat et Vision pour faciliter la continuité du projet"),
        ),
    ),
)


def wrap_lines(text: str, width: int) -> list[str]:
    return textwrap.wrap(
        text,
        width=width,
        break_long_words=False,
        break_on_hyphens=False,
    )


def svg_text(
    text: str,
    x: float,
    y: float,
    *,
    size: int = 18,
    weight: int = 400,
    fill: str = "#13283A",
    anchor: str = "start",
) -> str:
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-size="{size}" '
        f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">'
        f"{html.escape(text)}</text>"
    )


def rounded_rect(
    x: float,
    y: float,
    w: float,
    h: float,
    *,
    fill: str,
    stroke: str,
    stroke_width: float = 1.5,
    rx: float = 10,
) -> str:
    return (
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
        f'rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" '
        f'stroke-width="{stroke_width:.1f}"/>'
    )


def draw_wrapped_text(
    lines: list[str],
    x: float,
    y: float,
    *,
    size: int,
    fill: str,
    weight: int = 400,
    max_lines: int | None = None,
) -> tuple[str, float]:
    rendered: list[str] = []
    line_height = size * 1.22
    selected = lines if max_lines is None else lines[:max_lines]
    for idx, line in enumerate(selected):
        rendered.append(svg_text(line, x, y + idx * line_height, size=size, fill=fill, weight=weight))
    return "\n".join(rendered), y + len(selected) * line_height


def draw_card(pkg: WorkPackage, x: float, y: float, w: float, h: float) -> str:
    parts: list[str] = []
    parts.append(
        '<g filter="url(#shadow)">'
        + rounded_rect(x, y, w, h, fill="#FFFFFF", stroke="#D5DEE7", stroke_width=1.2, rx=12)
        + "</g>"
    )
    parts.append(rounded_rect(x, y, w, 9, fill=pkg.accent, stroke=pkg.accent, stroke_width=0, rx=4))

    badge_w = 54
    parts.append(rounded_rect(x + 22, y + 26, badge_w, 36, fill=pkg.accent, stroke=pkg.accent, rx=8))
    parts.append(svg_text(pkg.code, x + 22 + badge_w / 2, y + 50, size=21, weight=700, fill="#FFFFFF", anchor="middle"))

    title_lines = wrap_lines(pkg.title, 36)
    title_svg, after_title = draw_wrapped_text(
        title_lines,
        x + 92,
        y + 39,
        size=22,
        fill="#173B5C",
        weight=700,
        max_lines=2,
    )
    parts.append(title_svg)

    sep_y = max(y + 82, after_title + 13)
    parts.append(f'<line x1="{x + 22:.1f}" y1="{sep_y:.1f}" x2="{x + w - 22:.1f}" y2="{sep_y:.1f}" stroke="#E5EBF0" stroke-width="1.2"/>')

    task_y = sep_y + 33
    task_gap = 58 if len(pkg.tasks) <= 5 else 52
    for task in pkg.tasks:
        parts.append(rounded_rect(x + 24, task_y - 25, 66, 34, fill="#EEF4F7", stroke="#DCE7ED", stroke_width=1, rx=8))
        parts.append(svg_text(task.code, x + 57, task_y - 3, size=15, weight=700, fill=pkg.accent, anchor="middle"))

        chars = 50
        if task.status != "Réalisé":
            status_fill = "#FFF5DA"
            status_text = "#8A6817"
            parts.append(rounded_rect(x + w - 92, task_y - 26, 68, 25, fill=status_fill, stroke=status_fill, rx=12))
            parts.append(svg_text(task.status, x + w - 58, task_y - 9, size=11, weight=700, fill=status_text, anchor="middle"))
            chars = 41

        lines = wrap_lines(task.title, chars)
        body_svg, _ = draw_wrapped_text(lines, x + 106, task_y - 10, size=15, fill="#273B4A", max_lines=2)
        parts.append(body_svg)
        task_y += task_gap

    return "\n".join(parts)


def build_svg() -> str:
    width = WIDTH
    height = HEIGHT
    card_w = CARD_W
    card_h = CARD_H
    row_1_y = ROW_1_Y
    xs = [MARGIN_X, MARGIN_X + CARD_W + GAP_X, MARGIN_X + (CARD_W + GAP_X) * 2]
    positions = [(xs[i % 3], ROW_1_Y if i < 3 else ROW_2_Y) for i in range(len(WBS))]

    root_x = ROOT_X
    root_y = ROOT_Y
    root_w = ROOT_W
    root_h = ROOT_H
    trunk_y = TRUNK_Y

    parts: list[str] = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        '<title id="title">WBS réel du projet TAMEO-IA</title>',
        '<desc id="desc">Work Breakdown Structure des tâches réellement réalisées ou engagées, dérivé du dossier de réalisation et du rapport final.</desc>',
        "<defs>",
        '<filter id="shadow" x="-5%" y="-5%" width="110%" height="115%">',
        '<feDropShadow dx="0" dy="6" stdDeviation="7" flood-color="#0B2336" flood-opacity="0.13"/>',
        "</filter>",
        '<linearGradient id="pageBg" x1="0" x2="1" y1="0" y2="1">',
        '<stop offset="0%" stop-color="#F7FAFC"/>',
        '<stop offset="100%" stop-color="#EEF4F7"/>',
        "</linearGradient>",
        "</defs>",
        '<rect width="1800" height="1275" fill="url(#pageBg)"/>',
        svg_text("TAMEO - Pôle IA", 70, 72, size=28, weight=700, fill="#173B5C"),
        svg_text("WBS réel des tâches réalisées", width / 2, 75, size=44, weight=800, fill="#173B5C", anchor="middle"),
        svg_text("Périmètre constaté au 21 avril 2026", width / 2, 112, size=19, fill="#526778", anchor="middle"),
        f'<image href="{SVG_LOGO_HREF}" x="1500" y="44" width="235" height="67" preserveAspectRatio="xMidYMid meet"/>',
        '<g filter="url(#shadow)">'
        + rounded_rect(root_x, root_y, root_w, root_h, fill="#173B5C", stroke="#173B5C", stroke_width=0, rx=14)
        + "</g>",
        svg_text("Projet Bateau IA - TAMEO", root_x + 70, root_y + 48, size=27, weight=800, fill="#FFFFFF"),
        svg_text("Perception, intégration, contrôle, tests et transition vers le bateau réel", root_x + 70, root_y + 74, size=16, fill="#DDEBF1"),
        f'<line x1="{root_x + root_w / 2:.1f}" y1="{root_y + root_h:.1f}" x2="{root_x + root_w / 2:.1f}" y2="{trunk_y:.1f}" stroke="#8AA2B3" stroke-width="2.3"/>',
        f'<line x1="{positions[0][0] + card_w / 2:.1f}" y1="{trunk_y:.1f}" x2="{positions[2][0] + card_w / 2:.1f}" y2="{trunk_y:.1f}" stroke="#8AA2B3" stroke-width="2.3"/>',
    ]

    for x, y in positions[:3]:
        parts.append(f'<line x1="{x + card_w / 2:.1f}" y1="{trunk_y:.1f}" x2="{x + card_w / 2:.1f}" y2="{y:.1f}" stroke="#8AA2B3" stroke-width="2.3"/>')

    parts.extend(
        [
            f'<line x1="{positions[1][0] + card_w / 2:.1f}" y1="{row_1_y + card_h:.1f}" x2="{positions[1][0] + card_w / 2:.1f}" y2="{LOWER_TRUNK_Y:.1f}" stroke="#B4C3CE" stroke-width="2"/>',
            f'<line x1="{positions[3][0] + card_w / 2:.1f}" y1="{LOWER_TRUNK_Y:.1f}" x2="{positions[5][0] + card_w / 2:.1f}" y2="{LOWER_TRUNK_Y:.1f}" stroke="#B4C3CE" stroke-width="2"/>',
        ]
    )
    for x, y in positions[3:]:
        parts.append(f'<line x1="{x + card_w / 2:.1f}" y1="{LOWER_TRUNK_Y:.1f}" x2="{x + card_w / 2:.1f}" y2="{y:.1f}" stroke="#B4C3CE" stroke-width="2"/>')

    for pkg, (x, y) in zip(WBS, positions):
        parts.append(draw_card(pkg, x, y, card_w, card_h))

    legend_y = 1188
    parts.extend(
        [
            rounded_rect(70, legend_y - 31, 1660, 54, fill="#FFFFFF", stroke="#DCE5EC", stroke_width=1, rx=12),
            svg_text("Légende", 438, legend_y + 2, size=16, weight=800, fill="#173B5C", anchor="middle"),
            svg_text("Tous les éléments sont réalisés, sauf mention explicite", 535, legend_y + 2, size=14, fill="#526778"),
            f'<line x1="980" y1="{legend_y - 17}" x2="980" y2="{legend_y + 9}" stroke="#DCE5EC" stroke-width="1"/>',
            rounded_rect(1014, legend_y - 18, 70, 24, fill="#FFF5DA", stroke="#FFF5DA", rx=12),
            svg_text("Engagé", 1049, legend_y - 1, size=11, weight=700, fill="#8A6817", anchor="middle"),
            svg_text("Travail commencé et décrit comme en cours de transition", 1122, legend_y + 2, size=14, fill="#526778"),
        ]
    )

    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def write_png(output: Path, scale: int = PNG_SCALE) -> bool:
    try:
        from PIL import Image, ImageDraw, ImageFilter, ImageFont
    except ModuleNotFoundError:
        return False

    scale = max(1, scale)

    def sc(value: float) -> int:
        return round(value * scale)

    def sc_box(box: tuple[float, float, float, float]) -> tuple[int, int, int, int]:
        return tuple(sc(value) for value in box)

    def sc_points(points: list[tuple[float, float]]) -> list[tuple[int, int]]:
        return [(sc(x), sc(y)) for x, y in points]

    def font(size: int, bold: bool = False):
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        try:
            return ImageFont.truetype(name, size=sc(size))
        except OSError:
            return ImageFont.load_default()

    def text(
        draw: ImageDraw.ImageDraw,
        xy: tuple[float, float],
        value: str,
        *,
        size: int,
        fill: str,
        bold: bool = False,
        anchor: str | None = None,
    ) -> None:
        draw.text((sc(xy[0]), sc(xy[1])), value, font=font(size, bold), fill=fill, anchor=anchor)

    def wrapped(
        draw: ImageDraw.ImageDraw,
        value: str,
        x: float,
        y: float,
        *,
        chars: int,
        size: int,
        fill: str,
        bold: bool = False,
        max_lines: int | None = None,
    ) -> float:
        lines = wrap_lines(value, chars)
        if max_lines is not None:
            lines = lines[:max_lines]
        line_height = size * 1.22
        for idx, line in enumerate(lines):
            text(draw, (x, y + idx * line_height), line, size=size, fill=fill, bold=bold)
        return y + len(lines) * line_height

    def shadowed_round_rect(
        image: Image.Image,
        draw: ImageDraw.ImageDraw,
        box: tuple[float, float, float, float],
        *,
        radius: int,
        fill: str,
        outline: str,
        width: int = 1,
    ) -> None:
        shadow = Image.new("RGBA", image.size, (0, 0, 0, 0))
        shadow_draw = ImageDraw.Draw(shadow)
        shifted = (box[0], box[1] + 8, box[2], box[3] + 8)
        shadow_draw.rounded_rectangle(sc_box(shifted), radius=sc(radius), fill=(11, 35, 54, 28))
        image.alpha_composite(shadow.filter(ImageFilter.GaussianBlur(sc(8))))
        draw.rounded_rectangle(sc_box(box), radius=sc(radius), fill=fill, outline=outline, width=sc(width))

    image = Image.new("RGBA", (WIDTH * scale, HEIGHT * scale), "#F4F8FA")
    bg = Image.new("RGBA", (WIDTH * scale, HEIGHT * scale), "#F4F8FA")
    bg_draw = ImageDraw.Draw(bg)
    for y in range(HEIGHT * scale):
        ratio = y / max(HEIGHT * scale - 1, 1)
        r = int(247 * (1 - ratio) + 238 * ratio)
        g = int(250 * (1 - ratio) + 244 * ratio)
        b = int(252 * (1 - ratio) + 247 * ratio)
        bg_draw.line([(0, y), (WIDTH * scale, y)], fill=(r, g, b, 255))
    image.alpha_composite(bg)
    draw = ImageDraw.Draw(image)

    text(draw, (70, 47), "TAMEO - Pôle IA", size=28, fill="#173B5C", bold=True)
    if LOGO_PATH.exists():
        logo = Image.open(LOGO_PATH).convert("RGBA")
        logo_w = 235
        logo_h = round(logo.height * logo_w / logo.width)
        logo = logo.resize((sc(logo_w), sc(logo_h)), Image.Resampling.LANCZOS)
        image.alpha_composite(logo, (sc(WIDTH - 70 - logo_w), sc(42)))
    text(draw, (WIDTH / 2, 42), "WBS réel des tâches réalisées", size=44, fill="#173B5C", bold=True, anchor="ma")
    text(
        draw,
        (WIDTH / 2, 92),
        "Périmètre constaté au 21 avril 2026",
        size=19,
        fill="#526778",
        anchor="ma",
    )

    root_box = (ROOT_X, ROOT_Y, ROOT_X + ROOT_W, ROOT_Y + ROOT_H)
    shadowed_round_rect(image, draw, root_box, radius=14, fill="#173B5C", outline="#173B5C", width=0)
    #text(draw, (ROOT_X + 54, ROOT_Y + 43), "0", size=30, fill="#FFFFFF", bold=True, anchor="mm")
    text(draw, (ROOT_X + 55, ROOT_Y + 16), "Projet Bateau IA - TAMEO", size=27, fill="#FFFFFF", bold=True)
    text(
        draw,
        (ROOT_X + 55, ROOT_Y + 55),
        "Perception, intégration, contrôle, tests et transition vers le bateau réel",
        size=16,
        fill="#DDEBF1",
    )

    xs = [MARGIN_X, MARGIN_X + CARD_W + GAP_X, MARGIN_X + (CARD_W + GAP_X) * 2]
    positions = [(xs[i % 3], ROW_1_Y if i < 3 else ROW_2_Y) for i in range(len(WBS))]

    draw.line(sc_points([(ROOT_X + ROOT_W / 2, ROOT_Y + ROOT_H), (ROOT_X + ROOT_W / 2, TRUNK_Y)]), fill="#8AA2B3", width=sc(3))
    draw.line(sc_points([(positions[0][0] + CARD_W / 2, TRUNK_Y), (positions[2][0] + CARD_W / 2, TRUNK_Y)]), fill="#8AA2B3", width=sc(3))
    for x, y in positions[:3]:
        draw.line(sc_points([(x + CARD_W / 2, TRUNK_Y), (x + CARD_W / 2, y)]), fill="#8AA2B3", width=sc(3))
    draw.line(sc_points([(positions[1][0] + CARD_W / 2, ROW_1_Y + CARD_H), (positions[1][0] + CARD_W / 2, LOWER_TRUNK_Y)]), fill="#B4C3CE", width=sc(2))
    draw.line(sc_points([(positions[3][0] + CARD_W / 2, LOWER_TRUNK_Y), (positions[5][0] + CARD_W / 2, LOWER_TRUNK_Y)]), fill="#B4C3CE", width=sc(2))
    for x, y in positions[3:]:
        draw.line(sc_points([(x + CARD_W / 2, LOWER_TRUNK_Y), (x + CARD_W / 2, y)]), fill="#B4C3CE", width=sc(2))

    for pkg, (x, y) in zip(WBS, positions):
        shadowed_round_rect(image, draw, (x, y, x + CARD_W, y + CARD_H), radius=12, fill="#FFFFFF", outline="#D5DEE7")
        draw.rounded_rectangle(sc_box((x, y, x + CARD_W, y + 9)), radius=sc(4), fill=pkg.accent)
        draw.rounded_rectangle(sc_box((x + 22, y + 26, x + 76, y + 62)), radius=sc(8), fill=pkg.accent)
        text(draw, (x + 49, y + 44), pkg.code, size=21, fill="#FFFFFF", bold=True, anchor="mm")
        after_title = wrapped(draw, pkg.title, x + 92, y + 31, chars=36, size=22, fill="#173B5C", bold=True, max_lines=2)
        sep_y = max(y + 82, after_title + 13)
        draw.line(sc_box((x + 22, sep_y, x + CARD_W - 22, sep_y)), fill="#E5EBF0", width=sc(1))

        task_y = sep_y + 33
        task_gap = 58 if len(pkg.tasks) <= 5 else 52
        for task in pkg.tasks:
            draw.rounded_rectangle(sc_box((x + 24, task_y - 25, x + 90, task_y + 9)), radius=sc(8), fill="#EEF4F7", outline="#DCE7ED", width=sc(1))
            text(draw, (x + 57, task_y - 8), task.code, size=15, fill=pkg.accent, bold=True, anchor="mm")
            chars = 50
            if task.status != "Réalisé":
                draw.rounded_rectangle(sc_box((x + CARD_W - 92, task_y - 26, x + CARD_W - 24, task_y - 1)), radius=sc(12), fill="#FFF5DA")
                text(draw, (x + CARD_W - 58, task_y - 14), task.status, size=11, fill="#8A6817", bold=True, anchor="mm")
                chars = 41
            wrapped(draw, task.title, x + 106, task_y - 22, chars=chars, size=15, fill="#273B4A", max_lines=2)
            task_y += task_gap

    legend_y = 1188
    draw.rounded_rectangle(sc_box((70, legend_y - 31, 1730, legend_y + 23)), radius=sc(12), fill="#FFFFFF", outline="#DCE5EC", width=sc(1))
    text(draw, (438, legend_y - 11), "Légende", size=16, fill="#173B5C", bold=True, anchor="ma")
    #draw.line(sc_points([(535, legend_y - 17), (535, legend_y + 9)]), fill="#DCE5EC", width=sc(1))
    text(draw, (535, legend_y - 10), "Tous les éléments sont réalisés, sauf mention explicite", size=14, fill="#526778")
    draw.line(sc_points([(980, legend_y - 17), (980, legend_y + 9)]), fill="#DCE5EC", width=sc(1))
    draw.rounded_rectangle(sc_box((1014, legend_y - 18, 1084, legend_y + 6)), radius=sc(12), fill="#FFF5DA")
    text(draw, (1049, legend_y - 6), "Engagé", size=11, fill="#8A6817", bold=True, anchor="mm")
    #draw.line(sc_points([(1122, legend_y - 17), (1122, legend_y + 9)]), fill="#DCE5EC", width=sc(1))
    text(draw, (1122, legend_y - 10), "Travail commencé et décrit comme en cours de transition", size=14, fill="#526778")

    output.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output)
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate the real WBS SVG for the TAMEO-IA project.")
    parser.add_argument(
        "-o",
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT,
        help=f"SVG output path. Default: {DEFAULT_OUTPUT.relative_to(REPO_ROOT)}",
    )
    parser.add_argument(
        "--png-output",
        type=Path,
        default=None,
        help=f"PNG output path. Default: {DEFAULT_PNG_OUTPUT.relative_to(REPO_ROOT)}",
    )
    parser.add_argument("--no-png", action="store_true", help="Only generate the SVG file.")
    parser.add_argument("--png-scale", type=int, default=PNG_SCALE, help=f"PNG resolution scale. Default: {PNG_SCALE}.")
    args = parser.parse_args()

    output = args.output if args.output.is_absolute() else REPO_ROOT / args.output
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(build_svg(), encoding="utf-8")
    print(f"Generated {output.relative_to(REPO_ROOT)}")
    if not args.no_png:
        png_output_arg = args.png_output or output.with_suffix(".png")
        png_output = png_output_arg if png_output_arg.is_absolute() else REPO_ROOT / png_output_arg
        if write_png(png_output, scale=args.png_scale):
            print(f"Generated {png_output.relative_to(REPO_ROOT)}")
        else:
            print("Skipped PNG generation because Pillow is not installed.")


if __name__ == "__main__":
    main()
