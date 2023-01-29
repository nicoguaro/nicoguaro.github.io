.. title: Reto de métodos numéricos: Día 16
.. slug: numerical-16
.. date: 2017-10-17 16:29:00 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, cuadratura
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Cuadratura de Clenshaw-Curtis
=============================

Hoy tenemos la `cuadratura de Clenshaw-Curtis
<https://en.wikipedia.org/wiki/Clenshaw%E2%80%93Curtis_quadrature>`_. Este
método se basa en la expansión del integrando en
`polinomios de Chebyshev <https://en.wikipedia.org/wiki/Chebyshev_polynomials>`_.

Vamos a probar la cuadratura con la integral

.. math::
    \int_0^3 e^{-x^2} \mathrm{d}x \approx 0.8862073482595214

A continuación se presentan los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import linspace, cos, pi, exp, sum


    def clenshaw_curtis(fun, N=10, a=-1, b=1):
        nodes = linspace(-1, 1, N + 1)*pi
        jac = 0.5*(b - a)
        tfun = lambda x: fun(a + jac*(x + 1))
        inte = 0
        for k in range(0, N + 1, 2):
            coef = 1/N*(tfun(1) + tfun(-1)*(-1)**k +\
                2*sum(tfun(cos(nodes[1:-1]))*cos(k*nodes[1:-1])))
            if k == 0:
                inte += coef
            elif k == N:
                inte += coef/(1 - N**2)
            else:
                inte += 2*coef/(1 - k**2)
        return inte*jac

    N = 100
    fun = lambda x: exp(-x**2)
    print(clenshaw_curtis(fun, N=N, a=0, b=3))


con resultado

.. code:: python

    0.885906202792

Julia
-----

.. code:: julia

    function clenshaw_curtis(fun; N=50, a=-1, b=1)
        nodes = linspace(-1, 1, N + 1)*pi
        jac = 0.5*(b - a)
        tfun(x) = fun(a + jac*(x + 1))
        inte = 0
        for k = 0:2:N
            coef = 1/N*(tfun(1) + tfun(-1)*(-1)^k +
                2*sum(tfun(cos.(nodes[2:end-1])).*cos.(k*nodes[2:end-1])))
            if k == 0
                inte += coef
            elseif k == N
                inte += coef/(1 - N^2)
            else
                inte += 2*coef/(1 - k^2)
            end
        end
        return inte*jac
    end

    N = 100
    fun(x) = exp.(-x.^2)
    print(clenshaw_curtis(fun, N=N, a=0, b=3))


con resultado

.. code:: julia

    0.8859062027920102



Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 24 en Python y 23 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit -n 10000 clenshaw_curtis(fun, N=N, a=0, b=3)

con resultado

.. code::

    10000 loops, best of 3: 2.4 ms per loop

Para Julia:

.. code:: julia

    @benchmark clenshaw_curtis(fun, N=N, a=0, b=3)


con result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  359.56 KiB
      allocs estimate:  565
      --------------
      minimum time:     381.676 μs (0.00% GC)
      median time:      388.497 μs (0.00% GC)
      mean time:        413.471 μs (1.77% GC)
      maximum time:     1.298 ms (49.07% GC)
      --------------
      samples:          10000
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 6 veces
más lento que el de Julia.
