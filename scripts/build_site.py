"""Build the PASE guide as static HTML without rewriting its supplied text."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "content" / "guia-original.txt").read_text(encoding="utf-8")
DOCUMENT_TITLE = "Guía práctica para gestionar la marca del PASE y sus programas con base en la evidencia empírica del marketing"
INTRO_HTML = """<p>Esta guía presenta principios prácticos para orientar las decisiones de marca y publicidad del PASE.</p>
<p>Su propósito es ofrecer criterios claros para construir una marca más reconocible y despertar mayor interés de los estudiantes por los servicios que ofrece.</p>
<h3 class="intro-list-title">Leer esta guía servirá para:</h3>
<ul class="intro-list">
<li><strong>Saber en qué enfocarse al construir la marca del PASE</strong>, evitando invertir tiempo y recursos en aspectos secundarios u opciones que podrían acabar perjudicando el crecimiento de la marca.</li>
<li><strong>Entender qué decisiones aparentemente pequeñas pueden terminar teniendo un gran impacto</strong> en la consistencia y reconocimiento de la marca.</li>
<li><strong>Contar con criterios claros para evaluar decisiones de diseño, comunicación y publicidad</strong>, más allá del gusto personal.</li>
<li><strong>Detectar errores que pueden fragmentar la identidad del PASE</strong> y dificultar que los estudiantes lo reconozcan.</li>
<li><strong>Orientar la publicidad hacia lo que realmente importa: captar atención, comunicar con claridad y generar interés por los servicios del PASE.</strong></li>
</ul>"""

TITLES = [
    "Definir primero qué debe significar el PASE",
    "Construir activos de marca reconocibles",
    "Centrarse en los estudiantes (lo más importante)",
    "Hacer las cosas siempre de la misma manera",
    "Construir un sistema, no una colección de marcas separadas",
    "Hacer que la experiencia refleje la marca",
    "Los elementos más importantes para crear publicidad",
    "Primero claridad, después creatividad",
    "Llegar también a quienes todavía no participan",
    "Repetir para permanecer disponible en la memoria",
    "Mantener dos líneas: construcción de marca y activación",
    "Medir para convertir la publicidad en un sistema de mejora continua",
]

SOURCE_TITLES = {
    3: "Ser distintivo antes que obsesionarse con ser diferente",
    4: "La consistencia debe formar parte del rebranding",
    6: "Diseñar para facilitar el acceso, no únicamente para comunicar",
    7: "La publicidad debe entenderse rápidamente",
    8: "Captar atención, pero conseguir que esa atención llegue a PASE",
    9: "No hablar únicamente con quienes ya conocen PASE",
    10: "Mantener presencia durante el tiempo",
    11: "Diferenciar construcción de marca y activación",
    12: "Medir si la marca está entrando en la memoria, no únicamente si consigue interacciones",
}

# Each image follows the precise example sentence it illustrates. No visible
# captions or replacement prose are introduced into the supplied guide.
EXAMPLE_IMAGES = {}

ALTS = {
    "cocacola.webp": "Botella de contorno de Coca-Cola.",
    "hathaway.webp": "Anuncio de Hathaway con el hombre del parche en el ojo.",
    "mcdonalds.webp": "Rótulo de McDonald's con los arcos dorados.",
    "nike.webp": "Publicidad de Nike con un atleta, Just Do It y el swoosh.",
    "gmail.svg": "Ícono de Gmail.",
    "drive.svg": "Ícono de Google Drive.",
    "maps.svg": "Ícono de Google Maps.",
    "calendar.svg": "Ícono de Google Calendar.",
    "amazon.webp": "Opción de compra en un clic de Amazon.",
    "volkswagen.webp": "Anuncio Think Small de Volkswagen.",
}

# APA 7 references matched to the research and historical examples named in
# each point. The first field is formatted citation text; the second is its URL.
REFERENCES = {
    1: [
        ("Mark, M., & Pearson, C. S. (2001). <em>The hero and the outlaw: Building extraordinary brands through the power of archetypes</em>. McGraw-Hill.", "https://carolspearson.com/books-page/the-hero-and-the-outlaw-building-extraordinary-brands-through-the-power-of-archetypes"),
        ("Romaniuk, J. (2022). <em>Category Entry Points in a business-to-business (B2B) world</em>. Ehrenberg-Bass Institute for Marketing Science.", "https://marketingscience.info/news-and-insights/category-entry-points-in-a-business-to-business-b2b-world"),
    ],
    2: [
        ("Romaniuk, J. (s. f.). <em>Brands of distinction</em>. Ehrenberg-Bass Institute for Marketing Science.", "https://marketingscience.info/news-and-insights/brands-of-distinction"),
        ("Ogilvy, D. (1963). <em>Confessions of an advertising man</em>. Atheneum.", "https://search.worldcat.org/title/244600"),
        ("Ogilvy. (2024). <em>Ogilvy 75: 75 years of iconic campaigns</em>.", "https://www.ogilvy.com/ideas/ogilvy-75-75-years-iconic-campaigns"),
    ],
    3: [
        ("Romaniuk, J., Sharp, B., & Ehrenberg, A. (2007). Evidence concerning the importance of perceived brand differentiation. <em>Australasian Marketing Journal, 15</em>(2), 42–54.", "https://doi.org/10.1016/S1441-3582(07)70042-3"),
    ],
    4: [
        ("Romaniuk, J. (s. f.). <em>The four commandments: Future proofing a brand’s identity</em>. Ehrenberg-Bass Institute for Marketing Science.", "https://marketingscience.info/news-and-insights/the-four-commandments-future-proofing-a-brands-identity"),
        ("Ehrenberg-Bass Institute for Marketing Science. (s. f.). <em>Distinctive asset measurement</em>.", "https://marketingscience.info/learn-with-us/commercial-research/distinctive-asset"),
    ],
    5: [
        ("Ehrenberg-Bass Institute for Marketing Science. (s. f.). <em>Commercial research: Cohesion analysis</em>.", "https://marketingscience.info/learn-with-us/commercial-research"),
    ],
    6: [
        ("Romaniuk, J., & Dunstone, L. (s. f.). <em>Sink or soar? Standing out in the e-commerce world</em>. Ehrenberg-Bass Institute for Marketing Science.", "https://marketingscience.info/news-and-insights/sink-or-soar-standing-out-in-the-e-commerce-world"),
    ],
}

ARCHETYPES = [
    ("El inocente", "Optimismo y sencillez", "Quiere hacer lo correcto y confiar en que las cosas pueden salir bien."),
    ("La persona común", "Cercanía y pertenencia", "Habla sin pretensión y recuerda que nadie tiene que resolverlo todo a solas."),
    ("El héroe", "Esfuerzo y superación", "Invita a afrontar retos y desarrollar capacidades."),
    ("El cuidador", "Apoyo y protección", "Pone el bienestar de las personas en el centro."),
    ("El explorador", "Autonomía y descubrimiento", "Abre caminos para buscar nuevas posibilidades."),
    ("El rebelde", "Cambio y ruptura", "Cuestiona una norma que ya no sirve y propone otra forma de actuar."),
    ("El amante", "Vínculo y aprecio", "Da valor a la conexión personal y al sentido de cercanía."),
    ("El creador", "Imaginación y expresión", "Transforma ideas en algo propio y tangible."),
    ("El bufón", "Alegría y ligereza", "Usa el humor y el juego para aliviar tensión y acercarse."),
    ("El sabio", "Conocimiento y criterio", "Ayuda a comprender mejor antes de tomar una decisión."),
    ("El mago", "Transformación y posibilidad", "Hace visible un cambio que parecía difícil de imaginar."),
    ("El gobernante", "Orden y responsabilidad", "Ofrece estructura, continuidad y confianza en el sistema."),
]

ARCHETYPE_BRANDS = [
    [("Coca-Cola", "cocacola.svg"), ("Dove", "dove.png")],
    [("IKEA", "ikea.svg"), ("Ford", "ford.svg")],
    [("Nike", "nike.svg"), ("Gymshark", "gymshark.png")],
    [("Johnson & Johnson", "johnsonandjohnson.png"), ("TOMS", "toms.png")],
    [("The North Face", "thenorthface.svg"), ("Jeep", "jeep.svg")],
    [("Dr. Martens", "drmartens.png"), ("Red Bull", "redbull.svg")],
    [("Victoria’s Secret", "victoriassecret.png"), ("Godiva", "godiva.png")],
    [("Apple", "apple.svg"), ("Crayola", "crayola.png")],
    [("Duolingo", "duolingo.svg"), ("Doritos", "doritos.png")],
    [("Google", "google.svg"), ("CNN", "cnn.svg")],
    [("Disney", "disney.png"), ("Dyson", "dyson.png")],
    [("BMW", "bmw.svg"), ("Rolex", "rolex.png")],
]

ARCHETYPE_REFERENCES = [
    ("Dopson, E. (2026, 17 de septiembre). <em>12 brand archetypes and how to choose yours</em>. Shopify.", "https://www.shopify.com/blog/brand-archetypes"),
    ("Hower, D. (2026, 10 de mayo). <em>The 12 brand archetypes: A complete guide</em>. Sunup.", "https://studiosunup.com/blog/brand-archetypes-pro-cons/"),
    ("Mark, M., & Pearson, C. S. (2001). <em>The hero and the outlaw: Building extraordinary brands through the power of archetypes</em>. McGraw-Hill.", "https://carolspearson.com/books-page/the-hero-and-the-outlaw-building-extraordinary-brands-through-the-power-of-archetypes"),
    ("Thompson, J. (2026, 17 de agosto). <em>How to create a brand archetype for your business [+ brand examples and 2026 data]</em>. HubSpot.", "https://blog.hubspot.com/marketing/brand-archetypes"),
]


def esc(value: str) -> str:
    return html.escape(value, quote=True)


def brand_text(value: str) -> str:
    """Apply the requested name and Spanish articles without editing the source."""
    value = re.sub(r"\bPASE\b", "PASE", value, flags=re.IGNORECASE)
    for pattern, replacement in [
        (r"\bde PASE\b", "del PASE"),
        (r"\ba PASE\b", "al PASE"),
        (r"\ben PASE\b", "en el PASE"),
        (r"\bcon PASE\b", "con el PASE"),
        (r"\bpara PASE\b", "para el PASE"),
        (r"\bque PASE\b", "que el PASE"),
        (r"\bmarca PASE\b", "marca del PASE"),
        (r"\b(conocen|conozcan|entiendan|recuerden|utilizan|habilitar|facilitar|hacer|es|puede|haría) PASE\b", r"\1 el PASE"),
    ]:
        value = re.sub(pattern, replacement, value)
    value = re.sub(r"^PASE (?=[a-záéíóúñ])", "El PASE ", value)
    value = value.replace("¿PASE ", "¿El PASE ")
    for before, after in [
        ("reconocida como PASE incluso", "reconocida como propia del PASE incluso"),
        ("reconocerse como PASE rápidamente", "reconocerse rápidamente como propia del PASE"),
        ("De manera equivalente, PASE", "De manera equivalente, el PASE"),
        ("parezca PASE", "parezca el PASE"),
        ("dejar de parecer PASE", "dejar de parecer el PASE"),
        ("está construyendo PASE", "está construyendo la marca del PASE"),
        ("necesite PASE", "necesite al PASE"),
        ("pero no PASE", "pero no al PASE"),
        ("En PASE", "En el PASE"),
        ("Para PASE", "Para el PASE"),
        (": PASE no es", ": el PASE no es"),
        ("represente PASE", "represente el PASE"),
        ("acompañar PASE", "acompañar el PASE"),
        ("reconozcan PASE", "reconozcan el PASE"),
    ]:
        value = value.replace(before, after)
    return value


def page(title: str, body: str, prefix: str = "") -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="theme-color" content="#ffffff">
  <title>{esc(title)}</title>
  <link rel="icon" type="image/svg+xml" href="{prefix}favicon.svg">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Lato:wght@300;400;700;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{prefix}assets/css/styles.css">
  <script src="{prefix}assets/js/main.js" defer></script>
</head>
<body>
  <header class="site-header"><div class="page-wrap"><img src="{prefix}logo_armando.svg" alt="Armando" width="100" height="38"></div></header>
  {body}
</body>
</html>"""


