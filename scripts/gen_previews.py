#!/usr/bin/env python3
"""Generate animated SVG style previews for the README (assets/previews/*.svg).

Characters share one rig: big white head with expressive face, thin limbs with
elbows/knees, solid round hands, optional outfit/hat/props. Character motion
uses SMIL so pivots stay exact inside scaled groups.
"""
import itertools
import math
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[1] / "assets" / "previews"
W, H = 480, 270
_ids = itertools.count()

CSS = """<style>
.pop{transform-box:fill-box;transform-origin:50% 50%;animation:pop 1.6s ease-in-out infinite}
.blink{animation:blink 1.4s steps(2) infinite}
.draw{stroke-dasharray:400;animation:draw 3s linear infinite}
.spin{transform-box:fill-box;transform-origin:50% 50%;animation:spin 8s linear infinite}
@keyframes pop{0%,100%{transform:scale(1)}50%{transform:scale(1.15)}}
@keyframes blink{50%{opacity:.35}}
@keyframes draw{from{stroke-dashoffset:400}to{stroke-dashoffset:0}}
@keyframes spin{to{transform:rotate(360deg)}}
</style>"""


def svg(body, defs="", extra_attr=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}"{extra_attr}>'
            f'{CSS}<defs>{defs}</defs>{body}</svg>\n')


def rot(a, b, cx, cy, dur, begin="0s"):
    return (f'<animateTransform attributeName="transform" type="rotate" values="{a} {cx} {cy};{b} {cx} {cy};{a} {cx} {cy}" '
            f'dur="{dur}" begin="{begin}" repeatCount="indefinite" calcMode="spline" keySplines=".45 0 .55 1;.45 0 .55 1"/>')


# ---------------------------------------------------------------- character rig
# Local coordinates: feet on y=0, head centre (0,-130), r=30, shoulders (0,-88), hips (0,-45).
HEAD_Y, HEAD_R, SH, HIP = -130, 30, (0, -88), (0, -45)

POSES = {  # (right elbow, right hand, swing deg), (left elbow, left hand, swing deg)
    "wave":  (((32, -96), (48, -122), 16), ((-16, -66), (-22, -43), 3)),
    "point": (((26, -84), (54, -88), 4), ((-16, -66), (-22, -43), 3)),
    "think": (((20, -68), (9, -104), 3), ((-14, -66), (6, -66), 2)),
    "cheer": (((24, -108), (32, -134), 10), ((-24, -108), (-32, -134), 10)),
    "hold":  (((20, -70), (40, -78), 4), ((-16, -66), (-22, -43), 3)),
    "panic": (((36, -106), (27, -138), 4), ((-36, -106), (-27, -138), 4)),
}


