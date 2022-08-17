.. title: Reto de métodos numéricos: Día 8
.. slug: numerical-08
.. date: 2017-10-09 16:15:50 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, optimización
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Método de Newton para optimización
==================================

Hoy tenemos el `método de Newton
<https://en.wikipedia.org/wiki/Newton%27s_method_in_optimization>`_
para optimización. La diferencia principal de este método con el descenso
de gradiente es el uso de derivadas de order superior, en este caso, el hessiano
de la función objetivo. El uso de derivadas de orden superior brinda información
de la curvatura además de la pendiente que estaba disponible en el descenso del
gradiente. La siguietne imagen compara el trayecto para el método
del descenso del gradiente (verde) y método de Newton (rojo).

.. image:: https://upload.wikimedia.org/wikipedia/commons/d/da/Newton_optimization_vs_grad_descent.svg
   :width: 400 px
   :alt: Comparación del trayecto seguido por el descendo del gradiente y el
         método de Newton.
   :align:  center

Matemáticamente, la actualización se escribe como

.. math::

    \mathbf{x}_k = \mathbf{x}_{k-1} -
        H(\mathbf{x}_k)^{-1} \nabla f(\mathbf{x_k})

donde :math:`H(\mathbf{x}_k)` es el hessiano en el paso k-ésimo.

Probaremos el método con la `función de Rosenbrock's
<https://en.wikipedia.org/wiki/Rosenbrock_function>`_

.. math::

    f(x_1, x_2) = (1-x_1)^2 + 100(x_2-{x_1}^2)^2

A continuación se presenta el código.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import array
    from numpy.linalg import norm, solve


    def newton_opt(fun, grad, hess, x, niter=50, gtol=1e-8, verbose=False):
        msg = "Maximum number of iterations reached."
        g = grad(x)
        for cont in range(niter):
            if verbose:
                print("n: {}, x: {}, g: {}".format(cont, x, g))
            x = x - solve(hess(x), g)
            g = grad(x)
            if norm(g) < gtol:
                msg = "Extremum found with desired accuracy."
                break
        return x, fun(x), msg


    def rosen(x):
        return (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2


    def rosen_grad(x):
        return array([
            -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2),
            200*(x[1] - x[0]**2)])

    def rosen_hess(x):
        return array([[-400*(x[1]-x[0]**2) + 800*x[0]**2 + 2, -400*x[0]],
                     [-400*x[0], 200]])


    print(newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0], verbose=True))


con resultado


.. code:: python

    n: 0, x: [2.0, 1.0], g: [ 2402.  -600.]
    n: 1, x: [ 1.99833611  3.99334443], g: [  1.99888520e+00  -5.53708323e-04]
    n: 2, x: [ 1.00055248  0.0055331 ], g: [ 398.44998412 -199.11443262]
    n: 3, x: [ 1.00054972  1.00109974], g: [  1.09944359e-03  -1.52451385e-09]
    n: 4, x: [ 1.         0.9999997], g: [  1.20876952e-04  -6.04384753e-05]
    (array([ 1.,  1.]), 0.0, 'Extremum found with desired accuracy.'

Julia
-----

.. code:: julia

    function newton_opt(fun, grad, hess, x; niter=50, gtol=1e-8, verbose=false)
        msg = "Maximum number of iterations reached."
        g = grad(x)
        for cont = 1:niter
            if verbose
                println("n: $(cont), x: $(x), g: $(g)")
            end
            x = x - hess(x)\g
            g = grad(x)
            if norm(g) < gtol
                msg = "Extremum found with desired accuracy."
                break
            end
        end
        return x, fun(x), msg
    end


    function rosen(x)
        return (1 - x[1])^2 + 100*(x[2] - x[1]^2)^2
    end


    function rosen_grad(x)
        return [-2*(1 - x[1]) - 400*x[1]*(x[2] - x[1]^2);
                200*(x[2] - x[1]^2)]
    end


    function rosen_hess(x)
        return [-400*(x[2] - x[1]^2) + 800*x[1]^2 + 2 -400*x[1];
                -400*x[1] 200]
    end



    println(newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0], verbose=true))


con resultado

.. code:: julia

    n: 1, x: [2.0, 1.0], g: [2402.0, -600.0]
    n: 2, x: [1.99834, 3.99334], g: [1.99889, -0.000553708]
    n: 3, x: [1.00055, 0.0055331], g: [398.45, -199.114]
    n: 4, x: [1.00055, 1.0011], g: [0.00109944, -1.52451e-9]
    n: 5, x: [1.0, 1.0], g: [0.000120877, -6.04385e-5]
    ([1.0, 1.0], 0.0, "Extremum found with desired accuracy.")



Comparación Python/Julia
-----------------------

Respecto al número de líneas tenemos: 34 en Python y 37 en Julia. La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0])

con resultado

.. code::

    1000 loops, best of 3: 247 µs per loop

Para Julia:

.. code:: julia

    @benchmark newton_opt(rosen, rosen_grad, rosen_hess, [2.0, 1.0])

con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  5.48 KiB
      allocs estimate:  120
      --------------
      minimum time:     5.784 μs (0.00% GC)
      median time:      6.030 μs (0.00% GC)
      mean time:        6.953 μs (10.00% GC)
      maximum time:     572.279 μs (95.96% GC)
      --------------
      samples:          10000
      evals/sample:     6

En este caso, podemos decir que el código de Python es 40 veces más lento
que el de Julia.

Comparación con el descenso del gradiente
------------------------------------------

Vemos una mejora en el número de iteraciones en comparación con el descenso
del gradiente, es decir, pasamos de 40 iteraciones a 4 iteraciones, incluso
se buscamos soluciones con mayor precisión, :math:`10^{-12}`, por ejemplo.

La aparición de esta convergencia más rápida no es gratuita, por supuesto.
Cuando usamos el método de Newton tenemos dos desventajas principales:

- Necesitamos calcular el hessiano de la función, esto puede ser difícil
  en algunos casos incluso si tenemos la expresión analítica para nuestra
  función.
- Necesitamos resolver un sistema de ecuaciones en cada iteración.
