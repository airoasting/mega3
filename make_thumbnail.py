from pathlib import Path
from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
OUT = ROOT / "thumbnail.png"

SCALE = 2
W, H = 1280 * SCALE, 720 * SCALE

PAPER = "#F0EBDE"
INK = "#1F2BE0"
INK_80 = (31, 43, 224, 205)
INK_55 = (31, 43, 224, 140)
GRID = (31, 43, 224, 24)

FONT_DIR = Path("/Users/jaydenkang/Library/Fonts")
PRETENDARD_BOLD = FONT_DIR / "Pretendard-Bold.ttf"
PRETENDARD_MEDIUM = FONT_DIR / "Pretendard-Medium.ttf"
PRETENDARD_REGULAR = FONT_DIR / "Pretendard-Regular.ttf"
GEORGIA = Path("/System/Library/Fonts/Supplemental/Georgia.ttf")


def font(path, size):
    return ImageFont.truetype(str(path), size * SCALE)


def xy(v):
    return tuple(int(x * SCALE) for x in v)


def box(v):
    return tuple(int(x * SCALE) for x in v)


def text(draw, pos, value, fnt, fill=INK, anchor=None, spacing=0):
    draw.text(xy(pos), value, font=fnt, fill=fill, anchor=anchor, spacing=spacing * SCALE)


def centered_text(draw, y, value, fnt, fill=INK, spacing=0, x=640):
    text(draw, (x, y), value, fnt, fill=fill, anchor="ma", spacing=spacing)


def draw_grid(draw):
    step = 38 * SCALE
    for x in range(0, W + step, step):
        draw.line([(x, 0), (x, H)], fill=GRID, width=1 * SCALE)
    for y in range(0, H + step, step):
        draw.line([(0, y), (W, y)], fill=GRID, width=1 * SCALE)


def draw_qr_block(draw):
    x, y, s = 48, 68, 84
    draw.rectangle(box((x, y, x + s, y + s)), fill=PAPER)
    cells = [
        (0, 0, 2, 2), (6, 0, 8, 2), (0, 6, 2, 8),
        (3, 1, 4, 2), (5, 2, 6, 3), (2, 3, 3, 4),
        (4, 3, 5, 4), (6, 3, 7, 4), (3, 4, 4, 5),
        (5, 5, 6, 6), (2, 6, 3, 7), (4, 6, 5, 7),
        (3, 7, 4, 8), (6, 6, 7, 7),
    ]
    c = s / 8
    for a, b, c2, d in cells:
        draw.rectangle(box((x + a * c, y + b * c, x + c2 * c, y + d * c)), fill=INK)


def draw_pixel_glitch(draw):
    # Same right-side motif as the index hero: eight striped blocks in a stepped column.
    x0, y0 = 1008, 162
    scale = 1.08
    blocks = [
        (0, 0, 200, 40),
        (20, 45, 200, 85),
        (40, 90, 200, 130),
        (60, 135, 200, 175),
        (40, 180, 200, 220),
        (20, 225, 200, 265),
        (0, 270, 200, 310),
        (30, 315, 200, 355),
    ]
    stripe_w = 1.2 * scale
    gap_w = 2.4 * scale
    for bx1, by1, bx2, by2 in blocks:
        left = x0 + bx1 * scale
        top = y0 + by1 * scale
        right = x0 + bx2 * scale
        bottom = y0 + by2 * scale
        cur = left
        while cur < right:
            draw.rectangle(
                box((cur, top, min(cur + stripe_w, right), bottom)),
                fill=INK_55,
            )
            cur += gap_w


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img, "RGBA")
    draw_grid(draw)
    draw_qr_block(draw)
    draw_pixel_glitch(draw)

    centered_text(
        draw,
        96,
        "BUSINESS LEADER BRIEFING · 2026.6.29 발표 · 7월 4일 기준 업데이트",
        font(PRETENDARD_MEDIUM, 18),
        fill=INK,
    )
    centered_text(draw, 184, "대한민국 대도약", font(PRETENDARD_MEDIUM, 58), fill=INK)
    centered_text(draw, 254, "3대 메가프로젝트", font(PRETENDARD_MEDIUM, 58), fill=INK)

    # Georgia has no Hangul glyphs on some systems, so use Pretendard for the Korean unit.
    text(draw, (640, 384), "4,755", font(GEORGIA, 128), fill=INK, anchor="mm")
    text(draw, (856, 397), "조원", font(PRETENDARD_BOLD, 40), fill=INK, anchor="lm")

    centered_text(draw, 466, "삼성·SK 국내 투자 발표 계획 합산", font(PRETENDARD_MEDIUM, 25), fill=INK_80, x=704)
    centered_text(
        draw,
        540,
        "'26년 정부 예산(약 728조원)의 6.5배.\n그러나 성패를 가를 변수는 투자 규모가 아니라 실행의 완결성입니다.",
        font(PRETENDARD_REGULAR, 25),
        fill=INK_80,
        spacing=9,
    )
    centered_text(
        draw,
        636,
        "반도체 · 피지컬 AI · AI 데이터센터 | 관계부처 합동 발표 원문 기반 팩트 브리핑",
        font(PRETENDARD_MEDIUM, 18),
        fill=INK_80,
    )
    centered_text(draw, 668, "Researched & Scored with Claude Fable 5", font(PRETENDARD_REGULAR, 15), fill=(31, 43, 224, 115))

    img = img.resize((1280, 720), Image.Resampling.LANCZOS)
    img.save(OUT, quality=95)
    print(OUT)


if __name__ == "__main__":
    main()
