.. title: Solución de la ecuación de Schrödinger usando el método de Ritz
.. slug: hermite_ritz_qm
.. date: 2017-07-11 19:04:57 UTC-05:00
.. tags: métodos variacionales, elementos finitos, polinomios de Hermite
.. category: Scientific Computing
.. type: text
.. has_math: yes

En esta publicación describimos la solcuión de la ecuación de Schrödinger
usando el método de Ritz y base de
`funciones de <https://en.wikipedia.org/wiki/Hermite_polynomials#Hermite_functions>`_
Esta base parece ser una buena elección para la ecuación de Schrödinger
ya que es una base ortogonal sobre :math:`(-\infty, \infty)`.

Transformando la ecuación en una algebraica
=============================================

Queremos resolver la 
`ecuación de Schrödinger <https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation>`_
independiente del tiempo

.. math::

    \left[-\frac{1}{2}\nabla^2 + V(x)\right] \psi = E\psi\, ,

donde estamos usando 
`unidades naturales <https://en.wikipedia.org/wiki/Natural_units>`_
ya que son una buena elección para cálculos numéricos.

Resolver esta ecuación es equivalente a resolver la siguiente
ecuación variacional

.. math::

    \delta \Pi[\psi] = 0\, ,

con

.. math::

   \Pi[\psi] = \frac{1}{2} \langle \nabla \psi, \nabla\psi\rangle +
                 \langle \psi, V(x) \psi\rangle -
                  E\langle \psi, \psi\rangle \, ,

con :math:`\psi` la función de onda, :math:`V(x)` el potencial y
:math:`E` la energía. Esta formulación variacional es equivalente a la
ecuación de Schrödinger independiente del tiempo, y :math:`E`
funciona como un multiplicador de Lagrange que garantiza que la 
probabilidad sobre todo el dominio sea 1.

Podemos expandir la función de onda en la base ortogonal

.. math:: \psi = \sum_{n=0}^N c_n u_n(x)\, ,

donde :math:`u_n(x) \equiv \mu_n H_n(x) e^{-x^2/2}` es una función de
Hermite normalizada, :math:`\mu_n` es el inverso de la magnitud del 
:math:`n`-ésimo polinomio de Hermite

.. math:: \mu_n = \frac{1}{\sqrt{\pi^{1/2} n! 2^n}}\, ,

y :math:`c_n` son los coeficientes de la expansión. Esta representación
es exacta en el límite :math:`N \rightarrow \infty`.

Si remplazamos la expansión en el funcional, obtenemos

.. math::

   \Pi_N = \sum_{m=0}^N\sum_{n=0}^N c_m c_n\left[
             \frac{1}{2} \langle \nabla u_m, \nabla u_n\rangle +
             \langle u_m, V(x) u_n\rangle -
             E^N \delta_{mn}\right]\, .

El integrando que involucra las dos derivadas sería

.. math::

   u_m' u_n' =& \left[2m \frac{\mu_{m-1}}{\mu_m}u_{m-1} - x u_m\right]
               \left[2n \frac{\mu_{n-1}}{\mu_n}u_{n-1} - x u_n\right]\\
             =& 4mn\frac{\mu_{m-1} \mu_{n-1}}{\mu_m \mu_n} u_{n-1} u_{m-1}
              - 2m\frac{\mu_{m-1}}{\mu_{m}}x u_{m-1} u_n\\
              &- 2n\frac{\mu_{n-1}}{\mu_{n}}x u_{n-1} u_m + x^2 u_m u_n

Entonces, el término de la energía cinética sería

.. math::

   \langle \nabla u_m, \nabla u_n \rangle =&
       4mn\frac{\mu_{m-1} \mu_{n-1}}{\mu_m \mu_n} \langle u_{n-1}, u_{m-1}\rangle
       - 2m\frac{\mu_{m-1}}{\mu_{m}} \langle u_{m-1}, x u_n\rangle\\
       &- 2n\frac{\mu_{n-1}}{\mu_{n}} \langle u_{m}, x u_{n - 1}\rangle
        + \langle u_m, x^2 u_n\rangle\\
       =& 4mn \frac{\mu_{m-1}^2}{\mu_m^2}\delta_{mn} -
         2m \frac{\mu_{m-1}}{\mu_m} \alpha_{m-1, n} -
         2n \frac{\mu_{n-1}}{\mu_n} \alpha_{m, n-1} + \beta_{mn} \, ,


con

.. math::

   \alpha_{m,n} \equiv \langle u_{m}, x u_n\rangle = \begin{cases}
   \sqrt{\frac{n + 1}{2}} & m=n +1\\
   \sqrt{\frac{n}{2}} & m=n - 1\\
   0 & \text{otherwise}\end{cases}\, ,

y

.. math::

   \beta_{m,n} \equiv \langle u_{m}, x^2 u_n\rangle = \begin{cases}
   \frac{\sqrt{n(n-1)}}{2} & m = n - 2\\
   \frac{2n + 1}{2} & m = n \\
   \frac{\sqrt{(n+1)(n+1)}}{2} & m = n + 2 \\
   0 & \text{otherwise}\end{cases}\, .

