"""Render the supplied replacement copy for principles 7–12 verbatim."""

from __future__ import annotations

import html
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = (ROOT / "content" / "puntos-07-12.txt").read_text(encoding="utf-8-sig")

HEADINGS = {
    7: {
        "Ejemplo de aplicación: Zarzuela USA", "Aplicado al PASE",
        "Para encontrar esta variable", "También debe ser fácil actuar",
        "1. Problema o deseo urgente: sirve para captar la atención",
        "2. Promesa única: dar una razón para elegir",
        "3. Prueba incuestionable: demostrar que la promesa es cierta",
        "4. Proposición fácil de aceptar: facilitar la decisión",
    },
    8: {"Ejemplo real: Apple", "Aplicado al PASE", "Pregunta clave muy importante"},
    9: {"Aplicado al PASE", "Pregunta por responder"},
    10: {"Aplicado al PASE", "Pregunta por responder"},
    11: {
        "1. Construcción de marca", "2. Respuesta directa", "Aplicado al PASE",
        "Línea de construcción de marca", "Línea de activación", "Preguntas por responder",
    },
    12: {
        "Los tests A/B", "Medir según el objetivo", "Si es activación",
        "Si es construcción de marca", "Preguntas por responder",
    },
}

FIGURES = {
    7: (
        "Problema urgente + Promesa única + Prueba incuestionable + Proposición fácil de aceptar = Persuasion",
        "07.webp", "Cuatro elementos que confluyen en una composición violeta, imagen conceptual de la ecuación de persuasión.",
    ),
    8: (
        "“1,000 canciones en tu bolsillo.”",
        "ipod-primera-generacion.webp", "Fotografía de un iPod de primera generación con su rueda mecánica.",
    ),
    9: (
        "si queremos aumentar la participación, necesitamos incorporar estudiantes que todavía no participan.",
        "09.webp", "Una invitación que llega a estudiantes distribuidos por un espacio universitario.",
    ),
    10: (
        "repetir ayuda a recordar, pero la memoria necesita mantenerse con el tiempo. Una sola exposición suele ser una base muy débil para construir memoria.",
        "10.webp", "Motivo visual violeta repetido a lo largo de una galería.",
    ),
    11: (
        "A diferencia de la publicidad enfocada principalmente en construir la marca a largo plazo, aquí el objetivo es provocar una respuesta inmediata y medible.",
        "11.webp", "Dos líneas violetas complementarias recorren un espacio blanco.",
    ),
    12: (
        "Después se compara cuál consigue mejor el resultado previamente definido.",
        "12.webp", "Dos piezas visuales similares se presentan lado a lado para su comparación.",
    ),
}

def esc(value: str) -> str:
    return html.escape(value, quote=True)


def render_lines(number: int, lines: list[str]) -> str:
    out: list[str] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if not line:
            i += 1
            continue
        if line == "Referencias":
            out.append('<section class="references" aria-labelledby="referencias"><h2 id="referencias">Referencias</h2><ol>')
            for reference in lines[i + 1:]:
                match = re.fullmatch(r"\d+\.\s+(.+)", reference.strip())
                if not match:
                    raise ValueError(f"Unexpected reference in point {number}: {reference}")
                out.append(f"<li>{esc(match.group(1))}</li>")
            out.append("</ol></section>")
            break
        if number == 7 and line == "Objeción\tRespuesta":
            rows = [row.split("\t", 1) for row in lines[i + 1:i + 5]]
            assert len(rows) == 4 and all(len(row) == 2 for row in rows)
            body = "".join(f"<tr><td>{esc(left)}</td><td>{esc(right)}</td></tr>" for left, right in rows)
            out.append(f'<div class="editorial-table-wrap"><table class="editorial-table"><thead><tr><th>Objeción</th><th>Respuesta</th></tr></thead><tbody>{body}</tbody></table></div>')
            i += 5
            continue
        heading = re.sub(r"\s+", " ", line)
        if heading in HEADINGS[number]:
            level = "h3" if heading in {"Para encontrar esta variable", "También debe ser fácil actuar", "Si es activación", "Si es construcción de marca"} else "h2"
            out.append(f"<{level}>{esc(heading)}</{level}>")
        elif line.startswith("•"):
            out.append(f'<p class="list-line">{esc(line)}</p>')
        elif line.startswith("“") and line.endswith("”"):
            out.append(f"<blockquote>{esc(line)}</blockquote>")
        else:
            out.append(f"<p>{esc(line)}</p>")
        trigger, image, alt = FIGURES[number]
        if line == trigger:
            image_dir = "" if number == 8 else "articulos/"
            image_class = "source-images--documentary" if number == 8 else "source-images--concept"
            size = 'width="1200" height="900"' if number == 8 else 'width="1200" height="675"'
            out.append(
                f'<div class="source-images {image_class}">'
                f'<figure><img src="../assets/img/{image_dir}{image}" alt="{esc(alt)}" '
                f'loading="lazy" {size}></figure></div>'
            )
        i += 1
    return "\n".join(out)


def main() -> None:
    sections = [part.strip() for part in re.split(r"(?m)^← Volver\s*$", SOURCE) if part.strip()]
    if len(sections) != 6:
        raise ValueError(f"Expected six articles, found {len(sections)}")
    for number, section in enumerate(sections, 7):
        lines = [line.strip() for line in section.splitlines() if line.strip()]
        if not lines[0].startswith(f"{number}. "):
            raise ValueError(f"Unexpected title for point {number}: {lines[0]}")
        body = render_lines(number, lines[1:])
        (ROOT / "content" / f"punto-{number:02d}.html").write_text(body, encoding="utf-8")
    print("Generated replacement article fragments for points 7–12.")


if __name__ == "__main__":
    main()
