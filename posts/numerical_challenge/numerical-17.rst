.. title: Numerical methods challenge: Day 17
.. slug: numerical-17
.. date: 2017-10-17 16:29:05 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, ode
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Euler method
============

Today we have the `Euler method <https://en.wikipedia.org/wiki/Euler_method>`_.
Which is the simplest of `Runge-Kutta methods
<https://en.wikipedia.org/wiki/Runge%E2%80%93Kutta_method>`_, and was named after
Leonhard Euler who used in the 18th century.

The method consist in making updates of the function using the slope
value with the formula

.. math::

    y_{n + 1} = y_n + hf(t_n, y_n)


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt


    def euler(dydt, y0, t, args=()):
        ndof = len(y0)
        ntimes = len(t)
        y = np.zeros((ndof, ntimes))
        y[:, 0] = y0
        for cont in range(1, ntimes):
            h = t[cont] - t[cont - 1]
            y[:, cont] = y[:, cont - 1] + h*dydt(y[:, cont - 1], t[cont], *args)
        return y


    def pend(y, t, b, c):
        theta, omega = y
        dydt = [omega, -b*omega - c*np.sin(theta)]
        return np.array(dydt)


    b = 0.25
    c = 5.0
    y0 = [np.pi - 0.1, 0.0]
    t = np.linspace(0, 10, 10001)
    y = euler(pend, y0, t, args=(b, c))
    plt.plot(t, y[0, :])
    plt.plot(t, y[1, :])
    plt.xlabel(r"$t$")
    plt.legend([r"$\theta(t)$", r"$\omega(t)$"])
    plt.show()



Julia
-----

.. code:: julia

    using PyPlot


    function euler(dydt, y0, t; args=())
        ndof = length(y0)
        ntimes = length(t)
        y = zeros(ndof, ntimes)
        y[:, 1] = y0
        for cont = 2:ntimes
            h = t[cont] - t[cont - 1]
            y[:, cont] = y[:, cont - 1] + h*dydt(y[:, cont - 1], t[cont], args...)
        end
        return y
    end


    function pend(y, t, b, c)
        theta, omega = y
        dydt = [omega, -b*omega - c*sin(theta)]
        return dydt
    end


    b = 0.25
    c = 5.0
    y0 = [pi - 0.1, 0.0]
    t = linspace(0, 10, 1001)
    y = euler(pend, y0, t, args=(b, c))
    plot(t, y[1, :])
    plot(t, y[2, :])
    xlabel(L"$t$")
    legend([L"$\theta(t)$", L"$\omega(t)$"])
    show()


In both cases the result is the following plot

.. image:: /images/euler.svg
   :width: 500 px
   :alt: Solution for a pendulum using Euler method.
   :align:  center



Comparison Python/Julia
-----------------------

Regarding number of lines we have: 32 in Python and 33 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit euler(pend, y0, t, args=(b, c))

with result

.. code::

    100 loops, best of 3: 18.5 ms per loop

For Julia:

.. code:: julia

    @benchmark euler(pend, y0, t, args=(b, c))


with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  648.33 KiB
      allocs estimate:  15473
      --------------
      minimum time:     366.236 μs (0.00% GC)
      median time:      399.615 μs (0.00% GC)
      mean time:        486.364 μs (16.96% GC)
      maximum time:     4.613 ms (80.26% GC)
      --------------
      samples:          10000
      evals/sample:     1



In this case, we can say that the Python code is roughly 40 times slower than Julia.
