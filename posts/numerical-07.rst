.. title: Numerical methods challenge: Day 7
.. slug: numerical-07
.. date: 2017-10-07 14:51:35 UTC-05:00
.. tags: mathjax, numerical methods, python, julia, scientific computing, optimization
.. category: Scientific Computing
.. link: 
.. description: 
.. type: text

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Nelder-Mead method
==================

Today we have
`Nelder-Mead method <https://en.wikipedia.org/wiki/Nelder%E2%80%93Mead_method>`_.
This method uses a simplex over :math:`\mathbb{R}^n`, e.g., a triangle in
:math:`\mathbb{R}^2` or a tetrahedron over :math:`\mathbb{R}^3`.


.. image:: https://upload.wikimedia.org/wikipedia/commons/e/e4/Nelder-Mead_Rosenbrock.gif
   :width: 600 px
   :alt: Animation showing Nelder-Mead method.
   :align:  center

*In a single step of the method, we remove the vertex with the worst function
value and replace it with another one with a better value. The new point is
obtained by reflecting, expanding, or contracting the simplex along the line
joining the worst vertex with the centroid of the remaining vertices. If we
cannot find a better point in this manner, we retain only the vertex with
the best function value, and we shrink the simplex by moving all other
vertices towards this value.* Nocedal and Wright (2006), Numerical Optimization.

Following are the codes.


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
        if f[0]<=fr and fr<f[1]:
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

with result


.. code:: python

    (array([ 0.99994674,  0.99987728]), 2.9076931146734301e-08, 'Extremum found with desired accuracy.')

Julia
------

.. code:: julia

    function nelder_mead_step(fun, verts; alpha=1, gamma=2, rho=0.5,
                         sigma=0.5)
        nverts, _ = size(verts)
        f = [fun(x[row, :]) for row in 1:nverts]
        # 1. Order
        order = sortperm(f)
        verts = verts[order, :]
        f = f[order]
        # 2. Calculate xo, the centroid
        xo = mean(verts[1:end - 1, :], 1)
        # 3. Reflection
        xr = xo + alpha*(xo - verts[end, :]')
        fr = fun(xr)
        if f[1]<=fr && fr<f[2]
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


    function nelder_mead(fun, x; niter=200, atol=1e-8, verbose=false)
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
    println(nelder_mead(rosen, x))
