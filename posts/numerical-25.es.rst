.. title: Reto de métodos numéricos: Día 25
.. slug: numerical-25
.. date: 2017-10-25 21:41:53 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica, método de elementos finitos
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) estaré escribiendo un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tengo experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Método de elementos finitos
===========================

Hoy tenemos el `método de elementos finitos
<https://en.wikipedia.org/wiki/Finite_element_method>`_ para resolver la
ecuación:

.. math::

    \nabla^2 u = -f(x)

con

.. math::

    u(\sqrt{3}, 1) = 0

Como en el `método de Ritz <posts/numerical-23>`_ formamos un funcional
que es *equivalente* a la ecuación diferencial, proponemos una aproximación que
es una combinación lineal de funciones base y encontramos el *mejor* conjunto
de coeficientes para esta combinación. La *mejor* solución se encuentra
minimizando el funcional.

El funcional para este ecuación diferencial es

.. math::

    \Pi[u] = -\int_\Omega \left(\nabla u\right)^2 d\Omega
             -\int_\Omega  u f(x) d\Omega

Usando triángulos lineales, las matrices de rigidez son

.. math::

    K_\text{local} =  \frac{1}{2|J|}
        \begin{bmatrix}
            2 & -1 &1\\
            -1 & 1 &0\\
            -1 & 0 &1\\
        \end{bmatrix}

y

.. math::

    b_\text{local} = -|J| f(x_m) \mathbf{1}_3\, ,

donde :math:`|J|` es el determinante jacobiano de la transformación y
:math:`x_m` es el centroide del triángulo. Me estoy
saltando muchos detalles respecto al ensamblaje; sería muy costoso describir
el proceso completo.

Vamos a resolver el problema en una malla de 6 triángulos que forman un
hexágono regular.

A continuación se presenta el código.

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

En ambos casos tenemos el mismo resultado.

.. image:: /images/FEM2D.svg
   :width: 500 px
   :alt: Aproximación por el método de elementos finitos.
   :align:  center

Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 51 en Python y 56 en Julia.  La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia. Para la comparación solo estamos considerando el
tiempo que toma formar las matrices.

Para Python:

.. code:: IPython

    %timeit assem(coords, elems, source)

con resultado

.. code::

     1000 loops, best of 3: 671 µs per loop


Para Julia:

.. code:: julia

    @benchmark assem(coords, elems, source)


con resultado

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


En este caso, podemos decir que el código de Python es alrededor de 70 veces más
lento que el de Julia.
