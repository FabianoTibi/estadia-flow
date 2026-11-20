#!/usr/bin/env python3
"""Gera os arquivos da marca EstadiaFlow (SVG, PNG, favicon, ícones de app).

Uso:
  python3 scripts/build-brand.py --sora-bold <Sora-700.woff|ttf> --inter-medium <Inter-500.woff|ttf>

Requisitos: fonttools, Pillow e o binário rsvg-convert (pacote librsvg2-bin).
As fontes servem apenas para converter o nome e o slogan em curvas; os SVGs gerados
não dependem de fonte instalada. Os arquivos gerados são versionados, então só é
preciso rodar este script quando o desenho da marca mudar.
"""
import argparse
import subprocess
import tempfile
from pathlib import Path

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
BRAND = ROOT / "apps/web/public/brand"
ICONS = ROOT / "apps/web/public/icons"
APP = ROOT / "apps/web/src/app"

C1, BLUE, C2, NAVY, WHITE = "#19C8F5", "#2563EB", "#7C3AED", "#0B1B4D", "#FFFFFF"
ROUND = 'stroke-linecap="round" stroke-linejoin="round"'
LIGHT_BLUE = "#7DB4FF"
# Desenho do símbolo (caixa 64x64). Replicado em apps/web/src/components/brand/Logo.tsx.
ROOF = "M16.5 26 L31 13 L41.4 22.3"
BASE = "M50 36.5 V50 a5 5 0 0 1 -5 5 H17 a5 5 0 0 1 -5 -5 V37.5"
TAIL = "M1 31 C11 29.5 22 30 29.2 35.2 L25.2 39.2 C20 34.5 11 32 1 31 Z"
CHECK = "M27 37 L35 45 L58 11"
ROOF_REDUCED = "M12 30 L31 13 L41.4 22.3"
BASE_REDUCED = "M50 37.5 V50 a5 5 0 0 1 -5 5 H17 a5 5 0 0 1 -5 -5 V30"
CHECK_REDUCED = "M26 36 L35 45 L58 11"
TAGLINE = "Gerencie. Automatize. Encante."


# ----------------------------------------------------------------------------- símbolo
def symbol(mode: str, uid: str, reduced: bool = False) -> str:
    """Símbolo EstadiaFlow numa caixa 64x64: casa em contorno aberto atravessada por um check em movimento.

    mode: color (fundo claro) | dark (fundo escuro: casa branca, check ciano) | navy (uma cor) | white (tudo branco).
    """
    if mode == "color":
        house, light = f"url(#{uid}h)", f"url(#{uid}s)"
        grads = (
            f'<linearGradient id="{uid}h" x1="8" y1="12" x2="54" y2="58" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{NAVY}"/><stop offset="0.55" stop-color="{BLUE}"/><stop offset="1" stop-color="{C2}"/></linearGradient>'
            f'<linearGradient id="{uid}s" x1="2" y1="40" x2="60" y2="8" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{C1}"/><stop offset="1" stop-color="{BLUE}"/></linearGradient>'
        )
    elif mode == "dark":
        house, light = WHITE, f"url(#{uid}s)"
        grads = (
            f'<linearGradient id="{uid}s" x1="2" y1="40" x2="60" y2="8" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{C1}"/><stop offset="1" stop-color="{LIGHT_BLUE}"/></linearGradient>'
        )
    else:
        house = light = NAVY if mode == "navy" else WHITE
        grads = ""
    defs = f"<defs>{grads}</defs>" if grads else ""
    if reduced:
        # Abaixo de ~40 px: sem o rastro, traço mais grosso.
        return (
            defs
            + f'<path d="{ROOF_REDUCED}" stroke="{house}" stroke-width="7" {ROUND}/>'
            + f'<path d="{BASE_REDUCED}" stroke="{house}" stroke-width="7" {ROUND}/>'
            + f'<path d="{CHECK_REDUCED}" stroke="{light}" stroke-width="7" {ROUND}/>'
        )
    return (
        defs
        + f'<path d="{ROOF}" stroke="{house}" stroke-width="5.5" {ROUND}/>'
        + f'<path d="{BASE}" stroke="{house}" stroke-width="5.5" {ROUND}/>'
        + f'<path d="{TAIL}" fill="{light}"/>'
        + f'<path d="{CHECK}" stroke="{light}" stroke-width="5.5" {ROUND}/>'
    )


