.. title: Numerical methods challenge: Day 5
.. slug: numerical-05
.. date: 2017-10-05 13:21:41 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, root finding
.. description: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Broyden's method
================

Today we have
`Broyden's method <https://en.wikipedia.org/wiki/Broyden%27s_method>`_.
The main idea in this method is to compute the Jacobian matrix just at the
first iteration and change it for each iteration doing rank-1
updates.

.. math::

    \mathbf{x}_k = \mathbf{x}_{k-1} -
        J_n \mathbf{F}(\mathbf{x_k})

where we need estimate the Jacobian matrix at step :math:`n` by

.. math::

    \mathbf J_n = \mathbf J_{n - 1} + \frac{\Delta \mathbf f_n - \mathbf J_{n - 1} \Delta \mathbf x_n}{\|\Delta \mathbf x_n\|^2} \Delta \mathbf x_n^{\mathrm T}

that correspond to rank-1 updates of the Jacobian matrix.


We will test the method with the function
:math:`\mathbf{F}(x, y) = (x + 2y - 2, x^2 + 4x - 4)`
with solution :math:`\mathbf{x} = (0, 1)`.

Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import array, outer, dot
    from numpy.linalg import solve, norm, det

    def broyden(fun, jaco, x, niter=50, ftol=1e-12, verbose=False):
        msg = "Maximum number of iterations reached."
        J = jaco(x)
        for cont in range(niter):
            if det(J) < ftol:
                x = None
                msg = "Derivative near to zero."
                break
            if verbose:
                print("n: {}, x: {}".format(cont, x))
            f_old = fun(x)
            dx = -solve(J, f_old)
            x = x + dx
            f = fun(x)
            df = f - f_old
            J = J + outer(df - dot(J, dx), dx)/dot(dx, dx)
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


    print(broyden(fun, jaco, [1.0, 2.0]))


Julia
-----

.. code:: julia

    function broyden(fun, jaco, x, niter=50, ftol=1e-12, verbose=false)
        msg = "Maximum number of iterations reached."
        J = jaco(x)
        for cont = 1:niter
            if det(J) < ftol
                x = nothing
                msg = "Derivative near to zero."
                break
            end
            if verbose
                println("n: $(cont), x: $(x)")
            end
            f_old = fun(x)
            dx = -J\f_old
            x = x + dx
            f = fun(x)
            df = f - f_old
            J = J + (df - J*dx) * dx'/ (dx' * dx)
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
        return [1 2;
               2*x[1] 8*x[2]]
    end


    println(broyden(fun, jaco, [1.0, 2.0]))





Comparison Python/Julia
-----------------------

Regarding number of lines we have: 38 in Python and 39 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit broyden(fun, jaco, [1.0, 2.0])

with result

.. code::

    1000 loops, best of 3: 703 µs per loop

For Julia:

.. code:: julia

    @benchmark broyden(fun, jaco, [1.0, 2.0])

with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  14.41 KiB
      allocs estimate:  220
      --------------
      minimum time:     12.099 μs (0.00% GC)
      median time:      12.867 μs (0.00% GC)
      mean time:        15.378 μs (10.78% GC)
      maximum time:     3.511 ms (97.53% GC)
      --------------
      samples:          10000
      evals/sample:     1



In this case, we can say that the Python code is roughly 50 times slower
than the Julia one.

Comparison Newton/Broyden
-------------------------

Following, we are comparing Newton's and Broyden's method. We are using
the function :math:`\mathbf{x}^T \mathbf{x} + \mathbf{x}` for this test.

Python
~~~~~~

The code for the function and Jacobian is

.. code:: Python

    from numpy import diag
    fun = lambda x: x**2 + x
    jaco = lambda x: diag(2*x + 1)

and the results are:


+-----+---------------+--------------+
|  n  | Newton (μs)   | Broyden (μs) |
+-----+---------------+--------------+
|  2  |      500      |      664     |
+-----+---------------+--------------+
|  10 |      541      |      717     |
+-----+---------------+--------------+
| 100 |      3450     |     4800     |
+-----+---------------+--------------+

Julia
~~~~~

The code for the function and Jacobian is

.. code:: julia

    fun(x) = x' * x + x
    jaco(x) = diagm(2*x + 1)

and the results are:

+-----+---------------+--------------+
|  n  | Newton (μs)   | Broyden (μs) |
+-----+---------------+--------------+
|  2  |      1.76     |     1.65     |
+-----+---------------+--------------+
|  10 |     56.42     |     5.12     |
+-----+---------------+--------------+
| 100 |      1782     |      367     |
+-----+---------------+--------------+

In this case, we are comparing the mean values of the results from
``@benchmark``.
