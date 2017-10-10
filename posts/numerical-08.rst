.. title: Numerical methods challenge: Day 8
.. slug: numerical-08
.. date: 2017-10-09 16:15:50 UTC-05:00
.. tags: mathjax, numerical methods, python, julia, scientific computing, optimization
.. category: Scientific Computing
.. link:
.. description:
.. type: text

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Newton's method for optimization
================================

Today we have
`Newton's method <https://en.wikipedia.org/wiki/Newton%27s_method_in_optimization>`_
for optimization. The main difference of this method with gradient descent
is the use of higher derivatives, namely, the Hessian matrix of the
objective function. The use of higher derivatives provides information of
the curvature besides the slope information used in gradient descent.
The following image compare the path for gradient descent (green) and
Newton's method (red).

.. image:: https://upload.wikimedia.org/wikipedia/commons/d/da/Newton_optimization_vs_grad_descent.svg
   :width: 400 px
   :alt: Comparison of the path followed by gradient descent and Newton's method.
   :align:  center

Mathematically, the update is written as

.. math::

    \mathbf{x}_k = \mathbf{x}_{k-1} -
        H(\mathbf{x}_k)^{-1} \nabla f(\mathbf{x_k})

where :math:`H(\mathbf{x}_k)` is the Hessian matrix at step k.


We will test the method with the
`Rosenbrock's function <https://en.wikipedia.org/wiki/Rosenbrock_function>`_

.. math::

    f(x_1, x_2) = (1-x_1)^2 + 100(x_2-{x_1}^2)^2


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import array
    from numpy.linalg import norm, solve


    def newton_opt(fun, grad, hess, x, niter=50, gtol=1e-8, verbose=False):
        msg = "Maximum number of iterations reached."
        g = grad(x)
        for cont in range(niter):
            if verbose:
                print("n: {}, x: {}, g: {}".format(cont, x, g))
            x = x - solve(hess(x), g)
            g = grad(x)
            if norm(g) < gtol:
                msg = "Extremum found with desired accuracy."
                break
        return x, fun(x), msg


    def rosen(x):
        return (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2


    def rosen_grad(x):
        return array([
            -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2),
            200*(x[1] - x[0]**2)])

    def rosen_hess(x):
        return array([[-400*(x[1]-x[0]**2) + 800*x[0]**2 + 2, -400*x[0]],
                     [-400*x[0], 200]])


    print(newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0], verbose=True))


with result


.. code:: python

    n: 0, x: [2.0, 1.0], g: [ 2402.  -600.]
    n: 1, x: [ 1.99833611  3.99334443], g: [  1.99888520e+00  -5.53708323e-04]
    n: 2, x: [ 1.00055248  0.0055331 ], g: [ 398.44998412 -199.11443262]
    n: 3, x: [ 1.00054972  1.00109974], g: [  1.09944359e-03  -1.52451385e-09]
    n: 4, x: [ 1.         0.9999997], g: [  1.20876952e-04  -6.04384753e-05]
    (array([ 1.,  1.]), 0.0, 'Extremum found with desired accuracy.'

Julia
-----

.. code:: julia

    function newton_opt(fun, grad, hess, x; niter=50, gtol=1e-8, verbose=false)
        msg = "Maximum number of iterations reached."
        g = grad(x)
        for cont = 1:niter
            if verbose
                println("n: $(cont), x: $(x), g: $(g)")
            end
            x = x - hess(x)\g
            g = grad(x)
            if norm(g) < gtol
                msg = "Extremum found with desired accuracy."
                break
            end
        end
        return x, fun(x), msg
    end


    function rosen(x)
        return (1 - x[1])^2 + 100*(x[2] - x[1]^2)^2
    end


    function rosen_grad(x)
        return [-2*(1 - x[1]) - 400*x[1]*(x[2] - x[1]^2);
                200*(x[2] - x[1]^2)]
    end


    function rosen_hess(x)
        return [-400*(x[2] - x[1]^2) + 800*x[1]^2 + 2 -400*x[1];
                -400*x[1] 200]
    end



    println(newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0], verbose=true))


with result

.. code:: julia

    n: 1, x: [2.0, 1.0], g: [2402.0, -600.0]
    n: 2, x: [1.99834, 3.99334], g: [1.99889, -0.000553708]
    n: 3, x: [1.00055, 0.0055331], g: [398.45, -199.114]
    n: 4, x: [1.00055, 1.0011], g: [0.00109944, -1.52451e-9]
    n: 5, x: [1.0, 1.0], g: [0.000120877, -6.04385e-5]
    ([1.0, 1.0], 0.0, "Extremum found with desired accuracy.")



Comparison Python/Julia
-----------------------

Regarding number of lines we have: 34 in Python and 37 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0])

with result

.. code::

    1000 loops, best of 3: 247 µs per loop

For Julia:

.. code:: julia

    @benchmark newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0])

with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  5.48 KiB
      allocs estimate:  120
      --------------
      minimum time:     5.784 μs (0.00% GC)
      median time:      6.030 μs (0.00% GC)
      mean time:        6.953 μs (10.00% GC)
      maximum time:     572.279 μs (95.96% GC)
      --------------
      samples:          10000
      evals/sample:     6


In this case, we can say that the Python code is roughly 40 times slower
than the Julia one.

Comparison with gradient descent
--------------------------------
We see an improvement in the number of iterations compared with gradient
descent, that is, we moved from 40 iterations to 4 iterations, even if
we demand the method to have higher accuracy, :math:`10^{-12}`, for example.

The appearance of this faster convergence does not come for free, of course.
When using Newton's method we have two major drawbacks:

- We need to compute the Hessian of the function, that might prove
  really difficult, even if we have the analytical expression for our
  function.
- We need to solve a system of equation in each iteration.
