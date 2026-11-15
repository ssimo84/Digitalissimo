#!/usr/bin/env python3
"""Genera la piantina in scala 1:50 (foglio A3 orizzontale) dalle quote dello schizzo.

Sistema di coordinate del disegno (metri, orientamento "raddrizzato"):
  X' verso destra, Y' verso il basso. Y'=0 = parete d'ingresso (in alto).
Lo schizzo originale e' ruotato di 180 gradi rispetto a questo disegno.
"""
import math

S = 20.0            # mm di carta per metro reale  -> scala 1:50
OX, OY = 46.0, 56.0 # origine del disegno sul foglio (mm)
T = 0.30            # spessore muri ipotizzato (m)

BLUE, ORANGE, WALL, GREY = "#1f4e8c", "#d2691e", "#3b3b3b", "#666666"

out = []
add = out.append
X = lambda x: OX + S * x
Y = lambda y: OY + S * y
f = lambda v: f"{v:.2f}"


def line(x1, y1, x2, y2, stroke="#000", w=0.25, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<line x1="{f(X(x1))}" y1="{f(Y(y1))}" x2="{f(X(x2))}" y2="{f(Y(y2))}" '
        f'stroke="{stroke}" stroke-width="{w}"{d}/>')


def rect(x1, y1, x2, y2, fill="none", stroke="none", w=0.25, dash=None):
    d = f' stroke-dasharray="{dash}"' if dash else ""
    add(f'<rect x="{f(X(x1))}" y="{f(Y(y1))}" width="{f(S*(x2-x1))}" height="{f(S*(y2-y1))}" '
        f'fill="{fill}" stroke="{stroke}" stroke-width="{w}"{d}/>')


def text(x, y, s, size=2.6, fill="#000", anchor="middle", rot=0, weight="normal", style="normal"):
    px, py = X(x), Y(y)
    tr = f' transform="rotate({rot} {f(px)} {f(py)})"' if rot else ""
    add(f'<text x="{f(px)}" y="{f(py)}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
        f'font-weight="{weight}" font-style="{style}"{tr}>{s}</text>')


def ptext(px, py, s, size=3.2, fill="#000", anchor="start", weight="normal"):
    add(f'<text x="{f(px)}" y="{f(py)}" font-size="{size}" fill="{fill}" text-anchor="{anchor}" '
        f'font-weight="{weight}">{s}</text>')


def colour(kind):
    return ORANGE if kind == "e" else BLUE


def tick(x, y, col):
    d = 0.09
    line(x - d, y + d, x + d, y - d, col, 0.4)


def dim_h(x1, x2, yl, label, yobj=None, kind="m", txt_x=None, anchor="middle"):
    col = colour(kind)
    if yobj is not None:
        sgn = 1 if yl > yobj else -1
        for xx in (x1, x2):
            line(xx, yobj + sgn * 0.06, xx, yl + sgn * 0.12, col, 0.18)
    line(x1, yl, x2, yl, col, 0.25)
    tick(x1, yl, col)
    tick(x2, yl, col)
    text((x1 + x2) / 2 if txt_x is None else txt_x, yl - 0.10, label, 2.6, col, anchor=anchor)


def dim_v(y1, y2, xl, label, xobj=None, kind="m"):
    col = colour(kind)
    if xobj is not None:
        sgn = 1 if xl > xobj else -1
        for yy in (y1, y2):
            line(xobj + sgn * 0.06, yy, xl + sgn * 0.12, yy, col, 0.18)
    line(xl, y1, xl, y2, col, 0.25)
    tick(xl, y1, col)
    tick(xl, y2, col)
    text(xl - 0.10, (y1 + y2) / 2, label, 2.6, col, rot=-90)


