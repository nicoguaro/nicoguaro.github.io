.. title: Numerical methods challenge: Day 15
.. slug: numerical-15
.. date: 2017-10-17 16:22:06 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, quadrature
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Simpson's rule
==============

Today we have the `Simpson's rule <https://en.wikipedia.org/wiki/Simpson%27s_rule>`_.
This is another `Newton-Cotes formulas <https://en.wikipedia.org/wiki/Newton%E2%80%93Cotes_formulas>`_, used for numerical integration. Newton-Cotes is related to
Lagrange interpolation with equidistant points.


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np


    def simps(y, x=None, dx=1.0):
        n = len(y)
        if x is None:
            inte = np.sum(y[0:n-2:2] + 4*y[1:n-1:2] + y[2:n:2])*dx
        else:
            dx = x[1::2] - x[:-1:2]
            inte = np.dot(y[0:n-2:2] + 4*y[1:n-1:2] + y[2:n:2], dx)
        return inte/3


    n = 21
    x = np.linspace(0, 10, n)
    y = np.sin(x)
    print(simps(y, x=x))
    print(1 - np.cos(10))


with result

.. code:: python

    1.8397296125
    1.83907152908

Julia
-----

.. code:: julia

    function simps(y; x=nothing, dx=1.0)
        n = length(y)
        if x == nothing
            inte = sum(y[1:2:n-2] + 4*y[2:2:n-1] + y[3:2:n])*dx
        else
            dx = x[2:2:end] - x[1:2:end-1]
            inte = (y[1:2:n-2] + 4*y[2:2:n-1] + y[3:2:n])' * dx
        end
        return inte/3
    end


    n = 21
    x = linspace(0, 10, n)
    y = sin.(x)
    println(simps(y, x=x))
    println(1 - cos(10))


.. code:: julia

    1.8397296124951257
    1.8390715290764525


Comparison Python/Julia
-----------------------

Regarding number of lines we have: 19 in Python and 17 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit simps(y, x=x)

with result

.. code::

    100000 loops, best of 3: 13.8 µs per loop

For Julia:

.. code:: julia

    @benchmark simps(y, x=x)


with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  1.23 KiB
      allocs estimate:  14
      --------------
      minimum time:     1.117 μs (0.00% GC)
      median time:      1.200 μs (0.00% GC)
      mean time:        1.404 μs (7.04% GC)
      maximum time:     222.286 μs (96.45% GC)
      --------------
      samples:          10000
      evals/sample:     10


In this case, we can say that the Python code is 10 times slower than Julia.