def face(mood, line, skin):
    e = ""
    blink = ('<animate attributeName="ry" values="{r};{r};.6;{r}" keyTimes="0;.9;.95;1" dur="3.6s" repeatCount="indefinite"/>')
    def eye(cx, rx=3.6, ry=5.4, dx=0):
        return (f'<ellipse cx="{cx+dx}" cy="-133" rx="{rx}" ry="{ry}" fill="{line}">{blink.format(r=ry)}</ellipse>'
                f'<circle cx="{cx+dx+1.3}" cy="-135.5" r="1.3" fill="#fff"/>')
    sweat = ('<path d="M33 -152 q-6 9 0 12 q6 -3 0 -12z" fill="#7dd3fc" stroke="{l}" stroke-width="1.5">'
             '<animateTransform attributeName="transform" type="translate" values="0 0;0 5;0 0" dur="1.2s" repeatCount="indefinite"/></path>').format(l=line)
    if mood == "happy":
        e = (f'<path d="M-16 -143 q5 -5 10 0 M6 -143 q5 -5 10 0" stroke="{line}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
             + eye(-10) + eye(10) + f'<path d="M-10 -120 q10 12 20 0 z" fill="{line}"/>'
             f'<path d="M-5 -115 q5 3 10 0" stroke="#fb7185" stroke-width="3" stroke-linecap="round"/>')
    elif mood == "surprised":
        e = (f'<path d="M-17 -150 q5 -5 10 0 M7 -150 q5 -5 10 0" stroke="{line}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
             f'<circle cx="-10" cy="-134" r="6" fill="#fff" stroke="{line}" stroke-width="2.5"/><circle cx="10" cy="-134" r="6" fill="#fff" stroke="{line}" stroke-width="2.5"/>'
             f'<circle cx="-10" cy="-133" r="2.6" fill="{line}"/><circle cx="10" cy="-133" r="2.6" fill="{line}"/>'
             f'<ellipse cx="0" cy="-115" rx="5" ry="7" fill="{line}"/>' + sweat)
    elif mood == "determined":
        e = (f'<path d="M-17 -147 L-5 -141 M17 -147 L5 -141" stroke="{line}" stroke-width="3.5" stroke-linecap="round"/>'
             + eye(-10, ry=4.6) + eye(10, ry=4.6) +
             f'<path d="M-10 -119 q10 -3 20 -1 q-3 7 -10 7 q-8 0 -10 -6z" fill="#fff" stroke="{line}" stroke-width="2.5" stroke-linejoin="round"/>')
    elif mood == "worried":
        e = (f'<path d="M-16 -141 L-5 -146 M16 -141 L5 -146" stroke="{line}" stroke-width="2.5" stroke-linecap="round"/>'
             + eye(-10) + eye(10) +
             f'<path d="M-9 -116 q4.5 -5 9 0 q4.5 5 9 0" stroke="{line}" stroke-width="2.5" fill="none" stroke-linecap="round"/>' + sweat)
    elif mood == "calm":
        e = (f'<path d="M-15 -134 q5 5 10 0 M5 -134 q5 5 10 0" stroke="{line}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
             f'<path d="M-15 -142 q5 -3 10 -1 M5 -143 q5 -2 10 1" stroke="{line}" stroke-width="2" fill="none" stroke-linecap="round"/>'
             f'<path d="M-6 -119 q6 5 12 0" stroke="{line}" stroke-width="2.5" fill="none" stroke-linecap="round"/>')
    elif mood == "thinking":
        e = (f'<path d="M-16 -144 q5 -3 10 0 M6 -148 q5 -4 10 1" stroke="{line}" stroke-width="2.5" fill="none" stroke-linecap="round"/>'
             + eye(-10, dx=3) + eye(10, dx=3) +
             f'<path d="M-3 -118 h10" stroke="{line}" stroke-width="2.5" stroke-linecap="round"/>')
    return e


def hat(kind, line):
    return {
        "tuft": f'<path d="M-2 -159 q2 -14 14 -15 M-1 -159 q-4 -10 -13 -10" stroke="{line}" stroke-width="2.5" fill="none" stroke-linecap="round"/>',
        "bun": f'<circle cx="0" cy="-166" r="9" fill="{line}"/><path d="M-8 -159 h16" stroke="#b91c1c" stroke-width="3"/>'
               f'<path d="M-24 -150 q24 -20 48 0" stroke="{line}" stroke-width="5" fill="none"/>',
        "hardhat": f'<path d="M-30 -142 a30 28 0 0 1 60 0 z" fill="#fb923c" stroke="{line}" stroke-width="2.5"/>'
                   f'<rect x="-36" y="-145" width="72" height="7" rx="3" fill="#fb923c" stroke="{line}" stroke-width="2.5"/>'
                   f'<path d="M0 -168 v22" stroke="{line}" stroke-width="2"/>',
        "headphones": f'<path d="M-31 -130 a31 33 0 0 1 62 0" stroke="#e879f9" stroke-width="4" fill="none"/>'
                      f'<rect x="-38" y="-138" width="10" height="18" rx="4" fill="#e879f9"/><rect x="28" y="-138" width="10" height="18" rx="4" fill="#e879f9"/>',
        "strawhat": f'<ellipse cx="0" cy="-152" rx="42" ry="8" fill="#fde68a" stroke="{line}" stroke-width="2.5"/>'
                    f'<path d="M-20 -153 q0 -22 20 -22 q20 0 20 22z" fill="#fde68a" stroke="{line}" stroke-width="2.5"/>'
                    f'<path d="M-20 -157 h40" stroke="#ef4444" stroke-width="4"/>',
        "ponytail": f'<path d="M-28 -142 q8 -26 36 -18 q18 6 22 22 q-16 -16 -58 -4z" fill="{line}"/>'
                    f'<path d="M26 -150 q22 0 18 30 q-8 -16 -18 -18z" fill="{line}"/>',
        "cap": f'<path d="M-28 -142 a28 26 0 0 1 56 0 z" fill="#3b82f6" stroke="{line}" stroke-width="2.5"/>'
               f'<path d="M20 -144 q22 -2 30 6 q-14 4 -30 2z" fill="#2563eb" stroke="{line}" stroke-width="2.5"/>'
               f'<circle cx="0" cy="-168" r="3.5" fill="#2563eb"/>',
        "glasses": f'<g fill="none" stroke="{line}" stroke-width="2"><circle cx="-10" cy="-133" r="8"/><circle cx="10" cy="-133" r="8"/><path d="M-2 -134 h4 M-18 -134 l-11 -3 M18 -134 l11 -3"/></g>',
    }.get(kind, "")