# ------------------------------------------------------------------ geometria
W = 7.73
poly = [
    (0.00, 0.00), (0.49, 0.00), (0.49, -0.70), (2.65, -0.70), (2.65, 0.00),   # fronte: il muro nero e il vetro sono fuori,
    (3.99, 0.00), (3.99, -0.70), (7.07, -0.70), (7.07, 0.00), (7.73, 0.00),   # le basi stanno dentro (0,70)
    (7.73, 7.33),                          # parete lato destro fino in fondo alla nicchia
    (6.22, 7.33), (6.22, 6.13),            # nicchia in basso a destra (larghezza 1,51 stimata)
    (2.53, 6.13),                          # parete lato bagno (2,59 + porta bagno + muretto)
    (2.53, 7.62), (0.80, 7.57),            # rientranza: 1,49 / 1,73 / 1,49, fondo quasi dritto
    (0.80, 6.08), (0.00, 6.08),            # gradino 0,80 dalla parete sinistra, parte dritta
    (0.00, 4.85), (0.52, 4.85),            # pilastro a muro: spessore 0,52 x lunghezza 0,51
    (0.52, 4.34), (0.00, 4.34),
]
pts = " ".join(f"{f(X(x))},{f(Y(y))}" for x, y in poly)

# area (formula di Gauss)
area = 0.5 * abs(sum(poly[i][0] * poly[(i + 1) % len(poly)][1] - poly[(i + 1) % len(poly)][0] * poly[i][1]
                     for i in range(len(poly))))
perim = sum(math.dist(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))
pillar_area = 0.32 * 1.04
bases_area = 0.70 * (2.16 + 3.08)
net = area - pillar_area - bases_area
print(f"area lorda {area:.2f} m2, netta pilastro {net:.2f} m2, perimetro {perim:.2f} m")

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="420mm" height="297mm" viewBox="0 0 420 297" '
    f'font-family="Arial, Helvetica, sans-serif">')
add('<defs><pattern id="hatch" width="1.6" height="1.6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)">'
    '<line x1="0" y1="0" x2="0" y2="1.6" stroke="#777" stroke-width="0.25"/></pattern></defs>')
add('<rect width="420" height="297" fill="#ffffff"/>')
add('<rect x="6" y="6" width="408" height="285" fill="none" stroke="#000" stroke-width="0.5"/>')

# ---- muri: spessore verso l'esterno (trucco: tratto spesso + riempimento bianco sopra)
add(f'<polygon points="{pts}" fill="none" stroke="{WALL}" stroke-width="{f(2*T*S)}" '
    f'stroke-linejoin="miter" stroke-miterlimit="10"/>')
add(f'<polygon points="{pts}" fill="#fbfbf8" stroke="none"/>')

# colonna lato sinistro (tratteggiata nello schizzo)
rect(-T, 4.34, 0.52, 4.85, fill=WALL)

# bordo interno netto
add(f'<polygon points="{pts}" fill="none" stroke="#000" stroke-width="0.45" stroke-linejoin="miter"/>')


def opening(x1, y1, x2, y2, jambs):
    rect(x1, y1, x2, y2, fill="#fbfbf8")
    for (a, b, c, d) in jambs:
        line(a, b, c, d, "#000", 0.35)


# ---- aperture
# vetrine: il muro nero resta sul bordo esterno (Y' -1,00 -> -0,70) e il vetro sta li'
for (a, b) in [(0.49, 2.65), (3.99, 7.07)]:
    opening(a, -1.0 - 0.01, b, -0.70 + 0.01, [(a, -1.0, a, -0.70), (b, -1.0, b, -0.70)])
    for yy in (-1.0, -0.85, -0.70):
        line(a, yy, b, yy, "#000", 0.25)
# rientranza della porta (aperta verso la strada): tolgo i pilastri neri laterali, restano vetrate
rect(2.65, -0.70, 2.96, 0.0, fill="#fbfbf8")
rect(3.68, -0.70, 3.99, 0.0, fill="#fbfbf8")
# porta d'ingresso: apertura nello spessore del muro sulla linea Y' 0
opening(2.65, -T - 0.01, 3.99, 0.0, [(2.65, -T, 2.65, 0), (3.99, -T, 3.99, 0)])
rect(2.65, -0.70, 3.99, 0.0, fill="#eaeef2")
# vetrate: una a sinistra della porta e una tra porta e spazio portaombrelli
for xg in (2.65, 3.60):
    rect(xg - 0.03, -0.70, xg + 0.03, 0.0, fill="#bfdcf2", stroke="#000", w=0.3)
