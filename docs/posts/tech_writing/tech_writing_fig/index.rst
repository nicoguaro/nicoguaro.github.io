.. title: Technical writing: Using Figures
.. slug: tech_writing_fig
.. date: 2021-11-01 12:53:40 UTC-05:00
.. tags: writing, research, typography, libreoffice, latex, inkscape, figures
.. category: Writing
.. link:
.. description: Tips on figures in technical writing.
.. type: text
.. has_math: yes

In a `previous post <../tech_writing>`_ I mentioned some general aspects of
technical writing. In this one, I would like to talk about including
figures in technical documents.

This post is about some details on the planning of figures for technical
documents. The main document in mind is a technical article (research paper,
techincal report). Although, it also applies to presentations or posters.

Graphic formats
===============

First, I should mention that there are two main type of graphics, namely:

- vector graphics; and

- raster graphics.

They serve different purposes and we should use them accordingly. For example,
for diagrams or schematics is better to use vector formats, in general. On
the other hand, raster formats are better suited for images such as photographs
or illustrations.

Vector graphics
---------------

A `vector image <http://en.wikipedia.org/wiki/Vector_graphics>`__
is an image that is made up of geometric entities. In this case, the
stored information is not point-to-point but *the construction* of
the shapes that constitute it. For this reason, these images don't
*pixelate* because the information you have is how to build it.
This type of images is the best options for schematics and diagrams,
since the only stored information are the strokes and text added to
them. The *de facto* standard for this type of images is PDF —it is the one
I usually include in my documents \\(\\LaTeX\\). Although PDF is the
*standard*, the preferred format is `SVG (Scalable Vector
Graphics) <http://en.wikipedia.org/wiki/Scalable_Vector_Graphics>`__
which is a standard across the internet and most *modern* browsers
let you render them.

Raster graphics
---------------

A `raster image <http://en.wikipedia.org/wiki/Raster_graphics>`__ is an image
which is represented by an array (or rectangular grid) of pixels. In other
words, the color information that there are in each point of the image. The
most popular formats store the compressed information. For high contrast
graphics (such as schematics or diagrams) the best format is PNG. If you have
an animation, GIF would be preferable. And in the case of photographs it is
better to use JPG.

Summary for formats
-------------------

Summarizing, we should use JPG images (only) for photographs and SVG for
schematics/diagrams. Another attribute that may be useful is the management
of layers. Having several layers gives you the option of stacking different
type of information separately. For example, you can have the background,
the image, and the annotations in different layers. This way you can modify
only the part of the figure that concerns you. You can automate the translation
of the annotations this way without much problem. Formats such as SVG let you
have several layers. In the case of raster formats we have the
option to use TIFF.

Regarding software to generate/edit this type of images I must say that there
are a large number of programs that allow exporting to these formats:
Python/Matplotlib, Matlab, Inkscape, Adobe Illustrator, GIMP, Photoshop,
LibreOffice. If the graph is generated from a calculation or a data series I
use Matplotlib. If, instead, we want to make a schematic my tool of choice
is `Inkscape <http://www.inkscape.org/>`__. This program is intended to be a
free alternative to programs like Adobe Illustrator —and it does achieve it.
Obviously, you could use Illustrator or Corel Draw for this task. If the only
use would be to make technical schematics, I think it would be a waste.


Designing figures for documents
===============================

I suggest starting from the nominal size of the figure in the document. For
most of our documents the figures will remain digital and this
might seem counterintuitive. Nevertheless, I find this approach much easier.
One of the reasons is that we still embed our figure in a document with a
nominal size. For an article is common to use letter size that is 8.5 in × 11 in
(215.9 mm × 279.4 mm). Another common size is A4 that is 210 m × 297 mm 
(8.27 in × 11.7 in).

The sizes are the following

- 1 column width: 90 mm (3.5 in)
- 1.5 columns width: 140 mm (5.5 in)
- 2 columns width: 190 mm (6.5 in)



Mi consejo es empezar con el tamaño nominal que tendría la figura en el paper

Y devolverse

Y no al revés

Luego es mucho más teso saber qué tamaño de texto usar

O grosor de línea

En ambos casos utilice imágenes de una resolución mínima de 150 ppp
(puntos por pulgada), para esto tenga en cuenta el tamaño que la imagen
ocupará en el póster. Por ejemplo, tomemos una imagen de 6 × 3 in2. Esta
imagen tendría un tamaño (a 150 ppp) de 900 × 450 pixeles.
El siguiente bloque de código de Python crea una figura de 6 × 3 in2, reali-
za el gráfico de la función f(x) = sin(x2) y lo guarda en una figura de
900 × 450 pixeles.

.. code:: python

   import numpy as np
   import matplotlib.pyplot as plt
   x = np.linspace(0, 2*np.pi, 500)
   y = np.sin(x**2)
   plt.figure(figsize=(6, 3))
   plt.plot(x, y)
   plt.savefig("figura_ejemplo.png", dpi=150)

Mi consejo es eempezar con el tamaño nominal que tendría la figura en el paper

Y devolverse

Y no al revés

Luego es mucho más teso saber qué tamaño de texto usar

O grosor de línea

Pero no existe tal cosa como "resolución"

Eso ya no se imprime

Uno necesita es una cantidad de pixeles

Yo tengo una pantalla de 22 pulgadas acá

Y eso "apenas" tiene 1920 pixeles

Pero por eso, DPI no es algo real en imágenes digitales

Lo que cuenta es el número de pixeles

Porque DPI es el número de pixeles dividido por el tamaño nominal. Y el tamaño nominal es un número en los metadatos

No información "real"

Serían como 6 pulgadas

Entonces 6 in × 300 dpi = 1800 pixeles

Entonces, esa imagen no necesita tener más de 1800 pixeles de ancho




Hay varios objetivos en mi enfoque

Los editores de una revista te van a pedir una "resolución", usualmente 300 dpi

Y si tu imagen tiene un tamaño nominal muy grande pues va a quedar gigante

Si el tamaño nominal es el tamaño que tenés en mente para el paper pues queda melo

Lo mismo con coautores

Muchos no saben todo esto y te van a pelear

Y pues, tener 5 imágenes de 50 MB es un dolor de cabeza

Y eso es maluco. Porque una revista no va a meterlas tal cual sino que te las comprimen y ponen la versión online con más "resolución"

La otra razón, que me parece más importane es que te permite diseñar figuras de forma más efectiva

It depends on the document:

- Articles;

- Posters; or

- Slides




References
----------

1. Elsevier. (n.d.). "Artwork Overview." Retrieved November 1, 2021,
   from https://www.elsevier.com/authors/policies-and-guidelines/artwork-and-media-instructions/artwork-overview

2. Elsevier. (n.d.). "Artwork sizing." Retrieved November 1, 2021,
   from https://www.elsevier.com/authors/policies-and-guidelines/artwork-and-media-instructions/artwork-sizing

3. Journal of applied physics (n.d.). "Preparing Your Manuscript: Authors
   Instruction." Retrieved November 1, 2021, from https://aip.scitation.org/jap/authors/manuscript