El funcional se reescribe como

.. math::

   \Pi_N =& \sum_{m=0}^N \sum_{n=0}^N c_m c_n
     \left[2mn \frac{\mu^2_{m-1}}{\mu^2_m}\delta_{mn}
     - m\frac{\mu_{m-1}}{\mu_m}\alpha_{m - 1, n}
     - n\frac{\mu_{n-1}}{\mu_n}\delta_{m, n-1} \right.\nonumber \\
     &\left. - \frac{1}{2}\beta_{mn} + \langle u_m, V(x) u_n\rangle
     - E^N \delta_{mn}\right] \, .

Tomando la variación

.. math:: \delta \Pi_N = 0\, ,

que en este caso es equivalente a

.. math::

    \frac{\partial \Pi_N}{\partial c_i} = 0\quad \forall i=0, 1, \cdots N\, ,

lleva a

.. math:: [H]\lbrace c\rbrace = E^N\lbrace c\rbrace \, ,

donde las componentes de la matriz :math:`[H]` están dadas por

.. math::

   H_{mn} = 2mn \frac{\mu^2_{m-1}}{\mu^2_m}\delta_{mn}
     - m\frac{\mu_{m-1}}{\mu_m}\alpha_{m - 1, n}
     - n\frac{\mu_{n-1}}{\mu_n}\delta_{m, n-1}
     - \frac{1}{2}\beta_{mn} + \langle u_m, V(x) u_n\rangle\, .

La última integral se puede calcular usando la
`cuadratura de Gauss-Hermite <https://en.wikipedia.org/wiki/Gauss%E2%80%93Hermite_quadrature>`_.
Y necesitaremos más puntos de Gauss si queremos integrar polinomios
de orden alto. Este método funciona bien para funciones que pueden
ser aproximadas por polinomios.

Ejemplos
========
Una implementación en Python de este método se puede encontrar en
`este repo <https://github.com/nicoguaro/FEM_resources/blob/master/quantum_mechanics/hermite_QM.py>`_.

Para todos los ejemplos usamos las siguientes importaciones

.. code:: ipython

    from __future__ import division, print_function
    import numpy as np
    from hermite_QM import *

`Oscilador armónico cuántico <https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator>`_
------------------------------------------------------------------------------------------
En este caso el potencial (normalizado) está dado por

.. math:: V(x) = \frac{1}{2} x^2

y los valores propios exactos normalizados son

.. math:: E_n = n + \frac{1}{2}

El siguiente bloque de código calcula los primeros 10 valores propios
y grafica los estados propios correspondientes

.. code:: ipython

    potential = lambda x: 0.5*x**2
    vals, vecs = eigenstates(potential, nterms=11, ngpts=12)
    print(np.round(vals[:10], 6))
    fig, ax = plt.subplots(1, 1)
    plot_eigenstates(vals, vecs, potential);

con resultados

.. code::

    [ 0.5  1.5  2.5  3.5  4.5  5.5  6.5  7.5  8.5  9.5]

.. image:: /images/hermite_ritz_harmonic.svg

Potencial de valor absoluto
---------------------------

.. code:: ipython

    potential = lambda x: np.abs(x)
    vals, vecs = eigenstates(potential)
    print(np.round(vals[:10], 6))
    fig, ax = plt.subplots(1, 1)
    plot_eigenstates(vals, vecs, potential, lims=(-8, 8));

con resultados

.. code::

    [ 0.811203  1.855725  2.57894   3.244576  3.826353  4.38189   4.895365
      5.396614  5.911591  6.421015]

.. image:: /images/hermite_ritz_abs.svg

Potencial cúbico
----------------

.. code:: ipython

    potential = lambda x: np.abs(x/3)**3
    vals, vecs = eigenstates(potential)
    print(np.round(vals[:10], 6))
    fig, ax = plt.subplots(1, 1)
    plot_eigenstates(vals, vecs, potential, lims=(-6, 6));

con resultados

.. code::

    [ 0.180588  0.609153  1.124594  1.681002  2.272087  2.889805  3.530901
      4.191962  4.871133  5.566413]

.. image:: /images/hermite_ritz_cubic.svg

Oscilador armónico con perturbación cuártica
--------------------------------------------

.. code:: ipython

    potential = lambda x: 0.5*x**2 + 0.1*x**4
    vals, vecs = eigenstates(potential, nterms=20, ngpts=22)
    print(np.round(vals[:10], 6))
    fig, ax = plt.subplots(1, 1)
    plot_eigenstates(vals, vecs, potential, lims=(-5, 5))

con resultados

.. code::

    [  0.559146   1.769503   3.138624   4.628884   6.220303   7.899789
       9.658703  11.489094  13.38638   15.361055]

.. image:: /images/hermite_ritz_pert_harm.svg

Un notebook de Jupyter con los ejemplos se puede encontrar
`acá <https://github.com/nicoguaro/FEM_resources/blob/master/quantum_mechanics/Ritz_Hermite_QM.ipynb>`_.
