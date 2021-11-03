.. title: Reto de métodos numéricos: Día 2
.. slug: numerical-02
.. date: 2017-10-02 20:47:05 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, búsqueda de raíces
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Regula falsi
============

El segundo método a considerar es el `método de posición falsa
<https://en.wikipedia.org/wiki/False_position_method>`_,
o *regula falsi*. Este método se utiliza para resolver la ecuación
:math:`f(x) = 0` para :math:`x` real, y :math:`f` continua. Se comienza con
un intervalo :math:`[a, b]`, donde :math:`f (a)` y  :math:`f (b)` deben
tener signos opuestos. El método es similar al método de bisección pero en
lugar de dividir a la mitad el original intervalo toma como nuevo punto del
intervalo la intersección de la línea
que conecta la función evaluada en los dos puntos extremos. Entonces, el nuevo
el punto se calcula a partir de

.. math::

    c = \frac{a f(b) - b f(a)}{f(b) - f(a)}

Como en el método de bisección, mantenemos el intervalo donde la solución
aparece, es decir, donde cambia el signo de la función.

Usaremos la función :math:`f(x) = \cos(x) - x` para probar los códigos,
y como intervalo inicial :math:`[0.5, \pi/4]`.

A continuación se presentan los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import abs, cos, pi

    def regula_falsi(fun, a, b, niter=50, ftol=1e-12, verbose=False):
        if fun(a) * fun(b) > 0:
            c = None
            msg = "The function should have a sign change in the interval."
        else:
            for cont in range(niter):
                qa = fun(a)
                qb = fun(b)
                c = (a*qb - b*qa)/(qb - qa)
                qc = fun(c)
                if verbose:
                    print("n: {}, c: {}".format(cont, c))
                msg = "Maximum number of iterations reached."
                if abs(qc) < ftol:
                    msg = "Root found with desired accuracy."
                    break
                elif qa * qc < 0:
                    b = c
                elif qb * qc < 0:
                    a = c
        return c, msg

    def fun(x):
        return cos(x) - x

    print(regula_falsi(fun, 0.5, 0.25*pi))



Julia
-----

.. code:: julia

    function regula_falsi(fun, a, b, niter=50, ftol=1e-12, verbose=false)
        if fun(a) * fun(b) > 0
            c = nothing
            msg = "The function should have a sign change in the interval."
        else
            for cont = 1:niter
                qa = fun(a)
                qb = fun(b)
                c = (a*qb - b*qa)/(qb - qa)
                qc = fun(c)
                if verbose
                    println("n: $(cont), c: $(c)")
                end
                if abs(fun(c)) < ftol
                    msg = "Root found with desired accuracy."
                    break
                elseif qa * qc < 0
                    b = c
                elseif qb * qc < 0
                    a = c
                end
                msg = "Maximum number of iterations reached."
            end
        end
        return c, msg
    end

    function fun(x)
        return cos(x) - x
    end

    println(regula_falsi(fun, 0.5, 0.25*pi))


Comparación
-----------

Respecto al número de líneas de código tenemos: 29 en Python y 32 en Julia.
La comparación en tiempo de ejecución se realiza con el comando mágico
de IPython ``%timeit`` y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit regula_falsi(fun, 0.5, 0.25*pi)

con resultado

.. code:: IPython

    10000 loops, best of 3: 35.1 µs per loop

Para Julia:

.. code:: julia

    @benchmark regula_falsi(fun, 0.5, 0.25*pi)

con resultado

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  48 bytes
      allocs estimate:  2
      --------------
      minimum time:     449.495 ns (0.00% GC)
      median time:      464.371 ns (0.00% GC)
      mean time:        493.785 ns (0.52% GC)
      maximum time:     9.723 μs (92.54% GC)
      --------------
      samples:          10000
      evals/sample:     198