def split_content() -> tuple[list[str], str, str, str]:
    markers = []
    for number, title in enumerate(TITLES, 1):
        match = re.search(rf"(?m)^{number}\. {re.escape(SOURCE_TITLES.get(number, title))}\s*$", SOURCE)
        if not match:
            raise ValueError(f"Missing point {number}: {title}")
        markers.append(match)
    checklist_pos = SOURCE.index("III. CHECKLIST PARA TOMAR DECISIONES")
    bodies = []
    for index, marker in enumerate(markers):
        end = markers[index + 1].start() if index < 11 else checklist_pos
        bodies.append(SOURCE[marker.end():end].strip())
    purpose = SOURCE[SOURCE.index("¿Para qué sirve esta guía?") + len("¿Para qué sirve esta guía?"):SOURCE.index("I. PRINCIPIOS PARA GESTIONAR")].strip()
    checklist = SOURCE[checklist_pos + len("III. CHECKLIST PARA TOMAR DECISIONES"):SOURCE.index("IDEA CENTRAL DE LA GUÍA")].strip()
    central = SOURCE[SOURCE.index("IDEA CENTRAL DE LA GUÍA") + len("IDEA CENTRAL DE LA GUÍA"):].strip()
    return bodies, purpose, checklist, central


def image_html(files: list[str]) -> str:
    cls = "source-images source-images--icons" if files[0].endswith(".svg") else "source-images"
    figures = "".join(
        f'<figure><img src="../assets/img/{name}" alt="{esc(ALTS[name])}" loading="lazy"></figure>'
        for name in files
    )
    return f'<div class="{cls}">{figures}</div>'


