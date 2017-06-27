.. title: Using style sheets with matplotlib
.. slug: matplotlib_styles
.. date: 2017-06-27 17:14:14 UTC-05:00
.. tags: scientific computing, visualization, matplotlib, python
.. category: Scientific Computing
.. link:
.. description:
.. type: text


Using the `style package <http://matplotlib.org/users/customizing.html>`_
in matplotlib allows for easy style formatting of plots. The main idea
is to create a file with some of the parameters that want to be defined
(that can also be accessed through `rcParams`).

This post is not a tutorial on how to use those, for that you can check
the `style sheet reference <http://matplotlib.org/examples/style_sheets/style_sheets_reference.html>`_.
Here, I just want to play with some of these parameters to create three
different styles. The first two are for some infamous tools, that
is probably used for most people as the visualization platform, while the
third one is just a clean style. All the files used here can be download
`here <https://gist.github.com/nicoguaro/862ea1015917d99352401433d45684e2>`_.


For all the examples below the following imports are done:

.. code:: ipython3

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt

First example: MS 2003
----------------------

In our first example we want to reproduce the style that we used to see
more than a decade ago as default.

The following is the content of the file `MS2003.mplstyle <https://gist.githubusercontent.com/nicoguaro/862ea1015917d99352401433d45684e2/raw/79e08ea0fabd4e84bba9fef5d29ecf3f9bbe0436/MS2003.mplstyle>`_

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

The following code use this style

.. code:: ipython3

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

and this is the result

.. image:: /images/MS2003_style.svg

Second example: MS 2007
-----------------------

In the second example we want to reproduce the offspring of the style
in the first example. This is definitely an improvement over the previous
style, but it is `not perfect <http://analyticsdemystified.com/excel-tips/data-visualization-that-is-color-blind-friendly-excel-2007/>`_.

The following is the content of the file `MS2007.mplstyle <https://gist.githubusercontent.com/nicoguaro/862ea1015917d99352401433d45684e2/raw/79e08ea0fabd4e84bba9fef5d29ecf3f9bbe0436/MS2007.mplstyle>`_

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

The following code use this style

.. code:: ipython3

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

and this is the result

.. image:: /images/MS2007_style.svg


Third example: a clean style
----------------------------

The last example is a clean style that uses a color palette taken
from `ColorBrewer <http://colorbrewer2.org/#type=qualitative&scheme=Set1&n=8>`_.

The following is the content of the file `clean_style.mplstyle <https://gist.githubusercontent.com/nicoguaro/862ea1015917d99352401433d45684e2/raw/79e08ea0fabd4e84bba9fef5d29ecf3f9bbe0436/clean.mplstyle>`_

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

The following code use this style


.. code:: ipython3

    style = "clean.mplstyle"
    with plt.style.context(style):
        x = np.linspace(0, 4, 100)
        y = np.sin(np.pi*x + 1e-6)/(np.pi*x + 1e-6)
        fig = plt.figure()
        ax = plt.subplot(111)
        for cont in range(5):
            plt.plot(x, y/(cont + 1), label=cont)

        plt.legend()

and this is the result

.. image:: /images/clean_style.svg

We can also use files that are stored remotely. For example, in the third
example we could have used the following URL:


.. code:: python

    style = "https://gist.githubusercontent.com/nicoguaro/862ea1015917d99352401433d45684e2/raw/79e08ea0fabd4e84bba9fef5d29ecf3f9bbe0436/clean.mplstyle"


Resources
---------

As I mentioned above, the objective of this post was jut to create some
simple-enough style-sheets for matplotlib and see them in action.

This post does not pretend to be a guide for good plots/visualization.
For that matter you better look for some references, for example:


- Rougier, Nicolas P., Michael Droettboom, and Philip E. Bourne.
  `"Ten simple rules for better figures." <http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833>`_
  PLoS computational biology 10.9 (2014): e1003833.


Also, I found really useful the following tools:


- `ColorBrewer2 <http://colorbrewer2.org>`_ allows to pick colormaps
  with different criteria (quantitative/qualitative, printer friendly,
  colorblind friendly).

- `ColRD <http://colrd.com>`_ has plenty of color palettes. It also has the
  option to generate palettes from images.

- `Colorgorical <http://vrl.cs.brown.edu/color>`_ is a tool to
  make categorical color palettes for information visualization.


You can find the snippets present in this post in
`this Jupyter notebook <http://nbviewer.jupyter.org/gist/nicoguaro/862ea1015917d99352401433d45684e2/matplotlib_styles.ipynb>`_.
