#!/usr/bin/env python3
"""Generate animated SVG style previews for the README (assets/previews/*.svg)."""
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "assets" / "previews"
W, H = 480, 270

ANIM = """<style>
.bob{animation:bob 1.2s ease-in-out infinite}
.wave{transform-box:fill-box;transform-origin:0% 100%;animation:wave .8s ease-in-out infinite alternate}
.legA{transform-box:fill-box;transform-origin:50% 0%;animation:step .6s ease-in-out infinite alternate}
.legB{transform-box:fill-box;transform-origin:50% 0%;animation:step .6s ease-in-out infinite alternate-reverse}
.pop{transform-box:fill-box;transform-origin:50% 50%;animation:pop 1.6s ease-in-out infinite}
.blink{animation:blink 1.4s steps(2) infinite}
.draw{stroke-dasharray:400;animation:draw 3s linear infinite}
.spin{transform-box:fill-box;transform-origin:50% 50%;animation:spin 8s linear infinite}
@keyframes bob{50%{transform:translateY(-6px)}}
@keyframes wave{from{transform:rotate(-25deg)}to{transform:rotate(20deg)}}
@keyframes step{from{transform:rotate(-12deg)}to{transform:rotate(12deg)}}
@keyframes pop{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}
@keyframes blink{50%{opacity:.35}}
@keyframes draw{from{stroke-dashoffset:400}to{stroke-dashoffset:0}}
@keyframes spin{to{transform:rotate(360deg)}}
</style>"""


def svg(body, defs="", extra_attr=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"{extra_attr}>'
            f'{ANIM}<defs>{defs}</defs>{body}</svg>\n')


def stickman(x, y, c="#111", w=5, head_fill="none", face=True, eye=None, extra_head="", extra_body="",
             joints=False, glow=""):
    """Stick figure with feet on line y, about 125px tall, waving its right arm."""
    eye = eye or c
    hy = y - 105
    j = ""
    if joints:
        for py in (y - 75, y - 40):
            j += f'<circle cx="{x}" cy="{py}" r="4" fill="none" stroke="{c}" stroke-width="2"/>'
    eyes = (f'<circle cx="{x-6}" cy="{hy-2}" r="2.6" fill="{eye}"/><circle cx="{x+6}" cy="{hy-2}" r="2.6" fill="{eye}"/>'
            f'<path d="M{x-6} {hy+7} q6 5 12 0" fill="none" stroke="{eye}" stroke-width="2" stroke-linecap="round"/>'
            ) if face else ""
    return f'''<g class="bob" {glow}>
<g fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round">
<line x1="{x}" y1="{hy+18}" x2="{x}" y2="{y-40}"/>
<line x1="{x}" y1="{y-75}" x2="{x-28}" y2="{y-48}"/>
<line class="wave" x1="{x}" y1="{y-75}" x2="{x+42}" y2="{y-98}"/>
<line class="legA" x1="{x}" y1="{y-40}" x2="{x-18}" y2="{y}"/>
<line class="legB" x1="{x}" y1="{y-40}" x2="{x+18}" y2="{y}"/>
</g>{extra_body}
<circle cx="{x}" cy="{hy}" r="18" fill="{head_fill}" stroke="{c}" stroke-width="{w}"/>{eyes}{extra_head}{j}
</g>'''


def s1():
    b = f'<rect width="{W//2}" height="{H}" fill="#fff"/>' + stickman(120, 225, face=False)
    b += ('<path class="draw" d="M165 120 L215 70" stroke="#e11d48" stroke-width="5" fill="none" stroke-linecap="round"/>'
          '<path d="M200 68 L216 68 L216 84" stroke="#e11d48" stroke-width="5" fill="none" stroke-linecap="round"/>')
    b += f'<rect x="{W//2}" width="{W//2}" height="{H}" fill="#000"/>' + stickman(360, 225, c="#fff", face=False)
    b += ('<g class="pop"><circle cx="425" cy="80" r="18" fill="none" stroke="#3b82f6" stroke-width="5"/>'
          '<line x1="425" y1="98" x2="425" y2="112" stroke="#3b82f6" stroke-width="5"/></g>')
    return svg(b)


def s2():
    b = f'<rect width="{W}" height="{H}" fill="#bfeee0"/><circle cx="390" cy="65" r="34" fill="#fde68a"/>'
    b += ('<rect class="pop" x="320" y="160" width="60" height="60" rx="10" fill="#a78bfa"/>'
          '<circle class="pop" cx="420" cy="195" r="24" fill="#60a5fa"/>'
          '<rect y="230" width="480" height="40" fill="#99dcc8"/>')
    hoodie = '<path d="M226 152 h28 l5 40 h-38 z" fill="#f97316" stroke="#111" stroke-width="3"/>'
    b += stickman(240, 230, head_fill="#fff", extra_body=hoodie)
    return svg(b)


