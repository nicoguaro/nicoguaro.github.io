.. title: Reto de métodos numéricos: Día 9
.. slug: numerical-10
.. date: 2017-10-10 21:16:26 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, interpolación
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Interpolación de Lagrange: fenómeno de Runge
============================================

Hoy tenemos la `interpolación de Lagrange
<https://es.wikipedia.org/wiki/Interpolaci%C3%B3n_polin%C3%B3mica_de_Lagrange>`_,
de nuevo. Técnicamente, no estoy publicando sobre un método diferente sino
publicando el `mismo algoritmo para interpolar </posts/numerical-09/>`_.
La diferencia es que cambiaré el muestreo, es decir, usaré un muestreo que
no es uniforme.

El problema con la interpolación uniforme se conoce como
`fenómeno de Runge <https://es.wikipedia.org/wiki/Fen%C3%B3meno_de_Runge>`_
y se ilustra con la siguiente imagen.

.. image:: /images/runge_phenomenon.svg
   :width: 500 px
   :alt: Fenómeno de Runge.
   :align:  center

Una forma de mitigar el problema es usar muestreo no uniforme, como los
`nodos de Chebyshev <https://en.wikipedia.org/wiki/Chebyshev_nodes>`_ o los
`nodos de Lobatto <https://en.wikipedia.org/wiki/Gaussian_quadrature#Gauss.E2.80.93Lobatto_rules>`_.
El primero de estos muestreos minimiza el fenómeno de Runge, mientras que el
segundo maximiza el `determinant de Vandermonde 
<https://en.wikipedia.org/wiki/Vandermonde_matrix>`_.

En el ejemplo a continuación usamos el muestreo de Lobatto. Los nodos de Lobatto
son los ceros de

.. math::

    (1 - x^2) P'_N(x)

donde :math:`P_N` se refiere al N-ésimo polinomio de Legendre. El uso de estos
nodos es útil en integración numérica y métodos espectrales. Encontrar los ceros
de estos polinomios puede ser engorroso, en general. En este caso, usamos
un método originalmente implementado en `MATLAB por Greg von Winckel
<http://www.mathworks.com/matlabcentral/fileexchange/4775-legende-gauss-lobatto-nodes-and-weights>`_
que usa los nodos de Chebyshev como una aproximación inicial y luego
actualiza este aproximación usando el método de Newton-Raphson.

A continuación se presentan los códigos.

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

En cambos casos el resultado es el gráfico que se muestra a continuación