def outfit(kind, line, color="#f97316"):
    if kind == "hoodie":
        return (f'<path d="M-17 -95 Q0 -101 17 -95 L20 -46 Q0 -41 -20 -46 Z" fill="{color}" stroke="{line}" stroke-width="3" stroke-linejoin="round"/>'
                f'<path d="M-9 -66 h18 v10 h-18z" fill="none" stroke="{line}" stroke-width="2"/><path d="M-5 -95 v10 M5 -95 v10" stroke="#fff" stroke-width="2"/>')
    if kind == "tee":
        return f'<path d="M-15 -95 h30 l6 14 l-7 3 l-1 32 h-26 l-1 -32 l-7 -3z" fill="{color}" stroke="{line}" stroke-width="3" stroke-linejoin="round"/>'
    if kind == "tie":
        return (f'<path d="M-3 -95 h6 l-1 5 l5 26 l-7 8 l-7 -8 l5 -26z" fill="{color}" stroke="{line}" stroke-width="2" stroke-linejoin="round"/>')
    if kind == "robe":
        return (f'<path d="M-15 -96 Q0 -100 15 -96 L28 -16 Q0 -10 -28 -16 Z" fill="#d6d3d1" stroke="{line}" stroke-width="3" stroke-linejoin="round" opacity=".95"/>'
                f'<path d="M-12 -96 L4 -60 M12 -96 L-2 -72" stroke="{line}" stroke-width="2.5" fill="none"/><path d="M-24 -52 h48" stroke="#b91c1c" stroke-width="4"/>')
    if kind == "scarf":
        a = "M-10 -96 q-30 2 -52 -12 q16 18 50 22z"
        b = "M-10 -96 q-30 -10 -56 4 q22 8 54 8z"
        return (f'<path d="{a}" fill="{color}" stroke="{line}" stroke-width="3" stroke-linejoin="round">'
                f'<animate attributeName="d" values="{a};{b};{a}" dur=".7s" repeatCount="indefinite"/></path>'
                f'<rect x="-15" y="-101" width="30" height="11" rx="5" fill="{color}" stroke="{line}" stroke-width="3"/>')
    return ""


def arm(elbow, hand, swing, line, w, dur, hand_r=5.5, prop="", begin="0s", dx=0):
    sx, sy = SH[0] + dx, SH[1] - (4 if dx else 0)
    elbow, hand = (elbow[0] + dx, elbow[1]), (hand[0] + dx, hand[1])
    return (f'<g>{rot(-swing, swing, sx, sy, dur, begin)}'
            f'<polyline points="{sx},{sy} {elbow[0]},{elbow[1]} {hand[0]},{hand[1]}" fill="none" stroke="{line}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<circle cx="{hand[0]}" cy="{hand[1]}" r="{hand_r}" fill="{line}"/><g transform="translate({dx} 0)">{prop}</g></g>')


def leg(knee, foot, toe, swing, line, w, begin):
    hx, hy = HIP
    return (f'<g>{rot(-swing, swing, hx, hy, "1s", begin) if swing else ""}'
            f'<polyline points="{hx},{hy} {knee[0]},{knee[1]} {foot[0]},{foot[1]}" fill="none" stroke="{line}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>'
            f'<ellipse cx="{foot[0]+toe}" cy="{foot[1]-1}" rx="8" ry="4" fill="{line}"/></g>')


