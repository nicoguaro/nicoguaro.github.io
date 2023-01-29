.. title: Probability that a random tetrahedron over a sphere contains its center
.. slug: putnam_prob
.. date: 2017-12-13 15:24:52 UTC-05:00
.. tags: monte carlo, computational geometry, barycentric coordinates, probability, python
.. category: Scientific Computing
.. type: text
.. has_math: yes

I got interested in this problem watching the YouTube channel
`3Blue1Brown <https://www.youtube.com/channel/UCYO_jab_esuFRV4b17AJtAw>`_,
by Grant Sanderson, where he explains a way to tackle the problem that
is just … elegant!

I can't emphasize enough how much I like this channel. For example,
his approach to linear algebra in
`Essence of linear algebra <https://www.youtube.com/watch?v=kjBOesZCoqc&list=PLZHQObOWTQDPD3MizzM2xVFitgF8hE_ab>`_ is really
good. I mention it, just in case you don't know it.


The problem
===========

Let's talk business now. The problem was originally part of the 53rd
`Putnam competition on 1992 <http://kskedlaya.org/putnam-archive/1992.pdf>`_
and was stated as

    Four points are chosen at random on the surface of a
    sphere.   What is the probability that the center of the
    sphere lies inside the tetrahedron whose vertices are at
    the four points?  (It is understood that each point is in-
    dependently chosen relative to a uniform distribution on
    the sphere.)

As shown in the mentioned video, the probability is :math:`1/8`. Let's
come with an algorithm to obtain this result —approximately, at least.


The proposed approach
=====================

The approach that we are going to use is pretty straightforward. We are
going to obtain a sample of (independent) random sets, with four points
each, and check how many of them satisfy the condition of being inside
the tetrahedron with the points as vertices.

For this approach to work, we need two things:

1. A way to generate random numbers uniformly distributed. This is already
   in ``numpy.random.uniform``, so we don't need to do much about it.

2. A way to check if a point is inside a tetrahedron.

Checking that a point is inside a tetrahedron
---------------------------------------------

To find if a point is inside a tetrahedron, we could compute the
`barycentric coordinates <https://en.wikipedia.org/wiki/Barycentric_coordinate_system>`_
for that point and check that all of them are have the same sign. Equivalently,
as proposed `here <http://steve.hollasch.net/cgindex/geometry/ptintet.html>`_,
we can check that the determinants of the matrices

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

have the same sign. In this case, :math:`(x, y, z)` is the point of interest
and :math:`(x_i, y_i, z_i)` are the coordinates of each vertex.


The algorithm
=============

Below is a Python implementation of the approach discussed before

.. code:: python

    from __future__ import division, print_function
    from numpy import (random, pi, cos, sin, sign, hstack,
                       column_stack, logspace)
    from numpy.linalg import det
    import matplotlib.pyplot as plt


    def in_tet(x, y, z, pt):
        """
        Determine if the point pt is inside the
        tetrahedron with vertices coordinates x, y, z
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


    #%% Computation
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


    #%% Plotting
    plt.figure(figsize=(4, 3))
    plt.hlines(0.125, 10**N_min, 10**N_max, color="#3f3f3f")
    plt.semilogx(N_vals, prob, "o", alpha=0.5)
    plt.xlabel("Number of trials")
    plt.ylabel("Computed probability")
    plt.tight_layout()
    plt.show()

As expected, when the number of samples is sufficiently large, the
estimated probability is close to the theoretical value: 0.125. This
can be seen in the following figure.

.. image:: /images/random_tets.svg
   :width: 600 px
   :alt: Computed probability for different sample sizes
   :align:  center


