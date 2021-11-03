.. title: Reto de métodos numéricos: Día 6
.. slug: numerical-06
.. date: 2017-10-06 20:05:08 UTC-05:00
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

Descenso del gradiente
======================

Hoy tenemos el `método de descenso del gradiente
<https://en.wikipedia.org/wiki/Gradient_descent>`_.
La idea principal en este método es usar la dirección más empinada para
moverse de un punto a otro nuevo en una vecindad para una función diferenciable.
Esto se ilustra en la siguiente imagen, en donde podemos ver que los pasos
se dan perpendicularmente a los isocontornos de la función. Si pensamos en la
función como la topografía de cierta región, sería seguro pensar los
isocontornos de la función como el camino que recorren vacas mientras caminan,
mientras que la dirección del gradiente sería el camino recorrido por una
cabra de montaña.

.. image:: https://upload.wikimedia.org/wikipedia/commons/f/ff/Gradient_descent.svg
   :width: 400 px
   :alt: Ilustración del método del descenso del gradiente.
   :align:  center

Matemáticamente, la actualización se escribe como

.. math::

    \mathbf{x}_k = \mathbf{x}_{k-1} -
        \gamma_k \nabla f(\mathbf{x_k})

en donde :math:`\gamma_k` es el tamaño del paso k-ésimo. Intuitivamente,
podemos ver que el tamaño del paso debe disminuir a medidaque nos acerquemos
al extremo de la función. Esto se alcanza, usualmente, a través de una
`búsqueda de línea <https://en.wikipedia.org/wiki/Line_search>`_. Para el método
del gradiente, podemos usar el método de Barzilai-Borwein:

.. math::

    \gamma_{n} = \frac{(\mathbf x_{n} - \mathbf x_{n-1})^T[\nabla f(\mathbf x_{n}) - \nabla f(\mathbf x_{n-1})]}{||\nabla f(\mathbf x_{n}) - \nabla f(\mathbf x_{n-1})||^2}

Probaremos el método con la 
`función de Rosenbrock <https://en.wikipedia.org/wiki/Rosenbrock_function>`_

.. math::

    f(x_1, x_2) = (1-x_1)^2 + 100(x_2-{x_1}^2)^2

El descenso del gradiente presenta algunos problemas con esta función, que
no es convexa. Sin embargo, si usamos un punto inicial que está lo
suficientemente cerca del mínimo :math:`[1, 1]`, observamos convergencia.

A continuación se presentan los códigos.

Python
------

.. code:: python

    from __future__ import division, print_function
    from numpy import array
    from numpy.linalg import norm


    def grad_descent(fun, grad, x, niter=50, gtol=1e-8, verbose=False):
        msg = "Maximum number of iterations reached."
        g_old = grad(x)
        gamma = 0.1
        for cont in range(niter):
            if verbose:
                print("n: {}, x: {}, g: {}".format(cont, x, g_old))
            dx = -gamma*g_old
            x = x + dx
            g = grad(x)
            dg = g - g_old
            g_old = g
            gamma = dx.dot(dg)/dg.dot(dg)
            if norm(g) < gtol:
                msg = "Extremum found with desired accuracy."
                break
        return x, fun(x), msg


    def rosen(x):
        return (1 - x[0])**2 + 100*(x[1] - x[0]**2)**2


    def rosen_grad(x):
        return array([
            -2*(1 - x[0]) - 400*x[0]*(x[1] - x[0]**2),
            200*(x[1] - x[0]**2)])

        
    print(grad_descent(rosen, rosen_grad, [2.0, 1.0], verbose=True))

con resultado


