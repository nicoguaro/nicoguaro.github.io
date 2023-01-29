.. title: Reto de métodos numéricos: Día 28
.. slug: numerical-28
.. date: 2017-10-28 17:02:38 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, factorización lu
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Factorización LU
================

Hoy tenemos la `descomposición LU
<https://en.wikipedia.org/wiki/LU_decomposition>`_.
Este es la factorización de una matriz en su formas triangulares inferior (L)
y superior (U). Básicamente, almacena cada uno de los pasos de una eliminación
gaussiana en matrices.

A continuación el código.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np


    def LU(mat):
        m, _ = mat.shape
        mat = mat.copy()
        for col in range(0, m - 1):
            for row in range(col + 1, m):
                if mat[row, col] != 0.0:
                    lam = mat[row, col]/mat[col, col]
                    mat[row, col + 1:m] = mat[row, col + 1:m] -\
                                          lam * mat[col, col + 1:m]
                    mat[row, col] = lam
        return mat


    A = np.array([
        [1, 1, 0, 3],
        [2, 1, -1, 1],
        [3, -1, -1, 2],
        [-1, 2, 3, -1]], dtype=float)
    B = LU(A)


Julia
-----

.. code:: julia

    function LU(mat)
        m, _ = size(mat)
        mat = copy(mat)
        for col = 1:m - 2
            for row = col + 1:m
                if mat[row, col] != 0.0
                    lam = mat[row, col]/mat[col, col]
                    mat[row, col + 1:m] = mat[row, col + 1:m] -
                                          lam * mat[col, col + 1:m]
                    mat[row, col] = lam
                end
            end
        end
        return mat
    end


    A = [1.0 1.0 0.0 3.0;
        2.0 1.0 -1.0 1.0;
        3.0 -1.0 -1.0 2.0;
        -1.0 2.0 3.0 -1.0]
    B = LU(A)


Como un ejemplo tenemos la matriz

.. math::

    A = \begin{bmatrix}
        1 &1 &0 &3\\
        2 &1 &-1 &1\\
        3 &-1 &-1 &2\\
        -1 &2 &3 &-1
        \end{bmatrix} =
        \begin{bmatrix}
        1 &1 &0 &0\\
        2 &1 &0 &0\\
        3 &4 &1 &2\\
        -1 &-3 &0 &1
        \end{bmatrix}
        \begin{bmatrix}
        1 &1 &0 &3\\
        0 &-1 &-1 &-5\\
        0 &0 &3 &13\\
        0 &0 &0 &-13
        \end{bmatrix}

Y, la respuesta en ámbos códigos es

.. code::

    [[  1.,   1.,   0.,   3.],
     [  2.,  -1.,  -1.,  -5.],
     [  3.,   4.,   3.,  13.],
     [ -1.,  -3.,   0., -13.]]


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 23 en Python y 22 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit LU(np.random.rand(10, 10))

con resultado

.. code::

     1000 loops, best of 3: 303 µs per loop


Para Julia:

.. code:: julia

    @benchmark LU(rand(10, 10))


con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  29.25 KiB
      allocs estimate:  310
      --------------
      minimum time:     9.993 μs (0.00% GC)
      median time:      11.725 μs (0.00% GC)
      mean time:        14.943 μs (15.90% GC)
      maximum time:     3.285 ms (95.64% GC)
      --------------
      samples:          10000
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 30 veces
más lento que el de Julia.
