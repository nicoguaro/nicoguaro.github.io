.. title: Escritura técnica
.. slug: tech_writing
.. date: 2020-05-28 15:53:40 UTC-05:00
.. tags: escrotira, investigación, tipografía, libreoffice, latex
.. category: Writing
.. link:
.. description: Consejos sobre escritur ténica.
.. type: text
.. status:

Esta es la primera publicación sobre redacción técnica [*]_ de una serie que
crearé durante el transcurso de este año. La escritura técnica es algo con lo
que la mayoría de nosotros tenemos que lidiar en diferentes contextos. Por
ejemplo, en cursos universitarios, publicaciones de investigación,
documentación de software. La idea principal de la serie es mencionar algunos
de los trucos que he aprendido a lo largo de los años y algunas herramientas
que pueden ser útiles.

Las publicaciones futuras serán (probablemente) sobre:

- Uso de ecuaciones;

- Uso de figuras;

- Uso de tablas; y

- Gestión de referencias bibliográficas.


Esta publicación
================

Como se mencionó anteriormente, la escritura técnica es algo con lo que muchas
personas tienen que lidiar. Esta es una habilidad que a veces se pasa por alto,
pero no debería. De acuerdo con la
`U.S. Bureau of Labor Statistics <https://www.bls.gov/ooh/media-and-communication/technical-writers.htm>`_

  Los redactores técnicos preparan manuales, guías prácticas,
  artículos de revistas y otros documentos de respaldo para comunicar
  información compleja y técnica con mayor facilidad.

Y es una habilidad deseada en el lugar de trabajo. Se espera que su demanda crezca
alrededor del 10% en la década actual.

Tipografía
----------

Lo primero que debo mencionar es que escribir documentos es
tipografía ya que estamos *diseñando con texto* (Butterick, 2019). Por lo tanto,
deberíamos considerarnos tipógrafos, ya que constantemente diseñamos documentos.

Sugeriría echar un vistazo a "Butterick's Practical Typography"
ya que es un libro muy bueno sobre el tema y es fácil de leer. Voy a
mencionar algunos puntos importantes de acuerdo con la sección
"Tipografía en diez minutos":

1. La selección tipográfica más importante está en el cuerpo del texto.
   Esto se debe al hecho de que es la mayor parte del documento.

2. Elija un tamaño de punto entre 10-12 puntos para documentos impresos
   y 15-25 píxeles para documentos digitales.

3. El espacio entre líneas debe estar entre 120-145% del tamaño de la letra.

4. La longitud de la línea debe tener entre 45 y 90 caracteres. Esto es
   aproximadamente 2 o 3 alfabetos en minúsculas:

   abcdefghijklmnñopqrstuvwxyzabcdefghijklmnñopqrstuvwxyzabcd

5. Cuidado con la selección de su fuente. Intente evitar las fuentes
   predeterminadas como Arial, Calibri o Times New Roman.

Editores
---------

Otro punto que quiero tocar en esta publicación es el de los editores. La
primera pregunta que surge es "¿qué editor debo usar?". La respuesta corta es:
**usa lo que tus colegas estén usando**. Ese es mi mejor consejo; de esa
manera tu tienes personas con quienes hablar sobre tus dudas.

La respuesta larga ... es que cada editor tiene sus puntos débiles y fuertes.
Yo ha escrito artículos científicos en LaTeX, LibreOffice Writer y MS Word;
todos se ven profesionales. Entonces, al final, puedes escribir tu
documentos de varias maneras y lograr un resultado similar. Prefiero usar
LaTeX para documentos largos, ya que se centra en la estructura de la
documento en lugar de la apariencia y esta es la forma en que uno debe
administrar un documento largo como una disertación, en mi opinión.

Si solo quieres que elija un editor y te lo sugiera, diría que
`LibreOffice <https://www.libreoffice.org/>`_. Una buena referencia para
es "Designing with LibreOffice". Una vez que aprendas
cómo usar estilos, preguntarás cómo has estado escribiendo todos los documentos
hasta ahora.

Hay dos grupos de editores que voy a discutir:
WYSIWYG (siglas en inglés para "Lo que ves es lo que obtienes") y
editores basados en marcado.

- WYSIWYG. Esta categoría es la que la mayoría de la gente conoce.
  Dos ejemplos son:

  - LibreOffice writer; y

  - Microsoft Word.

- Los editores basados en marcado dependen de las marcas en el "texto" para
  diferenciar secciones y estilos. En este caso, su texto parece código,
  como se ve en la siguiente imagen

  .. image:: /images/rst_code.png

  Algunos ejemplos son:

  - LaTeX;

  - `Markdown <https://www.markdownguide.org/getting-started>`_; y

  - `reStructuredtext <https://docutils.sourceforge.io/rst.html>`_.


Independientemente de cuál sea tu editor principal, sugiero utilizar
`Pandoc <https://pandoc.org/>`_. Te permite convertir entre varios
formatos, haciendo el proceso un poco más fácil. Incluso hay un editor
basado completamente en él llamado `Panwriter <https://panwriter.com/>`_.


References
----------

1. Matthew Butterick (2019). `Butterick's Practical Typography <https://practicaltypography.com/>`_.
   Segunda edición, Matthew Butterick.

2. Wikibooks contributors. (2020). `LaTeX <https://en.wikibooks.org/wiki/LaTeX>`_.
   Wikibooks, The Free Textbook Project.

3. Bruce Byfield (2016). `Designing with LibreOffice <https://designingwithlibreoffice.com/>`_.
   Friends of OpenDocument, Inc.

4. Deville, S. (2015).
   `Writing academic papers in plain text with Markdown and Jupyter notebook
   <https://sylvaindeville.net/2015/07/17/writing-academic-papers-in-plain-text-with-markdown-and-jupyter-notebook/>`_.
   Sylvain Deville.

5. Eric Holscher (2016).
`An introduction to Sphinx and Read the Docs for Technical Writers
<https://www.ericholscher.com/blog/2016/jul/1/sphinx-and-rtd-for-writers/>`__



.. [*] Esta publicación está (algo) relacionada con una
   `publicación anterior <../ herramientas-investigacion />`__
   donde discutí sobre algunas herramientas de investigación que la mayoría
   de nosotros necesitamos pero que comúnmente no se enseñan de manera formal.