def svg_doc(inner: str, w: float, h: float, title: str) -> str:
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:g} {h:g}" width="{w:g}" height="{h:g}" fill="none" role="img" aria-label="{title}">'
        f"<title>{title}</title>{inner}</svg>\n"
    )


# ----------------------------------------------------------------------------- texto em curvas
class Outliner:
    def __init__(self, path: str):
        self.font = TTFont(path)
        self.glyphs = self.font.getGlyphSet()
        self.cmap = self.font.getBestCmap()
        self.upm = self.font["head"].unitsPerEm
        self.cap = getattr(self.font["OS/2"], "sCapHeight", 0) or self.upm * 0.7
        self.hmtx = self.font["hmtx"]

    def text(self, text: str, size: float, tracking_em: float = 0.0):
        """Retorna (d, largura, altura das maiúsculas) com a linha de base em y=0."""
        scale = size / self.upm
        x, parts = 0.0, []
        for i, ch in enumerate(text):
            name = self.cmap[ord(ch)]
            pen = SVGPathPen(self.glyphs, ntos=lambda v: f"{v:.2f}".rstrip("0").rstrip("."))
            self.glyphs[name].draw(TransformPen(pen, (scale, 0, 0, -scale, x, 0)))
            if pen.getCommands():
                parts.append(pen.getCommands())
            x += self.hmtx[name][0] * scale
            if i < len(text) - 1:
                x += tracking_em * size
        return " ".join(parts), x, self.cap * scale


def wordmark(sora: Outliner, size: float, mode: str, uid: str):
    """'Estadia' + 'Flow'. Retorna (svg, largura, altura das maiúsculas); linha de base em y=0."""
    d1, w1, cap = sora.text("Estadia", size, -0.035)
    x2 = w1 - size * 0.035  # mesma palavra: só o entreletras
    d2, w2, _ = sora.text("Flow", size, -0.035)
    main = {"color": NAVY, "navy": NAVY}.get(mode, WHITE)
    if mode in ("color", "dark"):
        a, b = (BLUE, C2) if mode == "color" else (C1, "#A9B8FF")
        grad = (
            f'<defs><linearGradient id="{uid}a" x1="0" y1="0" x2="{w2:.1f}" y2="0" gradientUnits="userSpaceOnUse">'
            f'<stop offset="0" stop-color="{a}"/><stop offset="1" stop-color="{b}"/></linearGradient></defs>'
        )
        flow = f"url(#{uid}a)"
    else:
        grad, flow = "", main
    out = f'{grad}<path d="{d1}" fill="{main}"/><g transform="translate({x2:.2f} 0)"><path d="{d2}" fill="{flow}"/></g>'
    return out, x2 + w2, cap


# ----------------------------------------------------------------------------- assinaturas
def horizontal(sora, mode, uid, pad=6):
    s, size, gap = 96, 46, 20
    word, ww, cap = wordmark(sora, size, mode, uid)
    w, h = pad + s + gap + ww + pad, s + 2 * pad
    base = pad + s * 0.53 + cap / 2
    inner = (
        f'<g transform="translate({pad} {pad}) scale({s / 64})">{symbol(mode, uid)}</g>'
        f'<g transform="translate({pad + s + gap:.2f} {base:.2f})">{word}</g>'
    )
    return inner, w, h


