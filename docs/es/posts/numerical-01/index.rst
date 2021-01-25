.. title: Reto de métodos numéricos
.. slug: numerical-01
.. date: 2017-10-01 23:12:04 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, búsqueda de raíces
.. category: Scientific Computing
.. type: text
.. has_math: yes

Por el próximo mes estaré escribiendo un programa por día para algunos métodos
numéricos conocidos en Python y Julia. Está destinado a ser un ejercicio,
entonces no espere que el código sea lo suficientemente bueno para un uso real.
Además, debo mencionar que casi no tengo experiencia con Julia, por lo que
probablemente no será Julia idiomático sino Julia más parecido a Python.

Día 1: Método de bisección
==========================
El primer método a considerar es el
`método de bisección <https://en.wikipedia.org/wiki/Bisection_method>`_.
Este método se usa para resolver la ecuación :math:`f(x) = 0` para
:math:`x` real, y :math:`f` continua. Se empieza con un intervalo :math:`[a,b]`,
donde :math:`f(a)` y :math:`f(b)` deben tener signos opuestos. El método procede
partiendo a la mitad el intervalo y seleccionando el subintervalo en donde
aparece la solución, es decir, el signo de la función cambia.

Usaremos la función :math:`f(x) = \cos(x) - x^2` para probar los códigos,
y el intervalo inicial es [0, 1].

A continuación están los códigos:

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import log2, ceil, abs, cos
    
    def bisection(fun, a, b, xtol=1e-6, ftol=1e-12):
        if fun(a) * fun(b) > 0:
            c = None
            msg = "The function should have a sign change in the interval."
        else:
            nmax = int(ceil(log2((b - a)/xtol)))
            for cont in range(nmax):
                c = 0.5*(a + b)
                if abs(fun(c)) < ftol:
                    msg = "Root found with desired accuracy."
                    break
                elif fun(a) * fun(c) < 0:
                    b = c
                elif fun(b) * fun(c) < 0:
                    a = c
                msg = "Maximum number of iterations reached."
        return c, msg
    
    def fun(x):
        return cos(x) - x**2
    
    print(bisection(fun, 0.0, 1.0))


Con resultado

.. code:: python

    (0.824131965637207, 'Maximum number of iterations reached.')

Julia
-----
.. code:: julia

    function bisection(fun, a, b, xtol=1e-6, ftol=1e-12)
        if fun(a) * fun(b) > 0
            c = nothing
            msg = "The function should have a sign change in the interval."
        else
            nmax = ceil(log2((b - a)/xtol))
            for cont = 1:nmax
                c = 0.5*(a + b)
                if abs(fun(c)) < ftol
                    msg = "Root found with desired accuracy."
                    break
                elseif fun(a) * fun(c) < 0
                    b = c
                elseif fun(b) * fun(c) < 0
                    a = c
                end
                msg = "Maximum number of iterations reached."
            end
        end
        return c, msg
    end

    function fun(x)
        return cos(x) - x^2
    end

    println(bisection(fun, 0.0, 1.0))

Con resultado

.. code:: julia

    (0.824131965637207, "Maximum number of iterations reached.")

En este caso, ambos códigos están bastante cerca. El código de Python tiene
25 líneas, mientras que el de Julia 27. Como se esperaba, los resultados
son iguales.

Edición (2017-10-02)
--------------------
Como sugirió Edward Villegas, decidí comparar los tiempos de ejecución.
Usé  ``%timeit`` para IPython y ``@benchmark`` (de ``BenchmarkTools``)
para Julia.

En IPython, tenemos

.. code:: IPython

    %timeit bisection(fun, 0.0, 2.0)

con resultado

.. code:: IPython

    10000 loops, best of 3: 107 µs per loop

Y en Julia, tenemos

.. code:: julia

    @benchmark bisection(fun, 0.0, 2.0)


con resultado

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  48 bytes
      allocs estimate:  2
      --------------
      minimum time:     1.505 μs (0.00% GC)
      median time:      1.548 μs (0.00% GC)
      mean time:        1.604 μs (0.00% GC)
      maximum time:     38.425 μs (0.00% GC)
      --------------
      samples:          10000
      evals/sample:     10

Parece que la versión de Julia es alrededor de 100 veces más rápida que
su equivalente en Python.
