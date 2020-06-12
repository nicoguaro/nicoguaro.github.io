.. title: Numerical methods challenge: Day 19
.. slug: numerical-19
.. date: 2017-10-19 15:24:57 UTC-05:00
.. tags: numerical methods, python, julia, scientific computing, ode, verlet integration
.. category: Scientific Computing
.. type: text
.. has_math: yes

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Verlet integration
==================

Today we have the `Verlet integration <https://en.wikipedia.org/wiki/Verlet_integration>`_
technique. This method is widely used to integrate equations of motion of
several systems, such as orbital mechanics or molecular dynamics. One of the
main reasons for choosing this method is that it is a
`symplectic integrator <https://en.wikipedia.org/wiki/Symplectic_integrator>`_.


The stepping is done with the formula

.. math::

    \mathbf{x}_{n+1}=2 \mathbf{x}_n- \mathbf{x}_{n-1}+ A(\mathbf{x}_n)\,\Delta t^2.

where :math:`A(\mathbf{x}_n)` is the aceleration for that time-step.


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt


    def verlet(force, x0, v0, m, t, args=()):
        ndof = len(x0)
        ntimes = len(t)
        x = np.zeros((ndof, ntimes))
        dt = t[1] - t[0]
        x[:, 0] = x0
        F = force(x0, v0, m, t, *args)
        x[::2, 1] = x0[::2] + v0[::2]*dt + 0.5*F[::2]*dt**2/m
        x[1::2, 1] = x0[1::2] + v0[1::2]*dt + 0.5*F[1::2]*dt**2/m
        for cont in range(2, ntimes):
            dt = t[cont] - t[cont - 1]
            v = (x[:, cont - 1] - x[:, cont - 2])/dt
            acel = force(x[:, cont - 1], v, m, t, *args)
            acel[::2] = acel[::2]/m
            acel[1::2] = acel[1::2]/m
            x[:, cont] = 2*x[:, cont - 1] - x[:, cont - 2] + acel*dt**2
        return x


    spring_force = lambda x, v, m, t, k: -k*x
    x0 = np.array([1.0, 0.0])
    v0 = np.array([0.0, 1.0])
    m = np.array([1.0])
    t = np.linspace(0, 10.0, 1000)
    k = 1.0
    x = verlet(spring_force, x0, v0, m, t, args=(k,))

    #%% Plot
    plt.figure(figsize=(6, 3))
    plt.subplot(121)
    plt.plot(t, x[0, :])
    plt.plot(t, x[1, :])
    plt.subplot(122)
    plt.plot(x[0, :], x[1, :])
    plt.show()



Julia
-----

.. code:: julia

    using PyPlot


    function verlet(force, x0, v0, m, t; args=())
        ndof = length(x0)
        ntimes = length(t)
        x = zeros(ndof, ntimes)
        dt = t[2] - t[1]
        x[:, 1] = x0
        F = force(x0, v0, m, t, args...)
        x[1:2:end, 2] = x0[1:2:end] + v0[1:2:end]*dt + 0.5*F[1:2:end]*dt^2./m
        x[2:2:end, 2] = x0[2:2:end] + v0[2:2:end]*dt + 0.5*F[2:2:end]*dt^2./m
        for cont = 3:ntimes
            dt = t[cont] - t[cont - 1]
            v = (x[:, cont - 1] - x[:, cont - 2])/dt
            acel = force(x[:, cont - 1], v, m, t, args...)
            acel[1:2:end] = acel[1:2:end]./m
            acel[2:2:end] = acel[2:2:end]./m
            x[:, cont] = 2*x[:, cont - 1] - x[:, cont - 2] + acel*dt^2
        end
        return x
    end


    spring_force(x, v, m, t, k) = -k*x
    x0 = [1.0, 0.0]
    v0 = [0.0, 1.0]
    m = [1.0]
    t = linspace(0, 10.0, 1000)
    k = 1.0
    x = verlet(spring_force, x0, v0, m, t, args=(k,))

    #%% Plot
    figure(figsize=(6, 3))
    subplot(121)
    plot(t, x[1, :])
    plot(t, x[2, :])
    subplot(122)
    plot(x[1, :], x[2, :])
    show()


In both cases the result is the following plot

.. image:: /images/verlet.svg
   :width: 600 px
   :alt: Verlet integration for a mass with two orthogonal springs.
   :align:  center



Comparison Python/Julia
-----------------------

Regarding number of lines we have: 40 in Python and 40 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia.

For Python:

.. code:: IPython

    %timeit -n 100 verlet(spring_force, x0, v0, m, t, args=(k,))

with result

.. code::

    100 loops, best of 3: 26.5 ms per loop

For Julia:

.. code:: julia

    @benchmark verlet(spring_force, x0, v0, m, t, args=(k,))


with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  4.36 MiB
      allocs estimate:  101839
      --------------
      minimum time:     73.159 ms (0.00% GC)
      median time:      74.883 ms (0.00% GC)
      mean time:        75.464 ms (1.02% GC)
      maximum time:     80.017 ms (4.87% GC)
      --------------
      samples:          67
      evals/sample:     1


In this case, we can say that the Python code is roughly 3 times faster than Julia.
