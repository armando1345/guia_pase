# Guía PASE

Sitio estático editorial con los 12 principios de marca y publicidad del documento compartido, una página sobre los 12 arquetipos de marca y ejemplos visuales locales. La copia del documento original se conserva intacta. Al generar el sitio se aplica el titular solicitado y se normalizan «PASE» y sus artículos en español. Cada principio incorpora una sección de referencias en formato APA; la página de arquetipos es contenido redactado para este sitio.

## Abrir y publicar cuando corresponda

- Abrir `index.html` en un navegador para una revisión rápida.
- Para una vista local con rutas HTTP: ejecutar `python -m http.server 8765` en esta carpeta y abrir `http://127.0.0.1:8765/`.
- Al subir a GitHub Pages, conservar esta estructura y publicar desde la raíz. Todos los enlaces internos son relativos y no se requiere proceso de compilación.
- Lato se carga mediante Google Fonts. El resto de imágenes, CSS y JS funciona desde archivos locales.

## Estructura

- `index.html`: título e índice de tarjetas, propósito, idea central y checklist desplegable al final.
- `puntos/01.html` a `puntos/12.html`: desarrollo de cada principio y sus referencias.
- `arquetipos.html`: los doce arquetipos aplicados a marcas.
- `assets/css/`, `assets/js/`, `assets/img/`: estilos, navegación de regreso y piezas visuales, incluidas las doce portadas generadas con Magnific.
- `content/guia-original.txt`: copia literal del texto entregado. `scripts/build_site.py` genera las páginas HTML y aplica las correcciones editoriales sin modificar el original.
- `CREDITOS.md`: procedencia y atribución de las imágenes. `content/creditos-imagenes.json` conserva los datos de origen.

No se ha publicado ni desplegado el sitio.
