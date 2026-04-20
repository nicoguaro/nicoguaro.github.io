.. title: Numerical methods challenge: Day 2
.. slug: numerical-02
.. date: 2017-10-02 20:47:05 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, root finding
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Regula falsi
============

The second method to be considered is the 
`false position method <https://en.wikipedia.org/wiki/False_position_method>`_,
or *regula falsi*. This method is used to solve the equation :math:`f(x) = 0`
for :math:`x` real, and :math:`f` continuous. It starts with an interval
:math:`[a,b]`, where :math:`f(a)` and :math:`f(b)` should have opposite signs.
The method is similar to bisection method but instead of halving the original
interval it takes as a new point of the interval the intercept of the line
that connect the function evaluated at the two extreme points. Then, the new
point is computed from

.. math::

    c = \frac{a f(b) - b f(a)}{f(b) - f(a)}


As in bisection method, we keep the interval where the solution
appears, i.e., the sign of the function changes.

We will use the function :math:`f(x) = \cos(x) - x` to test the codes,
and the initial interval is :math:`[0.5, \pi/4]`.

Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import abs, cos, pi

    def regula_falsi(fun, a, b, niter=50, ftol=1e-12, verbose=False):
        if fun(a) * fun(b) > 0:
            c = None
            msg = "The function should have a sign change in the interval."
        else:
            for cont in range(niter):
                qa = fun(a)
                qb = fun(b)
                c = (a*qb - b*qa)/(qb - qa)
                qc = fun(c)
                if verbose:
                    print("n: {}, c: {}".format(cont, c))
                msg = "Maximum number of iterations reached."
                if abs(qc) < ftol:
                    msg = "Root found with desired accuracy."
                    break
                elif qa * qc < 0:
                    b = c
                elif qb * qc < 0:
                    a = c
        return c, msg

    def fun(x):
        return cos(x) - x

    print(regula_falsi(fun, 0.5, 0.25*pi))



Julia
-----

.. code:: julia

    function regula_falsi(fun, a, b, niter=50, ftol=1e-12, verbose=false)
        if fun(a) * fun(b) > 0
            c = nothing
            msg = "The function should have a sign change in the interval."
        else
            for cont = 1:niter
                qa = fun(a)
                qb = fun(b)
                c = (a*qb - b*qa)/(qb - qa)
                qc = fun(c)
                if verbose
                    println("n: $(cont), c: $(c)")
                end
                if abs(fun(c)) < ftol
                    msg = "Root found with desired accuracy."
                    break
                elseif qa * qc < 0
                    b = c
                elseif qb * qc < 0
                    a = c
                end
                msg = "Maximum number of iterations reached."
            end
        end
        return c, msg
    end

    function fun(x)
        return cos(x) - x
    end

    println(regula_falsi(fun, 0.5, 0.25*pi))


Comparison
----------

Regarding number of lines we have: 29 in Python and 32 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit regula_falsi(fun, 0.5, 0.25*pi)

with result

.. code:: IPython

    10000 loops, best of 3: 35.1 µs per loop

For Julia:

.. code:: julia

    @benchmark regula_falsi(fun, 0.5, 0.25*pi)

with result

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  48 bytes
      allocs estimate:  2
      --------------
      minimum time:     449.495 ns (0.00% GC)
      median time:      464.371 ns (0.00% GC)
      mean time:        493.785 ns (0.52% GC)
      maximum time:     9.723 μs (92.54% GC)
      --------------
      samples:          10000
      evals/sample:     198

