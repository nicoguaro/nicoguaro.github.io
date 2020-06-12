.. title: Cyclic colormaps comparison
.. slug: cyclic_colormaps
.. date: 2018-01-02 18:55:41 UTC-05:00
.. tags: scientific computing, visualization, matplotlib, python
.. category: Visualization
.. type: text
.. has_math: yes


I started this post looking for a
`diffusion map <https://en.wikipedia.org/wiki/Diffusion_map>`_ on Python,
that I didn't find. Then I continued following an
`example <http://scikit-learn.org/stable/auto_examples/manifold/plot_compare_methods.html#sphx-glr-auto-examples-manifold-plot-compare-methods-py>`_
on `manifold learning <https://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction>`_
by `Jake Vanderplas <https://jakevdp.github.io/>`_ on a `different dataset
<https://commons.wikimedia.org/wiki/File:Diffusion_map_of_a_torodial_helix.jpg>`_.
It worked nicely,

.. image:: /images/manifold_learning_toroidal_helix.svg


but the colormap used is `Spectral <https://matplotlib.org/examples/color/colormaps_reference.html>`_, that is divergent. This made me think about
using a cyclic colormap, and ended up in
`this StackOverflow <https://stackoverflow.com/q/23712207/3358223>`_ question.
And I decided to compare some cyclic colormaps.

I picked up colormaps from different sources

- `cmocean <https://matplotlib.org/cmocean/>`_:

  - phase

- `Paraview <http://paraview.org/>`_:

  - hue_L60
  - erdc_iceFire
  - nic_Edge

- `Colorcet <https://github.com/bokeh/colorcet>`_:

  - colorwheel
  - cyclic_mrybm_35_75_c68
  - cyclic_mygbm_30_95_c78

and, of course, ``hsv``. You can download the colormaps in text
format from `here </downloads/cyclic_colormaps.zip>`_.

Comparison
----------

For all the examples below the following imports are done:

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from colorspacious import cspace_convert


Color map test image
~~~~~~~~~~~~~~~~~~~~

Peter Kovesi proposed a way to compare cyclic colormaps on a
`paper <http://peterkovesi.com/projects/colourmaps/colourmaptestimage.html>`_
on 2015. It consists of a spiral ramp with an undulation. In polar coordinates
it reads

.. math::

    c = (A \rho^p \sin(n \theta) + \theta)\, \mathrm{mod}\, 2\pi

with :math:`A` the amplitude of the oscilation, :math:`\rho` the normalized
radius in [0, 1], :math:`p` a positive number, and :math:`n` the number
of cycles.

And the following function creates the grid in Python

.. code:: python

    def circle_sine_ramp(r_max=1, r_min=0.3, amp=np.pi/5, cycles=50,
                         power=2, nr=50, ntheta=1025):
    r, t = np.mgrid[r_min:r_max:nr*1j, 0:2*np.pi:ntheta*1j]
    r_norm = (r - r_min)/(r_max - r_min)
    vals = amp * r_norm**power * np.sin(cycles*t) + t
    vals = np.mod(vals, 2*np.pi)
    return t, r, vals


The following is the result

.. image:: /images/sine_helix_cyclic_cmap.png

Colorblindness test
~~~~~~~~~~~~~~~~~~~

.. code:: python

    t, r, vals = circle_sine_ramp(cycles=0)
    cmaps = ["hsv",
             "cmocean_phase",
             "hue_L60",
             "erdc_iceFire",
             "nic_Edge",
             "colorwheel",
             "cyclic_mrybm",
             "cyclic_mygbm"]
    severity = [0, 50, 50, 50]
    for colormap in cmaps:
        data = np.loadtxt(colormap + ".txt")
        fig = plt.figure()
        for cont in range(4):
            cvd_space = {"name": "sRGB1+CVD",
                 "cvd_type": cvd_type[cont],
                 "severity": severity[cont]}
            data2 = cspace_convert(data, cvd_space, "sRGB1")
            data2 = np.clip(data2, 0, 1)
            cmap = LinearSegmentedColormap.from_list('my_colormap', data2)
            ax = plt.subplot(2, 2, 1 + cont, projection="polar")
            ax.pcolormesh(t, r, vals, cmap=cmap)
            ax.set_xticks([])
            ax.set_yticks([])
        plt.suptitle(colormap)
        plt.tight_layout()
        plt.savefig(colormap + ".png", dpi=300)



