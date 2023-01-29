.. title: Reto de métodos numéricos: Día 13
.. slug: numerical-13
.. date: 2017-10-13 19:20:06 UTC-05:00
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

Splines cúbicas
===============

Hoy tenemos `interpolación por splines cúbicas
<https://en.wikipedia.org/wiki/Spline_(mathematics)>`_.
Las splines cúbicas se usan a menudo porque brindan una aproximación a una
función con continuidad hasta la segunda derivada. Para más detalles se
puede revisar `este algoritmo
<https://en.wikipedia.org/wiki/Spline_(mathematics)#Algorithm_for_computing_natural_cubic_splines>`_.
La diferencia principal es qeu formaremos la matriz y luego resolveremos el
sistema. Es más común resolver el sistema de forma directa ya que este es
tridiagonal.

A continuación los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt


    def spline_coeff(x, y):
        h = x[1:] - x[:-1]
        d_up = h.copy()
        d_up[0] = 0
        d_down = h.copy()
        d_down[-1] = 0
        d_cent = np.ones_like(x)
        d_cent[1:-1] = 2*(h[:-1] + h[1:])
        mat = np.diag(d_cent) + np.diag(d_up, 1) + np.diag(d_down, -1)
        alpha = np.zeros_like(x)
        alpha[1:-1] = 3/h[1:]*(y[2:] - y[1:-1]) - 3/h[:-1]*(y[1:-1] - y[:-2])
        c = np.linalg.solve(mat, alpha)
        b = np.zeros_like(x)
        d = np.zeros_like(x)
        b[:-1] = (y[1:] - y[:-1])/h - h/3*(c[1:] + 2*c[:-1])
        d[:-1] = (c[1:] - c[:-1])/(3*h)
        return y, b, c, d


    n = 20
    x = np.linspace(0, 2*np.pi, n)
    y = np.sin(x)
    a, b, c, d = spline_coeff(x, y)
    for cont in range(n - 1):
        x_loc = np.linspace(x[cont], x[cont + 1], 100)
        y_loc = a[cont] + b[cont]*(x_loc - x[cont]) +\
                c[cont]*(x_loc - x[cont])**2 +\
                d[cont]*(x_loc - x[cont])**3
        plt.plot(x_loc, y_loc, "red")
    plt.plot(x, y, "o")
    plt.show()



Julia
-----

.. code:: julia

    using PyPlot


    function spline_coeff(x, y)
        h = x[2:end] - x[1:end-1]
        d_up = copy(h)
        d_up[1] = 0.0
        d_down = copy(h)
        d_down[end-1] = 0.0
        d_cent = ones(x)
        d_cent[2:end-1] = 2*(h[1:end-1] + h[2:end])
        mat = diagm(d_cent) + diagm(d_up, 1) + diagm(d_down, -1)
        alpha = zeros(x)
        alpha[2:end-1] = 3./h[2:end].*(y[3:end] - y[2:end-1]) - 3./h[1:end-1].*(y[2:end-1] - y[1:end-2])
        c = mat \ alpha
        b = zeros(x)
        d = zeros(x)
        b[1:end-1] = (y[2:end] - y[1:end-1])./h - h./3.*(c[2:end] + 2*c[1:end-1])
        d[1:end-1] = (c[2:end] - c[1:end-1])./(3*h)
        return y, b, c, d
    end


    n = 21
    x = collect(linspace(0, 2*pi, n))
    y = sin.(x)
    a, b, c, d = spline_coeff(x, y)
    for cont = 1:n - 1
        x_loc = linspace(x[cont], x[cont + 1], 100)
        y_loc = a[cont] + b[cont]*(x_loc - x[cont]) +
                c[cont]*(x_loc - x[cont]).^2 +
                d[cont]*(x_loc - x[cont]).^3
        plot(x_loc, y_loc, "red")
    end
    plot(x, y, "o")
    show()


En ambos casos el resultado es la siguiente gráfica.

.. image:: /images/spline.svg
   :width: 500 px
   :alt: Interpolación spline.
   :align:  center




Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 36 en Python y 37 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit a, b, c, d = spline_coeff(x, y)

con resultado

.. code::

    1000 loops, best of 3: 216 µs per loop

Para Julia:

.. code:: julia

    @benchmark a, b, c, d = spline_coeff(x, y)

con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  31.59 KiB
      allocs estimate:  52
      --------------
      minimum time:     18.024 μs (0.00% GC)
      median time:      26.401 μs (0.00% GC)
      mean time:        44.035 μs (3.94% GC)
      maximum time:     9.833 ms (0.00% GC)
      --------------
      samples:          10000
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 10 veces más
lento.
