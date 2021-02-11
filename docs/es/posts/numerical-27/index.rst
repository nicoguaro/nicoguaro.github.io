.. title: Reto de métodos numéricos: Día 27
.. slug: numerical-27
.. date: 2017-10-27 21:27:06 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, monte carlo
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Integración Monte Carlo
========================

Hoy tenemos la `integración Monte Carlo
<https://en.wikipedia.org/wiki/Monte_Carlo_integration>`_.
En donde usamos muestreo aleatorio para calcular una integral numéricamente.
Este método es importante cuando tenemos que evaluar integrales 
multidimensionales ya que las técnicas de cuadratura usuales implican un
crecimiento exponencial con el número de puntos de muestreo.

El método cálcula una integral

.. math::

    I = \int_\Omega f(x) dx

donde :math:`\Omega` tiene volumen :math:`V`.

La integral es aproximada como

.. math::

    I \approx \frac{V}{N} \sum_{i=1}^{N} f(x_i)

donde :math:`x_i` está distribuido de manera uniforme sobre :math:`\Omega`.


A continuación se presenta el código.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np


    def monte_carlo_int(fun, N, low, high, args=()):
        ndims = len(low)
        pts = np.random.uniform(low=low, high=high, size=(N, ndims))
        V = np.prod(np.asarray(high) - np.asarray(low))
        return V*np.sum(fun(pts, *args))/N


    def circ(x, rad):
        return 0.5*(1 - np.sign(x[:, 0]**2 + x[:, 1]**2 - rad**2))


    N = 1000000
    low = [-1, -1]
    high = [1, 1]
    rad = 1
    inte = monte_carlo_int(circ, N, low, high, args=(rad,))


Julia
-----

.. code:: julia

    using Distributions


    function monte_carlo_int(fun, N, low, high; args=())
        ndims = length(low)
        pts = rand(Uniform(0, 1), N, ndims)
        for cont = 1:ndims
            pts[:, cont] = pts[:, cont]*(high[cont] - low[cont]) + low[cont]
        end
        V = prod(high - low)
        return V*sum(fun(pts, args...))/N
    end


    function circ(x, rad)
        return 0.5*(1 - sign.(x[:, 1].^2 + x[:, 2].^2 - rad^2))
    end


    N = 1000000
    low = [-1, -1]
    high = [1, 1]
    rad = 1
    inte = monte_carlo_int(circ, N, low, high, args=(rad,))


Una de los ejemplos más comunes es el cálculo de :math:`\pi`, esto se
ilustra en la siguiente animación.

.. image:: https://upload.wikimedia.org/wikipedia/commons/8/84/Pi_30K.gif
   :width: 500 px
   :alt: Aproximación de pi usando Monte Carlo.
   :align:  center


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 20 en Python y 24 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit monte_carlo_int(circ, N, low, high, args=(rad,))

con resultado

.. code::

     10 loops, best of 3: 53.2 ms per loop


Para Julia:

.. code:: julia

    @benchmark monte_carlo_int(circ, N, low, high, args=(rad,))


con result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  129.70 MiB
      allocs estimate:  46
      --------------
      minimum time:     60.131 ms (5.15% GC)
      median time:      164.018 ms (55.64% GC)
      mean time:        204.366 ms (49.50% GC)
      maximum time:     357.749 ms (64.04% GC)
      --------------
      samples:          25
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 3 veces más
rápido que el de Julia.
