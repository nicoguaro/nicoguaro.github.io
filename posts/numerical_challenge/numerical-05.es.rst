.. title: Reto de métodos numéricos: Día 5
.. slug: numerical-05
.. date: 2017-10-05 13:21:41 UTC-05:00
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

Método de Broyden
=================

Hoy tenemos el `método de Broyden
<https://en.wikipedia.org/wiki/Broyden%27s_method>`_.
La idea principal en este método es calcular la matriz jacobiana solo en la
primera iteración y cambiarla para cada iteración realizando actualizaciones
de rango 1.

.. math::

    \mathbf{x}_k = \mathbf{x}_{k-1} -
        J_n \mathbf{F}(\mathbf{x_k})

en donde estimamos la matriz jacobiana en el paso :math:`n` usando

.. math::

    \mathbf J_n = \mathbf J_{n - 1} + \frac{\Delta \mathbf f_n - \mathbf J_{n - 1} \Delta \mathbf x_n}{\|\Delta \mathbf x_n\|^2} \Delta \mathbf x_n^{\mathrm T}

que corresponde a actualizaciones de rango 1 de la matriz jacobiana.

Probaremos el método con la función
:math:`\mathbf{F}(x, y) = (x + 2y - 2, x^2 + 4x - 4)`
con solución :math:`\mathbf{x} = (0, 1)`.

A continuación se presentan los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import array, outer, dot
    from numpy.linalg import solve, norm, det

    def broyden(fun, jaco, x, niter=50, ftol=1e-12, verbose=False):
        msg = "Maximum number of iterations reached."
        J = jaco(x)
        for cont in range(niter):
            if det(J) < ftol:
                x = None
                msg = "Derivative near to zero."
                break
            if verbose:
                print("n: {}, x: {}".format(cont, x))
            f_old = fun(x)
            dx = -solve(J, f_old)
            x = x + dx
            f = fun(x)
            df = f - f_old
            J = J + outer(df - dot(J, dx), dx)/dot(dx, dx)
            if norm(f) < ftol:
                msg = "Root found with desired accuracy."
                break
        return x, msg


    def fun(x):
        return array([x[0] + 2*x[1] - 2, x[0]**2 + 4*x[1]**2 - 4])


    def jaco(x):
        return array([
                [1, 2],
                [2*x[0], 8*x[1]]])


    print(broyden(fun, jaco, [1.0, 2.0]))


Julia
-----

.. code:: julia

    function broyden(fun, jaco, x, niter=50, ftol=1e-12, verbose=false)
        msg = "Maximum number of iterations reached."
        J = jaco(x)
        for cont = 1:niter
            if det(J) < ftol
                x = nothing
                msg = "Derivative near to zero."
                break
            end
            if verbose
                println("n: $(cont), x: $(x)")
            end
            f_old = fun(x)
            dx = -J\f_old
            x = x + dx
            f = fun(x)
            df = f - f_old
            J = J + (df - J*dx) * dx'/ (dx' * dx)
            if norm(f) < ftol
                msg = "Root found with desired accuracy."
                break
            end
        end
        return x, msg
    end

    function fun(x)
        return [x[1] + 2*x[2] - 2, x[1]^2 + 4*x[2]^2 - 4]
    end


    function jaco(x)
        return [1 2;
               2*x[1] 8*x[2]]
    end


    println(broyden(fun, jaco, [1.0, 2.0]))


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 38 en Python y 39 en Julia. La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit broyden(fun, jaco, [1.0, 2.0])

con resultado

.. code::

    1000 loops, best of 3: 703 µs per loop

Para Julia:

.. code:: julia

    @benchmark broyden(fun, jaco, [1.0, 2.0])

con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  14.41 KiB
      allocs estimate:  220
      --------------
      minimum time:     12.099 μs (0.00% GC)
      median time:      12.867 μs (0.00% GC)
      mean time:        15.378 μs (10.78% GC)
      maximum time:     3.511 ms (97.53% GC)
      --------------
      samples:          10000
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 50
veces más lento que el de Julia.

Comparación Newton/Broyden
--------------------------

A continuación, comparamos el método de Newton y Broyden. Estamos usando
la función :math:`\mathbf{x}^T \mathbf{x} + \mathbf{x}` para la prueba.

Python
~~~~~~

El código para la función y el jacobiano es

.. code:: Python

    from numpy import diag
    fun = lambda x: x**2 + x
    jaco = lambda x: diag(2*x + 1)

y los resultados son:


+-----+---------------+--------------+
|  n  | Newton (μs)   | Broyden (μs) |
+-----+---------------+--------------+
|  2  |      500      |      664     |
+-----+---------------+--------------+
|  10 |      541      |      717     |
+-----+---------------+--------------+
| 100 |      3450     |     4800     |
+-----+---------------+--------------+

Julia
~~~~~


El código para la función y el jacobiano es

.. code:: julia

    fun(x) = x' * x + x
    jaco(x) = diagm(2*x + 1)

y los resultados son:

+-----+---------------+--------------+
|  n  | Newton (μs)   | Broyden (μs) |
+-----+---------------+--------------+
|  2  |      1.76     |     1.65     |
+-----+---------------+--------------+
|  10 |     56.42     |     5.12     |
+-----+---------------+--------------+
| 100 |      1782     |      367     |
+-----+---------------+--------------+

En este caso, estamos comparando el valor medio de los resultados de
``@benchmark``.
