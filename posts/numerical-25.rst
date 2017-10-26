.. title: Numerical methods challenge: Day 25
.. slug: numerical-25
.. date: 2017-10-25 21:41:53 UTC-05:00
.. tags: mathjax, numerical methods, python, julia, scientific computing, finite element method
.. category: Scientific Computing
.. link:
.. description:
.. type: text

During October (2017) I will write a program per day for some well-known
numerical methods in both Python and Julia. It is intended to be an exercise
then don't expect the code to be good enough for real use. Also,
I should mention that I have almost no experience with Julia, so it
probably won't be idiomatic Julia but more Python-like Julia.

Finite element method
=====================

Today we have the `Finite element method <https://en.wikipedia.org/wiki/Finite_element_method>`_
to solve the equation:

.. math::

    \nabla^2 u = -f(x)

with

.. math::

    u(\sqrt{3}, 1) = 0

As in the `Ritz method <posts/numerical-23>`_ we form
a functional that is *equivalent* to the
differential equation, propose an approximation as a linear combination of
a set of basis functions and find the *best* set of coefficients for that
combination. That *best* solution is found minimizing the functional.

The functional for this differential equation is

.. math::

    \Pi[u] = -\int_\Omega \left(\nabla u\right)^2 d\Omega
             -\int_\Omega  u f(x) d\Omega

Using linear triangles, the local stiffness matrices read

.. math::

    K_\text{local} =  \frac{1}{|J|}
        \begin{bmatrix}
            2 & -1 &1\\
            -1 & 1 &0\\
            -1 & 0 &1\\
        \end{bmatrix}

and

.. math::

    b_\text{local} = -|J| f(x_m) \mathbf{1}_3\, ,

where :math:`|J|` is the Jacobian determinant of the transformation and
:math:`x_m` is the centroid of the triangle. I am
skipping a great deal about assembling, but it would be just too extensive
to describe the complete process.

We will solve the problem in a mesh with 6 triangles forming
a regular hexagon


Following are the codes.

Python
------

.. code:: python

    from __future__ import division, print_function
    import numpy as np
    import matplotlib.pyplot as plt

    def assem(coords, elems, source):
        ncoords = coords.shape[0]
        stiff = np.zeros((ncoords, ncoords))
        rhs = np.zeros((ncoords))
        for el_cont, elem in enumerate(elems):
            stiff_loc, jaco = local_stiff(coords[elem])
            rhs[elem] += jaco*np.mean(source[elem])
            for row in range(3):
                for col in range(3):
                    row_glob, col_glob = elem[row], elem[col]
                    stiff[row_glob, col_glob] += stiff_loc[row, col]
        return stiff, rhs


    def local_stiff(coords):
        dHdr = np.array([[-1, 1, 0], [-1, 0, 1]])
        jaco = dHdr.dot(coords)
        stiff = 0.5*np.array([[2, -1, -1], [-1, 1, 0], [-1, 0, 1]])
        return stiff/np.linalg.det(jaco), np.linalg.det(jaco)


    sq3 = np.sqrt(3)
    coords = np.array([
            [sq3, -1],
            [0, 0],
            [2*sq3, 0],
            [0, 2],
            [2*sq3, 2],
            [sq3, 3],
            [sq3, 1]])
    elems = np.array([
            [1, 0, 6],
            [0, 2, 6],
            [2, 4, 6],
            [4, 5, 6],
            [5, 3, 6],
            [3, 1, 6]])
    source = -np.ones(7)
    stiff, rhs = assem(coords, elems, source)
    free = range(6)
    sol = np.linalg.solve(stiff[np.ix_(free, free)], rhs[free])
    sol_c = np.zeros(coords.shape[0])
    sol_c[free] = sol
    plt.tricontourf(coords[:, 0], coords[:, 1], sol_c, cmap="hot")
    plt.colorbar()
    plt.axis("image")
    plt.show()

Julia
-----

.. code:: julia

    using PyPlot


    function assem(coords, elems, source)
        ncoords = size(coords)[1]
        nelems = size(elems)[1]
        stiff = zeros(ncoords, ncoords)
        rhs = zeros(ncoords)
        for el_cont = 1:nelems
            elem = elems[el_cont, :]
            stiff_loc, jaco = local_stiff(coords[elem, :])
            rhs[elem] += jaco*mean(source[elem])
            for row = 1:3
                for col = 1:3
                    row_glob = elem[row]
                    col_glob = elem[col]
                    stiff[row_glob, col_glob] += stiff_loc[row, col]
                end
            end
        end
        return stiff, rhs
    end


    function local_stiff(coords)
        dHdr = [-1 1 0; -1 0 1]
        jaco = dHdr * coords
        stiff = 0.5*[2 -1 -1; -1 1 0; -1 0 1]
        return stiff/det(jaco), det(jaco)
    end


    sq3 = sqrt(3)
    coords =[sq3 -1;
            0 0;
            2*sq3 0;
            0 2;
            2*sq3 2;
            sq3 3;
            sq3 1]
    elems =[2 1 7;
            1 3 7;
            3 5 7;
            5 6 7;
            6 4 7;
            4 2 7]
    source = -ones(7)
    stiff, rhs = assem(coords, elems, source)
    free = 1:6
    sol = stiff[free, free] \ rhs[free]
    sol_c = zeros(size(coords)[1])
    sol_c[free] = sol
    tricontourf(coords[:, 1], coords[:, 2], sol_c, cmap="hot")
    colorbar()
    axis("image")
    show()

Both have the same result, as follows

.. image:: /images/FEM2D.svg
   :width: 500 px
   :alt: Finite element method approximation.
   :align:  center



Comparison Python/Julia
-----------------------

Regarding number of lines we have: 51 in Python and 56 in Julia. The comparison
in execution time is done with ``%timeit`` magic command in IPython and
``@benchmark`` in Julia. For the test we are just comparing the time it takes
to generate the matrices.

For Python:

.. code:: IPython

    %timeit assem(coords, elems, source)

with result

.. code::

     1000 loops, best of 3: 671 µs per loop


For Julia:

.. code:: julia

    @benchmark assem(coords, elems, source)


with result

.. code:: julia

    BenchmarkTools.Trial:
      memory estimate:  13.30 KiB
      allocs estimate:  179
      --------------
      minimum time:     7.777 μs (0.00% GC)
      median time:      8.934 μs (0.00% GC)
      mean time:        10.810 μs (14.54% GC)
      maximum time:     797.432 μs (95.85% GC)
      --------------
      samples:          10000
      evals/sample:     4



In this case, we can say that the Python code is about 70 times slower than
Julia code.
