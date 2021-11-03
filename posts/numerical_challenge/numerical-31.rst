.. title: Numerical methods challenge: Day 31
.. slug: numerical-31
.. date: 2017-10-31 20:45:09 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, conjugate gradient, finite element method
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I wrote a program per day for some well-known
numerical methods in both Python and Julia. It was intended to be an exercise,
then don't expect the code to be good enough for real use. Also,
I should mention that I had almost no experience with Julia, so it
probably is not idiomatic Julia but more Python-like Julia.

Putting some things together
============================

Today, I am putting some things together, namely, I am going to solve the
system of equations that results in the finite element using the conjugate
gradient.


Following are the codes

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt


    def FEM1D(coords, source):
        N = len(coords)
        stiff_loc = np.array([[2.0, -2.0], [-2.0, 2.0]])
        eles = [np.array([cont, cont + 1]) for cont in range(0, N - 1)]
        stiff = np.zeros((N, N))
        rhs = np.zeros(N)
        for ele in eles:
            jaco = coords[ele[1]] - coords[ele[0]]
            rhs[ele] = rhs[ele] + jaco*source(coords[ele])
            for cont1, row in enumerate(ele):
                for cont2, col in enumerate(ele):
                    stiff[row, col] = stiff[row, col] +  stiff_loc[cont1, cont2]/jaco
        return stiff, rhs


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


    fun = lambda x: x**3
    N_vec = np.logspace(0.5, 3, 50, dtype=int)
    err_vec = np.zeros_like(N_vec, dtype=float)
    niter_vec = np.zeros_like(N_vec)
    plt.figure(figsize=(8, 3))
    for cont, N in enumerate(N_vec):
        x = np.linspace(0, 1, N)
        stiff, rhs = FEM1D(x, fun)
        sol = np.zeros(N)
        sol[1:-1], niter, _ = conj_grad(stiff[1:-1, 1:-1], -rhs[1:-1], rhs[1:-1])
        err = np.linalg.norm(sol - x*(x**4 - 1)/20)/np.linalg.norm(x*(x**4 - 1)/20)
        err_vec[cont] = err
        niter_vec[cont] = niter

    plt.subplot(121)
    plt.loglog(N_vec, err_vec)
    plt.xlabel("Number of nodes")
    plt.ylabel("Relative error")
    plt.subplot(122)
    plt.loglog(N_vec, niter_vec)
    plt.xlabel("Number of nodes")
    plt.ylabel("Number of iterations")
    plt.tight_layout()
    plt.show()





Julia
-----

.. code:: julia

    using PyPlot


    function FEM1D(coords, source)
        N = length(coords)
        stiff_loc = [2.0 -2.0; -2.0 2.0]
        eles = [[cont, cont + 1] for cont in 1:N-1]
        stiff = zeros(N, N)
        rhs = zeros(N)
        for ele in eles
            jaco = coords[ele[2]] - coords[ele[1]]
            rhs[ele] = rhs[ele] + jaco*source(coords[ele])
            stiff[ele, ele] = stiff[ele, ele] +  stiff_loc/jaco
        end
        return stiff, rhs
    end


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



    fun(x) = x.^3
    N_vec = round.(logspace(0.5, 3, 50))
    err_vec = zeros(N_vec)
    niter_vec = zeros(N_vec)
    figure(figsize=(8, 3))
    for (cont, N) in enumerate(N_vec)
        x = linspace(0.0, 1.0,N)
        stiff, rhs = FEM1D(x, fun)
        sol = zeros(N)
        sol[2:end-1], niter, _ = conj_grad(stiff[2:end-1, 2:end-1],
                                    -rhs[2:end-1], rhs[2:end-1])
        err = norm(sol - x.*(x.^4 - 1)/20)/norm(x.*(x.^4 - 1)/20)
        err_vec[cont] = err
        niter_vec[cont] = niter
    end
    subplot(121)
    loglog(N_vec, err_vec)
    xlabel("Number of nodes")
    ylabel("Relative error")
    subplot(122)
    loglog(N_vec, niter_vec)
    xlabel("Number of nodes")
    ylabel("Number of iterations")
    tight_layout()
    show()



In this case, we are analyzing the error of the solution as a function
of the number of nodes. This, and the number of iterations required
in the conjugate gradient are shown in the following image

.. image:: /images/FEM1D_convergence.svg
   :width: 800 px
   :alt: Relative error in the solution.
   :align:  center
