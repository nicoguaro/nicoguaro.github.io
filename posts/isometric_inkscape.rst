.. title: Isometric graphics in Inkscape
.. slug: isometric_inkscape
.. date: 2018-05-24 15:42:02 UTC-05:00
.. tags: inkscape, computer graphics, linear algebra, tutorial
.. category: Computer graphics
.. description: How to make isometric drawings using Inkscape.
.. type: text
.. has_math: yes

Sometimes I find myself in need of making a schematic using an
`isometric projection <https://en.wikipedia.org/wiki/Isometric_projection>`__.
When the schematic is complicated the best shot is to use some
CAD like `FreeCAD <https://freecadweb.org/>`__, but sometimes it's just
needed in simple diagrams. Another situation where this is a common needed
is in `video games <https://en.wikipedia.org/wiki/Isometric_graphics_in_video_games_and_pixel_art>`__,
where `"isometric art" <https://youtu.be/toWMFcWB4HA>`__ and
`pixel art <https://en.wikipedia.org/wiki/Pixel_art>`__ are pretty common.

What we want is depicted in the following figure.


.. image:: /images/isometric_inkscape/isometric_example.svg
   :width: 400 px
   :alt: Views names in third angle representation
   :align:  center


That is, we want to start with some information that is drawn, or
written in the case of the example, and we want to obtain how would it
been seen on one of the faces of an isometric box.

Following, I will describe briefly the transformations involved in this process.
If you are just interested in the recipe for doing this in Inkscape, skip to
the end of this post.

Transformations involved
------------------------

Since we are working on a computer screen, we are talking of 2 dimensions.
Hence, all transformations are represented by 2×2 matrices. In the particular
example of interest in this post we need the following transformations:

1. Vertical scaling
2. Horizontal skew
3. Rotation

Following are the transformation matrices.

Scaling in the vertical direction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The matrix is given by

.. math::

   M_\text{scaling} = \begin{bmatrix} 1 &0\\ 0 &a\end{bmatrix}\, ,

where :math:`a` is the scaling factor.


Horizontal skew
~~~~~~~~~~~~~~~

The matrix is given by

.. math::

   M_\text{skew} = \begin{bmatrix} 1 &\tan a\\ 0 &1\end{bmatrix}\, ,

where :math:`a` is the skewing angle.


Rotation
~~~~~~~~~

The matrix is given by

.. math::

   M_\text{rotation} = \begin{bmatrix} \cos a &-\sin a\\ \sin a &\cos a\end{bmatrix}\, ,

where :math:`a` is the rotation angle.


Complete transformation
~~~~~~~~~~~~~~~~~~~~~~~

The complete transformation is given by

.. math::

   M_\text{complete} = M_\text{rotation} M_\text{skew} M_\text{scaling}\, ,

particularly,


.. math::

   &M_\text{side} =
     \frac{1}{2}\begin{bmatrix} \sqrt{3} & 0\\ -1 &2\end{bmatrix}\approx
     \begin{bmatrix} 0.866 & 0.000\\ -0.500 &1.000\end{bmatrix}\, , \\
   &M_\text{front} = \frac{1}{2}\begin{bmatrix} \sqrt{3} & 0\\ 1 &2\end{bmatrix}\approx
     \begin{bmatrix} 0.866 & 0.000\\ 0.500 &1.000\end{bmatrix}\, , \\
   &M_\text{plant} = \frac{1}{2}\begin{bmatrix} \sqrt{3} & -\sqrt{3}\\ -1 &1\end{bmatrix}\approx
     \begin{bmatrix} 0.866 & -0.866\\ 0.500 &0.500\end{bmatrix}\, .

The values seem a bit arbitrary, but they can be obtained from the
`isometric projection <https://en.wikipedia.org/wiki/Isometric_projection#Mathematics>`__
itself. But that explanation would be a bit too long for this post.


Tranformation in Inkscape
~~~~~~~~~~~~~~~~~~~~~~~~~

We already have the transformation matrices and we can use them in Inkscape.
But first, we need to understand how it works. Inkscape uses
`SVG <https://en.wikipedia.org/wiki/Scalable_Vector_Graphics>`__, the web
standard for vector graphics. `Transformations <https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform>`__ in SVG are done using the following
matrix

.. math::

   \begin{bmatrix} a &c &e\\ b &d &f\\ 0 &0 &1\end{bmatrix}\, ,

that uses `homogeneous coordinates <https://en.wikipedia.org/wiki/Homogeneous_coordinates>`__. So, one can just press ``Shift + Ctrl + M``
and type the components of the matrices obtained above for
:math:`a`, :math:`b`, :math:`c`, and :math:`d`; leaving
:math:`e` and :math:`f` as zero.

My preferred method, though, is to apply each transformation after the
other in the `Transform` dialog (``Shift + Ctrl + M``). And, this is the
method presented in the cheatsheet at the bottom of this post.


TL;DR
-----
If you are just interested in the transformations needed in Inkscape
you can check the cheatsheet below. It uses third-angle as presented
below.

.. image:: /images/isometric_inkscape/third_angle.svg
   :width: 400 px
   :alt: Views names in third angle representation
   :align:  center

Cheatsheet
~~~~~~~~~~

Keep in mind that Inkscape treats clockwise rotation as positive. Opposite
to common notation in mathematics.

.. image:: /images/isometric_inkscape/isometric_instructions.svg
   :width: 500 px
   :alt: Cheatsheet for isometric schematics in Inkscape
   :align:  center
