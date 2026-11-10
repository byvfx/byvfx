"""Draw the 88x31 buttons: python assets/make.py assets <public repo count>."""
import sys
from pathlib import Path

OUT = Path(sys.argv[1])
OUT.mkdir(parents=True, exist_ok=True)

FONT = "Verdana, Geneva, 'DejaVu Sans', sans-serif"
STYLE = (
    "<style>text{font-family:" + FONT + ";text-anchor:middle}"
    ".b{animation:b 1.2s steps(1) infinite}@keyframes b{50%{opacity:0}}"
    "@media (prefers-reduced-motion:reduce){.b{animation:none}}</style>"
)


def frame(bg, body, title):
    return (
        '<svg xmlns="http://www.w3.org/2000/svg" width="88" height="31" viewBox="0 0 88 31" role="img">'
        f"<title>{title}</title>{STYLE}"
        '<g shape-rendering="crispEdges">'
        '<rect width="88" height="31" fill="#000"/>'
        f'<rect x="1" y="1" width="86" height="29" fill="{bg}"/>'
        '<rect x="1" y="1" width="86" height="1" fill="#fff" opacity=".55"/>'
        '<rect x="1" y="1" width="1" height="29" fill="#fff" opacity=".55"/>'
        '<rect x="1" y="29" width="86" height="1" fill="#000" opacity=".45"/>'
        '<rect x="86" y="1" width="1" height="29" fill="#000" opacity=".45"/>'
        "</g>" + body + "</svg>\n"
    )


def button(name, title, bg, fg, l1, l2, block=None, blink=False, l2fill=None):
    """block = (bg, fg, glyph) draws a square on the left; the two lines sit to its right."""
    body = ""
    cx = 44
    if block:
        bbg, bfg, glyph = block
        size = 12 if len(glyph) < 3 else 9
        body += (
            f'<rect x="4" y="4" width="24" height="23" fill="{bbg}" shape-rendering="crispEdges"/>'
            f'<text x="16" y="{20 if size == 12 else 19}" font-size="{size}" font-weight="bold" fill="{bfg}">{glyph}</text>'
        )
        cx = 58
    cls = ' class="b"' if blink else ""
    body += f'<text x="{cx}" y="13" font-size="8" fill="{fg}">{l1}</text>'
    body += f'<text x="{cx}" y="24" font-size="9" font-weight="bold" fill="{l2fill or fg}"{cls}>{l2}</text>'
    (OUT / f"{name}.svg").write_text(frame(bg, body, title), encoding="utf-8")


button("houdini", "made with Houdini", "#1a1a1a", "#ffffff", "made with", "HOUDINI", ("#ff4713", "#fff", "H"))
button("python", "powered by Python", "#ffd43b", "#1e3a5f", "powered by", "PYTHON", ("#306998", "#ffd43b", "Py"))
button("rust", "written in Rust", "#2b1d16", "#f4c9a8", "written in", "RUST", ("#ce422b", "#fff", "Rs"))
button("go", "gotta Go fast", "#00add8", "#ffffff", "gotta", "GO FAST", ("#ffffff", "#00add8", "Go"))
button("usd", "USD native", "#000080", "#ffffff", "100%", "NATIVE", ("#c0c0c0", "#000080", "USD"))
button("exr", "OpenEXR now!", "#c0c0c0", "#000000", "OpenEXR", "NOW!", ("#000", "#00ff66", "EXR"), blink=True, l2fill="#c00000")
button("fps", "best viewed at 24 fps", "#000000", "#00ff66", "best viewed", "at 24 fps")
button("email", "e-mail me", "#008080", "#ffffff", "e-mail", "ME!", ("#ffffff", "#008080", "@"))
button("kofi", "buy me a coffee on Ko-fi", "#ff5e5b", "#ffffff", "buy me a", "COFFEE", ("#ffffff", "#ff5e5b", "Ko"))
button("guestbook", "sign my guestbook", "#ffffff", "#0000cc", "sign my", "guestbook", ("#ffea00", "#000", "!"))

# the name plate
body = (
    '<text x="44" y="17" font-size="14" font-weight="bold" fill="#ff7a00" letter-spacing="1">BYVFX</text>'
    '<text x="44" y="26" font-size="7" fill="#c0c0c0">las vegas, nv</text>'
)
(OUT / "byvfx.svg").write_text(frame("#000000", body, "byvfx"), encoding="utf-8")


def counter(n):
    """An odometer: the number of public repos, six digits."""
    digits = f"{n:06d}"
    body = '<text x="44" y="11" font-size="7" fill="#c0c0c0">public repos</text>'
    for i, d in enumerate(digits):
        x = 8 + i * 12
        body += (
            f'<rect x="{x}" y="14" width="11" height="13" fill="#111" stroke="#555" stroke-width="1" shape-rendering="crispEdges"/>'
            f'<text x="{x + 5.5}" y="24.5" font-size="10" font-weight="bold" fill="#00ff66" '
            f"style=\"font-family:'Courier New',monospace\">{d}</text>"
        )
    (OUT / "counter.svg").write_text(frame("#2a2a2a", body, f"{n} public repos"), encoding="utf-8")


counter(int(sys.argv[2]) if len(sys.argv) > 2 else 37)

# NEW! tag for the what's-new list
(OUT / "new.svg").write_text(
    '<svg xmlns="http://www.w3.org/2000/svg" width="34" height="13" viewBox="0 0 34 13" role="img"><title>new</title>'
    + STYLE
    + '<g class="b"><rect width="34" height="13" fill="#ffea00" shape-rendering="crispEdges"/>'
    '<text x="17" y="10" font-size="9" font-weight="bold" fill="#d00000">NEW!</text></g></svg>\n',
    encoding="utf-8",
)
print(sorted(p.name for p in OUT.glob("*.svg")))
