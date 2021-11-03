.. title: Numerical methods challenge: Day 28
.. slug: numerical-28
.. date: 2017-10-28 17:02:38 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, lu factorization
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

LU factorization
================

Today we have `LU decomposition <https://en.wikipedia.org/wiki/LU_decomposition>`_.
That is a factorization of a matrix into a lower (L) and upper (U) matrix.
Basically it stores de steps of a Gauss elimination in matrices.

Following are the codes

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


As an example we have the matrix

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

And, the answer of both codes is

.. code::

    [[  1.,   1.,   0.,   3.],
     [  2.,  -1.,  -1.,  -5.],
     [  3.,   4.,   3.,  13.],
     [ -1.,  -3.,   0., -13.]]


Comparison Python/Julia
-----------------------

Regarding number of lines we have: 23 in Python and 22 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit LU(np.random.rand(10, 10))

with result

.. code::

     1000 loops, best of 3: 303 µs per loop


For Julia:

.. code:: julia

    @benchmark LU(rand(10, 10))


with result

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


In this case, we can say that the Python code is roughly 30 times slower than
Julia code.
