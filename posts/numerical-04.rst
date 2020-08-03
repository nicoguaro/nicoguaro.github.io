.. title: Numerical methods challenge: Day 4
.. slug: numerical-04
.. date: 2017-10-04 21:30:15 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, root finding
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Newton's method: vector case
============================

Today we have 
`Newton's method <https://en.wikipedia.org/wiki/Newton%27s_method>`_
one more time. In this case, the function is vector-valued. This implies
a slight modification over the original post. The new approximation is
computed from the old one using

.. math::

    \mathbf{x}_k = \mathbf{x}_{k-1} -
        J(\mathbf{x}_k)^{-1} \mathbf{F}(\mathbf{x_k}) 

where we need to use the Jacobian matrix :math:`J`.


We will test the method with the function
:math:`\mathbf{F}(x, y) = (x + 2y - 2, x^2 + 4x - 4)`
with solution :math:`\mathbf{x} = (0, 1)`.

Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import array
    from numpy.linalg import solve, norm, det

    def newton(fun, jaco, x, niter=50, ftol=1e-12, verbose=False):
        msg = "Maximum number of iterations reached."
        for cont in range(niter):
            J = jaco(x)
            f = fun(x)
            if det(J) < ftol:
                x = None
                msg = "Derivative near to zero."
                break
            if verbose:
                print("n: {}, x: {}".format(cont, x))
            x = x - solve(J, f)
            if norm(f) < ftol:
                msg = "Root found with desired accuracy."
                break
        return x, msg


    def fun(x):
        return array([x[0] + 2*x[1] - 2, x[0]**2 + 4*x[1]**2 - 4])


    def jaco(x):
        return array([
                [1, 2],
                [2*x[0], 8*x[1]]])


    print(newton(fun, jaco, [1.0, 10.0]))






Julia
-----

.. code:: julia

    function newton(fun, jaco, x, niter=50, ftol=1e-12, verbose=false)
        msg = "Maximum number of iterations reached."
        for cont = 1:niter
            J = jaco(x)
            f = fun(x)
            if det(J) < ftol
                x = nothing
                msg = "Derivative near to zero."
                break
            end
            if verbose
                println("n: $(cont), x: $(x)")
            end
            x = x - J\f
            if norm(f) < ftol
                msg = "Root found with desired accuracy."
                break
            end
        end
        return x, msg
    end


    function fun(x)
        return [x[1] + 2*x[2] - 2, x[1]^2 + 4*x[2]^2 - 4]
    end


    function jaco(x)
        return [1.0 2.0;
                2*x[1] 8*x[2]]
    end


    println(newton(fun, jaco, [1.0, 10.0]))





Comparison
----------

Regarding number of lines we have: 31 in Python and 33 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit newton(fun, jaco, [1.0, 10.0])

with result

.. code:: IPython

    1000 loops, best of 3: 284 µs per loop

For Julia:

.. code:: julia

    @benchmark newton(fun, jaco, [1.0, 10.0])

with result

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  10.44 KiB
      allocs estimate:  192
      --------------
      minimum time:     6.818 μs (0.00% GC)
      median time:      7.167 μs (0.00% GC)
      mean time:        9.607 μs (16.53% GC)
      maximum time:     2.953 ms (97.40% GC)
      --------------
      samples:          10000
      evals/sample:     4



In this case, we can say that the Python code is roughly 40 times slower
than the Julia one. This is an improvement compared to the previous examples,
where the ratio was around 100. The reason for this "improvement" might be
in the inversion of the Jacobian, that calls a ``numpy`` routine, doing
the weight-lifting for us.