def s3():
    d = ('<filter id="chalk"><feTurbulence baseFrequency="0.9" numOctaves="2" seed="3"/>'
         '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 -.3"/></filter>'
         '<filter id="rough"><feTurbulence baseFrequency="0.05" numOctaves="2"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>')
    b = f'<rect width="{W}" height="{H}" fill="#1f3b2d"/><rect width="{W}" height="{H}" filter="url(#chalk)" opacity=".25"/>'
    b += '<rect y="255" width="480" height="15" fill="#6b4f2a"/>'
    b += (f'<g filter="url(#rough)">{stickman(140, 235, c="#f5f5f4")}'
          '<path class="draw" d="M190 110 Q270 50 330 110" stroke="#fde047" stroke-width="4" fill="none"/>'
          '<circle cx="380" cy="150" r="38" fill="none" stroke="#f9a8d4" stroke-width="4"/>'
          '<circle cx="380" cy="150" r="9" fill="#93c5fd"/>'
          '<g class="spin"><ellipse cx="380" cy="150" rx="62" ry="20" fill="none" stroke="#93c5fd" stroke-width="3"/></g></g>')
    return svg(b, d)


def s4():
    b = f'<rect width="{W}" height="{H}" fill="#f8fafc"/><rect x="5" y="5" width="470" height="260" fill="none" stroke="#cbd5e1" stroke-width="10"/>'
    b += ('<rect x="245" y="65" width="70" height="46" rx="6" fill="none" stroke="#1d4ed8" stroke-width="4"/>'
          '<path class="draw" d="M320 88 h45" stroke="#111" stroke-width="4"/><path d="M357 80 l10 8 l-10 8" stroke="#111" stroke-width="4" fill="none"/>'
          '<circle cx="405" cy="88" r="25" fill="none" stroke="#16a34a" stroke-width="4"/><path d="M393 88 l8 9 l15 -18" stroke="#16a34a" stroke-width="4" fill="none"/>'
          '<path d="M260 160 l30 30 m0 -30 l-30 30" stroke="#dc2626" stroke-width="4"/>'
          '<g class="pop"><g transform="rotate(-35 410 190)"><rect x="380" y="182" width="70" height="16" rx="4" fill="#111"/>'
          '<path d="M380 182 l-14 8 l14 8 z" fill="#475569"/></g></g>')
    b += '<ellipse cx="150" cy="232" rx="34" ry="5" fill="#cbd5e1"/>' + stickman(150, 230)
    return svg(b)


def s5():
    d = ('<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="4" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#020617"/><stop offset="1" stop-color="#312e81"/></linearGradient>')
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    for i, (x, h) in enumerate([(0, 120), (60, 170), (130, 100), (300, 150), (365, 190), (430, 130)]):
        b += f'<rect x="{x}" y="{200-h}" width="55" height="{h}" fill="#0f172a"/>'
        b += f'<rect class="blink" x="{x+12}" y="{215-h}" width="8" height="8" fill="#fbbf24" style="animation-delay:{i*.3}s"/>'
    b += '<rect y="200" width="480" height="70" fill="#020617"/>'
    b += '<rect class="blink" x="300" y="55" width="80" height="40" rx="6" fill="none" stroke="#e879f9" stroke-width="4" filter="url(#glow)"/>'
    b += stickman(220, 200, c="#22d3ee", face=False, glow='filter="url(#glow)"')
    b += '<g opacity=".25" transform="translate(0 400) scale(1 -1)">' + stickman(220, 200, c="#22d3ee", face=False) + '</g>'
    return svg(b, d)


def s6():
    d = '<filter id="sh"><feDropShadow dx="3" dy="4" stdDeviation="2" flood-opacity=".35"/></filter>'
    b = f'<rect width="{W}" height="{H}" fill="#c8a477"/>'
    b += ('<circle cx="400" cy="65" r="30" fill="#facc15" filter="url(#sh)"/>'
          '<path d="M0 200 Q120 140 240 190 T480 170 V270 H0z" fill="#86efac" filter="url(#sh)"/>'
          '<path d="M0 232 Q160 205 300 236 T480 226 V270 H0z" fill="#4ade80" filter="url(#sh)"/>'
          '<g class="pop"><path d="M340 150 l25 -40 l25 40 z" fill="#60a5fa" filter="url(#sh)"/>'
          '<rect x="345" y="150" width="40" height="40" fill="#ef4444" filter="url(#sh)"/></g>')
    cheeks = '<circle cx="189" cy="122" r="4" fill="#f9a8d4"/><circle cx="211" cy="122" r="4" fill="#f9a8d4"/>'
    pins = '<circle cx="200" cy="150" r="3.5" fill="#b45309"/><circle cx="200" cy="185" r="3.5" fill="#b45309"/>'
    b += f'<g filter="url(#sh)">{stickman(200, 225, head_fill="#fff", c="#1c1917", extra_head=cheeks + pins)}</g>'
    return svg(b, d)


