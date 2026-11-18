"""From the rule catalogue to design tokens for the web (interpretation layer, class D).

data/interpretation/web.json says which rules of the catalogue are carried over to a web page, how
closely, and which analogies were rejected. This module turns the accepted translations into numbers:

- one module (the body line height) and minutes of 1/60 module (W-MODUL, I.XIII.11);
- a spacing scale from Palladio's intercolumniations ¼ … 4 modules (W-ABSTAENDE);
- a type scale whose steps are the three means of I.XXIII: 4/3 on small screens, 3/2 on large ones,
  sliding in between (W-MITTEL, W-DECORUM);
- line height and letter spacing corrected for size (W-OTTICA);
- the six rectangular room forms of I.XXI.5 as aspect ratios (W-FORMEN);
- colours from today's scan of the 1570 print, lightened to a warm white (W-BIANCO).

It writes output/web/tokens.json and the theme.json of the WordPress theme in products/wordpress/palladio.

    python -m palladio_code.webdesign
"""
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INTERPRETATION = ROOT / "data/interpretation/web.json"
THEME = ROOT / "products/wordpress/palladio"

VIEWPORT_MIN, VIEWPORT_MAX = 22.0, 80.0          # rem; fluid values slide between these widths
BODY_MIN, BODY_MAX = 1.0625, 1.1875              # rem; free choice (data/interpretation/web.json)
LINE_HEIGHT = 1.5                                # free choice; defines the module
MEANS = {"harmonic": 4 / 3, "geometric": math.sqrt(2), "arithmetic": 3 / 2}   # the three means of 1 and 2
SPACING = [("10", 0.25, "¼ Modul"), ("20", 0.5, "½ Modul"), ("30", 1, "1 Modul"), ("40", 1.5, "1½ Moduln"),
           ("50", 2, "2 Moduln"), ("60", 2.25, "2¼ Moduln (Eustylos)"), ("70", 3, "3 Moduln"), ("80", 4, "4 Moduln")]
FORMS = [("1:1", 1, 1, "Quadrat"), ("√2:1", math.sqrt(2), 1, "Diagonale des Quadrats"), ("4:3", 4, 3, "4 : 3"),
         ("3:2", 3, 2, "3 : 2"), ("5:3", 5, 3, "5 : 3"), ("2:1", 2, 1, "zwei Quadrate")]
STEPS = [("small", -1, "Klein"), ("medium", 0, "Text"), ("large", 1, "Groß"),
         ("x-large", 2, "Sehr groß"), ("xx-large", 3, "Titel"), ("huge", 4, "Eingang")]
HEADING_STEP = {"h1": 3, "h2": 2, "h3": 1, "h4": 0, "h5": 0, "h6": -1}
COLOUR_NAMES = {"calce": "Calce (Grund)", "inchiostro": "Inchiostro (Schrift)", "carta": "Carta (Papier des Scans)",
                "pietra": "Pietra (Nebentext)", "linea": "Linea (Haarlinie)"}


def load() -> dict:
    return json.loads(INTERPRETATION.read_text(encoding="utf-8"))


def catalogue_ids() -> set[str]:
    return {r["id"] for path in (ROOT / "data/rules").glob("book*.json")
            for r in json.loads(path.read_text(encoding="utf-8"))["rules"]}


def validate(data: dict) -> list[str]:
    """Every translation cites existing catalogue rules and a known strength."""
    problems, known = [], catalogue_ids()
    for t in data["translations"] + data["rejected"]:
        for rule in t["rules"]:
            if rule not in known:
                problems.append(f"{t['id']}: unknown rule {rule}")
        if not t["rules"]:
            problems.append(f"{t['id']}: no rule")
    for t in data["translations"]:
        if t["strength"] not in data["strength_vocabulary"]:
            problems.append(f"{t['id']}: unknown strength {t['strength']}")
    ids = [t["id"] for t in data["translations"] + data["rejected"]]
    if len(ids) != len(set(ids)):
        problems.append("duplicate ids")
    return problems