def character(x, y, s=1.0, line="#111", skin="#fff", shade="#e5e7eb", mood="happy", pose="wave", top="", wear="",
              wear_color="#f97316", prop="", walk=False, w=5, joints=False, blush=False, flip=False, glow="",
              shadow="rgba(0,0,0,.15)", hand_r=5.5, delay="0s"):
    """Draw an expressive stick character with feet centred at (x, y)."""
    cid = next(_ids)
    (re, rh, rs), (le, lh, ls) = POSES[pose]
    legs = (leg((-8, -22), (-13, 0), -3, 8 if walk else 0, line, w, "0s")
            + leg((8, -22), (13, 0), 3, 8 if walk else 0, line, w, "-.5s"))
    joint_marks = "".join(f'<circle cx="{px}" cy="{py}" r="4" fill="{skin}" stroke="{line}" stroke-width="2"/>'
                          for px, py in [SH, HIP, re, le, (-8, -22), (8, -22)]) if joints else ""
    blush_svg = ('<ellipse cx="-19" cy="-121" rx="5.5" ry="3" fill="#fda4af" opacity=".8"/>'
                 '<ellipse cx="19" cy="-121" rx="5.5" ry="3" fill="#fda4af" opacity=".8"/>') if blush else ""
    head = (f'<g>{rot(-3, 3, 0, -100, "2.6s", delay)}'
            f'<clipPath id="hc{cid}"><circle cx="0" cy="{HEAD_Y}" r="{HEAD_R}"/></clipPath>'
            f'<circle cx="0" cy="{HEAD_Y}" r="{HEAD_R}" fill="{skin}"/>'
            + (f'<g clip-path="url(#hc{cid})"><rect x="-40" y="-170" width="80" height="80" fill="{shade}"/>'
               f'<circle cx="-6" cy="{HEAD_Y-5}" r="{HEAD_R}" fill="{skin}"/></g>' if shade else "")
            + f'<circle cx="0" cy="{HEAD_Y}" r="{HEAD_R}" fill="none" stroke="{line}" stroke-width="{w-0.5}"/>'
            + blush_svg + face(mood, line, skin) + hat(top, line) + '</g>')
    body = (f'<ellipse cx="0" cy="3" rx="30" ry="5" fill="{shadow}"/>' if shadow else "")
    body += legs + f'<path d="M0 -100 V{HIP[1]}" stroke="{line}" stroke-width="{w}" stroke-linecap="round"/>'
    body += outfit(wear, line, wear_color)
    sdx = 15 if wear in ("hoodie", "tee", "robe") else 0
    body += arm(le, lh, ls, line, w, "1.8s", hand_r, begin=delay, dx=-sdx)
    body += arm(re, rh, rs, line, w, ".9s" if pose == "wave" else "1.6s", hand_r, prop, delay, dx=sdx)
    body += joint_marks + head
    bob = f'<animateTransform attributeName="transform" type="translate" values="0 0;0 -4;0 0" dur="1.4s" begin="{delay}" repeatCount="indefinite"/>'
    sxs = -s if flip else s
    return f'<g transform="translate({x} {y}) scale({sxs} {s})" {glow}><g>{bob}{body}</g></g>'


# ---------------------------------------------------------------- styles
def s1():
    b = f'<rect width="{W//2}" height="{H}" fill="#fff"/>'
    b += ('<polyline class="draw" points="150,60 172,92 190,78 220,130" fill="none" stroke="#e11d48" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>'
          '<path d="M206 128 L222 133 L224 116" fill="none" stroke="#e11d48" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/>')
    b += character(90, 238, .95, mood="surprised", pose="panic", top="tuft")
    b += f'<rect x="{W//2}" width="{W//2}" height="{H}" fill="#000"/>'
    b += ('<g class="pop"><circle cx="425" cy="62" r="20" fill="#3b82f6"/><rect x="417" y="82" width="16" height="10" rx="2" fill="#93c5fd"/>'
          '<path d="M425 30 v-10 M450 40 l8 -7 M400 40 l-8 -7 M458 62 h10 M392 62 h-10" stroke="#3b82f6" stroke-width="4" stroke-linecap="round"/></g>')
    b += character(340, 238, .95, line="#fff", skin="#000", shade="", mood="thinking", pose="think", shadow="rgba(255,255,255,.15)", delay="-.4s")
    return svg(b)


def s2():
    b = f'<rect width="{W}" height="{H}" fill="#bfeee0"/><circle cx="400" cy="58" r="30" fill="#fde68a"/>'
    b += ('<rect class="pop" x="40" y="70" width="44" height="44" rx="10" fill="#a78bfa"/>'
          '<path class="pop" d="M410 120 l14 -26 l14 26z" fill="#f472b6"/>'
          f'<rect y="238" width="{W}" height="32" fill="#99dcc8"/>')
    ball = '<circle cx="40" cy="-94" r="12" fill="#60a5fa" stroke="#111" stroke-width="3"/>'
    b += character(190, 240, .95, mood="happy", pose="wave", top="tuft", wear="hoodie", wear_color="#f97316")
    b += character(320, 240, .85, mood="happy", pose="hold", top="ponytail", wear="tee", wear_color="#34d399",
                   prop=ball, blush=True, flip=True, delay="-.6s")
    return svg(b)


