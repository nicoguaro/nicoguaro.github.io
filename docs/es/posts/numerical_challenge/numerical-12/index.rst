.. title: Reto de métodos numéricos: Día 12
.. slug: numerical-12
.. date: 2017-10-12 15:06:10 UTC-05:00
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

Interpolación de Hermite: Invirtiendo la matriz de Vandermonde
===============================================================

Hoy vamos a comparar la `inerpolación de Lagrange <posts/numerical-11>`_ con la
`interpolación de Hermite <https://en.wikipedia.org/wiki/Hermite_interpolation>`_.
Para este ejemplo usaremos la `matriz de Vandermone confluente
<https://en.wikipedia.org/wiki/Vandermonde_matrix>`_ :math:`V`. El código está
basado en un código mío *viejo* que está disponible en
`este repo <https://github.com/nicoguaro/FEM_resources/terpolation/interp.py>`_.

Como en el caso de la interpolación de Lagrange, resolvemos el sistema

.. math::
    V\mathbf{c} = I

donde :math:`\mathbf{c}` es el vector de coeficientes y :math:`I` es la matriz
identidad. Este método no es estable y no debería usarse para cálculos de
interpoladores de orden alto, incluso para muestreos escogidos de forma óptima.
Este fallará alrededor de 20 puntos. Una mejor aproximación es usar interpolación
en `forma baricéntrico
<https://en.wikipedia.org/wiki/Lagrange_polynomial#Barycentric_form>`_.

En el ejemplo a continuación usamos los `nodos de Chebyshev
<https://en.wikipedia.org/wiki/Chebyshev_nodes>`_. Los nodos están dados por

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


    def conf_vander_mat(x):
        n = len(x)
        conf_van = np.zeros((2*n, 2*n))
        power = np.array(range(2*n))
        for row in range(n):
            conf_van[row, :] = x[row]**power
            conf_van[row + n, :] = power*x[row]**(power - 1)
        return conf_van


    def inter_coef(x, inter_type="lagrange"):
        if inter_type == "lagrange":
            vand_mat = vander_mat(x)
        elif inter_type == "hermite":
            vand_mat = conf_vander_mat(x)
        coef = np.linalg.solve(vand_mat, np.eye(vand_mat.shape[0]))
        return coef


    def compute_interp(x, f, x_eval, df=None):
        n = len(x)
        if df is None:
            coef = inter_coef(x, inter_type="lagrange")
        else:
            coef = inter_coef(x, inter_type="hermite")
        f_eval = np.zeros_like(x_eval)
        nmat = coef.shape[0]
        for row in range(nmat):
            for col in range(nmat):
                if col < n or nmat == n:
                    f_eval += coef[row, col]*x_eval**row*f[col]
                else:
                    f_eval += coef[row, col]*x_eval**row*df[col - n]
        return f_eval




    n = 7
    x = -np.cos(np.linspace(0, np.pi, n))
    f = lambda x: 1/(1 + 25*x**2)
    df = lambda x: -50*x/(1 + 25*x**2)**2
    x_eval = np.linspace(-1, 1, 500)
    interp_f = compute_interp(x, f(x), x_eval, df=df(x))
    plt.plot(x_eval, f(x_eval))
    plt.plot(x_eval, interp_f)
    plt.plot(x, f(x), ".")
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


    function conf_vander_mat(x)
        n = length(x)
        conf_van = zeros(2*n, 2*n)
        power = 0:2*n-1
        for row = 1:n
            conf_van[row, :] = x[row].^power
            conf_van[row + n, :] = power.*x[row].^(power - 1)
        end
        return conf_van
    end


    function inter_coef(x; inter_type="lagrange")
        if inter_type == "lagrange"
            vand_mat = vander_mat(x)
        elseif inter_type == "hermite"
            vand_mat = conf_vander_mat(x)
        end
        coef = vand_mat \ eye(size(vand_mat)[1])
        return coef
    end


    function compute_interp(x, f, x_eval; df=nothing)
        n = length(x)
        if df == nothing
            coef = inter_coef(x, inter_type="lagrange")
        else
            coef = inter_coef(x, inter_type="hermite")
        end
        f_eval = zeros(x_eval)
        nmat = size(coef)[1]
        for row = 1:nmat
            for col = 1:nmat
                if col <= n || nmat == n
                    f_eval += coef[row, col]*x_eval.^(row - 1)*f[col]
                else
                    f_eval += coef[row, col]*x_eval.^(row - 1)*df[col - n]
                end
            end
        end
        return f_eval
    end


    n = 7
    x = -cos.(linspace(0, pi, n))
    f = 1./(1 + 25*x.^2)
    df = -50*x./(1 + 25*x.^2).^2
    x_eval = linspace(-1, 1, 500)
    interp_f = compute_interp(x, f, x_eval, df=df)
    plot(x_eval, 1./(1 + 25*x_eval.^2))
    plot(x_eval, interp_f)
    plot(x, f, ".")
    ylim(0, 1.2)
    show()