def render(raw: str, point: int | None = None) -> str:
    output = []
    criterion_open = False
    for original in raw.splitlines():
        line = original.strip()
        if not line or line.startswith("________") or line.startswith("II. PRINCIPIOS PARA LA PUBLICIDAD"):
            continue
        if line == "Criterio operativo" and point is not None:
            output.append(f'<section class="criterion"><h2>{esc(line)}</h2>')
            criterion_open = True
        elif line in {"Aplicado al PASE", "Aplicado a PASE", "Ejemplo", "Comunicación de construcción de marca", "Comunicación de activación", "Identidad", "Comunicación", "Distribución", "Acceso", "Medición"} or line.startswith("Ejemplo:") or line.startswith("Un caso especialmente interesante:"):
            output.append(f'<h2>{esc(brand_text(line))}</h2>')
        elif line in {"Objetivo:", "PASE debería observar al menos cuatro niveles", "Ejemplo de medición de activos distintivos"} or re.match(r"^[1-4]\. (Reconocimiento|Asociación|Disponibilidad mental|Comportamiento)$", line):
            output.append(f'<h3>{esc(brand_text(line))}</h3>')
        elif line.startswith("“"):
            output.append(f'<blockquote>{esc(brand_text(line))}</blockquote>')
        elif line.startswith("•") or line.startswith("□"):
            output.append(f'<p class="list-line">{esc(brand_text(line))}</p>')
        else:
            output.append(f'<p>{esc(brand_text(line))}</p>')
        for trigger, files in EXAMPLE_IMAGES.get(point, []):
            if line.startswith(trigger):
                output.append(image_html(files))
    if criterion_open:
        output.append('</section>')
    return "\n".join(output)


