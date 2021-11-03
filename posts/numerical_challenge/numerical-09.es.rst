.. title: Reto de métodos numéricos: Día 9
.. slug: numerical-09
.. date: 2017-10-09 21:17:56 UTC-05:00
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

Interpolación de Lagrange
=========================

Hoy tenemos la `interpolación de Lagrange
<https://es.wikipedia.org/wiki/Interpolaci%C3%B3n_polin%C3%B3mica_de_Lagrange>`_.
Esta se define con

.. math::

    L(x) = \sum_{j=0}^{k} y_j \prod_{m\neq j}\frac{x - x_m}{x_j - x_m}

donde :math:`x` son los puntos en donde queremos interpolar.

Probaremos el meodo con una sigmoide

.. math::

    f(x) = \frac{1}{1 + e^{-x}}

A continuación se presentan los códigos.

Python
------

.. code:: python

    from __future__ import division
    from numpy import zeros_like, linspace, exp, prod
    import matplotlib.pyplot as plt


    def lagrange(x_int, y_int, x_new):
        y_new = zeros_like(x_new)
        for xi, yi in zip(x_int, y_int):
            y_new += yi*prod([(x_new - xj)/(xi - xj)
                             for xj in x_int if xi!=xj], axis=0)
        return y_new


    x_int = linspace(-5, 5, 11)
    y_int = 1/(1 + exp(-x_int))
    x_new = linspace(-5, 5, 1000)
    y_new = lagrange(x_int, y_int, x_new)
    plt.plot(x_int, y_int, "ok")
    plt.plot(x_new, y_new)
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


    x_int = linspace(-5, 5, 11)
    y_int = 1./(1 + exp.(-x_int))
    x_new = linspace(-5, 5, 1000)
    y_new = lagrange(x_int, y_int, x_new)
    plot(x_int, y_int, "ok")
    plot(x_new, y_new)

En ambos casos el resultado es el siguiente gráfico

.. image:: /images/lagrange_interp.svg
   :width: 400 px
   :alt: Interpolación de Lagrange.
   :align:  center


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 34 en Python y 37 en Julia. La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit lagrange(x_int, y_int, x_new)

con resultado

.. code::

    1000 loops, best of 3: 1.55 ms per loop

Para Julia:

.. code:: julia

    @benchmark newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0])

con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  1.97 MiB
      allocs estimate:  254
      --------------
      minimum time:     737.665 μs (0.00% GC)
      median time:      811.633 μs (0.00% GC)
      mean time:        916.450 μs (10.77% GC)
      maximum time:     3.119 ms (64.40% GC)
      --------------
      samples:          5433
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 2 veces
más lento que el de Julia, aunque es probable que no este usando el mejor
enfoque en Julia.
