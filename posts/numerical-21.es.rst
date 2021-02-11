.. title: Reto de métodos numéricos: Día 21
.. slug: numerical-21
.. date: 2017-10-21 14:57:55 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, edp, diferencias finitas
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Itearación de Jacobi
====================

Hoy tenemos el `método de diferencias finitas
<https://en.wikipedia.org/wiki/Finite_difference_method>`_ combinado con
el `método de Jacobi <https://en.wikipedia.org/wiki/Jacobi_method>`_.
Vamos a resolver la ecuación de Laplace.

.. math::

    \nabla^ 2 u = 0

con

.. math::
    
    u(0, y) = 1 -y,\quad u(x, 0) = 1 - x,\\
    u(1, y) = u(x, 1) = 0

A continuación se presenta el código.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt


    def jacobi(u, update, tol=1e-6, niter=500):
        for n in range(niter):
            u_new = update(u)
            if np.linalg.norm(u_new - u) < tol:
                break
            else:
                u = u_new.copy()
        return u, n


    def heat_FDM(u):
        u_new = u.copy()
        u_new[1:-1, 1:-1] = 0.25*(u_new[0:-2, 1:-1] + u_new[2:, 1:-1] +\
             u_new[1:-1, 0:-2] + u_new[1:-1, 2:])
        return u_new

        
    nx = 50
    ny = 50
    x_vec = np.linspace(-0.5, 0.5, nx)
    y_vec = np.linspace(-0.5, 0.5, ny)
    u0 = np.zeros((nx, ny))
    u0[:, 0] = 1 - x_vec
    u0[0, :] = 1 - y_vec
    nvec = [100, 1000, 10000, 100000]
    for num, niter in enumerate(nvec):
        u, n = jacobi(u0, heat_FDM, tol=1e-12, niter=niter)
        plt.subplot(2, 2, num + 1)
        plt.contourf(u, cmap='hot')
        plt.xlabel(r"$x$")
        plt.ylabel(r"$y$")
        plt.title('{} iterations'.format(n + 1))
        plt.axis('image')
    plt.tight_layout()
    plt.show()


Julia
-----

.. code:: julia

    using PyPlot


    function jacobi(u, update; tol=1e-6, niter=500)
        num = niter
        for n = 1:niter
            u_new = update(u)
            if norm(u_new - u) < tol
                num = n
                break
            else
                u = copy(u_new)
            end
        end
        return u, num
    end


    function heat_FDM(u)
        u_new = copy(u)
        u_new[2:end-1, 2:end-1] = 0.25*(u_new[1:end-2, 2:end-1] +
            u_new[3:end, 2:end-1] + u_new[2:end-1, 1:end-2] + u_new[2:end-1, 3:end])
        return u_new
    end

        
    nx = 50
    ny = 50
    x_vec = linspace(-0.5, 0.5, nx)
    y_vec = linspace(-0.5, 0.5, ny)
    u0 = zeros(nx, ny)
    u0[:, 1] = 1 - x_vec
    u0[1, :] = 1 - y_vec
    nvec = [100, 1000, 10000, 100000]
    for (num, niter) = enumerate(nvec)
        u, n = jacobi(u0, heat_FDM, tol=1e-12, niter=niter)
        subplot(2, 2, num)
        contourf(u, cmap="hot")
        xlabel(L"$x$")
        ylabel(L"$y$")
        title("$(n) iterations")
        axis("image")
    end
    tight_layout()
    show()

.. image:: /images/jacobi_heat.svg
   :width: 600 px
   :alt: Solución de la ecuación diferencial que satisface las condicionse de frontera.
   :align:  center


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 40 en Python y 45 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit jacobi(u0, heat_FDM, tol=1e-12, niter=1000)

con resultado

.. code::

    10 loops, best of 3: 29.6 ms per loop

Para Julia:

.. code:: julia

    @benchmark jacobi(u0, heat_FDM, tol=1e-12, niter=1000)


con resultado

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  247.89 MiB
      allocs estimate:  43002
      --------------
      minimum time:     196.943 ms (5.66% GC)
      median time:      203.230 ms (5.74% GC)
      mean time:        203.060 ms (6.01% GC)
      maximum time:     208.017 ms (5.51% GC)
      --------------
      samples:          25
      evals/sample:     1


En este caso, podemos decir que el código de Python es alrededor de 10 veces
más rápido que el de Julia.
