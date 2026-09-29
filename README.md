# Guía PASE

Sitio estático editorial con los 12 principios de marca y publicidad del documento compartido, una página sobre los 12 arquetipos de marca y ejemplos visuales locales. La copia del documento original se conserva intacta. Al generar el sitio se aplican el titular y la introducción solicitados, así como los nuevos textos de los principios 1 al 6; se normalizan «PASE» y sus artículos en los demás principios. Cada principio incorpora una sección de referencias; la página de arquetipos es contenido redactado para este sitio.

## Abrir y publicar cuando corresponda

- Abrir `index.html` en un navegador para una revisión rápida.
- Para una vista local con rutas HTTP: ejecutar `python -m http.server 8765` en esta carpeta y abrir `http://127.0.0.1:8765/`.
- Al subir a GitHub Pages, conservar esta estructura y publicar desde la raíz. Todos los enlaces internos son relativos y no se requiere proceso de compilación.
- Lato se carga mediante Google Fonts. El resto de imágenes, CSS y JS funciona desde archivos locales.

## Estructura

- `index.html`: título, propósito e índice de tarjetas.
- `puntos/01.html` a `puntos/12.html`: desarrollo de cada principio y sus referencias.
- `arquetipos.html`: los doce arquetipos, con ejemplos visuales de marcas y referencias al final.
- `assets/css/`, `assets/js/`, `assets/img/`: estilos, navegación de regreso y piezas visuales, incluidas las doce portadas generadas con Magnific.
- `content/guia-original.txt`: copia literal del primer texto entregado. `content/punto-01.html` a `content/punto-06.html` conservan las versiones más recientes de esos principios; `content/puntos-03-06.txt` conserva el texto nuevo de los puntos 3 a 6. `scripts/build_site.py` genera las páginas HTML sin modificar el original.
- `favicon.svg`: icono del sitio, incluido en las catorce páginas.
- `CREDITOS.md`: procedencia y atribución de las imágenes. `content/creditos-imagenes.json` y `content/creditos-logos-arquetipos.json` conservan los datos de origen.

No se ha publicado ni desplegado el sitio.
