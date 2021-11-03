.. title: Reto de métodos numéricos: Día 29
.. slug: numerical-29
.. date: 2017-10-29 21:10:08 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, descomposición de cholesky
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Descomposición de Cholesky
==========================

Hoy tenemos la `descomposición de Cholesky
<https://en.wikipedia.org/wiki/Cholesky_decomposition>`_.
Es una factorización de una matriz hermítica, positiva definita en matrices
triangulares inferior y superior. La diferencia principal con la descomposición LU
es que la matriz inferior es la transpuesta hermítica de la superior.

A continuación se presenta el código.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np


    def cholesky(mat):
        m, _ = mat.shape
        mat = mat.copy()
        for col in range(m):
            print(mat[col, col] -
                   mat[col, 0:col].dot(mat[col, 0:col]))
            mat[col, col] = np.sqrt(mat[col, col] -
                   mat[col, 0:col].dot(mat[col, 0:col]))
            for row in range(col + 1, m):
                mat[row, col] = (mat[row, col] -
                   mat[row, 0:col].dot(mat[col, 0:col]))/mat[col, col]
        for row in range(1, m):
            mat[0:row, row] = 0
        return mat


    A = np.array([
        [4, -1, 1],
        [-1, 4.25, 2.75],
        [1, 2.75, 3.5]], dtype=float)
    B = cholesky(A)


Julia
-----

.. code:: julia

    function cholesky(mat)
        m, _ = size(mat)
        mat = copy(mat)
        for col = 1:m
            mat[col, col] = sqrt(mat[col, col] -
                dot(mat[col, 1:col-1], mat[col, 1:col-1]))
            for row = col + 1:m
                mat[row, col] = (mat[row, col] -
                   dot(mat[row, 1:col-1], mat[col, 1:col-1]))/mat[col, col]
            end
        end
        for row = 2:m
            mat[1:row-1, row] = 0
        end
        return mat
    end


    A = [4 -1 1;
        -1 4.25 2.75;
        1 2.75 3.5]
    B = cholesky(A)


Como ejemplo tenemos la siguiente matriz

.. math::

    A = \begin{bmatrix}
         4 &-1 &1\\
        -1 &4.25 &2.75\\
         1 &2.75 &3.5
        \end{bmatrix}

Y la respuesta en ambos códigos es

.. code::

    2.0  0.0  0.0
    -0.5  2.0  0.0
    0.5  1.5  1.0



Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 23 en Python y 22 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit cholesky(np.eye(100))

con resultado

.. code::

     100 loops, best of 3: 13 ms per loop


Para Julia:

.. code:: julia

    @benchmark cholesky(eye(100))


con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  4.01 MiB
      allocs estimate:  20303
      --------------
      minimum time:     1.010 ms (0.00% GC)
      median time:      1.136 ms (0.00% GC)
      mean time:        1.370 ms (17.85% GC)
      maximum time:     4.652 ms (40.37% GC)
      --------------
      samples:          3637
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 10 veces
más lento que el de Julia.
