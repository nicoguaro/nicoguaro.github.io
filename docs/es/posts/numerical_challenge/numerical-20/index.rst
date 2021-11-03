.. title: Reto de métodos numéricos: Día 20
.. slug: numerical-20
.. date: 2017-10-20 20:10:43 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, edo, método del disparo
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Método del disparo
==================

Hoy tenemos el `método del disparo <https://en.wikipedia.org/wiki/Shooting_method>`_.
Este es un método para resolver problemas de valores en la frontera
convirtiéndolos en una sucesión de problemas de valores iniciales.

A grandes rasgos, para una ecuación de segundo orden tenemos

.. math::

    y''(x) = f(x, y(x), y'(x)),\quad y(x_0) = y_0,\quad y(x_1) = y_1\, ,

y resolvemos la sucesión de problemas
and we solve the sequence of problems

.. math::

    y''(x) = f(x, y(x), y'(x)),\quad y(x_0) = y_0,\quad y'(x_0) = a

hasta que la función :math:`F(a) = y(x_1; a) - y_1` tenga una raíz.

Vamos a probar este método con el problema de valores en la frontera

.. math::

    y''(x) = \frac{3}{2} y^2,\quad w(0) = 4,\quad w(1) = 1\, .

A continuación se presenta el código.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt
    from scipy.optimize import newton
    from scipy.integrate import odeint


    def shooting(dydx, x, x0, xf, shoot=None):
        if shoot is None:
            shoot = np.random.uniform(-20, 20)
        F = lambda s, x0, xf, x: odeint(dydx, [x0, s], x)[-1, 0] - xf
        shoot = newton(F, shoot, args=(x0, xf, x))
        y = odeint(dydx, [x0, shoot], x)
        return y[:, 0], shoot


    func = lambda y, t: [y[1], 1.5*y[0]**2]
    x = np.linspace(0, 1, 1000)
    y, shoot = shooting(func, x, 4, 1, shoot=-5)
    plt.plot(x, y)
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    plt.show()




Julia
-----

.. code:: julia

    using PyPlot, DifferentialEquations, Roots


    function shooting(dydx, x, y0, yf; shoot=nothing)
        if shoot == nothing
            shoot = rand(-20:0.1:20)
        end
        function F(s)
            prob = ODEProblem(dydx, [y0, s], (x[1], x[end]))
            sol = solve(prob)
            return sol(x[end])[1] - yf
        end
        shoot = fzero(F, shoot)
        prob = ODEProblem(dydx, [y0, shoot], (x[1], x[end]))
        sol = solve(prob, solveat=x)
        return sol(x)[1, :], shoot
    end


    func(x, y) = [y[2], 1.5*y[1]^2]
    x = linspace(0, 1, 1000)
    y, shoot = shooting(func, x , 4.0, 1.0, shoot=-5.0)
    plot(x, y)


En ambos casos el resultado es el siguiente gráfico, y la pendiente es
-7.9999999657800833.

.. image:: /images/shooting.svg
   :width: 600 px
   :alt: Solución de la ecuación diferencial que satisface las condiciones de frontera.
   :align:  center

Debemos mentionar que la convergencia del método depende de la selección de la
aproximación inicial. Por ejemplo, si escogemos como parámetro inicial -50
en el problema anterior, obtenemos una solución completamente diferente.

.. code:: 
    
    y, shoot = shooting(func, x , 4.0, 1.0, shoot=-50.0)


.. image:: /images/shooting-s-50.svg
   :width: 600 px
   :alt: Solución de la ecuación diferencial que satisface las condiciones de frontera.
   :align:  center

Y la pendiente que se obtiene es -35.858547970130971.


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 20 en Python y 23 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit shooting(func, x, 4, 1, shoot=-5)

con resultado

.. code::

    100 loops, best of 3: 1.9 ms per loop

Para Julia:

.. code:: julia

    @benchmark shooting(func, x, 4.0, 1.0, shoot=-5.0)


con resultado

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  4.18 MiB
      allocs estimate:  78552
      --------------
      minimum time:     10.065 ms (0.00% GC)
      median time:      10.593 ms (0.00% GC)
      mean time:        11.769 ms (9.28% GC)
      maximum time:     22.252 ms (48.58% GC)
      --------------
      samples:          425
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 5 veces más
rápido que el de Julia. Sin embargo, el código es más diferente que en los otros
retos. Por ejemplo, no estoy usando ``newton`` en Julia.
