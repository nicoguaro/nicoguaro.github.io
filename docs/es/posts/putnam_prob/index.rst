.. title: Probabilidad de que un tetraedro en una esfera contenga su centro
.. slug: putnam_prob
.. date: 2017-12-13 15:24:52 UTC-05:00
.. tags: monte carlo, geometría computacional
.. category: Scientific Computing
.. type: text
.. has_math: yes

Me interesé en este problema viendo el canal de YouTube
`3Blue1Brown <https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw>`_,
de Grant Sanderson, donde explica una forma de abordar el problema que
es simplemente ... elegante.

Este canal me gusta mucho. Por ejemplo, su acercamiento al álgebra
lineal en `La esencia del álgebra lineal
<https://www.youtube.com/watch?v=kjBOesZCoqc&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab>`_
es realmente bueno.


El problema
===========

Entremos en materia. El problema fue originalmente parte de la
`Competencia 53 de Putnam en 1992 <http://kskedlaya.org/putnam-archive/1992.pdf>`_.
Su planteamiento es el siguiente:

    Se eligen cuatro puntos al azar en la superficie de un
    esfera. ¿Cuál es la probabilidad de que el centro de la
    la esfera se encuentra dentro del tetraedro cuyos vértices están en
    los cuatro puntos? (Se entiende que cada punto es
    elegido de forma dependiente en relación con una distribución
    uniforme en la esfera.)

Como se muestra en el video mencionado, la probabilidad es
:math:`1/8`. Vamos a escribir un algoritmo para obtener este resultado,
aproximadamente, al menos.


El enfoque propuesto.
=====================

El enfoque que vamos a utilizar es bastante sencillo. Vamos a obtener
una muestra de conjuntos aleatorios (independientes), con cuatro puntos
cada uno, y vamos a verificar cuántos satisfacen la condición de estar
adentro del tetraedro con los puntos como vértices.

Para que este enfoque funcione, necesitamos dos cosas:

1. Una forma de generar números aleatorios distribuidos uniformemente.
   Esto ya lo tenemos en ``numpy.random.uniform``, por lo que no
   necesitamos hacer mucho al respecto.

2. Una forma de verificar si un punto está dentro de un tetraedro.

Verificar que un punto está dentro de un tetraedro
--------------------------------------------------

Para encontrar si un punto está dentro de un tetraedro, podríamos calcular
sus `coordenadas barcéntricas <https://en.wikipedia.org/wiki/Barycentric_coordinate_system>`_
y verificar que todas tienen el mismo signo. Equivalentemente,
como se propone `aquí <http://steve.hollasch.net/cgindex/geometry/ptintet.html>`_,
podemos comprobar que los determinantes de las matrices

.. math::
    M_0 =
    \begin{bmatrix}
    x_0 &y_0 &z_0 &1\\
    x_1 &y_1 &z_1 &1\\
    x_2 &y_2 &z_2 &1\\
    x_3 &y_3 &z_3 &1
    \end{bmatrix}\, ,

.. math::
    M_1 =
    \begin{bmatrix}
    x &y &z &1\\
    x_1 &y_1 &z_1 &1\\
    x_2 &y_2 &z_2 &1\\
    x_3 &y_3 &z_3 &1
    \end{bmatrix}\, ,

.. math::
    M_2 =
    \begin{bmatrix}
    x_0 &y_0 &z_0 &1\\
    x &y &z &1\\
    x_2 &y_2 &z_2 &1\\
    x_3 &y_3 &z_3 &1
    \end{bmatrix}\, ,

.. math::
    M_3 =
    \begin{bmatrix}
    x_0 &y_0 &z_0 &1\\
    x_1 &y_1 &z_1 &1\\
    x &y &z &1\\
    x_3 &y_3 &z_3 &1
    \end{bmatrix}\, ,

.. math::
    M_4 =
    \begin{bmatrix}
    x_0 &y_0 &z_0 &1\\
    x_1 &y_1 &z_1 &1\\
    x_2 &y_2 &z_2 &1\\
    x &y &z &1
    \end{bmatrix}\, ,

tienen el mismo signo. En este caso, :math:`(x, y, z)` es el punto de
interés y :math:`(x_i, y_i, z_i)` son las coordenadas de cada vértice.


El algoritmo
=============

A continuación se muestra una implementación de Python del enfoque
discutido anteriormente

.. code:: python

    from __future__ import division, print_function
    from numpy import (random, pi, cos, sin, sign, hstack,
                       column_stack, logspace)
    from numpy.linalg import det
    import matplotlib.pyplot as plt


    def in_tet(x, y, z, pt):
        """
        Determina si un punto pt está al interior de
        un tetraedro con vértices x, y, z
        """
        mat0 = column_stack((x, y, z, [1, 1, 1, 1]))
        det0 = det(mat0)
        for cont in range(4):
            mat = mat0.copy()
            mat[cont] = hstack((pt, 1))
            if sign(det(mat)*det0) < 0:
                inside = False
                break
            else:
                inside = True
        return inside


    #%% Cálculo
    prob = []
    random.seed(seed=2)
    N_min = 1
    N_max = 5
    N_vals = logspace(N_min, N_max, 100, dtype=int)
    for N in N_vals:
        inside_cont = 0
        for cont_pts in range(N):
            phi = random.uniform(low=0.0, high=2*pi, size=4)
            theta = random.uniform(low=0.0, high=pi, size=4)
            x = sin(theta)*cos(phi)
            y = sin(theta)*sin(phi)
            z = cos(theta)
            if in_tet(x, y, z, [0, 0, 0]):
                inside_cont += 1

        prob.append(inside_cont/N)


    #%% Graficación
    plt.figure(figsize=(4, 3))
    plt.hlines(0.125, 10**N_min, 10**N_max, color="#3f3f3f")
    plt.semilogx(N_vals, prob, "o", alpha=0.5)
    plt.xlabel("Number of trials")
    plt.ylabel("Computed probability")
    plt.tight_layout()
    plt.show()

Como se esperaba, cuando el número de muestras es suficientemente grande,
la probabilidad estimada es cercana al valor teórico: 0,125. Esto
se puede ver en la siguiente figura.

.. image:: /images/random_tets.svg
   :width: 600 px
   :alt: Probabilidad estimada para diferentes tamaños de muestras.
   :align:  center


