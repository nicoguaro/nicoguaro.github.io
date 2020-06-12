.. title: Comparación de mapas de colores cíclicos
.. slug: cyclic_colormaps
.. date: 2018-01-02 18:55:41 UTC-05:00
.. tags: computación científica, visualizaciónn, matplotlib, python
.. category: Visualization
.. type: text
.. has_math: yes

Empecé esta publicación buscando implementaciones de
`mapas de difusión <https://en.wikipedia.org/wiki/Diffusion_map>`_
en Python, que no pude encontrar. Me puse entonces a seguir un 
`ejemplo <http://scikit-learn.org/stable/auto_examples/manifold/plot_compare_methods.html#sphx-glr-auto-examples-manifold-plot-compare-methods-py>`_
sobre `aprendizaje de variedades <https://en.wikipedia.org/wiki/Nonlinear_dimensionality_reduction>`_
de `Jake Vanderplas <https://jakevdp.github.io/>`_ en un `conjunto de datos diferente
<https://commons.wikimedia.org/wiki/File:Diffusion_map_of_a_torodial_helix.jpg>`_.
Y funcionó bien

.. image:: /images/manifold_learning_toroidal_helix.svg

pero el mapa de color es `"Spectral" <https://matplotlib.org/examples/color/colormaps_reference.html>`_,
que es divergente. Esto me puso a pensar acerca de usar un mapa de
colores cícliclo, y terminé en esta pregunta de 
`StackOverflow <https://stackoverflow.com/q/23712207/3358223>`_.
Y decidí comparar algunos mapas de colores cíclicos.

Elegí mapas de colores de diferentes fuentes

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

y, obviamente, ``hsv``. Los mapas de colores en formato de texto
plano se pueden descargar `aquí </downloads/cyclic_colormaps.zip>`_.

Comparación
-----------

Para todos los ejemplos se importaron los siguientes módulos:

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt
    from matplotlib.colors import LinearSegmentedColormap
    from colorspacious import cspace_convert


Imagen de prueba 
~~~~~~~~~~~~~~~~

Peter Kovesi propuso una manera de comparar mapas de colores
cíclicos en un 
`artículo <http://peterkovesi.com/projects/colourmaps/colourmaptestimage.html>`_
en 2015. Consta de una rampa en espiral con ondulaciones. En
coordenadas polares es

.. math::

    c = (A \rho^p \sin(n \theta) + \theta)\, \mathrm{mod}\, 2\pi

con :math:`A` la amplitud de la oscilación, :math:`\rho`
el radio normalizado en [0, 1], :math:`p` un número positivo,
y :math:`n` el número de ciclos.

Y la siguiente función crea la rejilla en Python.

.. code:: python

    def circle_sine_ramp(r_max=1, r_min=0.3, amp=np.pi/5, cycles=50,
                         power=2, nr=50, ntheta=1025):
    r, t = np.mgrid[r_min:r_max:nr*1j, 0:2*np.pi:ntheta*1j]
    r_norm = (r - r_min)/(r_max - r_min)
    vals = amp * r_norm**power * np.sin(cycles*t) + t
    vals = np.mod(vals, 2*np.pi)
    return t, r, vals

El resultado es el siguiente

.. image:: /images/sine_helix_cyclic_cmap.png

Prueba para daltonismo
~~~~~~~~~~~~~~~~~~~~~~

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

    Comparación de ``hsv`` para diferentes deficiencias visuales
    del color.

.. figure:: /images/cmocean_phase_eval.png
    :align: center

    Comparación de ``Phase`` para diferentes deficiencias visuales
    del color.

.. figure:: /images/hue_L60_eval.png
    :align: center

    Comparación de ``hue_L60`` para diferentes deficiencias visuales
    del color.

.. figure:: /images/erdc_iceFire_eval.png
    :align: center

    Comparación de ``erdc_iceFire`` para diferentes deficiencias visuales
    del color.

.. figure:: /images/nic_Edge_eval.png
    :align: center

    Comparación de ``nic_Edge`` para diferentes deficiencias visuales
    del color.

.. figure:: /images/colorwheel_eval.png
    :align: center

    Comparación de ``Colorwheel`` para diferentes deficiencias visuales
    del color.

.. figure:: /images/cyclic_mrybm_eval.png
    :align: center

    Comparación de ``Cyclic_mrybm`` para diferentes deficiencias visuales
    del color.

.. figure:: /images/cyclic_mygbm_eval.png
    :align: center

    Comparación de ``Cyclic_mygbm`` para diferentes deficiencias visuales
    del color.


Mapas de colores cíclicos generados aleatoriamente
--------------------------------------------------

¿Qué pasa si generamos mapas de colores cíclicos aleatoriamente?
¿Cómo lucirían?

A continuación están las piezas de código y mapas de colores
resultantes.

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

    16 mapas de colores generados aleatoriamente.

.. figure:: /images/random_cmaps_traj.svg
    :align: center

    Trayectorias en espacio RGB para los mapas de colores generados
    aleatoriamente.

Una idea interesante sería tomar estos mapas de colores y optimizar
algunos parámetros perceptuales como luminosidad para obtener
mapas de colores útiles.

Conclusiones
------------

Probablemente, yo usaría ``phase``, ``colorwheel``, o ``mrybm`` en
el futuro.

.. figure:: /images/toroidal_helix_phase.svg
    :align: center

    Imagen inicial usando ``phase``.

.. figure:: /images/toroidal_helix_colorwheel.svg
    :align: center

    Imagen inicial usando ``colorwheel``.

.. figure:: /images/toroidal_helix_mrybm.svg
    :align: center

    Imagen inicial usando ``mrybm``.

Referencias
-----------

1. Peter Kovesi. Good Colour Maps: How to Design Them.
   arXiv:1509.03700 [cs.GR] 2015