.. figure:: /images/hsv_eval.png
    :align: center

    ``hsv`` colormap comparison for different color vision deficiencies.

.. figure:: /images/cmocean_phase_eval.png
    :align: center

    ``Phase`` colormap comparison for different color vision deficiencies.

.. figure:: /images/hue_L60_eval.png
    :align: center

    ``hue_L60`` colormap comparison for different color vision deficiencies.


.. figure:: /images/erdc_iceFire_eval.png
    :align: center

    ``erdc_iceFire`` colormap comparison for different color vision deficiencies.

.. figure:: /images/nic_Edge_eval.png
    :align: center

    ``nic_Edge`` colormap comparison for different color vision deficiencies.

.. figure:: /images/colorwheel_eval.png
    :align: center

    ``Colorwheel`` colormap comparison for different color vision deficiencies.

.. figure:: /images/cyclic_mrybm_eval.png
    :align: center

    ``Cyclic_mrybm`` colormap comparison for different color vision deficiencies.

.. figure:: /images/cyclic_mygbm_eval.png
    :align: center

    ``Cyclic_mygbm`` colormap comparison for different color vision deficiencies.


Randomly generated cyclic colormaps
-----------------------------------

What if we generate some random colormaps that are cyclic? How would they
look like?


Following are the snippet and resulting colormaps.

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap


    # Next line to silence pyflakes. This import is needed.
    Axes3D

    plt.close("all")
    fig = plt.figure()
    fig2 = plt.figure()
    nx = 4
    ny = 4
    azimuths = np.arange(0, 361, 1)
    zeniths = np.arange(30, 70, 1)
    values = azimuths * np.ones((30, 361))
    for cont in range(nx * ny):
        np.random.seed(seed=cont)
        rad = np.random.uniform(0.1, 0.5)
        center = np.random.uniform(rad, 1 - rad, size=(3, 1))
        mat = np.random.rand(3, 3)
        rot_mat, _ = np.linalg.qr(mat)
        t = np.linspace(0, 2*np.pi, 256)
        x = rad*np.cos(t)
        y = rad*np.sin(t)
        z = 0.0*np.cos(t)
        X = np.vstack((x, y, z))
        X = rot_mat.dot(X) + center

        ax = fig.add_subplot(ny, nx, 1 + cont, projection='polar')
        cmap = LinearSegmentedColormap.from_list('my_colormap', X.T)
        ax.pcolormesh(azimuths*np.pi/180.0, zeniths, values, cmap=cmap)
        ax.set_xticks([])
        ax.set_yticks([])

        ax2 = fig2.add_subplot(ny, nx, 1 + cont, projection='3d')
        ax2.plot(X[0, :], X[1, :], X[2, :])
        ax2.set_xlim(0, 1)
        ax2.set_ylim(0, 1)
        ax2.set_zlim(0, 1)
        ax2.view_init(30, -60)
        ax2.set_xticks([0, 0.5, 1.0])
        ax2.set_yticks([0, 0.5, 1.0])
        ax2.set_zticks([0, 0.5, 1.0])
        ax2.set_xticklabels([])
        ax2.set_yticklabels([])
        ax2.set_zticklabels([])


    fig.savefig("random_cmaps.png", dpi=300, transparent=True)
    fig2.savefig("random_cmaps_traj.svg", transparent=True)


.. figure:: /images/random_cmaps.png
    :align: center

    16 randomly generated colormaps.

.. figure:: /images/random_cmaps_traj.svg
    :align: center

    Trajectories in RGB space for the randomly generated colormaps.


A good idea would be to take these colormaps and optimize some perceptual
parameters such as lightness to get some usable ones.

Conclusions
-----------

I probably would use ``phase``, ``colorwheel``, or ``mrybm`` in the
future.

.. figure:: /images/toroidal_helix_phase.svg
    :align: center

    Initial image using ``phase``.


.. figure:: /images/toroidal_helix_colorwheel.svg
    :align: center

    Initial image using ``colorwheel``.

.. figure:: /images/toroidal_helix_mrybm.svg
    :align: center

    Initial image using ``mrybm``.

References
----------

1. Peter Kovesi. Good Colour Maps: How to Design Them.
   arXiv:1509.03700 [cs.GR] 2015
