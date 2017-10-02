.. title: Solution of the Schrödinger equation using Ritz method
.. slug: hermite_ritz_qm
.. date: 2017-07-11 19:04:57 UTC-05:00
.. tags: variational methods, finite elements, Hermite polynomials, mathjax
.. category: Scientific Computing
.. link:
.. description:
.. type: text

In this post, we describe the solution of the Schrödinger equation
using Ritz method and `Hermite functions <https://en.wikipedia.org/wiki/Hermite_polynomials#Hermite_functions>`_
basis. This basis seems to be
a good choice for the 1D Schrödinger equation since its an orthogonal
basis over :math:`(-\infty, \infty)`.

Transforming the equation to an algebraic one
=============================================

We want so solve the time-independent
`Schrödinger equation <https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation>`_

.. math ::

   \left[\frac{1}{2}\nabla^2 + V(x)\right] \psi = E\psi\, ,

where we are using
`natural units <https://en.wikipedia.org/wiki/Natural_units>`_
since they are a good choice for numeric calculations.

Solving equation is equivalent to solve the following
variational equation

.. math:: \delta \Pi[\psi] = 0\, ,

with

.. math::

   \Pi[\psi] = \frac{1}{2} \langle \nabla \psi, \nabla\psi\rangle +
                 \langle \psi, V(x) \psi\rangle -
                  E\langle \psi, \psi\rangle \, ,

being :math:`\psi` the wave function, :math:`V(x)` the potential and
:math:`E` the energy. This variational formulation is equivalent to the
time-independent Schrödinger equation, and :math:`E` works as a Lagrange
multiplier to enforce that the probability over the whole domain is 1.


We can expand the wave function in an orthonormal basis, namely

.. math:: \psi = \sum_{n=0}^N c_n u_n(x)\, ,

where :math:`u_n(x) \equiv \mu_n H_n(x) e^{-x^2/2}` is a normalized
Hermite function, :math:`\mu_n` is the inverse of magnitude of the
:math:`n`\ th Hermite polynomial

.. math:: \mu_n = \frac{1}{\sqrt{\pi^{1/2} n! 2^n}}\, ,

and :math:`c_n` are the coefficients of the expansion. This
representation is exact in the limit :math:`N \rightarrow \infty`.

If we replace the expansion in the functional, we obtain

.. math::

   \Pi_N = \sum_{m=0}^N\sum_{n=0}^N c_m c_n\left[
             \frac{1}{2} \langle \nabla u_m, \nabla u_n\rangle +
             \langle u_m, V(x) u_n\rangle -
             E^N \delta_{mn}\right]\, .

The integrand of the integral involving the two derivatives reads

.. math::

   u_m' u_n' =& \left[2m \frac{\mu_{m-1}}{\mu_m}u_{m-1} - x u_m\right]
               \left[2n \frac{\mu_{n-1}}{\mu_n}u_{n-1} - x u_n\right]\\
             =& 4mn\frac{\mu_{m-1} \mu_{n-1}}{\mu_m \mu_n} u_{n-1} u_{m-1}
              - 2m\frac{\mu_{m-1}}{\mu_{m}}x u_{m-1} u_n\\
              &- 2n\frac{\mu_{n-1}}{\mu_{n}}x u_{n-1} u_m + x^2 u_m u_n


Thus, the kinetic energy term reads

.. math::

   \langle \nabla u_m, \nabla u_n \rangle =&
       4mn\frac{\mu_{m-1} \mu_{n-1}}{\mu_m \mu_n} \langle u_{n-1}, u_{m-1}\rangle
       - 2m\frac{\mu_{m-1}}{\mu_{m}} \langle u_{m-1}, x u_n\rangle\\
       &- 2n\frac{\mu_{n-1}}{\mu_{n}} \langle u_{m}, x u_{n - 1}\rangle
        + \langle u_m, x^2 u_n\rangle\\
       =& 4mn \frac{\mu_{m-1}^2}{\mu_m^2}\delta_{mn} -
         2m \frac{\mu_{m-1}}{\mu_m} \alpha_{m-1, n} -
         2n \frac{\mu_{n-1}}{\mu_n} \alpha_{m, n-1} + \beta_{mn} \, ,


with

.. math::

   \alpha_{m,n} \equiv \langle u_{m}, x u_n\rangle = \begin{cases}
   \sqrt{\frac{n + 1}{2}} & m=n +1\\
   \sqrt{\frac{n}{2}} & m=n - 1\\
   0 & \text{otherwise}\end{cases}\, ,

and

.. math::

   \beta_{m,n} \equiv \langle u_{m}, x^2 u_n\rangle = \begin{cases}
   \frac{\sqrt{n(n-1)}}{2} & m = n - 2\\
   \frac{2n + 1}{2} & m = n \\
   \frac{\sqrt{(n+1)(n+1)}}{2} & m = n + 2 \\
   0 & \text{otherwise}\end{cases}\, .