def references_html(number: int) -> str:
    items = "".join(
        f'<li>{citation} <a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(url)}</a></li>'
        for citation, url in REFERENCES[number]
    )
    return f'<section class="references" aria-labelledby="referencias"><h2 id="referencias">Referencias</h2><ol>{items}</ol></section>'


def index_page(purpose: str, checklist: str, central: str) -> str:
    chapters = []
    for first, last, heading in [
        (1, 6, "I. Principios para gestionar el cambio visual en la marca"),
        (7, 12, "II. Principios para la publicidad del PASE"),
    ]:
        links = "".join(
            f'<a class="principle-card" href="puntos/{n:02d}.html"><span class="principle-card__image"><img src="assets/img/principios/{n:02d}.webp" alt="" loading="lazy" width="1200" height="675"></span><span class="principle-card__content"><span class="principle-card__title">{n}. {esc(brand_text(TITLES[n-1]))}</span><span class="principle-card__arrow" aria-hidden="true">↗</span></span></a>'
            for n in range(first, last + 1)
        )
        chapters.append(f'<section class="chapter"><h2>{heading}</h2><nav class="principle-grid" aria-label="{esc(heading)}">{links}</nav></section>')
    highlighted_title = esc(DOCUMENT_TITLE).replace("evidencia empírica", "<mark>evidencia empírica</mark>")
    body = f'''<main class="page-wrap home" id="contenido"><h1>{highlighted_title}</h1><section class="intro"><h2>¿Para qué sirve esta guía?</h2><div class="prose">{INTRO_HTML}</div></section><div class="chapter-list" id="principios">{''.join(chapters)}</div></main>'''
    return page(DOCUMENT_TITLE, body)