def s3():
    d = ('<filter id="chalk"><feTurbulence baseFrequency="0.9" numOctaves="2" seed="3"/>'
         '<feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .5 -.3"/></filter>'
         '<filter id="rough"><feTurbulence baseFrequency="0.06" numOctaves="2"/><feDisplacementMap in="SourceGraphic" scale="2.5"/></filter>')
    b = f'<rect width="{W}" height="{H}" fill="#1f3b2d"/><rect width="{W}" height="{H}" filter="url(#chalk)" opacity=".25"/>'
    b += f'<rect y="255" width="{W}" height="15" fill="#6b4f2a"/>'
    pointer = '<path d="M54 -88 L104 -110" stroke="#d6b88a" stroke-width="4" stroke-linecap="round"/>'
    b += (f'<g filter="url(#rough)">{character(130, 240, .95, line="#f5f5f4", skin="#1f3b2d", shade="", mood="happy", pose="point", top="glasses", prop=pointer, shadow="")}'
          '<path class="draw" d="M250 80 Q300 40 350 80" stroke="#fde047" stroke-width="4" fill="none"/>'
          '<circle cx="370" cy="150" r="38" fill="none" stroke="#f9a8d4" stroke-width="4"/>'
          '<circle cx="370" cy="150" r="9" fill="#93c5fd"/>'
          '<g class="spin"><ellipse cx="370" cy="150" rx="64" ry="20" fill="none" stroke="#93c5fd" stroke-width="3"/></g></g>')
    return svg(b, d)


def s4():
    b = f'<rect width="{W}" height="{H}" fill="#f8fafc"/><rect x="5" y="5" width="470" height="260" fill="none" stroke="#cbd5e1" stroke-width="10"/>'
    b += ('<rect x="245" y="55" width="70" height="46" rx="6" fill="none" stroke="#1d4ed8" stroke-width="4"/>'
          '<path class="draw" d="M320 78 h45" stroke="#111" stroke-width="4"/><path d="M357 70 l10 8 l-10 8" stroke="#111" stroke-width="4" fill="none"/>'
          '<circle cx="405" cy="78" r="25" fill="none" stroke="#16a34a" stroke-width="4"/><path d="M393 78 l8 9 l15 -18" stroke="#16a34a" stroke-width="4" fill="none"/>'
          '<path d="M262 150 l28 28 m0 -28 l-28 28" stroke="#dc2626" stroke-width="4"/>'
          '<g class="pop"><g transform="rotate(-35 410 190)"><rect x="380" y="182" width="70" height="16" rx="4" fill="#111"/>'
          '<path d="M380 182 l-14 8 l14 8 z" fill="#475569"/></g></g>')
    b += character(140, 238, .95, mood="determined", pose="point", top="tuft", wear="tie", wear_color="#2563eb")
    return svg(b)


def s5():
    d = ('<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="3" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
         '<linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#020617"/><stop offset="1" stop-color="#312e81"/></linearGradient>')
    b = f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
    for i, (x, h) in enumerate([(0, 120), (60, 170), (130, 100), (300, 150), (365, 190), (430, 130)]):
        b += f'<rect x="{x}" y="{215-h}" width="55" height="{h}" fill="#0f172a"/>'
        b += f'<rect class="blink" x="{x+12}" y="{230-h}" width="8" height="8" fill="#fbbf24" style="animation-delay:{i*.3}s"/>'
    b += f'<rect y="215" width="{W}" height="55" fill="#020617"/>'
    b += '<rect class="blink" x="300" y="45" width="80" height="40" rx="6" fill="none" stroke="#e879f9" stroke-width="4" filter="url(#glow)"/>'
    phone = '<rect x="34" y="-92" width="14" height="22" rx="3" fill="#22d3ee" stroke="#22d3ee" stroke-width="2"/>'
    b += character(220, 228, .9, line="#22d3ee", skin="#0b1026", shade="", mood="surprised", pose="hold", top="headphones",
                   prop=phone, glow='filter="url(#glow)"', shadow="rgba(34,211,238,.25)")
    return svg(b, d)


