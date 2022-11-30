.. title: Usando estilos predefinidos en matplotlib
.. slug: matplotlib_styles
.. date: 2017-06-27 17:14:14 UTC-05:00
.. tags: computación científica, visualización, matplotlib, python
.. category: Visualization
.. link:
.. description:
.. type: text

Podemos dar formato a los gráficos de forma simple usando el
`paquete de estilo <http://matplotlib.org/users/customizing.html>`_
en matplotlib. La idea principal es crear un archivo con algunos
parámetros predefinidos (esto también puede hacerse a través de
`rcParams`).

Esta publicación no es un tutorial en cómo usar estos archivos, para
estos puedes mirar la página
`style sheet reference <http://matplotlib.org/examples/style_sheets/style_sheets_reference.html>`_.
Acá, quiero jugar un poco con algunos de los parámetros para crear tres
estilos diferentes. Los primeros dos tienen el estilo de un software
(infame para algunos), que es usado por la mayoría de las personas como
su plataforma de visualización, el tercero es un estilo limpio. Todos
los archivos usados se pueden descargar
`aquí <https://github.com/nicoguaro/matplotlib_styles>`_.

Para todos los ejemplos se realizan las siguientes importaciones:

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt

Primer ejemplo: MS 2003
-----------------------

En nuestro primer ejemplo queremos reproducir el estilo que solíamos
ver como la opción por defecto hace más de una década.

Este es el contenido del archivo
`MS2003.mplstyle <https://github.com/nicoguaro/matplotlib_styles/blob/master/styles/MS2003.mplstyle>`_

.. code:: python

    font.family : sans-serif

    axes.facecolor : c0c0c0
    axes.edgecolor : black
    axes.prop_cycle : cycler('color',['000080', 'FF00FF', 'FFFF00', '00FFFF','800080', '800000', '008080', '0000FF'])
    axes.grid : True

    axes.spines.left   : True
    axes.spines.bottom : True
    axes.spines.top    : True
    axes.spines.right  : True

    grid.color : black
    grid.linestyle : -

    lines.linewidth : 1

    figure.figsize : 5, 3

    legend.fancybox : False
    legend.frameon : True
    legend.facecolor : white
    legend.edgecolor : black
    legend.loc : center left

El siguiente bloque de código usa este estilo

.. code:: python

    style = "MS2003.mplstyle"
    with plt.style.context(style):
        x = np.linspace(0, 4, 100)
        y = np.sin(np.pi*x + 1e-6)/(np.pi*x + 1e-6)
        fig = plt.figure()
        ax = plt.subplot(111)
        for cont in range(5):
            plt.plot(x, y/(cont + 1), label=cont)

        plt.gca().xaxis.grid(False)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        plt.legend(bbox_to_anchor=(1, 0.5))

y este es el resultado

.. image:: /images/MS2003_style.svg

Segundo ejemplo: MS 2007
------------------------

En el segundo ejemplo queremos reproducir la prole del primer estilo
en este ejemplo. Este estilo es una mejora respecto al anterior,
pero `no es perfecto <http://analyticsdemystified.com/excel-tips/data-visualization-that-is-color-blind-friendly-excel-2007/>`_.

El siguiente es el contenido del archivo
`MS2007.mplstyle <https://github.com/nicoguaro/matplotlib_styles/blob/master/styles/MS2007.mplstyle>`_

.. code:: python

    font.family : sans-serif

    axes.facecolor : white
    axes.edgecolor : 4d4d4d
    axes.prop_cycle : cycler('color',['4573a7', 'aa4644', '89a54e', '71588f','4298af', 'db843d', '93a9d0', 'd09392'])
    axes.grid : True
    axes.linewidth : 0.5

    axes.spines.left   : True
    axes.spines.bottom : True
    axes.spines.top    : False
    axes.spines.right  : False

    lines.linewidth : 2

    grid.color : 4d4d4d
    grid.linestyle : -
    grid.linewidth : 0.5

    figure.figsize : 5, 3

    legend.fancybox : False
    legend.frameon : False
    legend.facecolor : white
    legend.edgecolor : 4d4d4d
    legend.loc : center left

El siguiente código usa este estilo

.. code:: python

    style = "MS2007.mplstyle"
    with plt.style.context(style):
        x = np.linspace(0, 4, 100)
        y = np.sin(np.pi*x + 1e-6)/(np.pi*x + 1e-6)
        fig = plt.figure()
        ax = plt.subplot(111)
        for cont in range(5):
            plt.plot(x, y/(cont + 1), label=cont)

        plt.gca().xaxis.grid(False)
        box = ax.get_position()
        ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        plt.legend(bbox_to_anchor=(1, 0.5))

y este es el resultado

.. image:: /images/MS2007_style.svg


Tercer ejemplo: un estilo limpio
--------------------------------

El último ejemplo es un estilo limpio que usa una paleta de colores
tomada de
`ColorBrewer <http://colorbrewer2.org/#type=qualitative&scheme=Set1&n=8>`_.

Este es el contenido del archivo
`clean_style.mplstyle <https://github.com/nicoguaro/matplotlib_styles/blob/master/styles/clean.mplstyle>`_

.. code:: python

    font.family : sans-serif

    axes.facecolor : white
    axes.prop_cycle : cycler('color',['e41a1c', '377eb8', '4daf4a', '984ea3', 'ff7f00', 'ffff33', 'a65628', 'f781bf'])
    axes.linewidth : 0.0
    axes.grid : True

    lines.linewidth : 1.5

    xtick.direction : in
    ytick.direction : in

    grid.color : c7dedf
    grid.linestyle : -
    grid.linewidth : 0.3

    figure.figsize : 6, 4

    legend.fancybox : False
    legend.frameon : False
    legend.loc : best

El siguiente código usa este estilo

.. code:: python

    style = "clean.mplstyle"
    with plt.style.context(style):
        x = np.linspace(0, 4, 100)
        y = np.sin(np.pi*x + 1e-6)/(np.pi*x + 1e-6)
        fig = plt.figure()
        ax = plt.subplot(111)
        for cont in range(5):
            plt.plot(x, y/(cont + 1), label=cont)

        plt.legend()

y este es el resultado

.. image:: /images/clean_style.svg

También podemos usar archivos que están almacenado remotamente. Por ejemplo,
podríamos usar la siguiente URL:

.. code:: python

    style = "https://raw.githubusercontent.com/nicoguaro/matplotlib_styles/master/styles/clean.mplstyle"


Recursos
---------

Como mencioné anteriormente, el objetivo de esta publicación era crear
algunos archivos de estilo simples para matplotlib y verlos en acción.

Esta publicación no permite ser una guía para buenos gráficos/visualizaciones.
Para este propósito sugiero mirar la siguiente referencia:

- Rougier, Nicolas P., Michael Droettboom, and Philip E. Bourne.
  `"Ten simple rules for better figures." <http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833>`_
  PLoS computational biology 10.9 (2014): e1003833.

Además, encuentro muy útiles las siguientes herramientas:

- `ColorBrewer2 <http://colorbrewer2.org>`_ permite elegir mapas de colores
  con diferentes criterios (cuantitativo/cualitativo, apto para impresión,
  apto para daltónicos).

- `ColRD <http://colrd.com>`_ tiene muchas paletas de colores. También
  permite generar paletas a partir de imágenes.

- `Colorgorical <http://vrl.cs.brown.edu/color>`_ es una herramienta
  para crear paletas de colores categóricas (cualitativas) para visualización
  de información.
