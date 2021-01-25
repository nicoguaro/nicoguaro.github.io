.. title: Numerical methods challenge: Day 10
.. slug: numerical-10
.. date: 2017-10-10 21:16:26 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, interpolation
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Lagrange interpolation: Runge phenomenon
========================================

Today we have
`Lagrange interpolation <https://en.wikipedia.org/wiki/Lagrange_polynomial>`_,
again. Technically, I am not posting about a different method, but just
using the `same algorithm for interpolation </posts/numerical-09/>`_.
The difference is that I will change the sampling, that is, I will use
non-uniform sampling.

The problem with uniform interpolation is known as
`Runge phenomenon <https://en.wikipedia.org/wiki/Runge%27s_phenomenon>`_
and is illustrated in the following image.

.. image:: /images/runge_phenomenon.svg
   :width: 500 px
   :alt: Runge phenomenon.
   :align:  center

One way to mitigate the problem is to use non-uniform sampling, such as
`Chebyshev nodes <https://en.wikipedia.org/wiki/Chebyshev_nodes>`_ or
`Lobatto nodes <https://en.wikipedia.org/wiki/Gaussian_quadrature#Gauss.E2.80.93Lobatto_rules>`_. The former set minimizes
the Runge phenomenon, while the latter maximizes the
`Vandermonde determinant <https://en.wikipedia.org/wiki/Vandermonde_matrix>`_.

In the example below we use Lobatto sampling. Lobatto nodes are the zeros of

.. math::

    (1 - x^2) P'_N(x)

where :math:`P_N` refers to the Nth Legendre polynomial. The use of these
nodes is useful in numerical integration and spectral methods. Finding the
zeroes of these polynomials might be cumbersome in general. Nevertheless,
we use an approach originally implemented in
`MATLAB by Greg von Winckel <http://www.mathworks.com/matlabcentral/fileexchange/4775-legende-gauss-lobatto-nodes-and-weights>`_ that use Chebyshev nodes
as first guess and then update this guess using Newton-Raphson method.

Following are the codes.

Python
------

.. code:: python

    from __future__ import division
    from numpy import (zeros_like, pi, cos, zeros, amax, abs,
                       array, linspace, prod)
    import matplotlib.pyplot as plt


    def lagrange(x_int, y_int, x_new):
        y_new = zeros_like(x_new)
        for xi, yi in zip(x_int, y_int):
            y_new += yi*prod([(x_new - xj)/(xi - xj)
                             for xj in x_int if xi!=xj], axis=0)
        return y_new


    def gauss_lobatto(N, tol=1e-15):
        x = -cos(linspace(0, pi, N))
        P = zeros((N, N))  # Vandermonde Matrix
        x_old = 2
        while amax(abs(x - x_old)) > tol:
            x_old = x
            P[:, 0] = 1
            P[:, 1] = x
            for k in range(2, N):
                P[:, k] = ((2 * k - 1) * x * P[:, k - 1] -
                           (k - 1) * P[:, k - 2]) / k
            x = x_old - (x * P[:, N - 1] - P[:, N - 2]) / (N * P[:, N - 1])
            print(x)
        return array(x)


    runge = lambda x: 1/(1 + 25*x**2)
    x = linspace(-1, 1, 100)
    x_int = linspace(-1, 1, 11)
    x_int2 = gauss_lobatto(11)
    x_new = linspace(-1, 1, 1000)
    y_new = lagrange(x_int, runge(x_int), x_new)
    y_new2 = lagrange(x_int2, runge(x_int2), x_new)
    plt.plot(x, runge(x), "k")
    plt.plot(x_new, y_new)
    plt.plot(x_new, y_new2)
    plt.legend(["Runge function",
                "Uniform interpolation",
                "Lobatto-sampling interpolation"])
    plt.xlabel("x")
    plt.ylabel("y")
    plt.show()




Julia
-----

.. code:: julia

    using PyPlot


    function lagrange(x_int, y_int, x_new)
        y_new = zeros(x_new)
        for (xi, yi) in zip(x_int, y_int)
            prod = ones(x_new)
            for xj in x_int
                if xi != xj
                    prod = prod.* (x_new - xj)/(xi - xj)
                end
            end
            y_new += yi*prod
        end
        return y_new
    end


    function gauss_lobatto(N; tol=1e-15)
        x = -cos.(linspace(0, pi, N))
        P = zeros(N, N)  # Vandermonde Matrix
        x_old = 2
        while maximum(abs.(x - x_old)) > tol
            x_old = x
            P[:, 1] = 1
            P[:, 2] = x
            for k = 3:N
                P[:, k] = ((2 * k - 1) * x .* P[:, k - 1] -
                           (k - 1) * P[:, k - 2]) / k
            end
            x = x_old - (x .* P[:, N] - P[:, N - 1]) ./ (N* P[:, N])
        end
        return x
    end


    runge(x) =  1./(1 + 25*x.^2)
    x = linspace(-1, 1, 100)
    x_int = linspace(-1, 1, 11)
    x_int2 = gauss_lobatto(11)
    x_new = linspace(-1, 1, 1000)
    y_new = lagrange(x_int, runge(x_int), x_new)
    y_new2 = lagrange(x_int2, runge(x_int2), x_new)
    plot(x, runge(x), "k")
    plot(x_new, y_new)
    plot(x_new, y_new2)
    legend(["Runge function",
                "Uniform interpolation",
                "Lobatto-sampling interpolation"])
    xlabel("x")
    ylabel("y")


In both cases the result is plot shown above.
