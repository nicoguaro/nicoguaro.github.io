.. title: Numerical methods challenge: Day 3
.. slug: numerical-03
.. date: 2017-10-03 19:26:13 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, root finding
.. category:  Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Newton's method
===============

Today's method is  
`Newton's method <https://en.wikipedia.org/wiki/Newton%27s_method>`_.
This method is used to solve the equation :math:`f(x) = 0`
for :math:`x` real, and :math:`f`  a differentiable function.
It starts with an initial guess :math:`x_0` and it succesively refine it
by finding the intercept of the tangent line to the function with zero.
The new approximation is computed from the old one using

.. math::

    x_k = x_{k-1} - \frac{f(x)}{f'(x)} 


Convergence of this method is generally faster than bisection method.
Nevertheless, the convergence is not guaranteed. Another drawback is the
need of the derivative of the function.

We will use the function :math:`f(x) = \cos(x) - x` to test the codes,
and the initial guess is 1.0.

Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import abs, cos, sin

    def newton(fun, grad, x, niter=50, ftol=1e-12, verbose=False):
        msg = "Maximum number of iterations reached."
        for cont in range(niter):
            if abs(grad(x)) < ftol:
                x = None
                msg = "Derivative near to zero."
                break
            if verbose:
                print("n: {}, x: {}".format(cont, x))
            x = x - fun(x)/grad(x)
            if abs(fun(x)) < ftol:
                msg = "Root found with desired accuracy."
                break
        return x, msg


    def fun(x):
        return cos(x) - x


    def grad(x):
        return -sin(x) - 1.0


    print(newton(fun, grad, 1.0))




Julia
-----

.. code:: julia

    function newton(fun, grad, x, niter=50, ftol=1e-12, verbose=false)
        msg = "Maximum number of iterations reached."
        for cont = 1:niter
            if abs(grad(x)) < ftol
                x = nothing
                msg = "Derivative near to zero."
                break
            end
            if verbose
                println("n: $(cont), x: $(x)")
            end
            x = x - fun(x)/grad(x)
            if abs(fun(x)) < ftol
                msg = "Root found with desired accuracy."
                break
            end
        end
        return x, msg
    end


    function fun(x)
        return cos(x) - x
    end


    function grad(x)
        return -sin(x) - 1.0
    end


    println(newton(fun, grad, 1.0))



Comparison
----------

Regarding number of lines we have: 28 in Python and 32 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit newton(fun, grad, 1.0)

with result

.. code:: IPython

    10000 loops, best of 3: 27.3 µs per loop

For Julia:

.. code:: julia

    @benchmark newton(fun, grad, 1.0)

with result

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  48 bytes
      allocs estimate:  2
      --------------
      minimum time:     327.925 ns (0.00% GC)
      median time:      337.956 ns (0.00% GC)
      mean time:        351.064 ns (0.80% GC)
      maximum time:     8.118 μs (92.60% GC)
      --------------
      samples:          10000
      evals/sample:     226