def s6():
    d = '<filter id="sh"><feDropShadow dx="3" dy="4" stdDeviation="2" flood-opacity=".35"/></filter>'
    b = f'<rect width="{W}" height="{H}" fill="#c8a477"/>'
    b += ('<circle cx="410" cy="55" r="28" fill="#facc15" filter="url(#sh)"/>'
          '<path d="M0 200 Q120 140 240 190 T480 170 V270 H0z" fill="#86efac" filter="url(#sh)"/>'
          '<path d="M0 232 Q160 205 300 236 T480 226 V270 H0z" fill="#4ade80" filter="url(#sh)"/>'
          '<g class="pop"><path d="M360 160 l25 -40 l25 40 z" fill="#60a5fa" filter="url(#sh)"/>'
          '<rect x="365" y="160" width="40" height="40" fill="#ef4444" filter="url(#sh)"/></g>')
    balloon = ('<path d="M40 -78 q10 -30 -4 -62" stroke="#1c1917" stroke-width="1.5" fill="none"/>'
               '<ellipse cx="36" cy="-160" rx="17" ry="21" fill="#ef4444" stroke="#1c1917" stroke-width="2.5"/>'
               '<path d="M30 -170 q-5 6 -3 14" stroke="#fff" stroke-width="3" fill="none" stroke-linecap="round" opacity=".7"/>')
    pins = "".join(f'<circle cx="{px}" cy="{py}" r="3" fill="#b45309"/>' for px, py in [SH, HIP])
    b += (f'<g filter="url(#sh)">{character(190, 238, .95, line="#1c1917", mood="happy", pose="hold", top="strawhat", prop=balloon, blush=True, shadow="")}</g>'
          f'<g transform="translate(190 238) scale(.95)">{pins}</g>')
    return svg(b, d)


def s7():
    d = ('<filter id="ink"><feTurbulence baseFrequency=".035" numOctaves="3" seed="7"/><feDisplacementMap in="SourceGraphic" scale="5"/></filter>'
         '<filter id="mist"><feGaussianBlur stdDeviation="6"/></filter>')
    b = f'<rect width="{W}" height="{H}" fill="#f3ead7"/>'
    b += ('<path d="M200 170 L270 55 L330 140 L370 85 L470 170 Z" fill="#9ca3af" opacity=".55" filter="url(#mist)"/>'
          '<path d="M260 185 L320 110 L385 185 Z" fill="#57534e" opacity=".45" filter="url(#mist)"/>'
          '<path d="M0 214 Q120 204 240 216 T480 212" stroke="#94a3b8" stroke-width="3" fill="none" opacity=".7"/>'
          '<path d="M40 242 Q160 230 260 242 T480 236" stroke="#94a3b8" stroke-width="2" fill="none" opacity=".5"/>')
    b += ('<g><animateTransform attributeName="transform" type="translate" values="0 0;0 3;0 0" dur="2.4s" repeatCount="indefinite"/>'
          f'<g filter="url(#ink)">{character(135, 214, .85, line="#1c1917", skin="#f8f4ea", shade="#e7e0cf", mood="calm", pose="think", top="bun", wear="robe", shadow="")}</g>'
          '<path d="M50 210 Q135 226 220 210 L205 226 Q135 236 64 226 Z" fill="#1c1917" filter="url(#ink)"/></g>')
    b += '<ellipse class="pop" cx="250" cy="226" rx="14" ry="5" fill="none" stroke="#b91c1c" stroke-width="2"/>'
    b += '<rect x="425" y="20" width="30" height="30" rx="3" fill="#b91c1c"/><rect x="430" y="25" width="20" height="20" fill="none" stroke="#f3ead7" stroke-width="2"/>'
    return svg(b, d)