En ambos casos el resultado es el siguiente gráfico.

.. image:: /images/hermite_vandermonde.svg
   :width: 500 px
   :alt: Interpolación de Hermite usando la matriz de Vandermonde.
   :align:  center

Y, si probamos con un :math:`n` grande, digamos :math:`n=43`, podemos ver los
problemas.

.. image:: /images/hermite_vandermonde-n-23.svg
   :width: 500 px
   :alt: Interpolación de Hermite usando la matriz de Vandermonde.
   :align:  center


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 61 en Python y 70 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %%timeit -n 100
    n = 7
    x = -np.cos(np.linspace(0, np.pi, n))
    f = lambda x: 1/(1 + 25*x**2)
    df = lambda x: -50*x/(1 + 25*x**2)**2
    x_eval = np.linspace(-1, 1, 500)
    interp_f = compute_interp(x, f(x), x_eval, df=df(x))

con resultado

.. code::

    100 loops, best of 3: 18.1 ms per loop

Para Julia:

.. code:: julia

    function bench()
       n = 7
       x = -cos.(linspace(0, pi, n))
       f(x) = 1./(1 + 25*x.^2)
       df(x) = -50*x./(1 + 25*x.^2).^2
       x_eval = linspace(-1, 1, 500)
       interp_f = compute_interp(x, f(x), x_eval, df=df(x))
    end
    @benchmark bench()

con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  3.13 MiB
      allocs estimate:  836
      --------------
      minimum time:     10.318 ms (0.00% GC)
      median time:      10.449 ms (0.00% GC)
      mean time:        11.362 ms (1.74% GC)
      maximum time:     26.646 ms (0.00% GC)
      --------------
      samples:          100
      evals/sample:     1


En este caso, podemos decir que el código de Python es tan rápido como el de
Julia.

Comparación de Interpolación de Hermite/Lagrange
------------------------------------------------

Queremos comparar la interpolación de Hermite y de Lagrange para el mismo
número de grados de libertad. Usamos la misma función para la prueba

.. math::

    f(x) = \frac{1}{1 + 25x^2}

Este es el código de Python que hace la comparación

.. code:: Python

    n_dof = np.array(range(1, 20))
    error_herm = np.zeros(19)
    error_lag = np.zeros(19)
    for cont, n in enumerate(n_dof):
        f = lambda x: 1/(1 + 25*x**2)
        df = lambda x: -50*x/(1 + 25*x**2)**2
        x = -np.cos(np.linspace(0, np.pi, n))
        x2 = -np.cos(np.linspace(0, np.pi, 2*n))
        x_eval = np.linspace(-1, 1, 500)
        herm = compute_interp(x, f(x), x_eval, df=df(x))
        lag = compute_interp(x2, f(x2), x_eval)
        fun = f(x_eval)
        error_herm[cont] = np.linalg.norm(fun - herm)/np.linalg.norm(fun)
        error_lag[cont] = np.linalg.norm(fun - lag)/np.linalg.norm(fun)

    plt.plot(2*n_dof, error_lag)
    plt.plot(2*n_dof, error_herm)
    plt.xlabel("Number of degrees of freedom")
    plt.ylabel("Relative error")
    plt.legend(["Lagrange", "Hermite"])
    plt.show()

Y esta es la comparación de los errores relativos

.. image:: /images/hermite_lagrange_error.svg
   :width: 500 px
   :alt: Comparación de errores entre interpolación de Lagrange y Hermite.
   :align:  center

En general, la aproximación de Lagrange está cerca de la función.