.. code:: python

    n: 0, x: [2.0, 1.0], g: [ 2402.  -600.]
    n: 1, x: [-238.2   61. ], g: [ -5.40030319e+09  -1.13356480e+07]
    n: 2, x: [  1.87289769  61.50393131], g: [-43446.62297136  11599.23711122]
    n: 3, x: [  1.87482914  61.50341566], g: [-43485.61077531  11597.68626767]
    n: 4, x: [ -0.2532018   62.07096513], g: [  6277.59251909  12401.37079452]
    n: 5, x: [  1.40217916e-02   6.25988648e+01], g: [  -353.0701476   12519.73363327]
    n: 6, x: [  2.98797952e-04   6.30854769e+01], g: [ -9.53932693e+00   1.26170954e+04]
    n: 7, x: [  3.49096082e-03   5.88633946e+01], g: [   -84.18892291  11772.67648837]
    n: 8, x: [ 0.42114221  0.46054405], g: [-48.8618897  56.6366569]
    n: 9, x: [ 0.66471507  0.17821457], g: [ 69.42537577 -52.72631034]
    n: 10, x: [ 0.50504193  0.29948111], g: [-9.96223909  8.88275049]
    n: 11, x: [ 0.52491812  0.28175867], g: [-2.25608389  1.24392746]
    n: 12, x: [ 0.53044731  0.27871006], g: [-0.37379949 -0.53285773]
    n: 13, x: [ 0.53133016  0.27996858], g: [-0.43934324 -0.46863181]
    n: 14, x: [ 0.53252827  0.28124656], g: [-0.4365402  -0.46795943]
    n: 15, x: [ 0.75411231  0.51877873], g: [ 14.56231057  -9.98132891]
    n: 16, x: [ 0.7050077   0.55243611], g: [-16.21302574  11.08005   ]
    n: 17, x: [ 0.73088975  0.53474821], g: [-0.69854407  0.10967699]
    n: 18, x: [ 0.73204207  0.53456728], g: [-0.14989113 -0.26366293]
    n: 19, x: [ 0.73228024  0.53498623], g: [-0.16984866 -0.24962496]
    n: 20, x: [ 0.73260201  0.53545913], g: [-0.16949786 -0.24931553]
    n: 21, x: [ 0.93339279  0.83080364], g: [ 14.95730865  -8.08369381]
    n: 22, x: [ 0.89610321  0.85095683], g: [-17.39715957   9.59117536]
    n: 23, x: [ 0.91610476  0.83992984], g: [-0.41766894  0.13638094]
    n: 24, x: [ 0.91659561  0.83976956], g: [-0.02823623 -0.07559088]
    n: 25, x: [ 0.91662795  0.83985612], g: [-0.03817128 -0.0701336 ]
    n: 26, x: [ 0.91667285  0.83993863], g: [-0.03814167 -0.07009733]
    n: 27, x: [ 0.99186712  0.97813179], g: [ 2.23273615 -1.13372137]
    n: 28, x: [ 0.98342663  0.98241763], g: [-6.0476644   3.05793919]
    n: 29, x: [ 0.98959509  0.97929862], g: [ -2.08791162e-02   3.50119013e-05]
    n: 30, x: [ 0.98961644  0.97929858], g: [-0.00409146 -0.00842531]
    n: 31, x: [ 0.9896206   0.97930713], g: [-0.00421464 -0.00835884]
    n: 32, x: [ 0.98963284  0.97933141], g: [-0.0042095  -0.00834897]
    n: 33, x: [ 0.99991222  0.99971914], g: [ 0.04194186 -0.02106056]
    n: 34, x: [ 0.99597256  1.00169739], g: [-3.88678974  1.9472097 ]
    n: 35, x: [ 0.99987194  0.99974387], g: [ -2.42382231e-04  -6.86507784e-06]
    n: 36, x: [ 0.99987219  0.99974388], g: [ -5.01566886e-05  -1.02746923e-04]
    n: 37, x: [ 0.99987224  0.99974398], g: [ -5.10336616e-05  -1.02258276e-04]
    n: 38, x: [ 0.99987255  0.99974461], g: [ -5.09073070e-05  -1.02006794e-04]
    n: 39, x: [ 0.99999998  0.99999996], g: [  5.05854337e-06  -2.54465444e-06]
    n: 40, x: [ 0.99998735  1.00000631], g: [-0.01266881  0.00632184]
    (array([ 1.,  1.]), 7.2961338114681859e-21, 'Extremum found with desired accuracy.')

Julia
-----

.. code:: julia

    function grad_descent(fun, grad, x; niter=50, gtol=1e-8, verbose=false)
        msg = "Maximum number of iterations reached."
        g_old = grad(x)
        gamma = 0.1
        for cont = 1:niter
            if verbose
                println("n: $(cont), x: $(x), g: $(g_old)")
            end
            dx = - gamma*g_old
            x = x + dx
            g = grad(x)
            dg = g - g_old
            g_old = g
            gamma = dx' * dg / (dg' * dg)
            if norm(g) < gtol
                msg = "Extremum found with desired accuracy."
                break
            end
        end
        return x, fun(x), msg
    end


    function rosen(x)
        return (1 - x[1])^2 + 100*(x[2] - x[1]^2)^2
    end


    function rosen_grad(x)
        return [-2*(1 - x[1]) - 400*x[1]*(x[2] - x[1]^2);
                200*(x[2] - x[1]^2)]
    end


    println(grad_descent(rosen, rosen_grad, [2.0, 1.0], verbose=true))

con resultado

