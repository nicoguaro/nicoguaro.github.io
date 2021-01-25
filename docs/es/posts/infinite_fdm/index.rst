.. title: Diferencias finitas en dominios infinitos
.. slug: infinite_fdm
.. date: 2018-05-17 15:57:00 UTC-05:00
.. tags: computación científica, python, diferencias finitas, edp,
         mecánica cuántica
.. category: Scientific Computing
.. type: text
.. has_math: yes



Diferencias finitas en dominios infinitos
=========================================

Gracias a mi amigo, `Edward Villegas <http://cosmoscalibur.com/>`__,
terminé pensando acerca del uso de cambio de variables en la solución
de problemas de valores propios con diferencias finitas.

El problema
-----------

Digamos que queremos resolver una ecuación diferencias sobre un dominio
infinito. Un caso común es la solución de la  `ecuación de Schrödinger
independiente del tiempo <https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation#Time-independent_equation>`__
sujeta a un potencial :math:`V(x)`. Por ejemplo

.. math:: -\frac{1}{2}\frac{\mathrm{d}^2}{\mathrm{d}x^2}\psi(x) + V(x) \psi(x) = E\psi(x),\quad \forall x\in (-\infty, \infty),

en donde queremos encontrar las parejas de valores/funciones propias
:math:`(E_n, \psi_n(x))`.

Lo que normalmente hago cuando uso `diferencias
finitas <https://en.wikipedia.org/wiki/Finite_difference_method>`__
es dividir el dominio regularmente. Donde tomo un dominio lo *suficientemente
grande*, para que la solución haya decaído a cero. Lo que hago en esta
publicación es usar un cambio de variable para convertir el intervalo
a uno finito y luego dividir el dominio transformado regularmente
en intervalos finitos.

Mi enfoque usual
-----------------

Mi enfoque usual es aproximar la segunda derivada con una `diferencia
centrada <https://en.wikipedia.org/wiki/Finite_difference_coefficient>`__
para el punto :math:`x_i`, de la siguiente manera

.. math:: \frac{\mathrm{d}^2 f(x)}{\mathrm{d}x^2} \approx \frac{f(x + \Delta x) - 2 f(x_i) + f(x - \Delta x)}{\Delta x^2}\, ,

con :math:`\Delta x` la separación entre puntos consecutivos.

Podemos solucionar este problem en Python con el siguiente bloque
de código:

.. code:: python

    import numpy as np
    from scipy.sparse import diags
    from scipy.sparse.linalg import eigs


    def regular_FD(pot, npts=101, x_max=10, nvals=6):
        """
        Find eigenvalues/eigenfunctions for Schrodinger
        equation for the given potential `pot` using
        finite differences
        """
        x = np.linspace(-x_max, x_max, npts)
        dx = x[1] - x[0]
        D2 = diags([1, -2, 1], [-1, 0, 1], shape=(npts, npts))/dx**2
        V = diags(pot(x))
        H = -0.5*D2 + V
        vals, vecs = eigs(H, k=nvals, which="SM")
        return x, np.real(vals), vecs

Configuremos los gráficos con el siguiente bloque de código.

.. code:: python

    # Jupyter notebook plotting setup & imports
    %matplotlib notebook
    import matplotlib.pyplot as plt

    gray = '#757575'
    plt.rcParams["figure.figsize"] = 6, 4
    plt.rcParams["mathtext.fontset"] = "cm"
    plt.rcParams["text.color"] = gray
    fontsize = plt.rcParams["font.size"] = 12
    plt.rcParams["xtick.color"] = gray
    plt.rcParams["ytick.color"] = gray
    plt.rcParams["axes.labelcolor"] = gray
    plt.rcParams["axes.edgecolor"] = gray
    plt.rcParams["axes.spines.right"] = False
    plt.rcParams["axes.spines.top"] = False

Consideremos el `oscilador armónico
cuántico <https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator>`__,
que tiene como valores propios

.. math:: E_n = n + \frac{1}{2},\quad \forall n = 0, 1, 2 \cdots

Usando el método de diferencias finitas obtenemos valores que están
muy cerca de los analíticos.

.. code:: python

    x, vals, vecs = regular_FD(lambda x: 0.5*x**2, npts=201)
    vals

Con respuesta

.. code:: python

    array([0.4996873 , 1.49843574, 2.49593063, 3.49216962, 4.48715031,
           5.4808703 ])

Los valores analíticos son los siguientes

.. code::

    [0.5, 1.5, 2.5, 3.5, 4.5, 5.5])

