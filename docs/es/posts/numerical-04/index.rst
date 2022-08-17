.. title: Reto de métodos numéricos: Día 4
.. slug: numerical-04
.. date: 2017-10-04 21:30:15 UTC-05:00
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

Método de Newton: caso vectorial
================================

Hoy tenemos al `método de Newton
<https://en.wikipedia.org/wiki/Newton%27s_method#Nonlinear_systems_of_equations>`_
una vez más. En este caso, la función es vectorial. Esto implica una ligera
modificación a la publicación original. La nueva aproximación se calcula a
partir de la anterior usando

.. math::

    \mathbf{x}_k = \mathbf{x}_{k-1} -
        J(\mathbf{x}_k)^{-1} \mathbf{F}(\mathbf{x_k}) 

en donde necesitamos usa la matriz jacobiana :math:`J`.

Probaremos el método con la función
:math:`\mathbf{F}(x, y) = (x + 2y - 2, x^2 + 4x - 4)`
con solución :math:`\mathbf{x} = (0, 1)`.

A continuación se encuentran los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import array
    from numpy.linalg import solve, norm, det

    def newton(fun, jaco, x, niter=50, ftol=1e-12, verbose=False):
        msg = "Maximum number of iterations reached."
        for cont in range(niter):
            J = jaco(x)
            f = fun(x)
            if det(J) < ftol:
                x = None
                msg = "Derivative near to zero."
                break
            if verbose:
                print("n: {}, x: {}".format(cont, x))
            x = x - solve(J, f)
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


    print(newton(fun, jaco, [1.0, 10.0]))



Julia
-----

.. code:: julia

    function newton(fun, jaco, x, niter=50, ftol=1e-12, verbose=false)
        msg = "Maximum number of iterations reached."
        for cont = 1:niter
            J = jaco(x)
            f = fun(x)
            if det(J) < ftol
                x = nothing
                msg = "Derivative near to zero."
                break
            end
            if verbose
                println("n: $(cont), x: $(x)")
            end
            x = x - J\f
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
        return [1.0 2.0;
                2*x[1] 8*x[2]]
    end


    println(newton(fun, jaco, [1.0, 10.0]))



Comparación
-----------

Respecto al número de líneas tenemos: 31 en Python y 33 en Julia. La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit newton(fun, jaco, [1.0, 10.0])

con resultado

.. code:: IPython

    1000 loops, best of 3: 284 µs per loop

Para Julia:

.. code:: julia

    @benchmark newton(fun, jaco, [1.0, 10.0])

con resultado

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  10.44 KiB
      allocs estimate:  192
      --------------
      minimum time:     6.818 μs (0.00% GC)
      median time:      7.167 μs (0.00% GC)
      mean time:        9.607 μs (16.53% GC)
      maximum time:     2.953 ms (97.40% GC)
      --------------
      samples:          10000
      evals/sample:     4


En este caso, podemos decir que el código de Python es alrededor de 40 veces más
lento que el de Julia. Esta es una mejora respecto a los ejemplos anteriore,
en donde la razón era alrededor de 100. La razón para esta "mejora" puede ser
en la iversión del jacobiano, que llama a una rutina de ``numpy``, que hace
el trabajo sucio por nosotros.