def s7():
    d = ('<filter id="ink"><feTurbulence baseFrequency=".03" numOctaves="3" seed="7"/><feDisplacementMap in="SourceGraphic" scale="8"/><feGaussianBlur stdDeviation=".8"/></filter>'
         '<filter id="mist"><feGaussianBlur stdDeviation="6"/></filter>')
    b = f'<rect width="{W}" height="{H}" fill="#f3ead7"/>'
    b += ('<path d="M200 170 L270 55 L330 140 L370 85 L470 170 Z" fill="#9ca3af" opacity=".55" filter="url(#mist)"/>'
          '<path d="M260 185 L320 110 L385 185 Z" fill="#57534e" opacity=".45" filter="url(#mist)"/>'
          '<path d="M0 210 Q120 200 240 212 T480 208" stroke="#94a3b8" stroke-width="3" fill="none" opacity=".7"/>'
          '<path d="M40 238 Q160 226 260 238 T480 232" stroke="#94a3b8" stroke-width="2" fill="none" opacity=".5"/>'
          '<path d="M55 200 Q130 214 205 200 L192 214 Q130 224 68 214 Z" fill="#1c1917" filter="url(#ink)"/>')
    robe = '<path d="M130 130 q-16 30 -12 55 M130 130 q16 30 13 55" stroke="#78716c" stroke-width="3" fill="none"/>'
    b += f'<g filter="url(#ink)">{stickman(130, 202, c="#1c1917", head_fill="#d6d3d1", face=False, extra_body=robe)}</g>'
    b += '<ellipse class="pop" cx="225" cy="216" rx="14" ry="5" fill="none" stroke="#b91c1c" stroke-width="2"/>'
    b += '<rect x="425" y="20" width="30" height="30" rx="3" fill="#b91c1c"/><rect x="430" y="25" width="20" height="20" fill="none" stroke="#f3ead7" stroke-width="2"/>'
    return svg(b, d)


def s8():
    b = f'<rect width="{W}" height="{H}" fill="#5eb2ff"/>'
    for cx, cy in [(60, 40), (300, 50)]:
        for dx, dy, n in [(20, 0, 5), (10, 10, 7), (0, 20, 9)]:
            b += f'<rect x="{cx+dx}" y="{cy+dy}" width="{n*10}" height="10" fill="#fff"/>'
    for i in range(0, W, 40):
        b += (f'<rect x="{i}" y="220" width="40" height="10" fill="#22c55e"/><rect x="{i}" y="230" width="40" height="40" fill="#a16207"/>'
              f'<rect x="{i+6}" y="238" width="12" height="8" fill="#854d0e"/>')
    b += '<rect x="290" y="120" width="40" height="40" fill="#f59e0b"/><rect x="304" y="128" width="12" height="18" fill="#fde68a"/><rect x="304" y="150" width="12" height="4" fill="#fde68a"/>'
    for i, x in enumerate([370, 405, 440]):
        b += f'<g class="pop" style="animation-delay:{i*.2}s"><rect x="{x}" y="150" width="14" height="20" fill="#facc15"/><rect x="{x+4}" y="154" width="6" height="12" fill="#fef08a"/></g>'
    b += '<g class="pop"><rect x="200" y="190" width="30" height="30" fill="#7c3aed"/><rect x="205" y="198" width="6" height="6" fill="#fff"/><rect x="219" y="198" width="6" height="6" fill="#fff"/></g>'
    fig = "".join(f'<rect x="{x}" y="{y}" width="{w_}" height="{h_}" fill="#111"/>' for x, y, w_, h_ in
                  [(110, 130, 30, 30), (122, 160, 6, 30), (104, 166, 18, 6), (128, 156, 6, 6), (134, 150, 6, 6), (140, 144, 6, 6),
                   (116, 190, 6, 6), (110, 196, 6, 24), (128, 190, 6, 6), (134, 196, 6, 24)])
    fig += ('<rect x="114" y="134" width="22" height="22" fill="#fff"/><rect x="118" y="140" width="4" height="6" fill="#111"/>'
            '<rect x="128" y="140" width="4" height="6" fill="#111"/><rect x="108" y="133" width="34" height="5" fill="#dc2626"/>'
            '<rect x="100" y="133" width="8" height="4" fill="#dc2626"/>')
    b += f'<g class="bob">{fig}</g>'
    return svg(b, extra_attr=' shape-rendering="crispEdges"')