def s8():
    d = ('<radialGradient id="clayBg" cx=".5" cy=".35" r=".8"><stop offset="0" stop-color="#fde4c8"/><stop offset="1" stop-color="#f4b98a"/></radialGradient>'
         '<radialGradient id="clayHead" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#ffffff"/><stop offset=".6" stop-color="#f5f1ea"/><stop offset="1" stop-color="#d9d2c5"/></radialGradient>'
         '<filter id="clay" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur in="SourceAlpha" stdDeviation="2.5" result="b"/>'
         '<feSpecularLighting in="b" surfaceScale="4" specularConstant=".55" specularExponent="16" lighting-color="#fff" result="sp"><fePointLight x="80" y="-60" z="160"/></feSpecularLighting>'
         '<feComposite in="sp" in2="SourceAlpha" operator="in" result="sp2"/>'
         '<feComposite in="SourceGraphic" in2="sp2" operator="arithmetic" k2="1" k3=".6"/>'
         '<feDropShadow dx="2" dy="5" stdDeviation="3" flood-color="#7c2d12" flood-opacity=".3"/></filter>'
         '<filter id="thumb"><feTurbulence baseFrequency=".9" numOctaves="1" seed="4"/><feColorMatrix values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 .5 -.2"/>'
         '<feComposite in2="SourceGraphic" operator="in"/></filter>')
    b = f'<rect width="{W}" height="{H}" fill="url(#clayBg)"/>'
    b += f'<path d="M0 200 Q240 186 480 200 V270 H0z" fill="#d9784a" filter="url(#clay)"/>'
    b += f'<rect width="{W}" height="{H}" fill="#7c2d12" filter="url(#thumb)" opacity=".18"/>'
    b += ('<g filter="url(#clay)">'
          '<g class="pop"><circle cx="410" cy="60" r="26" fill="#facc15"/></g>'
          '<g><animateTransform attributeName="transform" type="translate" values="0 0;12 0;0 0" dur="6s" repeatCount="indefinite"/>'
          '<ellipse cx="70" cy="58" rx="34" ry="16" fill="#e0f2fe"/><circle cx="58" cy="48" r="16" fill="#e0f2fe"/><circle cx="82" cy="46" r="13" fill="#e0f2fe"/></g>'
          '<rect x="356" y="188" width="44" height="34" rx="8" fill="#c2410c"/>'
          '<rect x="370" y="128" width="16" height="64" rx="8" fill="#4ade80"/><rect x="348" y="146" width="14" height="30" rx="7" fill="#4ade80"/>'
          '<rect x="356" y="168" width="20" height="12" rx="6" fill="#4ade80"/><rect x="392" y="140" width="14" height="28" rx="7" fill="#4ade80"/>'
          '<rect x="382" y="158" width="18" height="12" rx="6" fill="#4ade80"/><circle class="pop" cx="378" cy="124" r="6" fill="#f472b6"/>'
          '<g class="pop"><circle cx="270" cy="196" r="14" fill="#60a5fa"/><circle cx="300" cy="200" r="10" fill="#facc15"/></g></g>')
    b += (f'<g filter="url(#clay)">{character(170, 228, .95, line="#3f3f46", skin="url(#clayHead)", shade="", mood="happy", pose="wave", top="cap", wear="tee", wear_color="#4ade80", w=9, hand_r=8, blush=True, shadow="")}</g>')
    return svg(b, d)


def s9():
    d = ('<pattern id="g" width="20" height="20" patternUnits="userSpaceOnUse"><path d="M20 0H0V20" fill="none" stroke="#3b82f6" stroke-width=".6"/></pattern>'
         '<pattern id="G" width="100" height="100" patternUnits="userSpaceOnUse"><path d="M100 0H0V100" fill="none" stroke="#60a5fa" stroke-width="1.2"/></pattern>')
    b = f'<rect width="{W}" height="{H}" fill="#1e3a8a"/><rect width="{W}" height="{H}" fill="url(#g)"/><rect width="{W}" height="{H}" fill="url(#G)"/>'
    b += character(120, 235, .95, line="#f8fafc", skin="#1e3a8a", shade="", mood="determined", pose="point", top="hardhat",
                   w=3, joints=True, shadow="", hand_r=4.5)
    teeth = "".join(f'<rect x="-6" y="-50" width="12" height="14" fill="#1e3a8a" stroke="#fb923c" stroke-width="2.5" transform="rotate({a})"/>' for a in range(0, 360, 45))
    b += (f'<g transform="translate(355 110)"><g class="spin">{teeth}<circle r="38" fill="#1e3a8a" stroke="#fb923c" stroke-width="2.5"/>'
          '<circle r="10" fill="none" stroke="#fb923c" stroke-width="2.5"/><line x1="0" y1="-38" x2="0" y2="38" stroke="#fb923c" stroke-width="1" stroke-dasharray="4 3"/></g></g>')
    b += ('<path class="draw" d="M180 152 H300" stroke="#67e8f9" stroke-width="2.5" stroke-dasharray="6 5" fill="none"/>'
          '<path d="M300 180 H410 M300 174 v12 M410 174 v12" stroke="#f8fafc" stroke-width="1.5"/>'
          '<path d="M307 176 l-7 4 l7 4 M403 176 l7 4 l-7 4" stroke="#f8fafc" stroke-width="1.5" fill="none"/>'
          '<rect x="300" y="226" width="164" height="32" fill="none" stroke="#f8fafc" stroke-width="1.5"/>'
          '<line x1="362" y1="226" x2="362" y2="258" stroke="#f8fafc" stroke-width="1.5"/>')
    return svg(b, d)


