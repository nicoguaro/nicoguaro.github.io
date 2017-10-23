.. title: Numerical methods challenge: Day 22
.. slug: numerical-22
.. date: 2017-10-22 10:51:10 UTC-05:00
.. tags: mathjax, numerical methods, python, julia, scientific computing, finite differences
.. category: Scientific Computing
.. link: 
.. description: 
.. type: text

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Finite Difference: Eigenproblems
================================

Today we have a `Finite difference method <https://en.wikipedia.org/wiki/Finite_difference_method>`_
to compute the vibration modes of a beam. The equation of interest is

.. math::

    \nabla^ 4 u = k^2 u

with

.. math::
    
    u(0) = u(L)  = 0


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    from scipy.linalg import eigh as eigsh
    import matplotlib.pyplot as plt


    def beam_FDM_eigs(L, N): 
        x = np.linspace(0, L, N)
        dx = x[1] - x[0]
        stiff = np.diag(6*np.ones(N - 2)) -\
                np.diag(4*np.ones(N - 3), -1) - np.diag(4*np.ones(N - 3), 1) +\
                np.diag(1*np.ones(N - 4), 2) + np.diag(1*np.ones(N - 4), -2)
        vals, vecs = eigsh(stiff/dx**4)     
        return vals, vecs, x


    N = 1001
    nvals = 20
    nvecs = 4
    vals, vecs, x = beam_FDM_eigs(1.0, N)

    #%% Plotting
    num = np.linspace(1, nvals, nvals)
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.figure(figsize=(8, 3))
    plt.subplot(1, 2, 1)
    plt.plot(num, np.sqrt(vals[0:nvals]), "o")
    plt.xlabel(r"$N$")
    plt.ylabel(r"$\omega\sqrt{\frac{\lambda}{EI}}$")
    plt.subplot(1, 2 ,2)
    for k in range(nvecs):
        vec = np.zeros(N)
        vec[1:-1] = vecs[:, k]
        plt.plot(x, vec, label=r'$n=%i$'%(k+1))

    plt.xlabel(r"$x$")
    plt.ylabel(r"$w$")
    plt.legend(ncol=2, framealpha=0.8, loc=1)
    plt.tight_layout()
    plt.show()



Julia
-----

.. code:: julia

    using PyPlot


    function beam_FDM_eigs(L, N)
        x = linspace(0, L, N)
        dx = x[2] - x[1]
        stiff = diagm(6*ones(N - 2)) -
                diagm(4*ones(N - 3), -1) - diagm(4*ones(N - 3), 1) +
                diagm(1*ones(N - 4), 2) + diagm(1*ones(N - 4), -2)
        vals, vecs = eig(stiff/dx^4)     
        return vals, vecs, x
    end


    N = 1001
    nvals = 20
    nvecs = 4
    vals, vecs, x = beam_FDM_eigs(1.0, N)

    #%% Plotting
    num = 1:nvals
    # Missing line for setting the math font
    figure(figsize=(8, 3))
    subplot(1, 2, 1)
    plot(num, sqrt.(vals[1:nvals]), "o")
    xlabel(L"$N$")
    ylabel(L"$\omega\sqrt{\frac{\lambda}{EI}}$")
    subplot(1, 2 ,2)
    for k in 1:nvecs
        vec = zeros(N)
        vec[2:end-1] = vecs[:, k]
        plot(x, vec, label="n=$(k)")
    end

    xlabel(L"$x$")
    ylabel(L"$w$")
    legend(ncol=2, framealpha=0.8, loc=1)
    tight_layout()
    show()

Both have (almost) the same result, as follows

.. image:: /images/beam_modes.svg
   :width: 800 px
   :alt: Vibration modes of an encastred beam.
   :align:  center


Comparison Python/Julia
-----------------------

Regarding number of lines we have: 40 in Python and 39 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit beam_FDM_eigs(1.0, N)

with result

.. code::

     10 loops, best of 3: 196 ms per loop


For Julia:

.. code:: julia

    @benchmark beam_FDM_eigs(1.0, N)


with result

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  99.42 MiB
      allocs estimate:  55
      --------------
      minimum time:     665.152 ms (17.14% GC)
      median time:      775.441 ms (21.76% GC)
      mean time:        853.401 ms (16.86% GC)
      maximum time:     1.236 s (15.68% GC)
      --------------
      samples:          6
      evals/sample:     1


In this case, we can say that the Python code is roughly 4 times faster than
Julia.
