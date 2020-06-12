.. title: Numerical methods challenge: Day 14
.. slug: numerical-14
.. date: 2017-10-14 14:00:42 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, quadrature
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Trapezoidal rule
================

Today we have the `trapezoidal rule <https://en.wikipedia.org/wiki/Trapezoidal_rule>`_.
This is the simplest of `Newton-Cotes formulas <https://en.wikipedia.org/wiki/Newton%E2%80%93Cotes_formulas>`_ for numerical integration. Newton-Cotes is related to
Lagrange interpolation with equidistant points.


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np


    def trapz(y, x=None, dx=1.0):
        if x is None:
            inte = 0.5*dx*(2*np.sum(y[1:-1]) + y[0] + y[-1])
        else:
            dx = x[1:] - x[:-1]
            inte = 0.5*np.dot(y[:-1] + y[1:], dx)
        return inte


    dx = 0.001
    x = np.arange(0, 10, dx)
    y = np.sin(x)
    print(trapz(y, dx=dx))
    print(1 - np.cos(10))

with result

.. code:: python

    1.83961497726
    1.83907152908

Julia
-----

.. code:: julia

    function trapz(y; x=nothing, dx=1.0)
        if x == nothing
            inte = 0.5*dx*(2*sum(y[2:end-1]) + y[1] + y[end])
        else
            dx = x[2:end] - x[1:end-1]
            inte = 0.5* (y[1:end-1] + y[2:end])' * dx
        end
        return inte
    end


    dx = 0.001
    x = 0:dx:10
    y = sin.(x)
    println(trapz(y, dx=dx))
    println(1 - cos(10))

with results

.. code:: julia

    1.8390713758204895
    1.8390715290764525



Comparison Python/Julia
-----------------------

Regarding number of lines we have: 18 in Python and 16 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit trapz(y, dx=dx)

with result

.. code::

    100000 loops, best of 3: 16.9 µs per loop

For Julia:

.. code:: julia

    @benchmark trapz(y, dx=dx)

with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  78.31 KiB
      allocs estimate:  4
      --------------
      minimum time:     13.080 μs (0.00% GC)
      median time:      16.333 μs (0.00% GC)
      mean time:        20.099 μs (12.66% GC)
      maximum time:     963.732 μs (90.60% GC)
      --------------
      samples:          10000
      evals/sample:     1


In this case, we can say that the Python code is roughly as fast as Julia.
