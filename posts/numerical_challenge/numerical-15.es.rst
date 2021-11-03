.. title: Reto de métodos numéricos: Día 15
.. slug: numerical-15
.. date: 2017-10-17 16:22:06 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, cuadratura
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Regla de Simpson
================

Hoy tenemos la `regla de Simpson
<https://es.wikipedia.org/wiki/Regla_de_Simpson>`_. Esta es otra de las
`fórmulas de Newton-Cotes <https://es.wikipedia.org/wiki/F%C3%B3rmulas_de_Newton%E2%80%93Cotes>`_,
que se usa para la integración numérica. Newton-Cotes está relacionada con
la interpolación de Lagrange con puntos equidistantes.

A continuación se presentan los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np


    def simps(y, x=None, dx=1.0):
        n = len(y)
        if x is None:
            inte = np.sum(y[0:n-2:2] + 4*y[1:n-1:2] + y[2:n:2])*dx
        else:
            dx = x[1::2] - x[:-1:2]
            inte = np.dot(y[0:n-2:2] + 4*y[1:n-1:2] + y[2:n:2], dx)
        return inte/3


    n = 21
    x = np.linspace(0, 10, n)
    y = np.sin(x)
    print(simps(y, x=x))
    print(1 - np.cos(10))


con resultados

.. code:: python

    1.8397296125
    1.83907152908

Julia
-----

.. code:: julia

    function simps(y; x=nothing, dx=1.0)
        n = length(y)
        if x == nothing
            inte = sum(y[1:2:n-2] + 4*y[2:2:n-1] + y[3:2:n])*dx
        else
            dx = x[2:2:end] - x[1:2:end-1]
            inte = (y[1:2:n-2] + 4*y[2:2:n-1] + y[3:2:n])' * dx
        end
        return inte/3
    end


    n = 21
    x = linspace(0, 10, n)
    y = sin.(x)
    println(simps(y, x=x))
    println(1 - cos(10))


con resultados

.. code:: julia

    1.8397296124951257
    1.8390715290764525


Comparación Python/Julia
-------------------------

Respecto al número de líneas tenemos: 19 en Python y 17 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit simps(y, x=x)

con resultado

.. code::

    100000 loops, best of 3: 13.8 µs per loop

Para Julia:

.. code:: julia

    @benchmark simps(y, x=x)


con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  1.23 KiB
      allocs estimate:  14
      --------------
      minimum time:     1.117 μs (0.00% GC)
      median time:      1.200 μs (0.00% GC)
      mean time:        1.404 μs (7.04% GC)
      maximum time:     222.286 μs (96.45% GC)
      --------------
      samples:          10000
      evals/sample:     10


En este caso, podemos decir que el código de Python es alrededor de 10 veces
más lento que el de Julia.
