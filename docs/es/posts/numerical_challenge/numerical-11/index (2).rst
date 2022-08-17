.. title: Reto de métodos numéricos: Día 11
.. slug: numerical-11
.. date: 2017-10-11 12:25:10 UTC-05:00
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

Interpolación: Invirtiendo la matriz de Vandermonde
====================================================

Hoy tenemos `Lagrange interpolation
<https://en.wikipedia.org/wiki/Lagrange_polynomial>`_, una vez más.
Esta vez usaré un enfoque diferente para calcular la interpolación;
construiré la `matriz de Vandermonde
<https://en.wikipedia.org/wiki/Vandermonde_matrix>`_ :math:`V` y resolveré
el sistema de ecuaciones.

.. math::
    V\mathbf{c} = I

donde :math:`\mathbf{c}` es el vector de coeficientes y :math:`I` es la matriz
identidad. Este método, y `el anterior <posts/numerical-09/>`_
no son estables y no deberían usarse para el cálculo de interpoladores de alto
orden, incluso para muestreos optimamente seleccionados. Fallará alrededor
de 40 puntos. Un mejor enfoque es usar la `forma baricéntrica
<https://en.wikipedia.org/wiki/Lagrange_polynomial#Barycentric_form>`_
de la interpolación.

En el ejemplo abajo usamos los `nodos de Chebyshev
<https://en.wikipedia.org/wiki/Chebyshev_nodes>`_.
Los nodos están dados por 

.. math::

    x_k = \cos\left(\frac{2k-1}{2n}\pi\right), \quad k = 1, \ldots, n

donde :math:`n` es el grado del polinomio.

A continuación se presentan los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt


    def vander_mat(x):
        n = len(x)
        van = np.zeros((n, n))
        power = np.array(range(n))
        for row in range(n):
            van[row, :] = x[row]**power
        return van


    def inter_coef(x):
        vand_mat = vander_mat(x)
        coef = np.linalg.solve(vand_mat, np.eye(len(x)))
        return coef


    def compute_interp(x, f, x_eval):
        n = len(x)
        coef = inter_coef(x)
        f_eval = np.zeros_like(x_eval)
        for row in range(n):
            for col in range(n):
                f_eval += coef[row, col]*x_eval**row*f[col]
        return f_eval


    n = 11
    x = -np.cos(np.linspace(0, np.pi, n))
    f = 1/(1 + 25*x**2)
    x_eval = np.linspace(-1, 1, 500)
    interp_f = compute_interp(x, f, x_eval)
    plt.figure()
    plt.plot(x_eval, 1/(1 + 25*x_eval**2))
    plt.plot(x_eval, interp_f)
    plt.plot(x, f, ".")
    plt.ylim(0, 1.2)
    plt.show()




Julia
-----

.. code:: julia

    using PyPlot


    function vander_mat(x)
        n = length(x)
        van = zeros(n, n)
        power = 0:n-1
        for row = 1:n
            van[row, :] = x[row].^power
        end
        return van
    end


    function inter_coef(x)
        vand_mat = vander_mat(x)
        coef = vand_mat \ eye(length(x))
        return coef
    end


    function compute_interp(x, f, x_eval)
        n = length(x)
        coef = inter_coef(x)
        f_eval = zeros(x_eval)
        for row = 1:n
            for col = 1:n
                f_eval += coef[row, col]*x_eval.^(row - 1)*f[col]
            end
        end
        return f_eval
    end


    n = 11
    x = - cos.(linspace(0, pi, n))
    f = 1./(1 + 25*x.^2)
    x_eval = linspace(-1, 1, 500)
    interp_f = compute_interp(x, f, x_eval)
    plot(x_eval, 1./(1 + 25*x_eval.^2))
    plot(x_eval, interp_f)
    plot(x, f, ".")
    ylim(0, 1.2)
    show()

En ambos casos el resultado es el siguiente gráfico.

.. image:: /images/lagrange_vandermonde.svg
   :width: 500 px
   :alt: Interpolación de Lagrange usando la matriz de Vandermonde.
   :align:  center

Y, si intentamos con un :math:`n` alto, digamos :math:`n=45`, podemos ver los
problemas.

.. image:: /images/lagrange_vandermonde-n-45.svg
   :width: 500 px
   :alt: Interpolación de Lagrange usando la matriz de Vandermonde para 45 puntos.
   :align:  center


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 41 en Python y 44 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %%timeit -n 100
    n = 11
    x = -np.cos(np.linspace(0, np.pi, n))
    f = 1/(1 + 25*x**2)
    x_eval = np.linspace(-1, 1, 500)
    interp_f = compute_interp(x, f, x_eval)

con resultado

.. code::

    100 loops, best of 3: 7.86 ms per loop

Para Julia:

.. code:: julia

    function bench()
       x = - cos.(linspace(0, pi, n))
       f = 1./(1 + 25*x.^2)
       x_eval = linspace(-1, 1, 500)
       interp_f = compute_interp(x, f, x_eval)
       return nothing
    end
    @benchmark bench()

con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  32.23 MiB
      allocs estimate:  8277
      --------------
      minimum time:     114.282 ms (1.50% GC)
      median time:      122.061 ms (1.46% GC)
      mean time:        129.733 ms (1.90% GC)
      maximum time:     163.716 ms (1.98% GC)
      --------------
      samples:          39
      evals/sample:     1

En este caso, podemos decir que el código de Python es alrededor de 16
veces más rápido que el de Julia.
