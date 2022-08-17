.. title: Escritura técnica: usando figuras
.. slug: tech_writing_figs
.. date: 2021-11-03 12:53:40 UTC-05:00
.. tags: escritura, investigación, tipografía, libreoffice, latex, inkscape, figuras
.. category: Writing
.. link:
.. description: Consejos para escritura técnica con figuras.
.. type: text
.. has_math: yes

En una `publicación anterior <../tech_writing>`_ mencioné algunos aspectos
generales de la escritura técnica. En este me gustaría hablar sobre la
inclusión de figuras en documentos técnicos.

Formatos de gráficos
====================

Primero, debo mencionar que hay dos tipos principales de gráficos, a saber:

- gráficos vectoriales; y

- gráficos de mapa de bits.

Sirven para diferentes propósitos y deberíamos usarlos teniendo esto en cuenta.
Por ejemplo, para diagramas o esquemas es mejor utilizar formatos vectoriales,
en general. Por otro lado, los formatos ráster son más adecuados para imágenes
como fotografías o ilustraciones.

Gráficos vectoriales
--------------------

Una `imagen vectorial <http://en.wikipedia.org/wiki/Vector_graphics>`__ es una
imagen que está conformada por entidades geométricas. En este caso, la 
información almacenada no es punto a punto sino *la construcción* de las formas
que la conforman. Por esta razón, estas imágenes no se *pixelan* ya que que la
información con la que se cuenta es de cómo se construye. Este tipo de imágenes
es la mejor opción para esquemas y diagramas, ya que sólo se almacenaría la
información de trazos y texto. El estándar *de facto* para este tipo de imágenes
es PDF—este es el tipo que uso en mis documentos de \\(\\LaTeX\\)—. Aunque PDF
es el *estándar*, mi formato preferido es `SVG (Scalable Vector Graphics)
<http://en.wikipedia.org/wiki/Scalable_Vector_Graphics>`__ que es un estándar
a través de internet y que se puede renderizar en la mayoría de navegadores
*modernos*.

Gráficos ráster
---------------

Una `imagen ráster <http://en.wikipedia.org/wiki/Raster_graphics>`__ es una
imagen que está representada por un arreglo (o rejilla rectangular) de píxeles.
En otras palabras, la información del color que hay en cada uno de los puntos
de la imagen. Los formatos más populares almacenan la información de forma
comprimida. Para gráficos de alto contraste (como esquemas o diagramas) el mejor
formato es PNG. Si se tienen animaciones, sería preferible usar GIF. Y en el
caso de fotografías es mejor usar JPG.

Resumen para los formatos
-------------------------

Resumiendo, deberíamos usar imágenes JPG (solo) para fotografías y SVG para
esquemas/diagramas. Otro atributo que puede resultar útil es la gestión de
capas. Tener varias capas brinda la opción de apilar diferentes tipos de
información por separado. Por ejemplo, puede tener el fondo, la imagen y las
anotaciones en diferentes capas. De esta forma se puede modificar sólo la parte
de la figura de interés. Se puede automatizar la traducción de las anotaciones
de esta manera sin muchos problemas. Los formatos como SVG permiten tener
varias capas. En el caso de los formatos ráster, tenemos la opción de utilizar
TIFF.

En cuanto al software para generar/editar este tipo de imágenes debo decir
que existe una gran cantidad de programas que permiten exportar a estos
formatos: Python/Matplotlib, Matlab, Inkscape, Adobe Illustrator, GIMP,
Photoshop, LibreOffice. Si el gráfico se genera a partir de un cálculo o una
serie de datos, uso Matplotlib. Si, en cambio, queremos hacer un esquema, mi
herramienta de elección es `Inkscape <http://www.inkscape.org/>`__. Este programa
está destinado a ser una alternativa gratuita a programas como Adobe
Illustrator, y lo logra. Obviamente, se puede usar Illustrator o Corel Draw para
esto. Si el único uso es hacer esquemas técnicos, creo que sería un desperdicio.


Diseñando figuras para documentos
=================================

Mi sugerencia es partir del tamaño nominal de la figura del documento. Para la
mayoría de nuestros documentos, las cifras seguirán siendo digitales y esto
puede parecer contradictorio. Sin embargo, encuentro este enfoque mucho más
fácil. Una de las razones es que todavía incrustamos nuestra figura en un
documento con un tamaño nominal. Además, a la hora de pensar en el tamaño de
la fuente es habitual que tengamos como referencia el texto impreso. Además de
eso, debemos considerar que el ojo humano tiene un límite de resolución, por lo
que no podemos simplemente reducir nuestras figuras.

Además, no existe la resolución de una imagen digital. La resolución se refiere
a una densidad de píxeles por unidad de longitud. Esto tiene sentido al imprimir
imágenes, pero no en el caso digital. Sin embargo, las figuras tienen un tamaño
nominal y, por lo tanto, una resolución nominal. Es decir, el número de píxeles
en una dirección dividido por su tamaño nominal. Es una buena idea considerar
una resolución mínima de 150 ppp (puntos por pulgada). Por ejemplo, una imagen
de 6 × 3 pulgadas. Esta imagen tendría un tamaño de (a 150 ppp) de
900 px × 450 px.

