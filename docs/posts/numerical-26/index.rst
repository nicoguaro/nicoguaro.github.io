.. title: Numerical methods challenge: Day 26
.. slug: numerical-26
.. date: 2017-10-26 19:15:08 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, boundary element method
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Boundary element method
=======================

Today we have the `Boundary element method <https://en.wikipedia.org/wiki/Boundary_element_method>`_
, or, an attempt. We want so solve the equation

.. math::

    \nabla^2 u = -f(x)

with

.. math::

    u(x) = g(x),\quad \forall (x, y)\in \partial \Omega


For this method, we need to use an integral representation of the equation,
that in this case is

.. math::

    u(\xi)  = \int_{S} [u(x) F(x, \xi) - q(x)G(x, \xi)]dS(x) +
              \int_{V} f(x) G(x, \xi) dV(x)


with

.. math::

    G(x,\xi)= -\frac{1}{2\pi}\ln|x- \xi|

and

.. math::

    F(x,\xi) = -\frac{1}{2\pi |x- \xi|^2}(x - \xi)\cdot\hat{n}


Then, we can form a system of equations

.. math::

    [G]\{q\} = [F]\{u\}\, ,

that we obtain by discretization of the boundary. If we take constant
variables over the discretization, the integral can be computed analytically
by

.. math::

    G_{nm} = -\frac{1}{2\pi}\left[r \sin\theta\left(\ln|r| - 1\right)
             + \theta r\cos\theta\right]^{\theta_B, r_B}_{\theta_A, r_A}

and

.. math::

    F_{nm} = \left[\frac{\theta}{2\pi}\right]^{\theta_B}_{\theta_A}

for points :math:`n` and :math:`m` in different elements, and the subindices
:math:`A,B` refer to the endpoints of the evaluation element. For diagonal
terms the integrals evaluate to


.. math::

    G_{nn} = -\frac{L}{2\pi}\left(\ln\left\vert\frac{L}{2}\right\vert - 1\right)

and

.. math::

    F_{nn} = - \frac{1}{2\pi}

with :math:`L` the size of the element.

Below is the Python code. In this case, I did not succeed and the
code is not working right now.

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    from numpy import log, sin, cos, arctan2, pi, mean, arctan
    from numpy.linalg import norm, solve
    import matplotlib.pyplot as plt


    def assem(coords, elems):
        nelems = elems.shape[0]
        Gmat = np.zeros((nelems, nelems))
        Fmat = np.zeros((nelems, nelems))
        for ev_cont, elem1 in enumerate(elems):
            print(coords[elem1[0]], coords[elem1[1]])
            for col_cont, elem2 in enumerate(elems):
                pt_col = mean(coords[elem2], axis=0)
                if ev_cont == col_cont:
                    L = norm(coords[elem1[1]] - coords[elem1[0]])
                    Gmat[ev_cont, ev_cont] = - L/(2*pi)*(log(L/2) - 1)
                    Fmat[ev_cont, ev_cont] = - 0.5
                else:
                    Gij, Fij = influence_coeff(elem1, coords, pt_col)
                    Gmat[ev_cont, col_cont] = Gij
                    Fmat[ev_cont, col_cont] = Fij
        return Gmat, Fmat


    def influence_coeff(elem, coords, pt_col):
        r_A = coords[elem[0]] - pt_col
        r_B = coords[elem[1]] - pt_col
        theta_A = arctan2(r_A[1], r_A[0])
        theta_B = arctan2(r_B[1], r_B[0])
        G_coeff = r_B[1]*(log(norm(r_B)) - 1) + theta_B*r_B[0] -\
                  (r_A[1]*(log(norm(r_A)) - 1) + theta_A*r_A[0])
        F_coeff = theta_B - theta_A
        return -G_coeff/(2*pi), F_coeff/(2*pi)


    def eval_sol(ev_coords, coords):
        nelems = elems.shape[0]
        Gmat = np.zeros((nelems, nelems))
        Fmat = np.zeros((nelems, nelems))
        for ev_cont, elem1 in enumerate(elems):
            L = norm(coords[elem1[1]] - coords[elem1[0]])
            for col_cont, elem2 in enumerate(elems):
                pt_col = mean(coords[elem2], axis=0)
                if ev_cont == col_cont:
                    Gmat[ev_cont, ev_cont] = - L/(2*pi)*(log(L/2) - 1)
                    Fmat[ev_cont, ev_cont] = - 0.5
                else:
                    Gmat[ev_cont, col_cont], Fmat[ev_cont, col_cont] = \
                        influence_coeff(elem1, coords, pt_col)

    nelems = 3
    rad = 1.0
    theta =  np.linspace(0, 2*pi, nelems, endpoint=False)
    coords = rad * np.vstack((cos(theta), sin(theta))).T
    elems = np.array([[cont, (cont + 1)%nelems] for cont in range(nelems)])
    Gmat, Fmat = assem(coords, elems)
    u_boundary = np.ones_like(theta)
    q_boundary = solve(Gmat, Fmat.dot(u_boundary))
