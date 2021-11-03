.. title: Reto de métodos numéricos: Día 7
.. slug: numerical-07
.. date: 2017-10-07 14:51:35 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, optimización
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Método de Nelder-Mead
=====================

Hoy tenemos el `métod de Nelder-Mead
<https://es.wikipedia.org/wiki/M%C3%A9todo_Nelder-Mead>`_. Este método usa un
`símplice <https://es.wikipedia.org/wiki/S%C3%ADmplex>`_ en
:math:`\mathbb{R}^n`, por ejemplo, un triángulo en :math:`\mathbb{R}^2` o un
tetraedro en :math:`\mathbb{R}^3`.


.. image:: https://upload.wikimedia.org/wikipedia/commons/e/e4/Nelder-Mead_Rosenbrock.gif
   :width: 600 px
   :alt: Animación ilustrando el método de Nelder-Mead.
   :align:  center


*En un solo paso del método, eliminamos el vértice con el peor valor de función
y lo reemplazamos por otro con un mejor valor. El nuevo punto se obtiene
reflejando, expandiendo o contrayendo el símplice a lo largo de la línea que une
el peor vértice con el centroide de los vértices restantes. Si no podemos
encontrar un punto mejor de esta manera, retenemos solo el vértice con el
mejor valor de función y encogemos el simplex moviendo todos los demás
vértices hacia este valor.*  Nocedal y Wright (2006), Numerical Optimization.

A continuación se presenta el código.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    from numpy import array
    from numpy.linalg import norm


    def nelder_mead_step(fun, verts, alpha=1, gamma=2, rho=0.5,
                         sigma=0.5):
        """Nelder-Mead iteration according to Wikipedia _[1]


        References
        ----------
         .. [1] Wikipedia contributors. "Nelder–Mead method." Wikipedia,
             The Free Encyclopedia. Wikipedia, The Free Encyclopedia,
             1 Sep. 2016. Web. 20 Sep. 2016.
        """
        nverts, _ = verts.shape
        f = np.apply_along_axis(fun, 1, verts)
        # 1. Order
        order = np.argsort(f)
        verts = verts[order, :]
        f = f[order]
        # 2. Calculate xo, the centroid"
        xo = verts[:-1, :].mean(axis=0)
        # 3. Reflection
        xr = xo + alpha*(xo - verts[-1, :])
        fr = fun(xr)
        if f[0]<=fr and fr<f[-2]:
            new_verts = np.vstack((verts[:-1, :], xr))
        # 4. Expansion
        elif fr<f[0]:
            xe = xo + gamma*(xr - xo)
            fe = fun(xe)
            if fe < fr:
                new_verts = np.vstack((verts[:-1, :], xe))
            else:
                new_verts = np.vstack((verts[:-1, :], xr))
        # 5. Contraction
        else:
            xc = xo + rho*(verts[-1, :] - xo)
            fc = fun(xc)
            if fc < f[-1]:
                new_verts = np.vstack((verts[:-1, :], xc))
        # 6. Shrink
            else:
                new_verts = np.zeros_like(verts)
                new_verts[0, :] = verts[0, :]
                for k in range(1, nverts):
                    new_verts[k, :] = sigma*(verts[k,:] - verts[0,:])

        return new_verts


    def nelder_mead(fun, x, niter=200, atol=1e-8, verbose=False):
        msg = "Maximum number of iterations reached."
        f_old = fun(x.mean(0))
        for cont in range(niter):
            if verbose:
                print("n: {}, x: {}".format(cont, x.mean(0)))
            x = nelder_mead_step(fun, x)
            df = fun(x.mean(0)) - f_old
            f_old = fun(x.mean(0))
            if norm(df) < atol:
                msg = "Extremum found with desired accuracy."
                break
        return x.mean(0), f_old, msg


    def rosen(x):
        return (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2


    x = array([[1, 0],
               [1, 1],
               [2, 0]])
    print(nelder_mead(rosen, x))

con resultado

.. code:: python

    (array([0.99994674, 0.99987728]), 2.90769311467343e-08, 'Extremum found with desired accuracy.')

Julia
------

.. code:: julia

    function nelder_mead_step(fun, verts; alpha=1, gamma=2, rho=0.5,
                         sigma=0.5)
        nverts, _ = size(verts)
        f = [fun(verts[row, :]) for row in 1:nverts]
        # 1. Order
        order = sortperm(f)
        verts = verts[order, :]
        f = f[order]
        # 2. Calculate xo, the centroid
        xo = mean(verts[1:end - 1, :], 1)
        # 3. Reflection
        xr = xo + alpha*(xo - verts[end, :]')
        fr = fun(xr)
        if f[1]<=fr && fr<f[end - 1]
            new_verts = [verts[1:end-1, :]; xr]
        # 4. Expansion
        elseif fr<f[1]
            xe = xo + gamma*(xr - xo)
            fe = fun(xe)
            if fe < fr
                new_verts = [verts[1:end-1, :]; xe]
            else
                new_verts = [verts[1:end-1, :]; xr]
            end
        # 5. Contraction
        else
            xc = xo + rho*(verts[end, :]' - xo)
            fc = fun(xc)
            if fc < f[end]
                new_verts = [verts[1:end-1, :]; xc]
        # 6. Shrink
            else
                new_verts = zeros(verts)
                new_verts[1, :] = verts[1, :]
                for k =  1:nverts
                    new_verts[k, :] = sigma*(verts[k,:] - verts[1,:])
                end
            end
        end

        return new_verts
    end


    function nelder_mead(fun, x; niter=50, atol=1e-8, verbose=false)
        msg = "Maximum number of iterations reached."
        f_old = fun(mean(x, 1))
        for cont = 1:niter
            if verbose
                println("n: $(cont), x: $(mean(x, 1))")
            end
            x = nelder_mead_step(fun, x)
            df = fun(mean(x, 1)) - f_old
            f_old = fun(mean(x, 1))
            if norm(df) < atol
                msg = "Extremum found with desired accuracy."
                break
            end
        end
        return mean(x, 1), f_old, msg
    end


    function rosen(x)
        return (1 - x[1])^2 + 100*(x[2] - x[1]^2)^2
    end


    x = [1 0;
        1 1;
        2 0]
    println(nelder_mead(rosen, x, verbose=false))

con resultado

.. code:: julia

    ([0.999947 0.999877], 2.9076931147093985e-8, "Extremum found with desired accuracy.")


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 38 en Python y 39 en Julia. La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit nelder_mead(rosen, x)

con resultado

.. code::

    100 loops, best of 3: 7.82 ms per loop

Para Julia:

.. code:: julia

    @benchmark grad_descent(rosen, rosen_grad, [2.0, 1.0])

con resultado

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  162.23 KiB
      allocs estimate:  4780
      --------------
      minimum time:     462.926 μs (0.00% GC)
      median time:      506.511 μs (0.00% GC)
      mean time:        552.411 μs (3.86% GC)
      maximum time:     5.179 ms (80.31% GC)
      --------------
      samples:          9008
      evals/sample:     1

En este caso, podemos decir que el código de Python es 15 veces más lento que
el de Julia.
