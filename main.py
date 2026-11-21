#!/usr/bin/env python3
"""news-image-20261120: front page of Friday 20 November 2026 in one image.

Pure Python 3 standard library only (struct, zlib, os). No network, no
files read, no randomness: two runs write byte-identical PNGs.

The program draws a newspaper front page -- masthead, lead story with a
drawn Kyiv skyline and bridge, then 37 more numbered stories in 7 region
sections (40 stories total) -- with a hand-written 5x7 bitmap font, and
encodes the pixels as a PNG by hand.
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- font: 5x7
# Each glyph is 7 rows of 5 pixels, '#' = on. All copy is set in capitals.
FONT = {
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": [".###.", "..#..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "##..#", "#.#.#", "#..##", "#..##", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", "#...#", ".#.#.", "..#..", ".#.#.", "#...#", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#..##", "#.#.#", "##..#", "#...#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", ".###."],
    "2": [".###.", "#...#", "....#", "...#.", "..#..", ".#...", "#####"],
    "3": ["####.", "....#", "....#", ".###.", "....#", "....#", "####."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", "..#..", "..#..", "..#.."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    ";": [".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."],
    "'": ["..#..", "..#..", ".....", ".....", ".....", ".....", "....."],
    "-": [".....", ".....", ".....", ".###.", ".....", ".....", "....."],
    "+": [".....", "..#..", "..#..", ".###.", "..#..", "..#..", "....."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "%": ["##..#", "##.#.", "...#.", "..#..", ".#...", "#.##.", "#..##"],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "&": [".##..", "#..#.", "#..#.", ".#...", "#.#.#", "#..#.", ".##.#"],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "...#.", "..#..", ".....", "..#.."],
    '"': [".#.#.", ".#.#.", ".....", ".....", ".....", ".....", "....."],
    "=": [".....", ".....", ".###.", ".....", ".###.", ".....", "....."],
    "*": [".....", ".#.#.", ".###.", "#####", ".###.", ".#.#.", "....."],
    "#": [".#.#.", ".#.#.", "#####", ".#.#.", "#####", ".#.#.", ".#.#."],
    "@": [".###.", "#...#", "#.###", "#.#.#", "#.###", "#....", ".###."],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
    "[": [".###.", ".#...", ".#...", ".#...", ".#...", ".#...", ".###."],
    "]": [".###.", "...#.", "...#.", "...#.", "...#.", "...#.", ".###."],
    "<": ["...#.", "..#..", ".#...", "#....", ".#...", "..#..", "...#."],
    ">": [".#...", "..#..", "...#.", "....#", "...#.", "..#..", ".#..."],
    "^": ["..#..", ".#.#.", ".....", ".....", ".....", ".....", "....."],
    "~": [".....", ".....", ".##.#", "#.#..", ".....", ".....", "....."],
    "\\": ["#....", "#....", ".#...", "..#..", "...#.", "....#", "....#"],
    "|": ["..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
}

# ------------------------------------------------------------- canvas
PAPER = (247, 242, 231)
INK = (20, 20, 20)
RED = (176, 30, 36)
NAVY = (27, 58, 92)
GOLD = (176, 132, 24)
TEAL = (14, 94, 88)
GREEN = (34, 110, 52)
PURPLE = (88, 52, 120)
BROWN = (122, 72, 28)
SLATE = (70, 76, 84)
WHITE = (255, 255, 255)
NIGHT = (16, 24, 46)
RIVER = (52, 96, 140)
FIRE = (232, 122, 26)
EMBER = (248, 196, 66)


class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def set(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i], self.px[i + 1], self.px[i + 2] = c

    def rect(self, x, y, w, h, c):
        for yy in range(max(0, y), min(self.h, y + h)):
            base = (yy * self.w + max(0, x)) * 3
            for xx in range(max(0, x), min(self.w, x + w)):
                self.px[base], self.px[base + 1], self.px[base + 2] = c
                base += 3

    def hline(self, x0, x1, y, c, t=1):
        for t_ in range(t):
            for x in range(x0, x1 + 1):
                self.set(x, y + t_, c)

    def vline(self, x, y0, y1, c, t=1):
        for t_ in range(t):
            for y in range(y0, y1 + 1):
                self.set(x + t_, y, c)

    def line(self, x0, y0, x1, y1, c):
        dx, dy = abs(x1 - x0), -abs(y1 - y0)
        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1
        err = dx + dy
        while True:
            self.set(x0, y0, c)
            if x0 == x1 and y0 == y1:
                break
            e2 = 2 * err
            if e2 >= dy:
                err += dy
                x0 += sx
            if e2 <= dx:
                err += dx
                y0 += sy

    def circle(self, cx, cy, r, c, fill=True):
        for y in range(cy - r, cy + r + 1):
            for x in range(cx - r, cx + r + 1):
                d2 = (x - cx) ** 2 + (y - cy) ** 2
                if fill:
                    if d2 <= r * r:
                        self.set(x, y, c)
                elif r * r - 2 * r <= d2 <= r * r:
                    self.set(x, y, c)

    def ring(self, cx, cy, r, c):
        self.circle(cx, cy, r, c, fill=False)

    def text(self, x, y, s, scale, c):
        for ch in s:
            g = FONT.get(ch, FONT["?"])
            for r in range(7):
                row = g[r]
                for col in range(5):
                    if row[col] == "#":
                        self.rect(x + col * scale, y + r * scale,
                                  scale, scale, c)
            x += 6 * scale

    def text_w(self, s, scale):
        return len(s) * 6 * scale - scale

    def text_c(self, cx, y, s, scale, c):
        self.text(cx - self.text_w(s, scale) // 2, y, s, scale, c)

    def wrap(self, s, scale, max_w):
        """Split s into lines of at most max_w pixels (word wrap)."""
        words, lines, cur = s.split(" "), [], ""
        for wd in words:
            trial = (cur + " " + wd).strip()
            if self.text_w(trial, scale) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines


def png_bytes(cv):
    raw = bytearray()
    stride = cv.w * 3
    for y in range(cv.h):
        raw.append(0)
        raw += cv.px[y * stride:(y + 1) * stride]
    data = zlib.compress(bytes(raw), 9)

    def chunk(tag, payload):
        out = struct.pack(">I", len(payload)) + tag + payload
        return out + struct.pack(">I", zlib.crc32(tag + payload) & 0xFFFFFFFF)

    ihdr = struct.pack(">IIBBBBB", cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", data) + chunk(b"IEND", b""))

# ------------------------------------------------------------- the news
# 40 stories, all events that happened or were first reported on
# Friday 20 November 2026, grouped in 7 regions. Headlines are kept
# short so each fits one line at body size; figures are as reported.
LEAD_KICKER = "LEAD STORY - UKRAINE"
LEAD_HEAD = ["KYIV BRIDGES HIT IN", "RUSSIA'S BIGGEST BARRAGE"]
LEAD_LINES = [
    "400+ DRONES, 110 MISSILES OVERNIGHT",
    "3 DNIPRO BRIDGES STRUCK - 8 KILLED, 30 HURT",
    "2 MISSILES LAND IN POLAND - NO CASUALTIES",
    "UKRAINE RETAKES 14 VILLAGES, HITS KERCH BRIDGE",
]

# (section title, colour, [(number, headline), ...]) -- stories 4..40.
SECTIONS_LEFT = [
    ("EUROPE", NAVY, [
        (4, "MERZ: NO NEW YALTA FOR EUROPE"),
        (5, "EU-UK SUMMIT: RESET DEEPENS"),
        (6, "DENMARK OKS GREENLAND-US ARCTIC DEAL"),
        (7, "DUTCH EMBASSY IN KYIV DAMAGED"),
        (8, "SPAIN DEBATE: SANCHEZ ADMITS ERRORS"),
    ]),
    ("ASIA - PACIFIC", TEAL, [
        (9, "CYCLONE AKVAN LANDFALL NEAR GOPALPUR"),
        (10, "TRUMP, XI, PUTIN: PEACE DECLARATION"),
        (11, "ICJ: MYANMAR GUILTY OF GENOCIDE"),
        (12, "RUSSIAN BOMBERS ENTER TAIWAN ZONE"),
        (13, "TAIWAN FLAGS 2,700 ACCOUNTS"),
        (14, "JAPAN AND INDIA DEEPEN DEFENCE TIES"),
        (15, "CHINA HOLDS RATES FOR 18TH MONTH"),
        (16, "PAKISTAN MINISTER VISITS DELHI"),
    ]),
    ("MIDDLE EAST", BROWN, [
        (17, "COP31 DRAFT DROPS FOSSIL FUELS"),
        (18, "HORMUZ TANKERS HIT AS BLOCKADE BITES"),
        (19, "IEA: HORMUZ SHOCK LARGEST ON RECORD"),
        (20, "IRAQ DEAL WITH KATAIB HEZBOLLAH"),
        (21, "GAZA: 22,000+ CHILDREN KILLED"),
        (22, "US WAR VS IRAN COST $48.3BN"),
    ]),
]
SECTIONS_RIGHT = [
    ("AFRICA", GREEN, [
        (23, "SOMALIA EXPELS UAE AMBASSADOR"),
        (24, "SUDAN WAR: DISPLACEMENT GROWS"),
        (25, "AFRICA PRESSES FOR CLIMATE FINANCE"),
        (26, "MOROCCO, SENEGAL SEAL AFCON SPOTS"),
    ]),
    ("THE AMERICAS", PURPLE, [
        (27, "ANTHROPIC IPO: $81BN, LARGEST EVER"),
        (28, "CALIFORNIA SUBPOENAS NVIDIA"),
        (29, "MICROSOFT 365 OUTAGE TOPS 9 HOURS"),
        (30, "US CYBER CHIEF QUITS AFTER OUTAGES"),
        (31, "HAITI POLICE KILL 34 GANG SUSPECTS"),
        (32, "LULA ADVANCES INDIGENOUS LAND RIGHTS"),
        (33, "BUKELE MOVES TOWARD THIRD TERM"),
        (34, "US-CHINA PACT ON HUMAN CONTROL OF AI"),
    ]),
    ("OCEANIA + THE WORLD", SLATE, [
        (35, "CYCLONE XAVIER, CAT 4, IN PACIFIC"),
        (36, "VOYAGER 1: SIGNALS NOW TAKE A DAY"),
        (37, "GTA VI LAUNCH: $2BN+ IN EARLY SALES"),
        (38, "FIONA THE HIPPO DIES IN CINCINNATI"),
        (39, "ALCARAZ BEATS MEDVEDEV IN TURIN"),
        (40, "US SENATE PASSES ENERGY BILL 62-33"),
    ]),
]

NUMBERS = [
    ("400+", "DRONES IN RUSSIA'S", "KYIV BARRAGE"),
    ("90", "KM/H GUSTS AS CYCLONE", "AKVAN MADE LANDFALL"),
    ("$81BN", "ANTHROPIC IPO, THE", "LARGEST EVER"),
    ("34", "SUSPECTED GANG MEMBERS", "KILLED IN HAITI OP"),
]


def draw_burst(cv, cx, cy, r, c1, c2):
    cv.circle(cx, cy, r, c1)
    cv.circle(cx, cy, max(1, r // 2), c2)
    for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1),
                   (1, 1), (-1, -1), (1, -1), (-1, 1)]:
        cv.line(cx, cy, cx + dx * (r + 8), cy + dy * (r + 8), c1)


def draw_lead_graphic(cv, x, y, w, h):
    """Night over Kyiv: skyline, the Dnipro, a bridge, missile bursts."""
    cv.rect(x, y, w, h, NIGHT)
    # stars: fixed positions, no randomness
    for sx, sy in [(18, 12), (52, 26), (96, 10), (140, 30), (190, 14),
                   (240, 24), (290, 10), (330, 28), (30, 44), (210, 44)]:
        cv.set(x + sx, y + sy, WHITE)
    # distant skyline silhouettes
    for bx, bw, bh in [(0, 34, 52), (36, 26, 70), (64, 40, 46), (106, 24, 64),
                       (132, 30, 40), (164, 36, 74), (202, 28, 52),
                       (232, 34, 66), (268, 26, 44), (296, 40, 58)]:
        cv.rect(x + bx, y + h - 58 - bh, bw, bh, (10, 16, 34))
    # lit windows
    for wx, wy in [(10, 96), (46, 80), (76, 104), (116, 88), (142, 110),
                   (176, 78), (214, 100), (244, 84), (278, 106), (306, 92)]:
        cv.rect(x + wx, y + wy, 4, 5, EMBER)
    # river
    cv.rect(x, y + h - 58, w, 58, RIVER)
    for rx in range(8, w - 8, 26):
        cv.hline(x + rx, x + rx + 14, y + h - 40, (120, 170, 210), 2)
        cv.hline(x + rx + 6, x + rx + 18, y + h - 24, (120, 170, 210), 2)
    # bridge deck and three arches over the river
    deck = y + h - 62
    cv.rect(x + 8, deck, w - 16, 5, (220, 220, 220))
    for ax in (52, 152, 252):
        for t in range(0, 47, 2):
            yy = deck - int(22 * (1 - ((t - 23) / 23.0) ** 2))
            cv.set(x + ax + t, yy, WHITE)
            cv.set(x + ax + t, yy + 1, WHITE)
            cv.set(x + ax + t, yy + 2, WHITE)
        cv.vline(x + ax + 23, deck - 22, deck, WHITE, 2)
        cv.vline(x + ax, deck - 10, deck, WHITE, 2)
        cv.vline(x + ax + 46, deck - 10, deck, WHITE, 2)
    # missile arcs and bursts above the bridge
    cv.line(x + 40, y + 8, x + 120, y + 62, FIRE)
    cv.line(x + 300, y + 6, x + 230, y + 58, FIRE)
    draw_burst(cv, x + 122, y + 64, 12, FIRE, EMBER)
    draw_burst(cv, x + 228, y + 60, 10, FIRE, EMBER)
    draw_burst(cv, x + 176, y + 34, 7, EMBER, WHITE)
    cv.text(x + 8, y + h - 16, "KYIV, UKRAINE - THE DNIPRO AT NIGHT",
            1, (200, 220, 240))


def draw_section(cv, x, y, w, title, colour, stories):
    cv.rect(x, y, w, 26, colour)
    cv.text(x + 10, y + 6, title, 2, WHITE)
    cv.text(x + w - 10 - cv.text_w("%d STORIES" % len(stories), 1),
            y + 9, "%d STORIES" % len(stories), 1, (220, 220, 220))
    y += 34
    for num, head in stories:
        lines = cv.wrap(head, 2, w - 44)
        cv.text(x + 2, y, "%02d" % num, 2, RED)
        for i, ln in enumerate(lines):
            cv.text(x + 44, y + i * 16, ln, 2, INK)
        y += len(lines) * 16 + 6
    return y


def build():
    cv = Canvas(W, H, PAPER)
    # outer frame
    cv.rect(0, 0, W, 6, INK)
    cv.rect(0, H - 6, W, 6, INK)
    cv.rect(0, 0, 6, H, INK)
    cv.rect(W - 6, 0, 6, H, INK)

    # masthead
    cv.text_c(W // 2, 18, "THE WORLD IN ONE DAY", 5, INK)
    cv.hline(24, W - 24, 62, RED, 3)
    cv.text(24, 72, "FRIDAY 20 NOVEMBER 2026", 2, RED)
    cv.text(W - 24 - cv.text_w("40 STORIES - 7 REGIONS", 2), 72,
            "40 STORIES - 7 REGIONS", 2, INK)
    cv.hline(24, W - 24, 96, INK, 2)

    # lead band
    cv.text(24, 110, LEAD_KICKER, 2, RED)
    yy = 132
    for ln in LEAD_HEAD:
        cv.text(24, yy, ln, 3, INK)
        yy += 24
    yy += 6
    for ln in LEAD_LINES:
        cv.text(24, yy, ln, 2, INK)
        yy += 20
    draw_lead_graphic(cv, 656, 108, 344, 148)
    cv.hline(24, W - 24, 268, INK, 2)

    # body: two columns of region sections
    left_y = 282
    for title, colour, stories in SECTIONS_LEFT:
        left_y = draw_section(cv, 24, left_y, 480, title, colour, stories)
        left_y += 10
    right_y = 282
    for title, colour, stories in SECTIONS_RIGHT:
        right_y = draw_section(cv, 520, right_y, 480, title, colour, stories)
        right_y += 10

    # the day in numbers
    band_y = max(left_y, right_y) + 6
    cv.text(24, band_y, "THE DAY IN NUMBERS", 2, RED)
    band_y += 24
    box_w, gap = 236, 8
    for i, (num, l1, l2) in enumerate(NUMBERS):
        bx = 24 + i * (box_w + gap)
        cv.rect(bx, band_y, box_w, 76, WHITE)
        cv.rect(bx, band_y, box_w, 3, RED)
        cv.rect(bx, band_y + 73, box_w, 3, INK)
        cv.text_c(bx + box_w // 2, band_y + 10, num, 3, RED)
        cv.text_c(bx + box_w // 2, band_y + 40, l1, 1, INK)
        cv.text_c(bx + box_w // 2, band_y + 52, l2, 1, INK)

    # footer
    cv.hline(24, W - 24, 972, INK, 2)
    cv.text_c(W // 2, 984,
              "ALL EVENTS HAPPENED OR WERE FIRST REPORTED ON 20 NOVEMBER 2026",
              2, INK)
    cv.text_c(W // 2, 1006,
              "SOURCES: REUTERS, AP, IMD, ICJ, CALIFORNIA DOJ, NASA - DRAWN BY CODE, NO PHOTOS",
              1, SLATE)
    return cv


def main():
    out = os.path.join(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"),
                       "entry.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    data = png_bytes(build())
    with open(out, "wb") as f:
        f.write(data)
    print("wrote %s (%d bytes)" % (out, len(data)))


if __name__ == "__main__":
    main()