Si graficamos estos dos conjuntos, obtenemos lo siguiente.

.. code:: python

    plt.figure()
    plt.plot(anal_vals)
    plt.plot(vals, "o")
    plt.xlabel(r"$n$", fontsize=16)
    plt.ylabel(r"$E_n$", fontsize=16)
    plt.legend(["Analytic", "Finite differences"])
    plt.tight_layout();


.. image:: /images/infinite_fdm/eigvals_regular.svg
   :width: 600 px
   :alt: Valores propios para la diferencia finita regular.
   :align:  center


Veamos las funciones propias

.. code:: python

    plt.figure()
    plt.plot(x, np.abs(vecs[:, :3])**2)
    plt.xlim(-6, 6)
    plt.xlabel(r"$x$", fontsize=16)
    plt.ylabel(r"$|\psi_n(x)|^2$", fontsize=16)
    plt.yticks([])
    plt.tight_layout();


.. image:: /images/infinite_fdm/eigvecs_regular.svg
   :width: 600 px
   :alt: Funciones propias para la diferencia finita regular.
   :align:  center

Un inconveniente con este método es el muestreo redundante hacia los extremos
del intervalo mientras submuestreamos el centro.

Transformando el dominio
-------------------------

Ahora, consideremos el caso en el que transormamos el dominio infinito a uno
finito usando un cambio de variable

.. math::

  \xi = \xi(x)

con :math:`\xi \in (-1, 1)`. Dos opciones para esta transformación son:

-  :math:`\xi = \tanh x`; y
-  :math:`\xi = \frac{2}{\pi} \arctan x`.

Haciendo este cambio de variable la ecuación, debemos resolver
la siguiente ecuación

.. math::

  -\frac{1}{2}\left(\frac{\mathrm{d}\xi}{\mathrm{d}x}\right)^2\frac{\mathrm{d}^2}{\mathrm{d}\xi^2}\psi(\xi) - \frac{1}{2}\frac{\mathrm{d}^2\xi}{\mathrm{d}x^2}\frac{\mathrm{d}}{\mathrm{d}\xi}\psi(\xi) + V(\xi) \psi(\xi) = E\psi(\xi)

El siguiente bloque de código resuelve el problema de valores propios
en el dominio transformado:

.. code:: python

    def mapped_FD(pot, fun, dxdxi, dxdxi2, npts=101, nvals=6, xi_tol=1e-6):
        """
        Find eigenvalues/eigenfunctions for Schrodinger
        equation for the given potential `pot` using
        finite differences over a mapped domain on (-1, 1)
        """
        xi = np.linspace(-1 + xi_tol, 1 - xi_tol, npts)
        x = fun(xi)
        dxi = xi[1] - xi[0]
        D2 = diags([1, -2, 1], [-1, 0, 1], shape=(npts, npts))/dxi**2
        D1 = 0.5*diags([-1, 1], [-1, 1], shape=(npts, npts))/dxi
        V = diags(pot(x))
        fac1 = diags(dxdxi(xi)**2)
        fac2 = diags(dxdxi2(xi))
        H = -0.5*fac1.dot(D2) - 0.5*fac2.dot(D1) + V
        vals, vecs = eigs(H, k=nvals, which="SM")
        return x, np.real(vals), vecs

Primera transformación: :math:`\xi = \tanh(x)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consideremos la primera transformación

.. math::

    \xi = \tanh(x)\, .

En este caso,

.. math::

  \frac{\mathrm{d}\xi}{\mathrm{d}x} = 1 - \tanh^2(x) = 1 - \xi^2\, ,

y

.. math::

  \frac{\mathrm{d}^2\xi}{\mathrm{d}x^2} = -2\tanh(x)[1 - \tanh^2(x)] = -2\xi[1 - \xi^2]\, .

Necesitamos definir las funciones

.. code:: python

    pot = lambda x: 0.5*x**2
    fun = lambda xi: np.arctanh(xi)
    dxdxi = lambda xi: 1 - xi**2
    dxdxi2 = lambda xi: -2*xi*(1 - xi**2)

y correr

.. code:: python

    x, vals, vecs = mapped_FD(pot, fun, dxdxi, dxdxi2, npts=201)
    vals

Y obtenemos los siguientes valores propios

.. code:: python

    array([0.49989989, 1.4984226 , 2.49003572, 3.46934257, 4.46935021,
           5.59552989])

Si los comparamos con los valores analítivos obtenemos lo siguiente.

.. code:: python

    plt.figure()
    plt.plot(anal_vals)
    plt.plot(vals, "o")
    plt.legend(["Analytic", "Finite differences"])
    plt.xlabel(r"$n$", fontsize=16)
    plt.ylabel(r"$E_n$", fontsize=16)
    plt.tight_layout();

.. image:: /images/infinite_fdm/eigvals_tanh.svg
   :width: 600 px
   :alt: Valores propios para la primera transormación.
   :align:  center

Y las siguientes funciones propias.

.. code:: python

    plt.figure()
    plt.plot(x, np.abs(vecs[:, :3])**2)
    plt.xlim(-6, 6)
    plt.xlabel(r"$x$", fontsize=16)
    plt.ylabel(r"$|\psi_n(x)|^2$", fontsize=16)
    plt.yticks([])
    plt.tight_layout();


.. image:: /images/infinite_fdm/eigvecs_tanh.svg
   :width: 600 px
   :alt: Funciones propias para la primera transformación.
   :align:  center


Segunda transformación: :math:`\xi = \frac{2}{\pi}\mathrm{atan}(x)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Consideremos ahora la segunda transformación