def s10():
    d = ('<filter id="wc" x="-20%" y="-20%" width="140%" height="140%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="4" seed="9" result="n"/>'
         '<feDisplacementMap in="SourceGraphic" in2="n" scale="16" result="d"/><feGaussianBlur in="d" stdDeviation="1.6"/></filter>'
         '<filter id="pencil"><feTurbulence baseFrequency=".8" numOctaves="1" seed="2" result="n"/><feDisplacementMap in="SourceGraphic" in2="n" scale="1.6"/></filter>'
         '<filter id="paper"><feTurbulence baseFrequency=".7" numOctaves="3" seed="5"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .45  0 0 0 0 .3  0 0 0 .35 -.1"/></filter>')
    b = f'<rect width="{W}" height="{H}" fill="#fbf7ef"/>'
    b += ('<g filter="url(#wc)" opacity=".75">'
          '<ellipse cx="240" cy="40" rx="280" ry="70" fill="#bfdbfe" opacity=".7"/>'
          '<ellipse cx="380" cy="70" rx="70" ry="30" fill="#e0e7ff" opacity=".8"/>'
          '<path d="M-20 215 Q120 170 260 205 T500 195 V290 H-20z" fill="#a7c4a0"/>'
          '<path d="M-20 240 Q160 215 320 242 T500 236 V290 H-20z" fill="#86a97f"/>'
          '<rect x="392" y="120" width="14" height="95" fill="#a16207" opacity=".7"/>'
          '<circle cx="399" cy="104" r="44" fill="#86a97f"/><circle cx="372" cy="124" r="26" fill="#a7c4a0"/><circle cx="428" cy="122" r="28" fill="#6b8f63"/>'
          '<circle cx="70" cy="222" r="8" fill="#f9a8d4"/><circle cx="96" cy="230" r="7" fill="#fca5a5"/><circle cx="310" cy="232" r="7" fill="#f9a8d4"/></g>')
    for i, x in enumerate(range(30, 480, 38)):
        y0 = (i * 37) % 120
        b += (f'<line x1="{x}" y1="{y0}" x2="{x-4}" y2="{y0+12}" stroke="#93c5fd" stroke-width="2" stroke-linecap="round" opacity=".8">'
              f'<animateTransform attributeName="transform" type="translate" values="0 -40;-16 200" dur="{1.6 + (i % 3) * .3:.1f}s" repeatCount="indefinite"/></line>')
    umbrella = ('<path d="M40 -78 L-14 -178" stroke="#57534e" stroke-width="3" stroke-linecap="round"/>'
                '<path d="M40 -78 q0 8 -8 8" stroke="#57534e" stroke-width="3" fill="none" stroke-linecap="round"/>'
                '<path d="M-76 -172 Q-14 -232 48 -172 Q32 -182 17 -172 Q2 -182 -14 -172 Q-30 -182 -45 -172 Q-60 -182 -76 -172z" fill="#ef4444" opacity=".85" stroke="#7f1d1d" stroke-width="2"/>'
                '<path d="M-14 -205 v-8" stroke="#57534e" stroke-width="3" stroke-linecap="round"/>')
    b += (f'<g filter="url(#pencil)">{character(200, 236, .9, line="#57534e", skin="#fffdf8", shade="#f3e6d3", mood="happy", pose="hold", top="tuft", wear="hoodie", wear_color="#fcd34d", w=4, blush=True, prop=umbrella, walk=True, shadow="rgba(87,83,78,.15)")}</g>')
    b += f'<rect width="{W}" height="{H}" filter="url(#paper)" opacity=".35"/>'
    return svg(b, d)


STYLES = {"s1-ink": s1, "s2-flat-pop": s2, "s3-chalkboard": s3, "s4-whiteboard": s4, "s5-neon-night": s5,
          "s6-paper-cutout": s6, "s7-ink-wash": s7, "s8-clay": s8, "s9-blueprint": s9, "s10-watercolor": s10}

if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    for name, fn in STYLES.items():
        (OUT / f"{name}.svg").write_text(fn(), encoding="utf-8")
    print(f"wrote {len(STYLES)} previews to {OUT}")
