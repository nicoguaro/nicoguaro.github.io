.. title: Reto de métodos numéricos: Día 30
.. slug: numerical-30
.. date: 2017-10-30 19:38:03 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, gradiente conjugado
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Gradiente conjugado
===================

Hoy tenemos el `método del gradiente conjugado
<https://en.wikipedia.org/wiki/Conjugate_gradient_method>`_.
Este método se usa comúnmente para resolver sistemas lineales positivos
definidos. En comparación con el descenso del gradiente, escogemos una
dirección de descenso que es conjugado con su residual, es decir, es ortogonal
con una matriz de ponderación.

A continuación se presenta el código.

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


En este caso, vamos a probar el método con una matriz que viene de una 
discretización de una derivada de segundo orden usando diferencias finitas.


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 27 en Python y 27 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit conj_grad(A, b, x0)

con resultado

.. code::

     10 loops, best of 3: 107 ms per loop


Para Julia:

.. code:: julia

    @benchmark conj_grad(A, b, x0)


con resultado

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


En este caso, podemos decir que el código de Python es alrededor de 2 veces más
rápido que el de Julia.