.. code:: julia

    n: 1, x: [2.0, 1.0], g: [2402.0, -600.0]
    n: 2, x: [-238.2, 61.0], g: [-5.4003e9, -1.13356e7]
    n: 3, x: [1.8729, 61.5039], g: [-43446.6, 11599.2]
    n: 4, x: [1.87483, 61.5034], g: [-43485.6, 11597.7]
    n: 5, x: [-0.253202, 62.071], g: [6277.59, 12401.4]
    n: 6, x: [0.0140218, 62.5989], g: [-353.07, 12519.7]
    n: 7, x: [0.000298798, 63.0855], g: [-9.53933, 12617.1]
    n: 8, x: [0.00349096, 58.8634], g: [-84.1889, 11772.7]
    n: 9, x: [0.421142, 0.460544], g: [-48.8619, 56.6367]
    n: 10, x: [0.664715, 0.178215], g: [69.4254, -52.7263]
    n: 11, x: [0.505042, 0.299481], g: [-9.96224, 8.88275]
    n: 12, x: [0.524918, 0.281759], g: [-2.25608, 1.24393]
    n: 13, x: [0.530447, 0.27871], g: [-0.373799, -0.532858]
    n: 14, x: [0.53133, 0.279969], g: [-0.439343, -0.468632]
    n: 15, x: [0.532528, 0.281247], g: [-0.43654, -0.467959]
    n: 16, x: [0.754112, 0.518779], g: [14.5623, -9.98133]
    n: 17, x: [0.705008, 0.552436], g: [-16.213, 11.08]
    n: 18, x: [0.73089, 0.534748], g: [-0.698544, 0.109677]
    n: 19, x: [0.732042, 0.534567], g: [-0.149891, -0.263663]
    n: 20, x: [0.73228, 0.534986], g: [-0.169849, -0.249625]
    n: 21, x: [0.732602, 0.535459], g: [-0.169498, -0.249316]
    n: 22, x: [0.933393, 0.830804], g: [14.9573, -8.08369]
    n: 23, x: [0.896103, 0.850957], g: [-17.3972, 9.59118]
    n: 24, x: [0.916105, 0.83993], g: [-0.417669, 0.136381]
    n: 25, x: [0.916596, 0.83977], g: [-0.0282362, -0.0755909]
    n: 26, x: [0.916628, 0.839856], g: [-0.0381713, -0.0701336]
    n: 27, x: [0.916673, 0.839939], g: [-0.0381417, -0.0700973]
    n: 28, x: [0.991867, 0.978132], g: [2.23274, -1.13372]
    n: 29, x: [0.983427, 0.982418], g: [-6.04766, 3.05794]
    n: 30, x: [0.989595, 0.979299], g: [-0.0208791, 3.50119e-5]
    n: 31, x: [0.989616, 0.979299], g: [-0.00409146, -0.00842531]
    n: 32, x: [0.989621, 0.979307], g: [-0.00421464, -0.00835884]
    n: 33, x: [0.989633, 0.979331], g: [-0.0042095, -0.00834897]
    n: 34, x: [0.999912, 0.999719], g: [0.0419419, -0.0210606]
    n: 35, x: [0.995973, 1.0017], g: [-3.88679, 1.94721]
    n: 36, x: [0.999872, 0.999744], g: [-0.000242382, -6.86508e-6]
    n: 37, x: [0.999872, 0.999744], g: [-5.01567e-5, -0.000102747]
    n: 38, x: [0.999872, 0.999744], g: [-5.10337e-5, -0.000102258]
    n: 39, x: [0.999873, 0.999745], g: [-5.09073e-5, -0.000102007]
    n: 40, x: [1.0, 1.0], g: [5.05854e-6, -2.54465e-6]
    n: 41, x: [0.999987, 1.00001], g: [-0.0126688, 0.00632184]
    ([1.0, 1.0], 7.296133811468186e-21, "Root found with desired accuracy.")


Comparación Python/Julia
------------------------

Respecto al número de líneas tenemos: 38 in Python and 39 in Julia. La comparación
en tiempo de ejecución se realizó con el comando mágico de IPython ``%timeit``
y con ``@benchmark`` en Julia.

Para Python:

.. code:: IPython

    %timeit grad_descent(rosen, rosen_grad, [2.0, 1.0])

con resultado

.. code::

    1000 loops, best of 3: 386 µs per loop

Para Julia:

.. code:: julia

    @benchmark grad_descent(rosen, rosen_grad, [2.0, 1.0])

con resultado

.. code:: julia

    BenchmarkTools.Trial: 
      memory estimate:  16.91 KiB
      allocs estimate:  251
      --------------
      minimum time:     6.479 μs (0.00% GC)
      median time:      7.393 μs (0.00% GC)
      mean time:        13.437 μs (18.45% GC)
      maximum time:     2.029 ms (95.94% GC)
      --------------
      samples:          10000
      evals/sample:     5


En estse caso, podemos decir que Python es alrededor de 50 veces más lento
que Julia.
