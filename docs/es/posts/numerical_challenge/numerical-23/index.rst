.. title: Reto de métodos numéricos: Día 23
.. slug: numerical-23
.. date: 2017-10-23 20:30:03 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, método de ritz
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Método de Ritz
==============

Hoy tenemos el `método de Ritz <https://en.wikipedia.org/wiki/Ritz_method>`_
para resolver la ecuación:

.. math::

    \frac{d^2 u}{dx^2} = f(x)

con

.. math::

    u(0) = u(1)  = 0

El método consiste en formar un funcional que es *equivalente* a la ecuación
diferencial, proponer una aproximación como una combinación lineal de un 
conjunto de funciones base y encontrar el *mejor* conjunto de coeficientes
para esta combinación. Este *mejor* solución se encuentra minimizando el 
funcional.

El funcional para esta ecuación diferencial es

.. math::

    \Pi[u] = -\int_{0}^{1} \left(\frac{d u}{d x}\right)^2 dx
             -\int_{0}^{1}  u f(x) dx

En este caso, estamos usando la aproximación

.. math::
    \hat{u}(x) = x (1 - x)\sum_{n=0}^{N} c_n x^n\, ,

en donde escogimos el factor :math:`x (1 - x)` para forzar que las funciones
satisfagan las condiciones de frontera. El funcional aproximado es

.. math::

    \Pi[\hat{u}] = -\sum_{n=0}^{N} \sum_{m=0}^{N} c_n c_m
        \left[\frac{2 + 2m + 2n + 2mn}{(n + m + 1)(n + m + 2)(n + m +3)}\right]
        -\\ \sum_{n=0}^{N} c_n\int_{0}^{1} x^{n + 1}(1 - x) f(x) dx

en donde, en general, necesitamos realizar una integración numérica para el
segundo término.

Minimizando el funcional

.. math::

    \frac{\partial \Pi[\hat{u}]}{\partial c_m} = 0\, ,

obtenmos el siguiente sistema de ecuaciones

.. math::

    [K]\{\mathbf{c}\} = \{\mathbf{b}\}

con

.. math::

    K_{mn} = \frac{2 + 2m + 2n + 2mn}{(n + m + 1)(n + m + 2)(n + m +3)}

y

.. math::

    b_m = -\int_{0}^{1} x^{m + 1}(1 - x) f(x) dx\, .

Probaremos la implementación con la función :math:`f(x) = x^3`, que
lleva a la solución

.. math::

    u(x) = \frac{x (x^4 - 1)}{20}


A continuación se presenta el código.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    from scipy.integrate import quad
    from scipy.linalg import solve
    import matplotlib.pyplot as plt


    def ritz(N, source):
        stiff_mat = np.zeros((N, N))
        rhs = np.zeros((N))
        for row in range(N):
            for col in range(N):
                numer = (2 + 2*row + 2*col + 2*row*col)
                denom = (row + col + 1) * (row + col + 2) * (row + col + 3)
                stiff_mat[row, col] = numer/denom
            fun = lambda x: x**(row + 1)*(1 - x)*source(x)
            rhs[row], _ = quad(fun, 0, 1)
        return stiff_mat, rhs


    N = 2
    source = lambda x: x**3
    mat, rhs = ritz(N, source)
    c = solve(mat, -rhs)
    x = np.linspace(0, 1, 100)
    y = np.zeros_like(x)
    for cont in range(N):
        y += c[cont]*x**(cont + 1)*(1 - x)

    #%% Plotting
    plt.figure(figsize=(4, 3))
    plt.plot(x, y)
    plt.plot(x, x*(x**4 - 1)/20, linestyle="dashed")
    plt.xlabel(r"$x$")
    plt.ylabel(r"$y$")
    plt.legend(["Ritz solution", "Exact solution"])
    plt.tight_layout()
    plt.show()




Julia
-----

.. code:: julia

    using PyPlot


    function ritz(N, source)
        stiff_mat = zeros(N, N)
        rhs = zeros(N)
        for row in 0:N-1
            for col in 0:N-1
                numer = (2 + 2*row + 2*col + 2*row*col)
                denom = (row + col + 1) * (row + col + 2) * (row + col + 3)
                stiff_mat[row + 1, col + 1] = numer/denom
            end
            fun(x) = x^(row + 1)*(1 - x)*source(x)
            rhs[row + 1], _  = quadgk(fun, 0, 1)
        end
        return stiff_mat, rhs
    end


    N = 2
    source(x) = x^3
    mat, rhs = ritz(N, source)
    c = -mat\rhs
    x = linspace(0, 1, 100)
    y = zeros(x)
    for cont in 0:N - 1
        y += c[cont + 1]*x.^(cont + 1).*(1 - x)
    end

    #%% Plotting
    figure(figsize=(4, 3))
    plot(x, y)
    plot(x, x.*(x.^4 - 1)/20, linestyle="dashed")
    xlabel(L"$x$")
    ylabel(L"$y$")
    legend(["Ritz solution", "Exact solution"])
    tight_layout()
    show()

Ambos tiene (casi) el mismo resultado y se muestra a continuación

.. image:: /images/ritz.svg
   :width: 400 px
   :alt: Método de Ritz usando 2 términos.
   :align:  center

Y si consideramos 3 términos en la expansion, obtenemos

.. image:: /images/ritz-N-3.svg
   :width: 400 px
   :alt: Método de Ritz usando 3 términos.
   :align:  center


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 38 en Python y 38 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %%timeit
    mat, rhs = ritz(5, source)
    c = solve(mat, -rhs)

con resultado

.. code::

     1000 loops, best of 3: 228 µs per loop


Para Julia:

.. code:: julia

    function bench()
       mat, rhs = ritz(N, source)
       c = -mat\rhs
    end
    @benchmark bench()


con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  6.56 KiB
      allocs estimate:  340
      --------------
      minimum time:     13.527 μs (0.00% GC)
      median time:      15.927 μs (0.00% GC)
      mean time:        17.133 μs (4.50% GC)
      maximum time:     2.807 ms (97.36% GC)
      --------------
      samples:          10000
      evals/sample:     1

En este caso, podemos decir que el código de Python es alrededor de 14 veces
más lento que el de Julia.