El siguiente código de Python crea una figura de tamaño 6 in × 3 in, y grafica
la función \\(f(x) = \\sin(x^2)\\) y la guarda como una imagen de tamaño
900 in × 450 in.

.. code:: python

   import numpy as np
   import matplotlib.pyplot as plt
   x = np.linspace(0, 2*np.pi, 500, linewidth=2)
   y = np.sin(x**2)
   plt.figure(figsize=(6, 3))
   plt.plot(x, y)
   plt.xlabel("x", fontsize=10)
   plt.ylabel("y", fontsize=10)
   plt.savefig("fig_ex_python.png", dpi)

|

Y el siguiente código de Matlab.

.. code:: matlab

   fig = figure(1);
   fig.Units = 'inches';
   fig.Position(3:4) =  [6 4];
   x = linspace(0, 2*pi, 500);
   y = sin(x.^2);
   plot(x, y, 'LineWidth', 2);
   xlabel('x', 'FontSize', 10)
   ylabel('y', 'FontSize', 10)
   set(fig, 'PaperSize', [6,4]);
   print(fig,'fig_ex_matlab', '-dpng', '-r150');

|

A continuación resumo algunos tamaños para artículos, pósters y diapositivas.

Artículos
---------

Para un artículo es común usar tamaño carta que es 8.5 in × 11 in
(215.9 mm × 279.4 mm). Otro formato común es A4 que es 210 mm × 297 mm 
(8.27 in × 11.7 in).

Una guía para tamaños comunes es la siguiente:

- ancho de 1.0 columna: 90 mm (3.5 in);
- ancho de 1.5 columna: 140 mm (5.5 in);
- ancho de 2.0 columna: 190 mm (6.5 in);

y se muestra en la siguiente imagen.

.. image:: /images/tech_writing/sizes.png
   :width: 400 px
   :alt: Anchos de figuras comparados con papel tamaño carta.
   :align: center

Si consideramos una *resolución* de 300 ppi, tenemos los siguientes números de
píxeles horizontalmente

- ancho de 1.0 columna: 1050 píxeles;
- ancho de 1.5 columna: 1650 píxeles; y
- ancho de 2.0 columna: 1950 píxeles.

Tenga en cuenta que un monitor HD tiene 1920 píxeles en la dirección horizontal.
Esto significa que se necesita un monitor HD para ser capaz de ver tanto
píxeles.

Respecto al tamaño del texto, es común tener tamaños entre 8 y 12 pts para
figuras.

Pósters
-------

En el caso de papel tamaño A0 (841 mm × 1189 mm, 33 in × 47 in) los tamaños
serían algo como:

- ancho de 1.0 columna: 360 mm (14 in);
- ancho de 1.5 columna: 560 mm (22 in); y
- ancho de 2.0 columna: 760 mm (26 in).

Tenga en cuenta que un póster puede que no encaje tan bien en el formato
de dos columans. Sin embargo, creo que la referencia sigue siendo útil.

Respecto al tamaño dl texto en pósters es una buena idea mantenerlo por encima
de 24 pts (ver referencia 3).

Diapositivas
------------

En el caso de diapositivas hay dos relaciones de aspecto comunes 16:9 y 4:3.
Además, diferentes programas usan diferentes tamaños nominales. La siguiente
tabla muestra los tamaños nomiales para LibreOffice Impress y MS Power Point.

+---------------------+--------------------+--------------------+
|                     |          16:9      |        4:3         |
+=====================+====================+====================+
| LibreOffice Impress | 11.02 in × 6.20 in | 11.02 in × 8.00 in |
+---------------------+--------------------+--------------------+
| MS Power Point      | 13.32 in × 7.50 in | 10.00 in × 7.50 in |
+---------------------+--------------------+--------------------+


Referencias
-----------

1. Matthew Butterick (2019). `Butterick's Practical Typography <https://practicaltypography.com/>`_.
   Segunda edición, Matthew Butterick.

2. Rougier, Nicolas P., Michael Droettboom, y Philip E. Bourne (2014).
   “Ten Simple Rules for Better Figures.” PLOS Computational Biology 10(9):e1003833.
   DOI: 10.1371/journal.pcbi.1003833.

3. Erren, Thomas C., y Philip E. Bourne. 2007.
   “Ten Simple Rules for a Good Poster Presentation.”
   PLOS Computational Biology 3(5):e102. DOI: 10.1371/journal.pcbi.0030102

4. Elsevier. (n.d.). "Artwork Overview." Fecha de acceso: Noviembre 1, 2021,
   de https://www.elsevier.com/authors/policies-and-guidelines/artwork-and-media-instructions/artwork-overview

5. Elsevier. (n.d.). "Artwork sizing." Fecha de acceso: Noviembre 1, 2021,
   de https://www.elsevier.com/authors/policies-and-guidelines/artwork-and-media-instructions/artwork-sizing

6. Journal of applied physics (n.d.). "Preparing Your Manuscript: Authors
   Instruction." Fecha de acceso: Noviembre 1, 2021, de https://aip.scitation.org/jap/authors/manuscript

|