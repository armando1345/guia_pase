"""Render the user's revised points 2–6 without rewriting their wording."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "content" / "puntos-02-06.txt"

HEADINGS = {
    2: {
        "Aplicado al PASE",
        "Ejemplo de aplicación: Coca-Cola",
        "Otro ejemplo histórico interesante: Hathaway",
        "Preguntas clave",
    },
    3: {
        "La evidencia",
        "Uno de los ejemplos más increíbles de la historia que muestran la importancia de la orientación al mercado: “Got Milk?”",
        "Aplicado al PASE",
        "Preguntas por responder",
    },
    4: {
        "Crear un manual de marca es fundamental",
        "Aplicado al PASE",
        "Ejemplo real: McDonald's",
        "La importancia práctica del manual de marca",
        "Preguntas por responder",
    },
    5: {"Aplicado al PASE", "Ejemplo", "Preguntas por responder"},
    6: {
        "No existe una única “buena experiencia”",
        "Un restaurante cuyos clientes están satisfechos por ser “maltratados”: Dick's Last Resort",
        "Aplicado al PASE",
        "Preguntas por responder",
    },
}

SUBHEADINGS = {6: {"Cercano", "Confiable", "Juvenil"}}

IMAGES = {
    2: {
        "La botella de Coca-Cola tiene una forma única": '<div class="source-images source-images--silhouette"><figure><img src="../assets/img/cocacola-silueta.png" alt="Silueta blanca de una botella de Coca-Cola sobre un fondo rojo" loading="lazy" width="1600" height="1270"></figure></div>',
        "El logo de Coca-Cola es un activo distintivo": '<div class="source-images source-images--scripts"><figure><img src="../assets/img/cocacola-escrituras.png" alt="Cuatro latas rojas de Coca-Cola con el nombre de la marca en distintos sistemas de escritura" loading="lazy" width="739" height="415"></figure></div>',
        "En 1951, David Ogilvy colocó un parche": '<div class="source-images"><figure><img src="../assets/img/hathaway.webp" alt="Anuncio de Hathaway con el hombre del parche en el ojo" loading="lazy"></figure></div>',
    },
    3: {
        "Los resultados fueron impresionantes.": '<div class="source-images source-images--got-milk"><figure><img src="../assets/img/got-milk.png" alt="Pieza de Got Milk? con el titular negro y una salpicadura de leche sobre fondo blanco" loading="lazy" width="447" height="447"></figure></div>',
    },
    4: {
        "Esas ilustraciones representan elementos": '<div class="source-images"><figure><img src="../assets/img/mcdonalds-sistema.webp" alt="Páginas del sistema de identidad visual de McDonald’s con arcos, colores, tipografía, ilustraciones y fotografías" loading="lazy" width="1600" height="1067"></figure></div>',
    },
    5: {
        "Google utiliza identidades diferentes": '<div class="source-images source-images--icons"><figure><img src="../assets/img/gmail.svg" alt="Ícono de Google Gmail" loading="lazy"></figure><figure><img src="../assets/img/drive.svg" alt="Ícono de Google Drive" loading="lazy"></figure><figure><img src="../assets/img/maps.svg" alt="Ícono de Google Maps" loading="lazy"></figure><figure><img src="../assets/img/calendar.svg" alt="Ícono de Google Calendar" loading="lazy"></figure></div>',
    },
    6: {
        "En Dick's Last Resort, es parte de la experiencia": '<div class="source-images"><figure><img src="../assets/img/dicks-experiencia.webp" alt="Gráfico oficial de Dick’s Last Resort que presenta su experiencia irreverente" loading="lazy" width="1366" height="771"></figure></div>',
    },
}


def render_lines(number: int, lines: list[str]) -> str:
    output: list[str] = []
    index = 0
    while index < len(lines):
        line = lines[index]
        safe = html.escape(line, quote=True)

        if line == "Referencias":
            output.append('<section class="references" aria-labelledby="referencias"><h2 id="referencias">Referencias</h2><ol>')
            for reference in lines[index + 1 :]:
                match = re.fullmatch(r"\d+\.\s+(.+)", reference)
                if not match:
                    raise ValueError(f"Unexpected reference in point {number}: {reference}")
                citation = html.escape(match.group(1), quote=True)
                citation = re.sub(r"https?://\S+", lambda m: f'<a href="{m.group(0)}" target="_blank" rel="noopener noreferrer">{m.group(0)}</a>', citation)
                output.append(f"<li>{citation}</li>")
            output.append("</ol></section>")
            break

        if line in HEADINGS[number]:
            output.append(f"<h2>{safe}</h2>")
        elif line in SUBHEADINGS.get(number, set()):
            output.append(f"<h3>{safe}</h3>")
        elif line.startswith("•"):
            bullets = []
            while index < len(lines) and lines[index].startswith("•"):
                bullets.append(f"<li>{html.escape(lines[index][1:].strip(), quote=True)}</li>")
                index += 1
            output.append("<ul>" + "".join(bullets) + "</ul>")
            continue
        elif line.startswith("“") and line.endswith("”"):
            output.append(f"<blockquote>{safe}</blockquote>")
        elif number == 2 and line.startswith("Prevalencia:"):
            output.append(f"<p><strong>Prevalencia:</strong>{html.escape(line[len('Prevalencia:'):], quote=True)}</p>")
        elif number == 2 and line.startswith("Unicidad:"):
            output.append(f"<p><strong>Unicidad:</strong>{html.escape(line[len('Unicidad:'):], quote=True)}</p>")
        elif number == 2 and index == 0:
            output.append(f"<p><strong>{safe}</strong></p>")
        else:
            output.append(f"<p>{safe}</p>")

        for trigger, figure in IMAGES.get(number, {}).items():
            if line.startswith(trigger):
                output.append(figure)
        index += 1

    return "\n".join(output) + "\n"


def main() -> None:
    text = SOURCE.read_text(encoding="utf-8-sig")
    sections = [part.strip() for part in re.split(r"(?m)^← Volver\s*$", text) if part.strip()]
    if len(sections) != 5:
        raise ValueError(f"Expected five articles, found {len(sections)}")
    for number, section in enumerate(sections, 2):
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        if not lines[0].startswith(f"{number}. "):
            raise ValueError(f"Unexpected title for point {number}: {lines[0]}")
        (ROOT / "content" / f"punto-{number:02d}.html").write_text(
            render_lines(number, lines[1:]), encoding="utf-8"
        )
    print("Updated article fragments 2–6 from the user's revised text.")


if __name__ == "__main__":
    main()
