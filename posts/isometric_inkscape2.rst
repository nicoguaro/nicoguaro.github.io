.. title: Isometric graphics in Inkscape: Part 2
.. slug: isometric_inkscape2
.. date: 2018-05-30 12:40:57 UTC-05:00
.. tags: mathjax, inkscape, computer graphics, tutorial
.. category: Computer graphics
.. link: 
.. description: 
.. type: text

`Last week <../isometric_inkscape>`__  I posted a quick guide on isometric
drawing using `Inkscape <https://inkscape.org/en/>`__. In that post I
showed how to obtain images that are projected to the faces of an
isometric box.

After my post, I was asked by `Biswajit Banerjee <https://twitter.com/parresianz>`__
on `Twitter <https://twitter.com/parresianz/status/999787980658126848>`__ if
I could repeat the process with a more complex example, and he suggested
the following schematic

.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Beam_moment_plain.svg/512px-Beam_moment_plain.svg.png
   :alt: Computing the moment of force in a beam
   :align:  center

which, I guess, was created in Inkscape using the "Create 3D Box" option.

In this post, I will:

1. Use the same approach from last week to recreate this schematic
2. Suggest my preferred approach for drawing this schematic


First approach
--------------

I will repeat the cheatsheet from last week. Keep in mind that Inkscape
treats clockwise rotation as positive. Opposite to common notation in
mathematics.

.. image:: /images/isometric_inkscape/isometric_instructions.svg
   :width: 500 px
   :alt: Cheatsheet for isometric schematics in Inkscape
   :align:  center


Then, to create a box with desired dimensions we first create each rectangle
with the right dimensiones (in parallel projections). In the following
example we used faces with aspect ratios 3:2, 2:1 and 4:3. The box at the right
is the figure obtained after applying the transformations described in
the previous schematic.

.. image:: /images/isometric_inkscape/isometric_ex2.svg
   :width: 500 px
   :alt: Orthogonal views and final isometric figure
   :align:  center

We can now proceed, to recreate the desired figure. I don't know the
exact dimensions of the box; my guess is that the cross section was
a square and the aspect ratio was 5:1. After applying the transformations
to each rectangle we obtain the following (adding some tweaks here and there).

.. image:: /images/isometric_inkscape/isometric_beam.svg
   :width: 500 px
   :alt: Recreated figure using the described approach
   :align:  center
   
Second approach
---------------

For this type of schematic I would prefer to create an axonometric grid
(``File > Document Properties > Grids``). After adding the grid to our
canvas it is pretty straightforward to draw the figures in isometric
view. The canvas should look similar to the following image.

.. image:: /images/isometric_inkscape/screenshot_inkscape.png
   :width: 500 px
   :alt: Second approach: using an axonometric grid
   :align:  center

We can then draw each face using the grid. If we want to be more precise
we can activate ``Snap to Cusp Nodes``. The following animation shows
the step by step construction.


.. image:: /images/isometric_inkscape/isometric_construction.gif
   :width: 500 px
   :alt: Step by step construction of the isometric
   :align:  center

And we obtain the final image.

.. image:: /images/isometric_inkscape/isometric_beam2.svg
   :width: 500 px
   :alt: Recreated figure using the second approach
   :align:  center
   
Conclusion
----------

As I mentioned, Inkscape can be used for drawing simple figures in isometric
projection. Nevertheless, I strongly suggest to use a CAD like 
`FreeCAD <https://freecadweb.org/>`__ for more compicated geometries.

