.. title: Numerical methods challenge: Day 20
.. slug: numerical-20
.. date: 2017-10-20 20:10:43 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, ode, shooting method
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Shooting method
===============

Today we have the `shooting method <https://en.wikipedia.org/wiki/Shooting_method>`_.
This is a method for solving boundary value problems by turning them into
a sequence of initial value problems.

Loosely speaking, for a second order equation we have

.. math::

    y''(x) = f(x, y(x), y'(x)),\quad y(x_0) = y_0,\quad y(x_1) = y_1\, ,

and we solve the sequence of problems

.. math::

    y''(x) = f(x, y(x), y'(x)),\quad y(x_0) = y_0,\quad y'(x_0) = a

until the function :math:`F(a) = y(x_1; a) - y_1` has a root.

We will test the method with the boundary value problem

.. math::

    y''(x) = \frac{3}{2} y^2,\quad w(0) = 4,\quad w(1) = 1\, .


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import newton
    from scipy.integrate import odeint


    def shooting(dydx, x, x0, xf, shoot=None):
        if shoot is None:
            shoot = np.random.uniform(-20, 20)
        F = lambda s, x0, xf, x: odeint(dydx, [x0, s], x)[-1, 0] - xf
        shoot = newton(F, shoot, args=(x0, xf, x))
        y = odeint(dydx, [x0, shoot], x)
        return y[:, 0], shoot


    func = lambda y, t: [y[1], 1.5*y[0]**2]
    x = np.linspace(0, 1, 1000)
    y, shoot = shooting(func, x, 4, 1, shoot=-5)
    plt.plot(x, y)
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    plt.show()




Julia
-----

.. code:: julia

    using PyPlot, DifferentialEquations, Roots


    function shooting(dydx, x, y0, yf; shoot=nothing)
        if shoot == nothing
            shoot = rand(-20:0.1:20)
        end
        function F(s)
            prob = ODEProblem(dydx, [y0, s], (x[1], x[end]))
            sol = solve(prob)
            return sol(x[end])[1] - yf
        end
        shoot = fzero(F, shoot)
        prob = ODEProblem(dydx, [y0, shoot], (x[1], x[end]))
        sol = solve(prob, solveat=x)
        return sol(x)[1, :], shoot
    end


    func(x, y) = [y[2], 1.5*y[1]^2]
    x = linspace(0, 1, 1000)
    y, shoot = shooting(func, x , 4.0, 1.0, shoot=-5.0)
    plot(x, y)


In both cases the result is the following plot, and the slope is
-7.9999999657800833.

.. image:: /images/shooting.svg
   :width: 600 px
   :alt: Solution of the differential equation that satisfy the boundary conditions.
   :align:  center

We should mention that the convergence of the method relies on the selection
of initial guesses. For example, if we choose as initial parameter -50
in the previous problem, we obtain a completely differente solution.

.. code:: 
    
    y, shoot = shooting(func, x , 4.0, 1.0, shoot=-50.0)


.. image:: /images/shooting-s-50.svg
   :width: 600 px
   :alt: Solution of the differential equation that satisfy the boundary conditions.
   :align:  center


And the obtained slope is -35.858547970130971.


Comparison Python/Julia
-----------------------

Regarding number of lines we have: 20 in Python and 23 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit shooting(func, x, 4, 1, shoot=-5)

with result

.. code::

    100 loops, best of 3: 1.9 ms per loop

For Julia:

.. code:: julia

    @benchmark shooting(func, x, 4.0, 1.0, shoot=-5.0)


with result

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  4.18 MiB
      allocs estimate:  78552
      --------------
      minimum time:     10.065 ms (0.00% GC)
      median time:      10.593 ms (0.00% GC)
      mean time:        11.769 ms (9.28% GC)
      maximum time:     22.252 ms (48.58% GC)
      --------------
      samples:          425
      evals/sample:     1


In this case, we can say that the Python code is roughly 5 times faster than
Julia. Although, the codes are more different than in the other challenges.
For example, I am not using ``newton`` in Julia.
