.. title: Reto de métodos numéricos: Día 3
.. slug: numerical-03
.. date: 2017-10-03 19:26:13 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, búsqueda de raíces
.. category:  Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Método de Newton
================

El método de hoy es el `método de Newton
<https://es.wikipedia.org/wiki/M%C3%A9todo_de_Newton>`_. Este método
se usa para resolver la ecuación :math:`f(x) = 0` para :math:`x` real, y
:math:`f` una función diferenciable. Inicia con un estimado inicial
:math:`x_0` y sucesivamente lo refina encoentrando el intercepto de la línea
tangente de la función con cero. La nueva aproximación se calcula a partir
de la anterior con

.. math::

    x_k = x_{k-1} - \frac{f(x)}{f'(x)} 

La convergencia de este método es generalmente más rápida que en el método
de bisección. Sin embargo, la convergencia no está garantizada. Otra
desventaje del método es que se necesita la derivada de la función.

Usaremos la función :math:`f(x) = \cos(x) - x` para probar los códigos,
y el estimado inicial es 1.0.

A continuación se presentan los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import abs, cos, sin

    def newton(fun, grad, x, niter=50, ftol=1e-12, verbose=False):
        msg = "Maximum number of iterations reached."
        for cont in range(niter):
            if abs(grad(x)) < ftol:
                x = None
                msg = "Derivative near to zero."
                break
            if verbose:
                print("n: {}, x: {}".format(cont, x))
            x = x - fun(x)/grad(x)
            if abs(fun(x)) < ftol:
                msg = "Root found with desired accuracy."
                break
        return x, msg


    def fun(x):
        return cos(x) - x


    def grad(x):
        return -sin(x) - 1.0


    print(newton(fun, grad, 1.0))




Julia
-----

.. code:: julia

    function newton(fun, grad, x, niter=50, ftol=1e-12, verbose=false)
        msg = "Maximum number of iterations reached."
        for cont = 1:niter
            if abs(grad(x)) < ftol
                x = nothing
                msg = "Derivative near to zero."
                break
            end
            if verbose
                println("n: $(cont), x: $(x)")
            end
            x = x - fun(x)/grad(x)
            if abs(fun(x)) < ftol
                msg = "Root found with desired accuracy."
                break
            end
        end
        return x, msg
    end


    function fun(x)
        return cos(x) - x
    end


    function grad(x)
        return -sin(x) - 1.0
    end


    println(newton(fun, grad, 1.0))



Comparación
-----------

Respecto al número de líneas tenemos: 28 en Python y 32 en Julia. La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit newton(fun, grad, 1.0)

com resultado

.. code:: IPython

    10000 loops, best of 3: 27.3 µs per loop

Para Julia:

.. code:: julia

    @benchmark newton(fun, grad, 1.0)

con resultado

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  48 bytes
      allocs estimate:  2
      --------------
      minimum time:     327.925 ns (0.00% GC)
      median time:      337.956 ns (0.00% GC)
      mean time:        351.064 ns (0.80% GC)
      maximum time:     8.118 μs (92.60% GC)
      --------------
      samples:          10000
      evals/sample:     226

