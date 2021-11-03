.. title: Reto de métodos numéricos: Día 14
.. slug: numerical-14
.. date: 2017-10-14 14:00:42 UTC-05:00
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

Regla del trapecio
==================

Hoy tenemos la `regla del trapecio
<https://es.wikipedia.org/wiki/Regla_del_trapecio>`_. Esta es la más simple de
las `fórmulas de Newton-Cotes
<https://es.wikipedia.org/wiki/F%C3%B3rmulas_de_Newton%E2%80%93Cotes>`_
para integración numérica. La integración de Newton-Cotes se relaciona con
la interpolación de Lagrange con puntos equidistantes.

A continuación se presentan los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np


    def trapz(y, x=None, dx=1.0):
        if x is None:
            inte = 0.5*dx*(2*np.sum(y[1:-1]) + y[0] + y[-1])
        else:
            dx = x[1:] - x[:-1]
            inte = 0.5*np.dot(y[:-1] + y[1:], dx)
        return inte


    dx = 0.001
    x = np.arange(0, 10, dx)
    y = np.sin(x)
    print(trapz(y, dx=dx))
    print(1 - np.cos(10))

con resultado

.. code:: python

    1.83961497726
    1.83907152908

Julia
-----

.. code:: julia

    function trapz(y; x=nothing, dx=1.0)
        if x == nothing
            inte = 0.5*dx*(2*sum(y[2:end-1]) + y[1] + y[end])
        else
            dx = x[2:end] - x[1:end-1]
            inte = 0.5* (y[1:end-1] + y[2:end])' * dx
        end
        return inte
    end


    dx = 0.001
    x = 0:dx:10
    y = sin.(x)
    println(trapz(y, dx=dx))
    println(1 - cos(10))

con resultado

.. code:: julia

    1.8390713758204895
    1.8390715290764525



Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 18 en Python y 16 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit trapz(y, dx=dx)

con resultado

.. code::

    100000 loops, best of 3: 16.9 µs per loop

Para Julia:

.. code:: julia

    @benchmark trapz(y, dx=dx)

con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  78.31 KiB
      allocs estimate:  4
      --------------
      minimum time:     13.080 μs (0.00% GC)
      median time:      16.333 μs (0.00% GC)
      mean time:        20.099 μs (12.66% GC)
      maximum time:     963.732 μs (90.60% GC)
      --------------
      samples:          10000
      evals/sample:     1


En este caso, podemos decir que el código de Python es tan rápido como
el de Julia.
