# Guía PASE

Sitio estático editorial con los 12 principios de marca y publicidad de los documentos compartidos, una página sobre los 12 arquetipos de marca y ejemplos visuales locales. Las copias de los textos entregados se conservan intactas. Al generar el sitio se aplican el titular y la introducción solicitados, así como las versiones más recientes de los doce principios. Cada principio incorpora una sección de referencias; la página de arquetipos es contenido redactado para este sitio.

## Abrir y publicar cuando corresponda

- Abrir `index.html` en un navegador para una revisión rápida.
- Para una vista local con rutas HTTP: ejecutar `python -m http.server 8765` en esta carpeta y abrir `http://127.0.0.1:8765/`.
- Al subir a GitHub Pages, conservar esta estructura y publicar desde la raíz. Todos los enlaces internos son relativos y no se requiere proceso de compilación.
- Lato se carga mediante Google Fonts. El resto de imágenes, CSS y JS funciona desde archivos locales.

## Estructura

- `index.html`: título, propósito e índice de tarjetas.
- `puntos/01.html` a `puntos/12.html`: desarrollo de cada principio y sus referencias.
- `arquetipos.html`: los doce arquetipos, con ejemplos visuales de marcas y referencias al final.
- `assets/css/`, `assets/js/`, `assets/img/`: estilos, navegación de regreso y piezas visuales. Las portadas 7 a 12 se generaron con Magnific siguiendo la dirección visual de las primeras seis.
- `content/guia-original.txt`: copia literal del primer texto entregado. `content/puntos-02-06.txt` conserva la versión más reciente de los puntos 2 a 6; `scripts/build_points_02_06.py` genera sus fragmentos HTML. `content/puntos-03-06.txt` guarda la versión anterior de ese grupo. `content/puntos-07-12.txt` y `scripts/build_points_07_12.py` hacen lo mismo para los puntos 7 a 12. `content/punto-01.html` a `content/punto-12.html` son los fragmentos que utiliza `scripts/build_site.py` para generar las páginas finales.
- `favicon.svg`: icono del sitio, incluido en las catorce páginas.
- `CREDITOS.md`: procedencia y atribución de las imágenes. `content/creditos-imagenes.json` y `content/creditos-logos-arquetipos.json` conservan los datos de origen.

No se ha publicado ni desplegado el sitio.