def horizontal_tagline(sora, inter, mode, uid, pad=8):
    s, size, gap = 132, 50, 24
    word, ww, cap = wordmark(sora, size, mode, uid)
    tsize = 15.8
    td, tw, tcap = inter.text(TAGLINE, tsize, 0.03)
    # ajusta o entreletras do slogan para fechar na largura do nome
    extra = (ww - tw) / (len(TAGLINE) - 1) / tsize
    td, tw, tcap = inter.text(TAGLINE, tsize, 0.03 + extra)
    color = NAVY if mode in ("color", "navy") else WHITE
    block_h = cap + 16 + tcap + 13 + 2.5
    top = pad + (s - block_h) / 2 + 3
    x = pad + s + gap
    line = (
        f'<defs><linearGradient id="{uid}l" x1="0" y1="0" x2="{ww:.1f}" y2="0" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{C1}"/><stop offset="0.55" stop-color="{BLUE}"/><stop offset="1" stop-color="{C2}"/></linearGradient></defs>'
        f'<rect width="{ww:.2f}" height="2.5" rx="1.25" fill="url(#{uid}l)"/>'
        if mode == "color"
        else f'<rect width="{ww:.2f}" height="2.5" rx="1.25" fill="{color}" opacity="0.55"/>'
    )
    inner = (
        f'<g transform="translate({pad} {pad}) scale({s / 64})">{symbol(mode, uid)}</g>'
        f'<g transform="translate({x:.2f} {top + cap:.2f})">{word}</g>'
        f'<g transform="translate({x:.2f} {top + cap + 16 + tcap:.2f})"><path d="{td}" fill="{color}"/></g>'
        f'<g transform="translate({x:.2f} {top + cap + 16 + tcap + 13:.2f})">{line}</g>'
    )
    return inner, x + ww + pad, s + 2 * pad


def vertical(sora, mode, uid, pad=8):
    s, size, gap = 120, 40, 16
    word, ww, cap = wordmark(sora, size, mode, uid)
    w = max(s, ww) + 2 * pad
    inner = (
        f'<g transform="translate({(w - s) / 2:.2f} {pad}) scale({s / 64})">{symbol(mode, uid)}</g>'
        f'<g transform="translate({(w - ww) / 2:.2f} {pad + s + gap + cap:.2f})">{word}</g>'
    )
    return inner, w, pad + s + gap + cap + pad


# ----------------------------------------------------------------------------- ícones de app
def app_icon(size: int, radius_ratio: float, mark_ratio: float, reduced: bool) -> str:
    """Quadrado em degradê com o símbolo branco. radius_ratio=0 gera fundo sem cantos (iOS, maskable)."""
    r = size * radius_ratio
    m = size * mark_ratio
    off = (size - m) / 2
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" width="{size}" height="{size}" fill="none">'
        f'<defs><linearGradient id="bg" x1="0" y1="0" x2="{size}" y2="{size}" gradientUnits="userSpaceOnUse">'
        f'<stop offset="0" stop-color="{C1}"/><stop offset="0.5" stop-color="{BLUE}"/><stop offset="1" stop-color="{C2}"/></linearGradient></defs>'
        f'<rect width="{size}" height="{size}" rx="{r:g}" fill="url(#bg)"/>'
        f'<g transform="translate({off:g} {off:g}) scale({m / 64:g})">{symbol("white", "i", reduced)}</g></svg>\n'
    )


def render(svg_text: str, out: Path, width: int | None = None, height: int | None = None, background: str | None = None):
    out.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".svg", delete=False, encoding="utf-8") as tmp:
        tmp.write(svg_text)
    cmd = ["rsvg-convert", tmp.name, "-o", str(out)]
    if width:
        cmd += ["-w", str(width)]
    if height:
        cmd += ["-h", str(height)]
    if background:
        cmd += ["-b", background]
    subprocess.run(cmd, check=True)
    Path(tmp.name).unlink()