def s9():
    d = ('<pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#3b82f6" stroke-width=".6"/></pattern>'
         '<pattern id="G" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" fill="none" stroke="#60a5fa" stroke-width="1.2"/></pattern>')
    b = f'<rect width="{W}" height="{H}" fill="#1e3a8a"/><rect width="{W}" height="{H}" fill="url(#g)"/><rect width="{W}" height="{H}" fill="url(#G)"/>'
    b += stickman(130, 225, c="#f8fafc", w=2.5, face=False, joints=True)
    teeth = "".join(f'<rect x="-6" y="-50" width="12" height="14" fill="#1e3a8a" stroke="#fb923c" stroke-width="2.5" transform="rotate({a})"/>' for a in range(0, 360, 45))
    b += (f'<g transform="translate(345 115)"><g class="spin">{teeth}<circle r="38" fill="#1e3a8a" stroke="#fb923c" stroke-width="2.5"/>'
          '<circle r="10" fill="none" stroke="#fb923c" stroke-width="2.5"/><line x1="0" y1="-38" x2="0" y2="38" stroke="#fb923c" stroke-width="1" stroke-dasharray="4 3"/></g></g>')
    b += ('<path class="draw" d="M175 150 H285" stroke="#67e8f9" stroke-width="2.5" stroke-dasharray="6 5" fill="none"/>'
          '<path d="M290 190 H400 M290 184 v12 M400 184 v12" stroke="#f8fafc" stroke-width="1.5"/>'
          '<path d="M297 186 l-7 4 l7 4 M393 186 l7 4 l-7 4" stroke="#f8fafc" stroke-width="1.5" fill="none"/>'
          '<rect x="300" y="226" width="164" height="32" fill="none" stroke="#f8fafc" stroke-width="1.5"/>'
          '<line x1="362" y1="226" x2="362" y2="258" stroke="#f8fafc" stroke-width="1.5"/>')
    return svg(b, d)


def s10():
    d = '<pattern id="dots" width="10" height="10" patternUnits="userSpaceOnUse"><circle cx="5" cy="5" r="2.4" fill="#000" opacity=".22"/></pattern>'
    rays = ""
    for a in range(0, 360, 20):
        r1, r2 = math.radians(a), math.radians(a + 10)
        rays += f'<path d="M240 135 L{240+600*math.cos(r1):.0f} {135+600*math.sin(r1):.0f} L{240+600*math.cos(r2):.0f} {135+600*math.sin(r2):.0f}Z" fill="#ef4444"/>'
    b = f'<rect width="{W}" height="{H}" fill="#fde047"/>{rays}<rect width="{W}" height="{H}" fill="url(#dots)"/>'
    for y in range(40, 240, 26):
        b += f'<line class="blink" x1="20" y1="{y}" x2="110" y2="{y}" stroke="#fff" stroke-width="4" style="animation-delay:{y/200:.2f}s"/>'
    b += ('<g class="pop"><path d="M370 55 l15 30 l32 -6 l-20 26 l22 24 l-32 -2 l-8 32 l-14 -28 l-30 10 l14 -28 l-24 -20 l32 -2z" '
          'fill="#fff" stroke="#111" stroke-width="5"/></g>')
    scarf = '<path d="M232 140 q-30 -2 -50 14 q22 -3 34 4" fill="#facc15" stroke="#111" stroke-width="4"/>'
    brows = '<path d="M228 110 l8 3 M252 110 l-8 3" stroke="#111" stroke-width="3"/>'
    b += stickman(240, 225, c="#111", w=8, head_fill="#fff", extra_head=brows, extra_body=scarf)
    b += f'<rect x="4" y="4" width="{W-8}" height="{H-8}" fill="none" stroke="#111" stroke-width="8"/>'
    return svg(b, d)


STYLES = {"s1-ink": s1, "s2-flat-pop": s2, "s3-chalkboard": s3, "s4-whiteboard": s4, "s5-neon-night": s5,
          "s6-paper-cutout": s6, "s7-ink-wash": s7, "s8-pixel-arcade": s8, "s9-blueprint": s9, "s10-comic-halftone": s10}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in STYLES.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print(f"wrote {len(STYLES)} previews to {OUT}")
