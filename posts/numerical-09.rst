.. title: Numerical methods challenge: Day 9
.. slug: numerical-09
.. date: 2017-10-09 21:17:56 UTC-05:00
.. tags: mathjax, numerical methods, python, julia, scientific computing, interpolation
.. category: Scientific Computing
.. link:
.. description:
.. type: text


During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Lagrange interpolation
======================

Today we have
`Lagrange interpolation <https://en.wikipedia.org/wiki/Lagrange_polynomial>`_.
This is defined by

.. math::

    L(x) = \sum_{j=0}^{k} y_j \prod_{m\neq j}\frac{x - x_m}{x_j - x_m}

with :math:`x` the point/points where we want to interpolate.


We will test the method with a sigmoid

.. math::

    f(x) = \frac{1}{1 + e^{-x}}


Following are the codes.

Python
------

.. code:: python

    from __future__ import division
    from numpy import zeros_like, linspace, exp, prod
    import matplotlib.pyplot as plt


    def lagrange(x_int, y_int, x_new):
        y_new = zeros_like(x_new)
        for xi, yi in zip(x_int, y_int):
            y_new += yi*prod([(x_new - xj)/(xi - xj)
                             for xj in x_int if xi!=xj], axis=0)
        return y_new


    x_int = linspace(-5, 5, 11)
    y_int = 1/(1 + exp(-x_int))
    x_new = linspace(-5, 5, 1000)
    y_new = lagrange(x_int, y_int, x_new)
    plt.plot(x_int, y_int, "ok")
    plt.plot(x_new, y_new)
    plt.show()



Julia
-----

.. code:: julia

    using PyPlot

    function lagrange(x_int, y_int, x_new)
        y_new = zeros(x_new)
        for (xi, yi) in zip(x_int, y_int)
            prod = ones(x_new)
            for xj in x_int
                if xi != xj
                    prod = prod.* (x_new - xj)/(xi - xj)
                end
            end
            y_new += yi*prod
        end
        return y_new
    end


    x_int = linspace(-5, 5, 11)
    y_int = 1./(1 + exp.(-x_int))
    x_new = linspace(-5, 5, 1000)
    y_new = lagrange(x_int, y_int, x_new)
    plot(x_int, y_int, "ok")
    plot(x_new, y_new)


In both cases the result is the following plot.

.. image:: /images/lagrange_interp.svg
   :width: 400 px
   :alt: Lagrange interpolation.
   :align:  center


Comparison Python/Julia
-----------------------

Regarding number of lines we have: 34 in Python and 37 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit lagrange(x_int, y_int, x_new)

with result

.. code::

    1000 loops, best of 3: 1.55 ms per loop

For Julia:

.. code:: julia

    @benchmark newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0])

with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  1.97 MiB
      allocs estimate:  254
      --------------
      minimum time:     737.665 μs (0.00% GC)
      median time:      811.633 μs (0.00% GC)
      mean time:        916.450 μs (10.77% GC)
      maximum time:     3.119 ms (64.40% GC)
      --------------
      samples:          5433
      evals/sample:     1


In this case, we can say that the Python code is roughly 2 times slower
than the Julia one, where probably I am not using the best approach for
Julia.