The functional is rewritten as

.. math::

   \Pi_N =& \sum_{m=0}^N \sum_{n=0}^N c_m c_n
     \left[2mn \frac{\mu^2_{m-1}}{\mu^2_m}\delta_{mn}
     - m\frac{\mu_{m-1}}{\mu_m}\alpha_{m - 1, n}
     - n\frac{\mu_{n-1}}{\mu_n}\delta_{m, n-1} \right.\nonumber \\
     &\left. - \frac{1}{2}\beta_{mn} + \langle u_m, V(x) u_n\rangle
     - E^N \delta_{mn}\right] \, .

Taking the variation

.. math:: \delta \Pi_N = 0\, ,

that in this case is equivalent to

.. math::

    \frac{\partial \Pi_N}{\partial c_i} = 0\quad \forall i=0, 1, \cdots N\, ,

yields to

.. math:: [H]\lbrace c\rbrace = E^N\lbrace c\rbrace \, ,

where the components of the matrix :math:`[H]` are given by

.. math::

   H_{mn} = 2mn \frac{\mu^2_{m-1}}{\mu^2_m}\delta_{mn}
     - m\frac{\mu_{m-1}}{\mu_m}\alpha_{m - 1, n}
     - n\frac{\mu_{n-1}}{\mu_n}\delta_{m, n-1}
     - \frac{1}{2}\beta_{mn} + \langle u_m, V(x) u_n\rangle\, .

The last integral can be computed using
`Gauss-Hermite quadrature <https://en.wikipedia.org/wiki/Gauss%E2%80%93Hermite_quadrature>`_.
And we will need more Gauss points if we want to integrate higher-order
polynomials. This method would work fine for functions that can be
approximated by polynomials.

Examples
========
A Python implementation of this method is presented in
`this repo <https://github.com/nicoguaro/FEM_resources/blob/master/quantum_mechanics/hermite_QM.py>`_.

For all the examples we use the following imports

.. code:: ipython

    from __future__ import division, print_function
    import numpy as np
    from hermite_QM import *

`Quantum harmonic oscilator <https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator>`_
-----------------------------------------------------------------------------------------
In this case the (normalized) potential is given by

.. math:: V(x) = \frac{1}{2} x^2

and the exact normalized eigenvalues are given by

.. math:: E_n = n + \frac{1}{2}

The following snippet computes the first 10 eigenvalues and plot
the corresponding eigenstates

.. code:: ipython

    potential = lambda x: 0.5*x**2
    vals, vecs = eigenstates(potential, nterms=11, ngpts=12)
    print(np.round(vals[:10], 6))
    fig, ax = plt.subplots(1, 1)
    plot_eigenstates(vals, vecs, potential);

with results

.. code::

    [ 0.5  1.5  2.5  3.5  4.5  5.5  6.5  7.5  8.5  9.5]

.. image:: /images/hermite_ritz_harmonic.svg

Absolute value potential
------------------------

.. code:: ipython

    potential = lambda x: np.abs(x)
    vals, vecs = eigenstates(potential)
    print(np.round(vals[:10], 6))
    fig, ax = plt.subplots(1, 1)
    plot_eigenstates(vals, vecs, potential, lims=(-8, 8));

with results

.. code::

    [ 0.811203  1.855725  2.57894   3.244576  3.826353  4.38189   4.895365
      5.396614  5.911591  6.421015]

.. image:: /images/hermite_ritz_abs.svg

Cubic potential
---------------

.. code:: ipython

    potential = lambda x: np.abs(x/3)**3
    vals, vecs = eigenstates(potential)
    print(np.round(vals[:10], 6))
    fig, ax = plt.subplots(1, 1)
    plot_eigenstates(vals, vecs, potential, lims=(-6, 6));

with results

.. code::

    [ 0.180588  0.609153  1.124594  1.681002  2.272087  2.889805  3.530901
      4.191962  4.871133  5.566413]

.. image:: /images/hermite_ritz_cubic.svg


Harmonic with quartic perturbation
----------------------------------

.. code:: ipython

    potential = lambda x: 0.5*x**2 + 0.1*x**4
    vals, vecs = eigenstates(potential, nterms=20, ngpts=22)
    print(np.round(vals[:10], 6))
    fig, ax = plt.subplots(1, 1)
    plot_eigenstates(vals, vecs, potential, lims=(-5, 5))

with results

.. code::

    [  0.559146   1.769503   3.138624   4.628884   6.220303   7.899789
       9.658703  11.489094  13.38638   15.361055]

.. image:: /images/hermite_ritz_pert_harm.svg

A Jupyter Notebook with the examples can be found
`here <https://github.com/nicoguaro/FEM_resources/blob/master/quantum_mechanics/Ritz_Hermite_QM.ipynb>`_.


