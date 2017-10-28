.. title: Numerical methods challenge: Day 27
.. slug: numerical-27
.. date: 2017-10-27 21:27:06 UTC-05:00
.. tags: mathjax, numerical methods, python, julia, scientific computing, finite element method
.. category:
.. link:
.. description:
.. type: text

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Monte Carlo integration
=======================

Today we have `Monte Carlo integration <https://en.wikipedia.org/wiki/Monte_Carlo_integration>`_.
Where we use random sampling to numerically compute an integral. This
method is important when we want to evaluate higher-dimensional
integrals since common quadrature techniques imply an exponential
growing in the number of sampling points.

The method computes an integral

.. math::

    I = \int_\Omega f(x) dx

where :math:`\Omega` has volume :math:`V`.

The integral is approximated as

.. math::

    I \approx \frac{V}{N} \sum_{i=1}^{N} f(x_i)

where the :math:`x_i` distribute uniform over :math:`\Omega`.


Following are the codes

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np


    def monte_carlo_int(fun, N, low, high, args=()):
        ndims = len(low)
        pts = np.random.uniform(low=low, high=high, size=(N, ndims))
        V = np.prod(np.asarray(high) - np.asarray(low))
        return V*np.sum(fun(pts, *args))/N


    def circ(x, rad):
        return 0.5*(1 - np.sign(x[:, 0]**2 + x[:, 1]**2 - rad**2))


    N = 1000000
    low = [-1, -1]
    high = [1, 1]
    rad = 1
    inte = monte_carlo_int(circ, N, low, high, args=(rad,))


Julia
-----

.. code:: julia

    using Distributions


    function monte_carlo_int(fun, N, low, high; args=())
        ndims = length(low)
        pts = rand(Uniform(0, 1), N, ndims)
        for cont = 1:ndims
            pts[:, cont] = pts[:, cont]*(high[cont] - low[cont]) + low[cont]
        end
        V = prod(high - low)
        return V*sum(fun(pts, args...))/N
    end


    function circ(x, rad)
        return 0.5*(1 - sign.(x[:, 1].^2 + x[:, 2].^2 - rad^2))
    end


    N = 1000000
    low = [-1, -1]
    high = [1, 1]
    rad = 1
    inte = monte_carlo_int(circ, N, low, high, args=(rad,))


One of the most common examples is the computation of :math:`\pi`, this
is illustrated in the following animation.

.. image:: https://upload.wikimedia.org/wikipedia/commons/8/84/Pi_30K.gif
   :width: 500 px
   :alt: Finite element method approximation.
   :align:  center


Comparison Python/Julia
-----------------------

Regarding number of lines we have: 20 in Python and 24 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit monte_carlo_int(circ, N, low, high, args=(rad,))

with result

.. code::

     10 loops, best of 3: 53.2 ms per loop


For Julia:

.. code:: julia

    @benchmark FEM1D(x, fun)


with result

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  129.70 MiB
      allocs estimate:  46
      --------------
      minimum time:     60.131 ms (5.15% GC)
      median time:      164.018 ms (55.64% GC)
      mean time:        204.366 ms (49.50% GC)
      maximum time:     357.749 ms (64.04% GC)
      --------------
      samples:          25
      evals/sample:     1



In this case, we can say that the Python code is roughly 3 times faster than
Julia code.