# porta d'ingresso 0,95 sulla linea Y' 0
line(2.65, 0.0, 3.60, 0.0, "#000", 0.6)
rect(2.65, -0.03, 2.69, 0.03, fill="#000")
rect(3.56, -0.03, 3.60, 0.03, fill="#000")
# spazio portaombrelli X' 3,60 -> 3,99 (0,39 ricavata): chiuso verso la strada dal muro nero esterno
rect(3.60, -1.0, 3.99, -0.70, fill=WALL)
# porta lato destro: Y' 1,93 -> 2,73 (0,80 stimata), cerniera lato ingresso, apre verso l'interno
opening(W, 1.93, W + T + 0.01, 2.73, [(W, 1.93, W + T, 1.93), (W, 2.73, W + T, 2.73)])
line(W, 1.93, W - 0.80, 1.93, "#000", 0.5)
add(f'<path d="M {f(X(W-0.80))} {f(Y(1.93))} A {f(S*0.8)} {f(S*0.8)} 0 0 0 {f(X(W))} {f(Y(2.73))}" '
    f'fill="none" stroke="#000" stroke-width="0.2" stroke-dasharray="1 0.8"/>')
# porta bagno: X' 5,37 -> 6,17 (stima)
opening(5.12, 6.13 - 0.01, 5.92, 6.13 + T + 0.01, [(5.12, 6.13, 5.12, 6.13 + T), (5.92, 6.13, 5.92, 6.13 + T)])
# porta della nicchia: X' 6,73 -> 7,63 (stima)
opening(6.73, 7.33 - 0.01, 7.63, 7.33 + T + 0.01, [(6.73, 7.33, 6.73, 7.33 + T), (7.63, 7.33, 7.63, 7.33 + T)])
rect(6.73, 7.33 - 0.01, 7.63, 7.33 + T + 0.01, fill="none")

# ---- basi marroni DENTRO la vetrina: lunghe quanto la vetrina, profonde 0,70
for (a, b) in [(0.49, 2.65), (3.99, 7.07)]:
    rect(a, -0.70, b, 0.0, fill="#ece6d8", stroke="#000", w=0.3)
    line(a, -0.70, b, 0.0, "#bbb39f", 0.15)
    line(a, 0.0, b, -0.70, "#bbb39f", 0.15)

# ---- pilastro centrale 0,32 x 1,04 (X' 4,33-4,65 ; Y' 4,03-5,07)
rect(4.33, 4.03, 4.65, 5.07, fill="#d4d4d4", stroke="#000", w=0.4)
line(4.33, 4.03, 4.65, 5.07, "#555", 0.2)
line(4.65, 4.03, 4.33, 5.07, "#555", 0.2)

# ---- termosifone lato sinistro: lungo 1,35 (Y' 2,99 -> 4,34), profondita' stimata 0,10
rect(0.0, 2.99, 0.10, 4.34, fill="#fff", stroke=ORANGE, w=0.35)
for i in range(1, 15):
    yy = 2.99 + i * 1.35 / 15
    line(0.0, yy, 0.10, yy, ORANGE, 0.2)
# termosifone lato destro (stima di posizione)
rect(W - 0.12, 4.93, W, 6.13, fill="#fff", stroke=ORANGE, w=0.35, dash="1.2 0.8")
text(W - 0.20, 5.53, "termosifone*", 2.2, ORANGE, anchor="middle", rot=-90)
# termostato (stima)
add(f'<circle cx="{f(X(W-0.14))}" cy="{f(Y(6.30))}" r="1.1" fill="#fff" stroke="{ORANGE}" stroke-width="0.35"/>')
ptext(X(W - 0.14), Y(6.30) + 0.8, "T", 1.9, ORANGE, "middle", "bold")
text(W - 0.45, 6.38, "termostato*", 2.0, ORANGE, anchor="end")