.. math::

   \xi = \frac{2}{\pi}\mathrm{atan}(x)\, .

En este caso,

.. math::

   \frac{\mathrm{d}\xi}{\mathrm{d}x} = \frac{2}{\pi(1 + x^2)} = \frac{2 \cos^2\xi}{\pi} \, ,

y

.. math::

   \frac{\mathrm{d}^2\xi}{\mathrm{d}x^2} = -\frac{4x}{\pi(1 + x^2)^2} = -\frac{4 \cos^4\xi \tan \xi}{\pi}\, .


Una vez más, definimos las funciones

.. code:: python

    pot = lambda x: 0.5*x**2
    fun = lambda xi: np.tan(0.5*np.pi*xi)
    dxdxi = lambda xi: 2/np.pi * np.cos(0.5*np.pi*xi)**2
    dxdxi2 = lambda xi: -4/np.pi * np.cos(0.5*np.pi*xi)**4 * np.tan(0.5*np.pi*xi)

y ejecutamos

.. code:: python

    x, vals, vecs = mapped_FD(pot, fun, dxdxi, dxdxi2, npts=201)
    vals

para obtener los siguientes valores propios

.. code:: python

    array([0.49997815, 1.49979632, 2.49930872, 3.49824697, 4.49627555,
           5.49295665])

con la siguiente gráfica

.. code:: python

    plt.figure()
    plt.plot(anal_vals)
    plt.plot(vals, "o")
    plt.legend(["Analytic", "Finite differences"])
    plt.xlabel(r"$n$", fontsize=16)
    plt.ylabel(r"$E_n$", fontsize=16)
    plt.tight_layout();


.. image:: /images/infinite_fdm/eigvals_atan.svg
   :width: 600 px
   :alt: Valores propios para la segunda transformación.
   :align:  center

y las siguientes funciones propias.

.. code:: python

    plt.figure()
    plt.plot(x, np.abs(vecs[:, :3])**2)
    plt.xlabel(r"$x$", fontsize=16)
    plt.ylabel(r"$|\psi|^2$", fontsize=16)
    plt.xlim(-6, 6)
    plt.xlabel(r"$x$", fontsize=16)
    plt.ylabel(r"$|\psi_n(x)|^2$", fontsize=16)
    plt.yticks([])
    plt.tight_layout();


.. image:: /images/infinite_fdm/eigvecs_atan.svg
   :width: 600 px
   :alt: Funciones propias para la segunda transformación.
   :align:  center


Conclusión
----------

El método funciona bien, aunque la ecuación diferencial es más
complicada por el cambio de variable. Aunque existen métodos más
elegantes para considerar dominiso infinitos, este es lo suficientemente
simple para hacerse en 10 líneas de código.

Podemos ver que la transforamción :math:`\xi = \mathrm{atan}(x)`, cubre
mejor el dominio que :math:`\xi = \tanh(x)`, donde la mayoría de los puntos
están ubicados en el centro del intervalo.

¡Gracias por leer!

.. raw:: html

  <small>
    <i>
      Esta publicación se escribió en el Jupyter notebook. Puedes
      <a href="./../../downloads/notebooks/finite_diff_map.ipynb">descargar</a>
      este notebook, o ver una versión estática en
      <a href="http://nbviewer.jupyter.org/url/nicoguaro.github.io/downloads/notebooks/finite_diff_map.ipynb">nbviewer</a>.
    <i>
  </small>
