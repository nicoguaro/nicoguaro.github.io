.. title: Reto de métodos numéricos: Día 24
.. slug: numerical-24
.. date: 2017-10-24 15:17:58 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, método de elementos finitos
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Método de elementos finitos
===========================

Hoy tenemos el `método de elementos finitos
<https://en.wikipedia.org/wiki/Finite_element_method>`_ para resolver la
ecuación:

.. math::

    \frac{d^2 u}{dx^2} = f(x)

con

.. math::

    u(0) = u(1)  = 0

Como en el `método de Ritz <posts/numerical-23>`_ formamos un funcional
que es *equivalente* a la ecuación diferencial, proponemos una aproximación que
es una combinación lineal de funciones base y encontramos el *mejor* conjunto
de coeficientes para esta combinación. La *mejor* solución se encuentra
minimizando el funcional.

El funcional para este ecuación diferencial es

.. math::

    \Pi[u] = -\int_{0}^{1} \left(\frac{d u}{d x}\right)^2 dx
             -\int_{0}^{1}  u f(x) dx

La diferencia principal es que usamos interpolación por tramos como funciones
base,

.. math::
    \hat{u}(x) = \sum_{n=0}^{N} u_n N_n(x)\, ,

Esto lleva al siguiente sistema de ecuaciones

.. math::

    [K]\{\mathbf{c}\} = \{\mathbf{b}\}

donde las matrices de rigidez locales están dadas por

.. math::

    K_\text{local} =  \frac{1}{|J|}\begin{bmatrix} 2 & -2\\ -2 &2\end{bmatrix}

y

.. math::

    b_\text{local} = -|J|\begin{bmatrix} f(x_m)\\ f(x_{n})\end{bmatrix}\, ,

donde :math:`|J|` es el determinante jacobian de la transformación. Me estoy
saltando muchos detalles respecto al ensamblaje; sería muy costoso describir
el proceso completo.

Probaremos la implementación con la función :math:`f(x) = x^3`, que lleva a
la solución
.. math::

    u(x) = \frac{x (x^4 - 1)}{20}


A continuacón se presenta el código.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt


    def FEM1D(coords, source):
        N = len(coords)
        stiff_loc = np.array([[2.0, -2.0], [-2.0, 2.0]])
        eles = [np.array([cont, cont + 1]) for cont in range(0, N - 1)]
        stiff = np.zeros((N, N))
        rhs = np.zeros(N)
        for ele in eles:
            jaco = coords[ele[1]] - coords[ele[0]]
            rhs[ele] = rhs[ele] + jaco*source(coords[ele])
            for cont1, row in enumerate(ele):
                for cont2, col in enumerate(ele):
                    stiff[row, col] = stiff[row, col] +  stiff_loc[cont1, cont2]/jaco
        return stiff, rhs


    N = 100
    fun = lambda x: x**3
    x = np.linspace(0, 1, N)
    stiff, rhs = FEM1D(x, fun)
    sol = np.zeros(N)
    sol[1:-1] = np.linalg.solve(stiff[1:-1, 1:-1], -rhs[1:-1])


    #%% Plotting
    plt.figure(figsize=(4, 3))
    plt.plot(x, sol)
    plt.plot(x, x*(x**4 - 1)/20, linestyle="dashed")
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    plt.legend(["FEM solution", "Exact solution"])
    plt.tight_layout()
    plt.show()

Julia
-----

.. code:: julia

    using PyPlot


    function FEM1D(coords, source)
        N = length(coords)
        stiff_loc = [2.0 -2.0; -2.0 2.0]
        eles = [[cont, cont + 1] for cont in 1:N-1]
        stiff = zeros(N, N)
        rhs = zeros(N)
        for ele in eles
            jaco = coords[ele[2]] - coords[ele[1]]
            rhs[ele] = rhs[ele] + jaco*source(coords[ele])
            stiff[ele, ele] = stiff[ele, ele] +  stiff_loc/jaco
        end
        return stiff, rhs
    end


    N = 100
    fun(x) = x.^3
    x = linspace(0, 1, N)
    stiff, rhs = FEM1D(x, fun)
    sol = zeros(N)
    sol[2:end-1] = -stiff[2:end-1, 2:end-1]\rhs[2:end-1]


    #%% Plotting
    figure(figsize=(4, 3))
    plot(x, sol)
    plot(x, x.*(x.^4 - 1)/20, linestyle="dashed")
    xlabel(L"$x$")
    ylabel(L"$y$")
    legend(["FEM solution", "Exact solution"])
    tight_layout()
    show()

Ambos presentan el mismo resultado que se ve a continuación.

.. image:: /images/FEM1D.svg
   :width: 400 px
   :alt: Aproximación por el método de elementos finitos.
   :align:  center



Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 37 en Python y 35 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia. Para la comparación solo estamos considerando el
tiempo que toma formar las matrices.

Para Python:

.. code:: IPython

    %timeit FEM1D(x, fun)

con resultado

.. code::

     100 loops, best of 3: 2.15 ms per loop


Para Julia:

.. code:: julia

    @benchmark FEM1D(x, fun)


con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  183.73 KiB
      allocs estimate:  1392
      --------------
      minimum time:     60.045 μs (0.00% GC)
      median time:      70.445 μs (0.00% GC)
      mean time:        98.276 μs (25.64% GC)
      maximum time:     4.269 ms (96.70% GC)
      --------------
      samples:          10000
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 30 veces
más lento que el de Julia.
