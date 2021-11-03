.. title: Numerical methods challenge: Day 23
.. slug: numerical-23
.. date: 2017-10-23 20:30:03 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, ritz method
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Ritz method
===========

Today we have the `Ritz method <https://en.wikipedia.org/wiki/Ritz_method>`_
to solve the equation:

.. math::

    \frac{d^2 u}{dx^2} = f(x)

with

.. math::

    u(0) = u(1)  = 0

The method consist in forming a functional that is *equivalent* to the
differential equation, propose an approximation as a linear combination of
a set of basis functions and find the *best* set of coefficients for that
combination. That *best* solution is found minimizing the functional.

The functional for this differential equation is

.. math::

    \Pi[u] = -\int_{0}^{1} \left(\frac{d u}{d x}\right)^2 dx
             -\int_{0}^{1}  u f(x) dx

In this case, we are using the approximation

.. math::
    \hat{u}(x) = x (1 - x)\sum_{n=0}^{N} c_n x^n\, ,

where we picked the factor :math:`x (1 - x)` to enforce that the basis
functions satisfy the boundary conditions. The approximated functional
reads

.. math::

    \Pi[\hat{u}] = -\sum_{n=0}^{N} \sum_{m=0}^{N} c_n c_m
        \left[\frac{2 + 2m + 2n + 2mn}{(n + m + 1)(n + m + 2)(n + m +3)}\right]
        -\\ \sum_{n=0}^{N} c_n\int_{0}^{1} x^{n + 1}(1 - x) f(x) dx

where, in general, we will need to perform numerical integration for the
second term.

Minimizing the functional

.. math::

    \frac{\partial \Pi[\hat{u}]}{\partial c_m} = 0\, ,

we obtain the system of equations

.. math::

    [K]\{\mathbf{c}\} = \{\mathbf{b}\}

with

.. math::

    K_{mn} = \frac{2 + 2m + 2n + 2mn}{(n + m + 1)(n + m + 2)(n + m +3)}

and

.. math::

    b_m = -\int_{0}^{1} x^{m + 1}(1 - x) f(x) dx\, .

We will test the implementation with the function :math:`f(x) = x^3`, that
leads to the solution

.. math::

    u(x) = \frac{x (x^4 - 1)}{20}


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    from scipy.integrate import quad
    from scipy.linalg import solve
    import matplotlib.pyplot as plt


    def ritz(N, source):
        stiff_mat = np.zeros((N, N))
        rhs = np.zeros((N))
        for row in range(N):
            for col in range(N):
                numer = (2 + 2*row + 2*col + 2*row*col)
                denom = (row + col + 1) * (row + col + 2) * (row + col + 3)
                stiff_mat[row, col] = numer/denom
            fun = lambda x: x**(row + 1)*(1 - x)*source(x)
            rhs[row], _ = quad(fun, 0, 1)
        return stiff_mat, rhs


    N = 2
    source = lambda x: x**3
    mat, rhs = ritz(N, source)
    c = solve(mat, -rhs)
    x = np.linspace(0, 1, 100)
    y = np.zeros_like(x)
    for cont in range(N):
        y += c[cont]*x**(cont + 1)*(1 - x)

    #%% Plotting
    plt.figure(figsize=(4, 3))
    plt.plot(x, y)
    plt.plot(x, x*(x**4 - 1)/20, linestyle="dashed")
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    plt.legend(["Ritz solution", "Exact solution"])
    plt.tight_layout()
    plt.show()




Julia
-----

.. code:: julia

    using PyPlot


    function ritz(N, source)
        stiff_mat = zeros(N, N)
        rhs = zeros(N)
        for row in 0:N-1
            for col in 0:N-1
                numer = (2 + 2*row + 2*col + 2*row*col)
                denom = (row + col + 1) * (row + col + 2) * (row + col + 3)
                stiff_mat[row + 1, col + 1] = numer/denom
            end
            fun(x) = x^(row + 1)*(1 - x)*source(x)
            rhs[row + 1], _  = quadgk(fun, 0, 1)
        end
        return stiff_mat, rhs
    end


    N = 2
    source(x) = x^3
    mat, rhs = ritz(N, source)
    c = -mat\rhs
    x = linspace(0, 1, 100)
    y = zeros(x)
    for cont in 0:N - 1
        y += c[cont + 1]*x.^(cont + 1).*(1 - x)
    end

    #%% Plotting
    figure(figsize=(4, 3))
    plot(x, y)
    plot(x, x.*(x.^4 - 1)/20, linestyle="dashed")
    xlabel(L"$x$")
    ylabel(L"$y$")
    legend(["Ritz solution", "Exact solution"])
    tight_layout()
    show()

Both have (almost) the same result, as follows

.. image:: /images/ritz.svg
   :width: 400 px
   :alt: Ritz method approximation using 2 terms.
   :align:  center

And if we consider 3 terms in the expansion, we get

.. image:: /images/ritz-N-3.svg
   :width: 400 px
   :alt: Ritz method approximation using 3 terms.
   :align:  center


Comparison Python/Julia
-----------------------

Regarding number of lines we have: 38 in Python and 38 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %%timeit
    mat, rhs = ritz(5, source)
    c = solve(mat, -rhs)

with result

.. code::

     1000 loops, best of 3: 228 µs per loop


For Julia:

.. code:: julia

    function bench()
       mat, rhs = ritz(N, source)
       c = -mat\rhs
    end
    @benchmark bench()




with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  6.56 KiB
      allocs estimate:  340
      --------------
      minimum time:     13.527 μs (0.00% GC)
      median time:      15.927 μs (0.00% GC)
      mean time:        17.133 μs (4.50% GC)
      maximum time:     2.807 ms (97.36% GC)
      --------------
      samples:          10000
      evals/sample:     1

In this case, we can say that the Python code is roughly 14 times slower than
Julia.
