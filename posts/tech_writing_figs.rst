.. title: Technical writing: Using Figures
.. slug: tech_writing_fig
.. date: 2020-05-28 15:53:40 UTC-05:00
.. tags: writing, research, typography, libreoffice, latex, inkscape, figures
.. category: Writing
.. link:
.. description: Tips on math in technical writing.
.. type: text
.. status: draft

In a `previous post <../tech_writing>`_ I mentioned some general aspects of
technical writing. In this one, I would like to talk about including
figures in technical documents.

First, I should mention that there are two main type of graphics, namely:

- vector graphics; and

- raster graphics.

Recapitulando, deberíamos usar imágenes JPG para fotografías y SVG
para esquemas/diagramas. Otro atributo que puede ser de utilidad es el
manejo de capas, SVG permite esto.... y de formatos ráster tenemos la
opción de usar TIFF.

En cuanto a software para generar/editar este tipo de imágenes debo
decir que existen gran cantidad de programas que permiten exportar a
estos formatos: Python/Matplotlib, Matlab, Inkscape, Adobe
Illustrator, GIMP, Photoshop, LibreOffice. Si el gráfico es generado a
partir de un cálculo o de una serie de datos yo uso Matplotlib. Si en
cambio, queremos hacer un esquema o —como suelo decir— un muñeco mi
herramienta favorita es `Inkscape. <http://www.inkscape.org/>`__ Este
programa pretende ser una alternativa libre a programas como Adobe
Illustrator —y sí que lo consigue. Obviamente, se podría usar
Illustrator o Corel Draw para esta tarea. Si el único uso sería hacer
esquemas técnico, creo que sería un desperdicio.


Vector graphics
---------------

`Imagen vectorial <http://en.wikipedia.org/wiki/Vector_graphics>`__:
es una imagen que está formada por entidades geométricas. En esta no
se almacena la información punto a punto sino *la construcción* de
las formas que la constituyen. Por esta razón, estas imágenes no se
*pixelan* pues la información que se tiene es de cómo construirla.
Este tipo de imágenes es la mejor opciones para esquemas y diagramas,
pues sólo se almacena la información de los trazos y texto que se
añadan en ellas (ver Figura 1). El estándar *de facto* para este tipo
de imágenes es PDF —es el que suelo para incluir en mis documentos
\\(\\LaTeX\\), aunque existe forma de embeber SVG en \\(\\LaTeX\\)
pero es algo que aún no exploro—. A pesar de que PDF sea el
*estándar*, el formato a preferir es `SVG (Scalable Vector
Graphics) <http://en.wikipedia.org/wiki/Scalable_Vector_Graphics>`__
que es un estándar a través de la internet y la mayoría de
navegadores *modernos* permiten visualizar.

Raster graphics
---------------

`Imagen de mapa de
bits <http://en.wikipedia.org/wiki/Raster_graphics>`__: es una imagen
que está representada por un arreglo (o rejilla rectangular) de
pixeles. Dicho de otro modo, se almacena la información de color que
hay en cada punto de la imagen. Los formatos más populares almacenan
la información comprimida. Para gráficos con alto contraste (como
esquemas o diagramas) el mejor formato es PNG. Si se tiene una
animación, GIF sería preferible. Y para el caso de fotografías es
mejor utilizar JPG.

Designing figures for documents
-------------------------------

It depends on the document:

- Articles;

- Posters; or

- Slides


References
----------

1. "Artwork Overview."
   https://www.elsevier.com/authors/author-schemas/artwork-and-media-instructions/artwork-overview.
   Accessed 9 Aug. 2020.