# ---- etichette ambienti/aperture
text(1.57, -0.30, "base vetrina 2,16 × 0,70", 2.4, "#000", style="italic")
text(5.53, -0.30, "base vetrina 3,08 × 0,70", 2.4, "#000", style="italic")
text(3.125, 0.45, "porta ingresso 0,95", 2.4, GREY, style="italic")
text(3.125, -0.30, "rientranza 0,70", 2.0, GREY, style="italic")
text(3.80, -0.35, "portaombrelli", 1.9, "#000", rot=-90, style="italic")
text(3.20, 5.50, "colonna centrale 1,04 × 0,32", 2.4, GREY, style="italic")
text(0.36, 3.70, "termosifone 1,35", 2.2, GREY, anchor="start", style="italic")
text(0.62, 4.83, "pilastro 0,52 × 0,51", 2.0, GREY, anchor="start", style="italic")
text(5.52, 7.42, "porta bagno", 2.4, GREY, style="italic")
text(7.18, 7.92, "uscita retro", 2.6, "#000", weight="bold")
text(2.6, 2.3, "AMBIENTE PRINCIPALE", 4.2, "#999", weight="bold")
text(2.6, 2.6, f"{net:.1f} m² netti", 3.0, "#999")

# ---------------------------------------------------------------- QUOTE
# fronte ingresso (in alto)
yl = -1.50
for (a, b, lab, k) in [(0, 0.49, "0,49", "m"), (0.49, 2.65, "2,16", "m"), (2.65, 3.60, "0,95", "m"), (3.60, 3.99, "0,39°", "m"),
                       (3.99, 7.07, "3,08", "m"), (7.07, 7.73, "0,66", "m")]:
    dim_h(a, b, yl, lab, yobj=-1.05, kind=k)
dim_h(0, 7.73, -2.05, "7,73", yobj=-1.05)

# lato destro (verso l'esterno)
xl = 8.55
for (a, b, lab, k) in [(0, 1.93, "1,93", "m"), (1.93, 2.73, "0,80*", "e"), (2.73, 4.93, "2,20", "m"),
                       (4.93, 6.13, "1,20°", "m")]:
    dim_v(a, b, xl, lab, xobj=W + T + 0.05, kind=k)

# lato sinistro
xl = -0.85
for (a, b, lab) in [(0, 2.99, "2,99"), (2.99, 4.34, "1,35"), (4.34, 4.85, "0,51"), (4.85, 6.08, "1,23")]:
    dim_v(a, b, xl, lab, xobj=-T - 0.05)
dim_v(0, 6.08, -1.45, "6,08°", xobj=-T - 0.05)

# interno: pilastro e distanze
dim_h(4.65, W, 4.20, "3,08")
dim_h(0.52, 4.33, 4.60, "4,02")
dim_v(0.0, 4.03, 4.49, "4,03")
dim_v(5.07, 6.13, 4.49, "1,06")
# colonna lato sinistro: sporgenza 0,25
# 0,80 e 2,59 lungo il muro in alto
dim_h(0.0, 0.80, 5.72, "0,80", yobj=6.08)
dim_h(2.53, 5.12, 5.85, "2,59", yobj=6.13, txt_x=3.30)

# rientranza (1,49 / 1,49 / 1,73)
dim_v(6.08, 7.57, 1.17, "1,49", xobj=0.80)
dim_v(6.13, 7.62, 2.17, "1,49", xobj=2.53)
dim_h(0.80, 2.53, 8.55, "1,73", yobj=7.95)

# porta bagno e nicchia (stima)
dim_h(5.12, 5.92, 6.95, "0,80", yobj=6.5)

