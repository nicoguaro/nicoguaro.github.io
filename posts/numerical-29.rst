.. title: Numerical methods challenge: Day 29
.. slug: numerical-29
.. date: 2017-10-29 21:10:08 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, cholesky decomposition
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Cholesky decomposition
======================

Today we have `Cholesky decomposition <https://en.wikipedia.org/wiki/Cholesky_decomposition>`_.
It is a factorization of a Hermitian, positive-definite matrix into
a lower and upper matrix, the main difference with LU decomposition
is that it the lower matrix is the Hermitian transpose of the upper one.

Following are the codes

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


As an example we have the matrix

.. math::

    A = \begin{bmatrix}
         4 &-1 &1\\
        -1 &4.25 &2.75\\
         1 &2.75 &3.5
        \end{bmatrix}

And, the answer of both codes is

.. code::

    2.0  0.0  0.0
    -0.5  2.0  0.0
    0.5  1.5  1.0



Comparison Python/Julia
-----------------------

Regarding number of lines we have: 23 in Python and 22 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit cholesky(np.eye(100))

with result

.. code::

     100 loops, best of 3: 13 ms per loop


For Julia:

.. code:: julia

    @benchmark cholesky(eye(100))


with result

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


In this case, we can say that the Python code is roughly 10 times slower than
Julia code.
