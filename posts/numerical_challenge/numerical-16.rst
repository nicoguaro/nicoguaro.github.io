.. title: Numerical methods challenge: Day 16
.. slug: numerical-16
.. date: 2017-10-17 16:29:00 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, quadrature
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Clenshaw-Curtis quadrature
==========================

Today we have the `Clenshaw-Curtis quadrature
<https://en.wikipedia.org/wiki/Clenshaw%E2%80%93Curtis_quadrature>`_.
This method is based in the expansion of the integrand in
`Chebyshev polynomials <https://en.wikipedia.org/wiki/Chebyshev_polynomials>`_.

We will test the quadrature with the integral

.. math::
    \int_0^3 e^{-x^2} \mathrm{d}x \approx 0.8862073482595214


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import linspace, cos, pi, exp, sum


    def clenshaw_curtis(fun, N=10, a=-1, b=1):
        nodes = linspace(-1, 1, N + 1)*pi
        jac = 0.5*(b - a)
        tfun = lambda x: fun(a + jac*(x + 1))
        inte = 0
        for k in range(0, N + 1, 2):
            coef = 1/N*(tfun(1) + tfun(-1)*(-1)**k +\
                2*sum(tfun(cos(nodes[1:-1]))*cos(k*nodes[1:-1])))
            if k == 0:
                inte += coef
            elif k == N:
                inte += coef/(1 - N**2)
            else:
                inte += 2*coef/(1 - k**2)
        return inte*jac

    N = 100
    fun = lambda x: exp(-x**2)
    print(clenshaw_curtis(fun, N=N, a=0, b=3))




with result

.. code:: python

    0.885906202792

Julia
-----

.. code:: julia

    function clenshaw_curtis(fun; N=50, a=-1, b=1)
        nodes = linspace(-1, 1, N + 1)*pi
        jac = 0.5*(b - a)
        tfun(x) = fun(a + jac*(x + 1))
        inte = 0
        for k = 0:2:N
            coef = 1/N*(tfun(1) + tfun(-1)*(-1)^k +
                2*sum(tfun(cos.(nodes[2:end-1])).*cos.(k*nodes[2:end-1])))
            if k == 0
                inte += coef
            elseif k == N
                inte += coef/(1 - N^2)
            else
                inte += 2*coef/(1 - k^2)
            end
        end
        return inte*jac
    end

    N = 100
    fun(x) = exp.(-x.^2)
    print(clenshaw_curtis(fun, N=N, a=0, b=3))


with result

.. code:: julia

    0.8859062027920102



Comparison Python/Julia
-----------------------

Regarding number of lines we have: 24 in Python and 23 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit -n 10000 clenshaw_curtis(fun, N=N, a=0, b=3)

with result

.. code::

    10000 loops, best of 3: 2.4 ms per loop

For Julia:

.. code:: julia

    @benchmark clenshaw_curtis(fun, N=N, a=0, b=3)


with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  359.56 KiB
      allocs estimate:  565
      --------------
      minimum time:     381.676 μs (0.00% GC)
      median time:      388.497 μs (0.00% GC)
      mean time:        413.471 μs (1.77% GC)
      maximum time:     1.298 ms (49.07% GC)
      --------------
      samples:          10000
      evals/sample:     1


In this case, we can say that the Python code is roughly 6 times slower than Julia.
