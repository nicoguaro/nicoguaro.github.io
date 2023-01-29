.. title: Reto de métodos numéricos: Día 26
.. slug: numerical-26
.. date: 2017-10-26 19:15:08 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, método de elementos de frontera
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Método de elementos de frontera
===============================

Hoy tenemos el `método de elementos de frontera
<https://en.wikipedia.org/wiki/Boundary_element_method>`_, o, un intento de él.
Queremos resolver la ecuación

.. math::

    \nabla^2 u = -f(x)

con

.. math::

    u(x) = g(x),\quad \forall (x, y)\in \partial \Omega

Para este método, necesitamos la repreentación integral de la ecuación, que 
en este caso es

.. math::

    u(\xi)  = \int_{S} [u(x) F(x, \xi) - q(x)G(x, \xi)]dS(x) +
              \int_{V} f(x) G(x, \xi) dV(x)


con

.. math::

    G(x,\xi)= -\frac{1}{2\pi}\ln|x- \xi|

y

.. math::

    F(x,\xi) = -\frac{1}{2\pi |x- \xi|^2}(x - \xi)\cdot\hat{n}


Entonces, podemos formar el sistema de ecuaciones

.. math::

    [G]\{q\} = [F]\{u\}\, ,

Que obtenemos de discretizar la frontera. Si tomamos variables constantes a lo
largo de la discretización, las integrales se pueden calcular analíticamente

.. math::

    G_{nm} = -\frac{1}{2\pi}\left[r \sin\theta\left(\ln|r| - 1\right)
             + \theta r\cos\theta\right]^{\theta_B, r_B}_{\theta_A, r_A}

y

.. math::

    F_{nm} = \left[\frac{\theta}{2\pi}\right]^{\theta_B}_{\theta_A}

para :math:`n` y :math:`m` en diferentes elementos, y los subíndices
:math:`A,B` se refieren a los puntos finales del elemento a evaluar.
Para los términos en la diagonal las integrales son


.. math::

    G_{nn} = -\frac{L}{2\pi}\left(\ln\left\vert\frac{L}{2}\right\vert - 1\right)

y

.. math::

    F_{nn} = - \frac{1}{2\pi}

con :math:`L`, el tamaño del elemento.

A continuación se muestra el código de Python. En este caso, no tuve éxito en 
hacer que el código funcionara.

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
