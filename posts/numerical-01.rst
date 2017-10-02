.. title: Numerical methods challenge
.. slug: numerical-01
.. date: 2017-10-01 23:12:04 UTC-05:00
.. tags: mathjax, numerical methods, python, julia, scientific computing,
         root finding
.. category: Scientific Computing
.. link: 
.. description: 
.. type: text

For the next month I will write a program per day for some well-known numerical
methods in both Python and Julia. It is intended to be an exercise, then
don't expect the code to be good enough for real use. Also, I should mention
that I have almost no experience with Julia, so it probably won't be 
idiomatic Julia but more Python-like Julia.

Day 1: Bisection method
=======================
The first method to be considered is the 
`bisection method <https://en.wikipedia.org/wiki/Bisection_method>`_. This
method is used to solve the equation :math:`f(x) = 0` for :math:`x` real,
and :math:`f` continuous. It starts with an interval :math:`[a,b]`, where
:math:`f(a)` and :math:`f(b)` should have opposite signs. The method then
proceeds by halving the interval and selecting the one where the solution
appears, i.e., the sign of the function changes.

We will use the function :math:`f(x) = \cos(x) - x^2` to test the codes,
and the initial interval is [0, 1].

The following are the codes:

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import log2, ceil, abs, cos
    
    def bisection(fun, a, b, xtol=1e-6, ftol=1e-12):
        if fun(a) * fun(b) > 0:
            c = None
            msg = "The function should have a sign change in the interval."
        else:
            nmax = int(ceil(log2((b - a)/xtol)))
            for cont in range(nmax):
                c = 0.5*(a + b)
                if abs(fun(c)) < ftol:
                    msg = "Root found with desired accuracy."
                    break
                elif fun(a) * fun(c) < 0:
                    b = c
                elif fun(b) * fun(c) < 0:
                    a = c
                msg = "Maximum number of iterations reached."
        return c, msg
    
    def fun(x):
        return cos(x) - x**2
    
    print(bisection(fun, 0.0, 1.0))


With result

.. code:: python

    (0.824131965637207, 'Maximum number of iterations reached.')

Julia
-----
.. code:: julia

    function bisection(fun, a, b, xtol=1e-6, ftol=1e-12)
        if fun(a) * fun(b) > 0
            c = nothing
            msg = "The function should have a sign change in the interval."
        else
            nmax = ceil(log2((b - a)/xtol))
            for cont = 1:nmax
                c = 0.5*(a + b)
                if abs(fun(c)) < ftol
                    msg = "Root found with desired accuracy."
                    break
                elseif fun(a) * fun(c) < 0
                    b = c
                elseif fun(b) * fun(c) < 0
                    a = c
                end
                msg = "Maximum number of iterations reached."
            end
        end
        return c, msg
    end

    function fun(x)
        return cos(x) - x^2
    end

    println(bisection(fun, 0.0, 1.0))

With result

.. code:: julia

    (0.824131965637207, "Maximum number of iterations reached.")

In this case, both codes are really close to each other. The Python code
has 25 lines, while the Julia one has 27. As expected, the results given by
them are the same.