# ---------------------------------------------------------------- cartiglio
ptext(12, 256, "PIANTINA – RILIEVO RICOSTRUITO DA SCHIZZO A MANO", 6.0, "#000", weight="bold")
ptext(12, 264, "Quote in metri · scala 1:50 su foglio A3 · schizzo ruotato di 180° (così le scritte si leggono dritte)", 3.2, "#333")
ptext(12, 271, "Ingresso in alto: porta tra due vetrine (basi dentro, muro nero e vetro fuori) · bagno oltre la parete in basso", 3.2, "#333")

# ---------------------------------------------------------------- pannello note
px = 262
ptext(px, 22, "LEGENDA", 4.2, "#000", weight="bold")
add(f'<line x1="{px}" y1="26.5" x2="{px+10}" y2="26.5" stroke="{BLUE}" stroke-width="0.6"/>')
ptext(px + 13, 27.8, "misura presa dallo schizzo", 3.2)
ptext(px + 1, 33.8, "1,34°", 3.2, BLUE, weight="bold")
ptext(px + 13, 33.8, "ricavata per differenza (calcolata)", 3.2)
ptext(px + 1, 40.0, "0,10*", 3.2, ORANGE, weight="bold")
ptext(px + 13, 40.0, "stimata: nello schizzo non c'era la quota", 3.2)
add(f'<rect x="{px}" y="43.2" width="10" height="4" fill="#3b3b3b" stroke="#000" stroke-width="0.3"/>')
ptext(px + 13, 46.5, "pilastro a muro: 0,52 × 0,51", 3.2)

ptext(px, 60, "DATI", 4.2, "#000", weight="bold")
ptext(px, 66.5, f"Superficie interna lorda: {area:.2f} m²".replace(".", ","), 3.2)
ptext(px, 72, f"Superficie netta (meno colonna e basi vetrina): {net:.2f} m²".replace(".", ","), 3.2)
ptext(px, 77.5, f"Perimetro interno: {perim:.2f} m".replace(".", ","), 3.2)
ptext(px, 83, "Spessore muri 0,30 m: ipotizzato, non misurato", 3.2, ORANGE)

ptext(px, 97, "DA VERIFICARE IN LOCO", 4.2, "#000", weight="bold")
notes = [
    "1. Rientranza d'ingresso 1,34° (per differenza: 7,73 −",
    "    0,49 − 2,16 − 3,08 − 0,66): porta 0,95 + spazio",
    "    portaombrelli 0,39°. Le vetrine hanno profondità",
    "    0,70: basi dentro, muro nero e vetro fuori.",
    "2. Porta lato destro 0,80*: stimata dal disegno",
    "    (1,93 + 0,80 + 2,20 = 4,93 dal lato ingresso).",
    "3. Quota 3,20 dello schizzo: non so dove",
    "    collocarla, non l'ho usata.",
    "4. Lato sinistro: 1,35 + 2,99 = 4,34",
    "    contro 4,31 scritto (3 cm di scarto).",
    "5. 3,08 + 0,32 + 4,02 = 7,42, ma 7,73 − 0,52 = 7,21:",
    "    21 cm di troppo, la quota 4,02 non torna: rimisurare.",
    "6. Rientranza: entrambi i lati 1,49, base 1,73.",
    "    Il fondo risulta quasi dritto (5 cm di dislivello).",
    "    Larghezza nicchia a destra 1,51* stimata.",
    "7. Termosifone a destra dopo il 2,20 (4,93 → 6,13,",
    "    lunghezza 1,20 stimata) e termostato: posizione",
    "    indicativa. Termosifone sinistro:",
    "    profondità 0,10* stimata.",
    "8. Basi vetrine: lunghe come la vetrina, dentro,",
    "    dietro al vetro (profondità 0,70).",
]
for i, n in enumerate(notes):
    ptext(px, 104 + i * 5.6, n, 3.1, "#222")

add('</svg>')
open("piantina.svg", "w", encoding="utf-8").write("\n".join(out))
print("ok")
