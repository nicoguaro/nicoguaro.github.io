.. title: Numerical methods challenge: Day 30
.. slug: numerical-30
.. date: 2017-10-30 19:38:03 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, conjugate gradient
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Conjugate gradient
==================

Today we have the `conjugate gradient method <https://en.wikipedia.org/wiki/Conjugate_gradient_method>`_.
This method is commonly used to solve positive-definite linear systems of
equations. Compared with gradient descent, we choose as descent direction
a direction that is conjugated with the residual, that is, it is
orthogonal with the matrix as weighting.


Following are the codes

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np


    def conj_grad(A, b, x, tol=1e-8):
        r = b - A.dot(x)
        p = r
        rsq_old = r.dot(r)
        for cont in range(len(b)):
            Ap = A.dot(p)
            alpha = rsq_old / p.dot(Ap)
            x = x + alpha*p
            r = r - alpha*Ap
            rsq_new = r.dot(r)
            if np.sqrt(rsq_new) < tol:
                break
            p = r + (rsq_new / rsq_old) * p
            rsq_old = rsq_new
        return x, cont, np.sqrt(rsq_new)


    N = 1000
    A = -np.diag(2*np.ones(N)) + np.diag(np.ones(N-1), -1) +\
        np.diag(np.ones(N-1), 1)
    b = np.ones(N)
    x0 = np.ones(N)
    x, niter, accu = conj_grad(A, b, x0)


Julia
-----

.. code:: julia

    function conj_grad(A, b, x; tol=1e-8)
        r = b - A * x
        p = r
        rsq_old = dot(r, r)
        niter = 1
        for cont = 1:length(b)
            Ap = A * p
            alpha = rsq_old / dot(p, Ap)
            x = x + alpha*p
            r = r - alpha*Ap
            rsq_new = dot(r, r)
            if sqrt(rsq_new) < tol
                break
            end
            p = r + (rsq_new / rsq_old) * p
            rsq_old = rsq_new
            niter += 1
        end
        return x, niter, norm(r)
    end


    N = 1000
    A = -diagm(2*ones(N)) + diagm(ones(N-1), -1) + diagm(ones(N-1), 1)
    b = ones(N)
    x0 = ones(N)
    x, niter, accu = conj_grad(A, b, x0)

In this case, we are testing the method with a matrix that comes from
the discretization of the second order derivative using finite differences.


Comparison Python/Julia
-----------------------

Regarding number of lines we have: 27 in Python and 27 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit conj_grad(A, b, x0)

with result

.. code::

     10 loops, best of 3: 107 ms per loop


For Julia:

.. code:: julia

    @benchmark conj_grad(A, b, x0)



with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  27.13 MiB
      allocs estimate:  3501
      --------------
      minimum time:     128.477 ms (0.54% GC)
      median time:      294.407 ms (0.24% GC)
      mean time:        298.208 ms (0.30% GC)
      maximum time:     464.223 ms (0.30% GC)
      --------------
      samples:          17
      evals/sample:     1


In this case, we can say that the Python code is roughly 2 times faster than
Julia code.