def point_page(number: int, body_text: str) -> str:
    title = f"{number}. {brand_text(TITLES[number - 1])}"
    override = ROOT / "content" / f"punto-{number:02d}.html"
    article_html = override.read_text(encoding="utf-8") if override.is_file() else render(body_text, number)
    refs = "" if number in {2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12} else references_html(number)
    body = f'''<main class="page-wrap detail" id="contenido"><a class="back-link" href="../index.html#principios" data-back>← Volver</a><article><h1>{esc(title)}</h1><div class="prose">{article_html}</div>{refs}</article></main>'''
    return page(title, body, "../")


def archetypes_page() -> str:
    cards = []
    for number, (name, essence, description) in enumerate(ARCHETYPES, 1):
        brands = "".join(
            f'<li><span class="brand-logo"><img src="assets/img/marcas/{esc(file)}" alt="" loading="lazy" width="42" height="42"></span><span>{esc(brand)}</span></li>'
            for brand, file in ARCHETYPE_BRANDS[number - 1]
        )
        cards.append(f'<article><span>{number:02d}</span><h2>{esc(name)}</h2><p class="archetype-essence">{esc(essence)}</p><p>{esc(description)}</p><div class="archetype-examples"><h3>Marcas que utilizan este arquetipo</h3><ul>{brands}</ul></div></article>')
    refs = "".join(
        f'<li>{citation} <a href="{esc(url)}" target="_blank" rel="noopener noreferrer">{esc(url)}</a></li>'
        for citation, url in ARCHETYPE_REFERENCES
    )
    references = f'<section class="references archetypes-references" aria-labelledby="referencias-arquetipos"><h2 id="referencias-arquetipos">Referencias</h2><ol>{refs}</ol></section>'
    body = f'''<main class="page-wrap archetypes" id="contenido"><a class="back-link" href="puntos/01.html" data-back>← Volver</a><h1>Los 12 arquetipos de marca</h1><p class="archetypes-intro">La idea de arquetipo proviene de Carl Jung. El sistema de doce aplicado a marcas se desarrolló posteriormente en el trabajo de Carol S. Pearson y Margaret Mark.</p><div class="archetype-list">{''.join(cards)}</div>{references}</main>'''
    return page("Los 12 arquetipos de marca", body)


def main() -> None:
    point_bodies, purpose, checklist, central = split_content()
    (ROOT / "index.html").write_text(index_page(purpose, checklist, central), encoding="utf-8")
    (ROOT / "arquetipos.html").write_text(archetypes_page(), encoding="utf-8")
    points = ROOT / "puntos"
    points.mkdir(exist_ok=True)
    for number, body_text in enumerate(point_bodies, 1):
        (points / f"{number:02d}.html").write_text(point_page(number, body_text), encoding="utf-8")
    print("Generated 14 static pages from the supplied guide, with the requested headline edit.")


if __name__ == "__main__":
    main()
