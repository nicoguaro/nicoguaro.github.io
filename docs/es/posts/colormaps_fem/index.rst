.. title: colormaps_fem
.. slug: colormaps_fem
.. date: 2021-03-01 10:23:07 UTC-05:00
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
.. status: draft


The selection of colormap should be based on your dataset and audience, e.g.,
you do not want to use a colormap that have some cultural background for a group
of people. Also, if your images are going to be printed (in grey scale), you
should consider using a colormap that will preserve the ordering after the color
transformation.

Then, you should take into account that when using/designing a colormap you are
doing a mapping from the values in your dataset to a color space. This space can
be defined in $(R,G,B)$ components, but there exist other color
spaces that are more intuitive like `(H,S,V) (Hue, Saturation, Value) and
(H,S,L) (Hue, Saturation, Lightness) <https://en.wikipedia.org/wiki/HSL_and_HSV>`_.
Based on this, we can think that a (univariate) color scale is equivalent to a
path in the color space. The rainbow colormap changes the Hue. From the
`matplotlib documentation <http://matplotlib.org/examples/color/colormaps_reference.html>`_:

    Sequential:
        These colormaps are approximately monochromatic colormaps varying smoothly
        between two color tones---usually from low saturation (e.g. white) to high
        saturation (e.g. a bright blue). Sequential colormaps are ideal for
        representing most scientific data since they show a clear progression from
        low-to-high values.

    Diverging:
        These colormaps have a median value (usually light in color) and vary
        smoothly to two different color tones at high and low values. Diverging
        colormaps are ideal when your data has a median value that is significant
        (e.g.  0, such that positive and negative values are represented by
        different colors of the colormap).

    Qualitative:
        These colormaps vary rapidly in color. Qualitative colormaps are useful for
        choosing a set of discrete colors. For example::

            color_list = plt.cm.Set3(np.linspace(0, 1, 12))

        gives a list of RGB colors that are good for plotting a series of lines on
        a dark background.

You can also use redundant colormaps, where you play with more than one
parameter at the time, an example for the `rainbow colormap 
<https://mycarta.wordpress.com/2012/12/06/the-rainbow-is-deadlong-live-the-rainbow-part-5-cie-lab-linear-l-rainbow/>`_.
This `talk in SciPy 2014 <https://youtu.be/rkDgBvT-giw>`_, discuss some topics
of colormaps in matplotlib and is really enlightening, the slides can be found
`here <https://github.com/dmcdougall/scipy14-colormaps>`_.

Why using colormaps
-------------------

Some reasons to use colormaps are:

- Mimic reality (use the same set of color that appear in the physical world)
- Show classification (qualitative)
- Show value (quantitative)
- Draw attention
- Show grouping / similarities

That is why some scales are better at qualitative judgments [2] (Relative shapes
and sizes). And, Other color scales are better for quantitative
judgments (Looking up values), that is the application that you are interested 
now.

Trumbos's Principles
--------------------

Trumbo's Principles present some guidelines to take into account when
designing/using colormaps [1]:

- Order: ordered values should be represented by
ordered colors
- Separation: significantly different levels should be
represented by distinguishable colors

The rainbow colormap is not good at present the color information ordered, and
that is why some people suggest to avoid it [3]. Although there are versions of
the raibow colormap that are redundant and present the ordering property. Some
examples of `colormaps <http://www.ncl.ucar.edu/Document/Graphics/color_table_gallery.shtml>`_.

References
-----------

1. Bruce E. Trumbo (1981), Theory for Coloring Bivariate Statistical Maps,
   The American Statistician, vol. 35, no. 4, pp. 220-226.
   http://www.tandfonline.com/doi/abs/10.1080/00031305.1981.10479360.

2. Ware, C., (1988). Color Sequences for Univariate Maps: Theory, Experiments 
   and Principles. IEEE Computer Graphics and Applications. 8(5), 41-49.
   http://ccom.unh.edu/vislab/PDFs/ColorSequences.pdf.

3. Borland, David, and Russell M. Taylor II. "Rainbow color map (still)
   considered harmful." IEEE computer graphics and applications 27.2 (2007):
   14-17. http://data3.mprog.nl/course/15%20Readings/40%20Reading%204/Borland_Rainbow_Color_Map.pdf

4. Kovesi Peter (2015) Bad Colour Maps Hide Big Features and Create False
   Anomalies. ASEG Extended Abstracts 2015 , 1–4.
   http://www.publish.csiro.au/?paper=ASEG2015ab107

5. Rougier, Nicolas P., Michael Droettboom, and Philip E. Bourne.
   "Ten simple rules for better figures." PLoS computational biology 10.9
   (2014): e1003833. http://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1003833

6. Moreland, K. (2016). Why we use bad color maps and what you can do about it.
   Electronic Imaging, 2016(16), 1-6. http://www.kennethmoreland.com/color-advice/BadColorMaps.pdf

7. Moreland, K. (2016). Color Map Advice for Scientific Visualization
   http://www.kennethmoreland.com/color-advice/