def num(x: float) -> str:
    return f"{x:.4f}".rstrip("0").rstrip(".")


def fluid(lo: float, hi: float) -> str:
    """clamp() that slides linearly from lo (at VIEWPORT_MIN) to hi (at VIEWPORT_MAX); all in rem."""
    if abs(hi - lo) < 1e-9:
        return f"{num(lo)}rem"
    slope = (hi - lo) / (VIEWPORT_MAX - VIEWPORT_MIN)
    intercept = lo - slope * VIEWPORT_MIN
    return f"clamp({num(lo)}rem, {num(intercept)}rem + {num(slope * 100)}vw, {num(hi)}rem)"


def hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def rgb_to_hex(rgb) -> str:
    return "#" + "".join(f"{round(c):02x}" for c in rgb)


def median_colour(colours: list[str]) -> str:
    channels = list(zip(*(hex_to_rgb(c) for c in colours)))
    return rgb_to_hex(sorted(ch)[len(ch) // 2] for ch in channels)


def mix(a: str, b: str, share_a: float) -> str:
    ra, rb = hex_to_rgb(a), hex_to_rgb(b)
    return rgb_to_hex(share_a * x + (1 - share_a) * y for x, y in zip(ra, rb))


def luminance(h: str) -> float:
    def lin(c):
        c /= 255
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    r, g, b = (lin(c) for c in hex_to_rgb(h))
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def contrast(a: str, b: str) -> float:
    la, lb = sorted((luminance(a), luminance(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def palette(data: dict) -> dict:
    scan = data["measured"]["scan_colors"]
    ink, paper = median_colour(scan["ink"]), median_colour(scan["paper"])
    calce = mix(paper, "#ffffff", 0.25)
    day = {"calce": calce, "inchiostro": ink, "carta": paper,
           "pietra": mix(ink, calce, 0.8), "linea": mix(ink, calce, 0.25)}
    night_ground = mix(ink, "#000000", 0.6)
    night = {"calce": night_ground, "inchiostro": mix(paper, "#ffffff", 0.6), "carta": mix(ink, "#000000", 0.85),
             "pietra": mix(paper, night_ground, 0.72), "linea": mix(paper, night_ground, 0.25)}
    return {"scan_ink": ink, "scan_paper": paper, "day": day, "night": night}


def tokens(data: dict) -> dict:
    lo_ratio, hi_ratio = MEANS["harmonic"], MEANS["arithmetic"]
    module_lo, module_hi = BODY_MIN * LINE_HEIGHT, BODY_MAX * LINE_HEIGHT
    sizes = {}
    for slug, k, name in STEPS:
        # below the text size the smaller mean holds at every width, so that small type never shrinks
        lo, hi = (BODY_MIN * lo_ratio ** k, BODY_MAX * hi_ratio ** k) if k >= 0 else \
            (BODY_MIN * lo_ratio ** k, BODY_MAX * lo_ratio ** k)
        mid = math.sqrt(2) ** k                       # geometric mean as the reference step for corrections
        sizes[slug] = {"name": name, "step": k, "min_rem": round(lo, 4), "max_rem": round(hi, 4),
                       "css": fluid(lo, hi),
                       "line_height": round(1 + 0.5 * mid ** -0.75, 3) if k > 0 else LINE_HEIGHT,
                       "letter_spacing_em": round(-0.005 * (k - 1), 3) if k >= 2 else 0}
    spacing = [{"slug": s, "name": n, "modules": f, "css": fluid(module_lo * f, module_hi * f)} for s, f, n in SPACING]
    colours = palette(data)
    checks = {
        "text_on_ground_day": round(contrast(colours["day"]["inchiostro"], colours["day"]["calce"]), 2),
        "secondary_on_ground_day": round(contrast(colours["day"]["pietra"], colours["day"]["calce"]), 2),
        "text_on_ground_night": round(contrast(colours["night"]["inchiostro"], colours["night"]["calce"]), 2),
        "secondary_on_ground_night": round(contrast(colours["night"]["pietra"], colours["night"]["calce"]), 2),
    }
    measure = 20 * (BODY_MIN + BODY_MAX) / 2 * LINE_HEIGHT
    return {
        "module": {"min_rem": module_lo, "max_rem": module_hi, "css": fluid(module_lo, module_hi),
                   "minute_css": f"calc({fluid(module_lo, module_hi)} / 60)"},
        "means": {k: round(v, 4) for k, v in MEANS.items()},
        "font_sizes": sizes,
        "headings": HEADING_STEP,
        "spacing": spacing,
        "aspect_ratios": [{"label": l, "ratio": f"{num(a)}/{num(b)}" if b != 1 or a == 1 else f"{num(a)}/1",
                           "value": round(a / b, 4), "name": n} for l, a, b, n in FORMS],
        "layout": {"contentSize": f"{num(measure)}rem", "wideSize": f"{num(measure * 3 / 2)}rem"},
        "target_min": "2.75rem",
        "colours": colours,
        "contrast": checks,
    }


def theme_json(t: dict) -> dict:
    """theme.json (schema version 3) of the block theme, built from the tokens."""
    font = "var(--wp--preset--font-family--eb-garamond)"
    faces = []
    ranges = json.loads((THEME / "assets/fonts/eb-garamond/unicode-ranges.json").read_text(encoding="utf-8"))
    for subset in ("latin", "latin-ext"):
        for style in ("normal", "italic"):
            faces.append({"fontFamily": "EB Garamond", "fontStyle": style, "fontWeight": "400 800",
                          "fontDisplay": "swap", "unicodeRange": ranges[subset],
                          "src": [f"file:./assets/fonts/eb-garamond/eb-garamond-{subset}-wght-{style}.woff2"]})
    day = t["colours"]["day"]
    names = COLOUR_NAMES
    heading_elements = {}
    for h, k in HEADING_STEP.items():
        slug = next(s for s, step, _ in STEPS if step == k)
        size = t["font_sizes"][slug]
        el = {"typography": {"fontSize": f"var(--wp--preset--font-size--{slug})",
                             "lineHeight": str(size["line_height"]),
                             "letterSpacing": f"{size['letter_spacing_em']}em" if size["letter_spacing_em"] else "0",
                             "fontWeight": "400"}}
        if h in ("h4", "h5"):
            el["typography"].update({"fontStyle": "italic"})
        if h == "h6":
            el["typography"].update({"textTransform": "uppercase", "letterSpacing": "0.08em"})
        heading_elements[h] = el
    sp = lambda slug: f"var(--wp--preset--spacing--{slug})"
    return {
        "$schema": "https://schemas.wp.org/wp/6.6/theme.json",
        "version": 3,
        "settings": {
            "appearanceTools": False,
            "useRootPaddingAwareAlignments": True,
            "border": {"color": True, "style": True, "width": True, "radius": False},
            "color": {"defaultPalette": False, "defaultGradients": False, "defaultDuotone": False,
                      "custom": False, "customGradient": False, "gradients": [], "duotone": [],
                      "palette": [{"slug": k, "name": names[k], "color": v} for k, v in day.items()]},
            "dimensions": {"defaultAspectRatios": False,
                           "aspectRatios": [{"name": a["label"], "slug": a["label"].replace(":", "-").replace("√", "r"),
                                             "ratio": a["ratio"]} for a in t["aspect_ratios"]]},
            "layout": t["layout"],
            "shadow": {"defaultPresets": False, "presets": []},
            "spacing": {"blockGap": True, "margin": True, "padding": True, "units": ["rem", "em", "%"],
                        "defaultSpacingSizes": False,
                        "spacingSizes": [{"slug": s["slug"], "name": s["name"], "size": s["css"]} for s in t["spacing"]]},
            "typography": {"defaultFontSizes": False, "customFontSize": False, "dropCap": False, "fluid": False,
                           "fontStyle": True, "fontWeight": True, "letterSpacing": False, "lineHeight": False,
                           "textDecoration": False, "textTransform": False,
                           "fontFamilies": [{"fontFamily": "\"EB Garamond\", Garamond, \"Times New Roman\", serif",
                                             "slug": "eb-garamond", "name": "EB Garamond", "fontFace": faces}],
                           "fontSizes": [{"slug": s, "name": v["name"], "size": v["css"]}
                                         for s, v in t["font_sizes"].items()]},
            "custom": {"palladio": {"modulo": t["module"]["css"], "minuto": t["module"]["minute_css"],
                                    "abschnitt": sp("60"), "ziel": t["target_min"]}},
        },
        "styles": {
            "color": {"background": "var(--wp--preset--color--calce)", "text": "var(--wp--preset--color--inchiostro)"},
            "typography": {"fontFamily": font, "fontSize": "var(--wp--preset--font-size--medium)",
                           "lineHeight": str(LINE_HEIGHT), "fontWeight": "400"},
            "spacing": {"blockGap": sp("30"),
                        "padding": {"top": "0", "bottom": "0", "left": sp("40"), "right": sp("40")}},
            "elements": {
                **heading_elements,
                "heading": {"typography": {"fontFamily": font, "fontWeight": "400"},
                            "spacing": {"margin": {"top": sp("50"), "bottom": sp("20")}}},
                "link": {"color": {"text": "var(--wp--preset--color--inchiostro)"},
                         "typography": {"textDecoration": "underline"},
                         ":hover": {"color": {"text": "var(--wp--preset--color--pietra)"}},
                         ":focus": {"outline": {"color": "var(--wp--preset--color--inchiostro)", "offset": "0.2em",
                                                "style": "solid", "width": "1px"}}},
                "button": {"color": {"background": "var(--wp--preset--color--inchiostro)",
                                     "text": "var(--wp--preset--color--calce)"},
                           "border": {"radius": "0", "width": "0"},
                           "typography": {"fontFamily": font, "fontSize": "var(--wp--preset--font-size--medium)"},
                           "spacing": {"padding": {"top": sp("20"), "bottom": sp("20"), "left": sp("40"),
                                                   "right": sp("40")}},
                           ":hover": {"color": {"background": "var(--wp--preset--color--pietra)"}}},
                "caption": {"color": {"text": "var(--wp--preset--color--pietra)"},
                            "typography": {"fontSize": "var(--wp--preset--font-size--small)", "fontStyle": "italic"}},
                "cite": {"typography": {"fontStyle": "italic"}},
            },
            "blocks": {
                "core/separator": {"color": {"text": "var(--wp--preset--color--linea)"},
                                   "border": {"width": "1px 0 0 0", "style": "solid"}},
                "core/quote": {"border": {"left": {"width": "1px", "style": "solid",
                                                   "color": "var(--wp--preset--color--linea)"}},
                               "spacing": {"padding": {"left": sp("40")}},
                               "typography": {"fontStyle": "italic"}},
                "core/pullquote": {"typography": {"fontSize": "var(--wp--preset--font-size--large)",
                                                  "fontStyle": "italic"},
                                   "border": {"width": "0"}},
                "core/site-title": {"typography": {"fontSize": "var(--wp--preset--font-size--large)",
                                                   "letterSpacing": "0.04em", "textTransform": "uppercase"}},
                "core/navigation": {"typography": {"fontSize": "var(--wp--preset--font-size--medium)"},
                                    "spacing": {"blockGap": sp("20")}},
                "core/post-title": {"typography": {"fontSize": "var(--wp--preset--font-size--xx-large)"}},
                "core/post-date": {"color": {"text": "var(--wp--preset--color--pietra)"},
                                   "typography": {"fontSize": "var(--wp--preset--font-size--small)"}},
                "core/image": {"border": {"radius": "0"}},
                "core/code": {"typography": {"fontSize": "var(--wp--preset--font-size--small)"},
                              "border": {"width": "1px", "style": "solid", "color": "var(--wp--preset--color--linea)"},
                              "spacing": {"padding": {"top": sp("20"), "bottom": sp("20"),
                                                      "left": sp("30"), "right": sp("30")}}},
            },
        },
        "templateParts": [{"name": "header", "title": "Kopf", "area": "header"},
                          {"name": "footer", "title": "Fuß", "area": "footer"}],
        "customTemplates": [{"name": "page-mitte", "title": "Seite mit Mitte (ohne Titelzeile)",
                             "postTypes": ["page"]}],
    }


def night_style(t: dict) -> dict:
    night = t["colours"]["night"]
    return {"$schema": "https://schemas.wp.org/wp/6.6/theme.json", "version": 3, "title": "Notte",
            "settings": {"color": {"palette": [{"slug": k, "name": COLOUR_NAMES[k], "color": v}
                                               for k, v in night.items()]}}}


def specimen_html(t: dict, data: dict) -> str:
    """A static preview page built from the same tokens and stylesheet as the theme (not WordPress output)."""
    from html import escape

    theme = theme_json(t)
    fonts = "../../products/wordpress/palladio/assets/fonts/eb-garamond"
    faces = "\n".join(
        f"@font-face {{ font-family: 'EB Garamond'; font-style: {f['fontStyle']}; font-weight: 400 800; "
        f"font-display: swap; unicode-range: {f['unicodeRange']}; "
        f"src: url('{fonts}/{f['src'][0].rsplit('/', 1)[1]}') format('woff2'); }}"
        for f in theme["settings"]["typography"]["fontFamilies"][0]["fontFace"])
    var = []
    for c in theme["settings"]["color"]["palette"]:
        var.append(f"--wp--preset--color--{c['slug']}: {c['color']};")
    for s in theme["settings"]["typography"]["fontSizes"]:
        var.append(f"--wp--preset--font-size--{s['slug']}: {s['size']};")
    for s in theme["settings"]["spacing"]["spacingSizes"]:
        var.append(f"--wp--preset--spacing--{s['slug']}: {s['size']};")
    var.append("--wp--preset--font-family--eb-garamond: " + theme["settings"]["typography"]["fontFamilies"][0]["fontFamily"] + ";")
    for k, v in theme["settings"]["custom"]["palladio"].items():
        var.append(f"--wp--custom--palladio--{k}: {v};")
    night = {c["slug"]: c["color"] for c in night_style(t)["settings"]["color"]["palette"]}
    night_vars = " ".join(f"--wp--preset--color--{k}: {v};" for k, v in night.items())
    heads = []
    for h, k in HEADING_STEP.items():
        el = theme["styles"]["elements"][h]["typography"]
        extra = "".join(f" {css}: {el[key]};" for key, css in (("fontStyle", "font-style"),
                                                               ("textTransform", "text-transform")) if key in el)
        heads.append(f"{h} {{ font-size: {el['fontSize']}; line-height: {el['lineHeight']}; "
                     f"letter-spacing: {el['letterSpacing']}; font-weight: 400;{extra} }}")
    style_css = (THEME / "style.css").read_text(encoding="utf-8").split("*/", 1)[1]
    layout = theme["settings"]["layout"]
    rows = "\n".join(
        f"<tr><td>{escape(x['title'])}</td><td>{escape(', '.join(x['rules']))}</td>"
        f"<td>{escape(x['strength'])}</td><td>{escape(x['web'])}</td></tr>" for x in data["translations"])
    rejected = "\n".join(f"<li><strong>{escape(x['idea'])}</strong> ({escape(', '.join(x['rules']))}). "
                         f"{escape(x['reason'])}</li>" for x in data["rejected"])
    sizes = "\n".join(
        f"<div class='step'><span class='label'>{escape(s['name'])} · {s['min_rem']:.2f}–{s['max_rem']:.2f} rem</span>"
        f"<span style='font-size: var(--wp--preset--font-size--{slug}); line-height: {s['line_height']}; "
        f"letter-spacing: {s['letter_spacing_em']}em'>Proportione</span></div>"
        for slug, s in t["font_sizes"].items())
    forms = "\n".join(
        f"<figure class='form'><div class='box' style='aspect-ratio: {a['ratio']}'></div>"
        f"<figcaption>{escape(a['label'])} · {escape(a['name'])}</figcaption></figure>" for a in t["aspect_ratios"])
    spaces = "\n".join(
        f"<div class='space'><span class='bar' style='width: var(--wp--preset--spacing--{s['slug']})'></span>"
        f"<span class='label'>{escape(s['name'])}</span></div>" for s in t["spacing"])
    swatches = "\n".join(
        f"<div class='swatch'><span class='chip' style='background: {v}'></span>"
        f"<span class='label'>{escape(COLOUR_NAMES[k])}<br>{v}</span></div>" for k, v in t["colours"]["day"].items())
    c = t["contrast"]
    return f"""<title>Palladio Musterseite</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
{faces}
:root {{ {' '.join(var)} color-scheme: light; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ {night_vars} color-scheme: dark; }} }}
:root[data-theme="dark"] {{ {night_vars} color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ margin: 0; background: var(--wp--preset--color--calce); color: var(--wp--preset--color--inchiostro);
  font-family: var(--wp--preset--font-family--eb-garamond); font-size: var(--wp--preset--font-size--medium);
  line-height: {LINE_HEIGHT}; padding-inline: var(--wp--preset--spacing--40); }}
h1, h2, h3, h4, h5, h6 {{ margin: var(--wp--preset--spacing--50) 0 var(--wp--preset--spacing--20); }}
{chr(10).join(heads)}
p {{ margin: 0 0 var(--wp--preset--spacing--30); }}
a {{ color: inherit; }} a:hover {{ color: var(--wp--preset--color--pietra); }}
.c {{ max-width: {layout['contentSize']}; margin-inline: auto; }}
.w {{ max-width: {layout['wideSize']}; margin-inline: auto; }}
header.site {{ display: flex; flex-direction: column; align-items: center; gap: var(--wp--preset--spacing--20);
  padding-block: var(--wp--preset--spacing--50) var(--wp--preset--spacing--40); }}
.site-title {{ font-size: var(--wp--preset--font-size--large); letter-spacing: 0.04em; text-transform: uppercase; margin: 0; }}
nav ul {{ list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; justify-content: center;
  gap: 0 var(--wp--preset--spacing--40); }}
nav a {{ text-decoration: none; }}
section {{ padding-block: var(--wp--preset--spacing--60); }}
.button {{ display: inline-flex; align-items: center; min-height: var(--wp--custom--palladio--ziel);
  background: var(--wp--preset--color--inchiostro); color: var(--wp--preset--color--calce); text-decoration: none;
  padding: var(--wp--preset--spacing--20) var(--wp--preset--spacing--40); }}
.lead {{ font-size: var(--wp--preset--font-size--large); line-height: {t['font_sizes']['large']['line_height']}; }}
.rooms {{ display: grid; grid-template-columns: 1fr 1fr; gap: var(--wp--preset--spacing--50); align-items: center; }}
.rooms img {{ width: 100%; aspect-ratio: 4/3; object-fit: cover; display: block; }}
figcaption, .label {{ color: var(--wp--preset--color--pietra); font-size: var(--wp--preset--font-size--small); }}
figcaption {{ font-style: italic; margin-top: var(--wp--preset--spacing--10); }}
.step {{ display: grid; grid-template-columns: 13rem 1fr; align-items: baseline; gap: var(--wp--preset--spacing--30);
  border-top: 1px solid var(--wp--preset--color--linea); padding-block: var(--wp--preset--spacing--10); overflow: hidden; }}
.forms {{ display: grid; grid-template-columns: repeat(6, 1fr); gap: var(--wp--preset--spacing--30); align-items: end; }}
.form {{ margin: 0; }} .box {{ width: 100%; max-width: 100%; border: 1px solid var(--wp--preset--color--inchiostro); }}
.space {{ display: grid; grid-template-columns: calc(4 * var(--wp--custom--palladio--modulo)) 1fr; align-items: center;
  gap: var(--wp--preset--spacing--30); margin-bottom: var(--wp--preset--spacing--10); }}
.bar {{ display: inline-block; height: 0.6rem; background: var(--wp--preset--color--inchiostro); flex: none; }}
.swatches {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: var(--wp--preset--spacing--30); }}
.chip {{ display: block; aspect-ratio: 1/1; border: 1px solid var(--wp--preset--color--linea); }}
.table-wrap {{ overflow-x: auto; }}
table {{ border-collapse: collapse; width: 100%; font-size: var(--wp--preset--font-size--small); line-height: 1.4; }}
th, td {{ text-align: left; vertical-align: top; padding: var(--wp--preset--spacing--10) var(--wp--preset--spacing--20) var(--wp--preset--spacing--10) 0;
  border-top: 1px solid var(--wp--preset--color--linea); }}
th {{ font-weight: 600; }}
footer.site {{ border-top: 1px solid var(--wp--preset--color--linea); margin-top: var(--wp--preset--spacing--70);
  padding-block: var(--wp--preset--spacing--60); text-align: center; }}
@media (max-width: 40rem) {{ .rooms {{ grid-template-columns: 1fr; }} .forms {{ grid-template-columns: repeat(3, 1fr); }}
  .swatches {{ grid-template-columns: repeat(3, 1fr); }} .step {{ grid-template-columns: 1fr; gap: 0; }} }}
{style_css}
</style>
<header class="site">
  <p class="site-title">Palladio</p>
  <nav aria-label="Hauptnavigation"><ul><li><a href="#mitte">Werk</a></li><li><a href="#regeln">Regeln</a></li>
  <li><a href="#formen">Formen</a></li><li><a href="#farben">Farben</a></li></ul></nav>
</header>
<main>
<section id="mitte" class="w palladio-mitte" style="padding-block: var(--wp--preset--spacing--80)">
  <h6>Musterseite</h6>
  <h1 style="font-size: var(--wp--preset--font-size--huge); line-height: {t['font_sizes']['huge']['line_height']}; letter-spacing: {t['font_sizes']['huge']['letter_spacing_em']}em">Klar, wahr, schön</h1>
  <p class="lead c">Ein WordPress-Theme nach Regeln aus Andrea Palladios <em>Quattro Libri</em>, Venedig 1570. Jede Übertragung ist eine Deutung und nennt ihre Fundstellen.</p>
  <p><a class="button" href="#regeln">Die Regeln ansehen</a></p>
</section>
<section class="w rooms">
  <figure style="margin:0"><img src="../../products/wordpress/palladio/assets/images/rotonda-alzato-4-3.jpg" alt="Villa Almerico, „La Rotonda“, Aufriss aus Palladios Quattro Libri, Buch II"><figcaption>Palladio, I quattro libri, 1570, Buch II, S. 19</figcaption></figure>
  <div><h2>Ein Raum für das Bild, einer für das Wort</h2>
  <p>Zwei gleiche Spalten, rechts wie links. Das Bild steht im Format 4 : 3, einer der sieben Raumformen. Text und Bild nutzen dieselben zwei Breiten wie alle Abschnitte, so dass die Kanten übereinander stehen.</p></div>
</section>
<section id="schrift" class="w">
  <h2 class="c">Schriftgrade aus den drei Mitteln</h2>
  <p class="c">Zwischen 1 und 2 liegen das harmonische Mittel 4/3, das geometrische √2 und das arithmetische 3/2 (I.XXIII). Auf schmalen Bildschirmen wächst die Skala in Schritten von 4/3, auf breiten von 3/2. Je größer der Grad, desto enger Zeilenabstand und Laufweite.</p>
  {sizes}
</section>
<section id="formen" class="w">
  <h2 class="c">Sieben Raumformen, sechs Formate</h2>
  <p class="c">Quadrat, Diagonale des Quadrats, 4 : 3, 3 : 2, 5 : 3 und zwei Quadrate (I.XXI.5). Nichts ist breiter als 2 : 1; der Kreis bleibt Porträts vorbehalten. In einer Reihe haben alle Bilder dasselbe Format (I.XXV.6).</p>
  <div class="forms">{forms}</div>
</section>
<section id="abstaende" class="c">
  <h2>Ein Modul, sechzig Minuten</h2>
  <p>Der Modul ist die Zeilenhöhe des Fließtexts ({t['module']['min_rem']:.3f}–{t['module']['max_rem']:.3f} rem). Die Abstände sind Vielfache, mit Palladios Säulenstellungen 1½, 2, 2¼ und 3 (I.XIII.11, I.XIII.6). Abschnitte stehen 2¼ Moduln auseinander.</p>
  {spaces}
</section>
<section id="farben" class="c">
  <h2>Farben aus dem Druck von 1570</h2>
  <p>Papier und Druckfarbe sind am Scan gemessen und zu einem warmen Weiß aufgehellt (IV.II.12). Schrift auf Grund {c['text_on_ground_day']} : 1, Nebentext {c['secondary_on_ground_day']} : 1.</p>
  <div class="swatches">{swatches}</div>
</section>
<section id="regeln" class="w">
  <h2 class="c">Die Regeln dieses Themes</h2>
  <div class="table-wrap"><table><thead><tr><th>Übertragung</th><th>Fundstellen</th><th>Analogie</th><th>Im Web</th></tr></thead>
  <tbody>{rows}</tbody></table></div>
  <h3 class="c">Verworfen</h3>
  <ul class="c">{rejected}</ul>
</section>
</main>
<footer class="site">
  <p class="palladio-servizi"><a href="#">Impressum</a> · <a href="#">Datenschutz</a></p>
  <p class="palladio-servizi">Gesetzt in EB Garamond. Maße nach Andrea Palladio, <em>I quattro libri dell'architettura</em>, Venedig 1570. Vorschau aus denselben Werten wie das Theme, keine WordPress-Ausgabe.</p>
</footer>
"""


def run(write_theme: bool = True) -> dict:
    data = load()
    problems = validate(data)
    if problems:
        raise ValueError("; ".join(problems))
    t = tokens(data)
    out = ROOT / "output/web"
    out.mkdir(parents=True, exist_ok=True)
    (out / "tokens.json").write_text(json.dumps(t, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    (out / "specimen.html").write_text(specimen_html(t, data), encoding="utf-8")
    if write_theme:
        (THEME / "theme.json").write_text(json.dumps(theme_json(t), ensure_ascii=False, indent="\t") + "\n",
                                          encoding="utf-8")
        (THEME / "styles/notte.json").write_text(json.dumps(night_style(t), ensure_ascii=False, indent="\t") + "\n",
                                                 encoding="utf-8")
    return t


def main() -> None:
    argparse.ArgumentParser(description="Design tokens from the rule catalogue (interpretation layer)").parse_args()
    t = run()
    print(f"module {t['module']['min_rem']}–{t['module']['max_rem']} rem; means {t['means']}")
    for slug, s in t["font_sizes"].items():
        print(f"  {slug:9s} {s['min_rem']:.3f}–{s['max_rem']:.3f} rem  lh {s['line_height']}  ls {s['letter_spacing_em']}em")
    print("colours", t["colours"]["day"])
    print("contrast", t["contrast"])


if __name__ == "__main__":
    main()
