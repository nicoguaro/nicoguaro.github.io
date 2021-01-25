.. title: Numerical methods challenge: Day 24
.. slug: numerical-24
.. date: 2017-10-24 15:17:58 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, finite element method
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Finite element method
=====================

Today we have the `Finite element method <https://en.wikipedia.org/wiki/Finite_element_method>`_
to solve the equation:

.. math::

    \frac{d^2 u}{dx^2} = f(x)

with

.. math::

    u(0) = u(1)  = 0

As in the `Ritz method <posts/numerical-23>`_ we form
a functional that is *equivalent* to the
differential equation, propose an approximation as a linear combination of
a set of basis functions and find the *best* set of coefficients for that
combination. That *best* solution is found minimizing the functional.

The functional for this differential equation is

.. math::

    \Pi[u] = -\int_{0}^{1} \left(\frac{d u}{d x}\right)^2 dx
             -\int_{0}^{1}  u f(x) dx

The main difference is that we use a piecewise interpolation for the basis
functions,

.. math::
    \hat{u}(x) = \sum_{n=0}^{N} u_n N_n(x)\, ,

this leads to the system of equations

.. math::

    [K]\{\mathbf{c}\} = \{\mathbf{b}\}

where the local stiffness matrices read

.. math::

    K_\text{local} =  \frac{1}{|J|}\begin{bmatrix} 2 & -2\\ -2 &2\end{bmatrix}

and

.. math::

    b_\text{local} = -|J|\begin{bmatrix} f(x_m)\\ f(x_{n})\end{bmatrix}\, ,

where :math:`|J|` is the Jacobian determinant of the transformation. I am
skipping a great deal about assembling, but it would be just too extensive
to describe the complete process.

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
    import matplotlib.pyplot as plt


    def FEM1D(coords, source):
        N = len(coords)
        stiff_loc = np.array([[2.0, -2.0], [-2.0, 2.0]])
        eles = [np.array([cont, cont + 1]) for cont in range(0, N - 1)]
        stiff = np.zeros((N, N))
        rhs = np.zeros(N)
        for ele in eles:
            jaco = coords[ele[1]] - coords[ele[0]]
            rhs[ele] = rhs[ele] + jaco*source(coords[ele])
            for cont1, row in enumerate(ele):
                for cont2, col in enumerate(ele):
                    stiff[row, col] = stiff[row, col] +  stiff_loc[cont1, cont2]/jaco
        return stiff, rhs


    N = 100
    fun = lambda x: x**3
    x = np.linspace(0, 1, N)
    stiff, rhs = FEM1D(x, fun)
    sol = np.zeros(N)
    sol[1:-1] = np.linalg.solve(stiff[1:-1, 1:-1], -rhs[1:-1])


    #%% Plotting
    plt.figure(figsize=(4, 3))
    plt.plot(x, sol)
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


    function FEM1D(coords, source)
        N = length(coords)
        stiff_loc = [2.0 -2.0; -2.0 2.0]
        eles = [[cont, cont + 1] for cont in 1:N-1]
        stiff = zeros(N, N)
        rhs = zeros(N)
        for ele in eles
            jaco = coords[ele[2]] - coords[ele[1]]
            rhs[ele] = rhs[ele] + jaco*source(coords[ele])
            stiff[ele, ele] = stiff[ele, ele] +  stiff_loc/jaco
        end
        return stiff, rhs
    end


    N = 100
    fun(x) = x.^3
    x = linspace(0, 1, N)
    stiff, rhs = FEM1D(x, fun)
    sol = zeros(N)
    sol[2:end-1] = -stiff[2:end-1, 2:end-1]\rhs[2:end-1]


    #%% Plotting
    figure(figsize=(4, 3))
    plot(x, sol)
    plot(x, x.*(x.^4 - 1)/20, linestyle="dashed")
    xlabel(L"$x$")
    ylabel(L"$y$")
    legend(["FEM solution", "Exact solution"])
    tight_layout()
    show()

Both have the same result, as follows

.. image:: /images/FEM1D.svg
   :width: 400 px
   :alt: Finite element method approximation.
   :align:  center



Comparison Python/Julia
-----------------------

Regarding number of lines we have: 37 in Python and 35 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia. For the test we are just comparing the time it takes
to generate the matrices.

For Python:

.. code:: IPython

    %timeit FEM1D(x, fun)

with result

.. code::

     100 loops, best of 3: 2.15 ms per loop


For Julia:

.. code:: julia

    @benchmark FEM1D(x, fun)


with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  183.73 KiB
      allocs estimate:  1392
      --------------
      minimum time:     60.045 μs (0.00% GC)
      median time:      70.445 μs (0.00% GC)
      mean time:        98.276 μs (25.64% GC)
      maximum time:     4.269 ms (96.70% GC)
      --------------
      samples:          10000
      evals/sample:     1


In this case, we can say that the Python code is roughly 30 times slower than
Julia code.