def write(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sora-bold", required=True)
    ap.add_argument("--inter-medium", required=True)
    args = ap.parse_args()
    sora, inter = Outliner(args.sora_bold), Outliner(args.inter_medium)

    # 1. Símbolos
    names = {"color": "", "navy": "-navy", "dark": "-white"}
    for mode, suffix in names.items():
        write(BRAND / f"symbol{suffix}.svg", svg_doc(symbol(mode, "s"), 64, 64, "EstadiaFlow"))
        write(BRAND / f"symbol-reduced{suffix}.svg", svg_doc(symbol(mode, "r", True), 64, 64, "EstadiaFlow"))

    # 2. Assinaturas
    docs = {}
    for mode, suffix in names.items():
        for key, builder in (
            ("logo-horizontal", lambda m: horizontal(sora, m, "h")),
            ("logo-horizontal-tagline", lambda m: horizontal_tagline(sora, inter, m, "t")),
            ("logo-vertical", lambda m: vertical(sora, m, "v")),
        ):
            inner, w, h = builder(mode)
            docs[f"{key}{suffix}"] = (svg_doc(inner, round(w, 1), round(h, 1), "EstadiaFlow"), w, h)
            write(BRAND / f"{key}{suffix}.svg", docs[f"{key}{suffix}"][0])

    # 3. PNGs para uso fora do sistema (e-mail, documentos, redes)
    png = BRAND / "png"
    for key in ("logo-horizontal", "logo-horizontal-white", "logo-horizontal-tagline", "logo-horizontal-tagline-white"):
        render(docs[key][0], png / f"{key}.png", width=1200)
    for key in ("logo-vertical", "logo-vertical-white"):
        render(docs[key][0], png / f"{key}.png", width=800)
    render(svg_doc(symbol("color", "s"), 64, 64, "EstadiaFlow"), png / "symbol-512.png", width=512)
    render(svg_doc(symbol("dark", "s"), 64, 64, "EstadiaFlow"), png / "symbol-white-512.png", width=512)

    # 4. Ícones do aplicativo web (Next.js lê icon.svg, favicon.ico e apple-icon.png de src/app)
    write(APP / "icon.svg", svg_doc(symbol("color", "f", True), 64, 64, "EstadiaFlow"))
    with tempfile.TemporaryDirectory() as tmp:
        frames = []
        for px in (16, 32, 48):
            p = Path(tmp) / f"{px}.png"
            render(svg_doc(symbol("color", "f", True), 64, 64, "EstadiaFlow"), p, width=px)
            frames.append(Image.open(p).convert("RGBA"))
        frames[-1].save(APP / "favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)], append_images=frames[:-1])
    render(app_icon(180, 0, 0.7, False), APP / "apple-icon.png")
    render(app_icon(192, 0.23, 0.7, True), ICONS / "icon-192.png")
    render(app_icon(512, 0.23, 0.7, False), ICONS / "icon-512.png")
    render(app_icon(192, 0, 0.56, True), ICONS / "icon-maskable-192.png")
    render(app_icon(512, 0, 0.56, False), ICONS / "icon-maskable-512.png")
    write(BRAND / "app-icon.svg", app_icon(512, 0.23, 0.7, False))

    # 5. Imagem de compartilhamento (Open Graph), 1200x630
    inner, w, h = horizontal_tagline(sora, inter, "color", "o")
    scale = 880 / w
    og = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 630" width="1200" height="630" fill="none">'
        f'<rect width="1200" height="630" fill="#FFFFFF"/>'
        f'<g transform="translate({(1200 - w * scale) / 2:.1f} {(630 - h * scale) / 2:.1f}) scale({scale:.4f})">{inner}</g></svg>'
    )
    render(og, APP / "opengraph-image.png")
    write(APP / "opengraph-image.alt.txt", "EstadiaFlow — Gerencie. Automatize. Encante.\n")

    print("Marca gerada em", BRAND.relative_to(ROOT), ICONS.relative_to(ROOT), APP.relative_to(ROOT))


if __name__ == "__main__":
    main()
