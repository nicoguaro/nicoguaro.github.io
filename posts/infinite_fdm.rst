.. title: Finite differences in infinite domains
.. slug: infinite_fdm
.. date: 2018-05-17 15:57:00 UTC-05:00
.. tags: scientific computing, python, finite difference, pde, quantum mechanics
.. category: Scientific Computing
.. type: text
.. has_math: yes



Finite differences in infinite domains
======================================

Because of my friend, `Edward Villegas <http://cosmoscalibur.com/>`__, I
ended up thinking about using a change of variables when solving an
eigenvalue problem with finite difference.

The problem
-----------

Let's say that we want to solve a differential equation over an infinite
domain. A common case is to solve the `Time independent Schrödinger
equation <https://en.wikipedia.org/wiki/Schr%C3%B6dinger_equation#Time-independent_equation>`__
subject to a potential :math:`V(x)`. For example

.. math:: -\frac{1}{2}\frac{\mathrm{d}^2}{\mathrm{d}x^2}\psi(x) + V(x) \psi(x) = E\psi(x),\quad \forall x\in (-\infty, \infty),

where we want to find the pairs of eigenvalues/eigenfunctions
:math:`(E_n, \psi_n(x))`.

What I normally do when using `finite
differences <https://en.wikipedia.org/wiki/Finite_difference_method>`__
is to regularly divide the domain. Where I take a *large enough* domain,
so the solution have decayed close to zero. What I do in this post is to
make a change of variable to render the interval finite first and then
regularly divide the transformed domain in finite intervals.

My usual approach
-----------------

My usual approach is to approach the second derivative with a `centered
difference <https://en.wikipedia.org/wiki/Finite_difference_coefficient>`__
for the point :math:`x_i` like this

.. math:: \frac{\mathrm{d}^2 f(x)}{\mathrm{d}x^2} \approx \frac{f(x + \Delta x) - 2 f(x_i) + f(x - \Delta x)}{\Delta x^2}\, ,

with :math:`\Delta x` the separation between points.

We can solve this in Python with the following snippet:

.. code:: ipython3

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

Let's setup the plotting details.

.. code:: ipython3

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

Let's consider the `Quantum harmonic
oscillator <https://en.wikipedia.org/wiki/Quantum_harmonic_oscillator>`__,
that has as eigenvalues

.. math:: E_n = n + \frac{1}{2},\quad \forall n = 0, 1, 2 \cdots

Using the finite difference method we have values that are really close
to the analytic ones.

.. code:: ipython3

    x, vals, vecs = regular_FD(lambda x: 0.5*x**2, npts=201)
    vals


with output

.. parsed-literal::

    array([0.4996873 , 1.49843574, 2.49593063, 3.49216962, 4.48715031,
           5.4808703 ])

With the analytic ones

.. code::

    [0.5, 1.5, 2.5, 3.5, 4.5, 5.5])

If we plot these two, we obtain the following.

.. code:: ipython3

    plt.figure()
    plt.plot(anal_vals)
    plt.plot(vals, "o")
    plt.xlabel(r"$n$", fontsize=16)
    plt.ylabel(r"$E_n$", fontsize=16)
    plt.legend(["Analytic", "Finite differences"])
    plt.tight_layout();


.. image:: /images/infinite_fdm/eigvals_regular.svg
   :width: 600 px
   :alt: Eigenvalues for the regular finite difference
   :align:  center


Let's see the eigenfunctions.

.. code:: ipython3

    plt.figure()
    plt.plot(x, np.abs(vecs[:, :3])**2)
    plt.xlim(-6, 6)
    plt.xlabel(r"$x$", fontsize=16)
    plt.ylabel(r"$|\psi_n(x)|^2$", fontsize=16)
    plt.yticks([])
    plt.tight_layout();


.. image:: /images/infinite_fdm/eigvecs_regular.svg
   :width: 600 px
   :alt: Eigenfunctions for the regular finite difference
   :align:  center


One inconvenient with this method is the redundant sampling towards the
extreme of the intervals, while under sample the middle part.

Changing the domain
-------------------

Let's now consider the case where we transform the infinite domain to a
finite one with a change of variable

.. math::

  \xi = \xi(x)

with :math:`\xi \in (-1, 1)`. Two options for this transformation are:

-  :math:`\xi = \tanh x`; and
-  :math:`\xi = \frac{2}{\pi} \arctan x`.

Making this change of variable the equation we need to solve the
following equation

.. math::

  -\frac{1}{2}\left(\frac{\mathrm{d}\xi}{\mathrm{d}x}\right)^2\frac{\mathrm{d}^2}{\mathrm{d}\xi^2}\psi(\xi) - \frac{1}{2}\frac{\mathrm{d}^2\xi}{\mathrm{d}x^2}\frac{\mathrm{d}}{\mathrm{d}\xi}\psi(\xi) + V(\xi) \psi(\xi) = E\psi(\xi)

The following snippet solve the eigenproblem for the mapped domain:

.. code:: ipython3

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

First transformation: :math:`\xi = \tanh(x)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's consider first the transformation

.. math::

    \xi = \tanh(x)\, .

In this case

.. math::

  \frac{\mathrm{d}\xi}{\mathrm{d}x} = 1 - \tanh^2(x) = 1 - \xi^2\, ,

and

.. math::

  \frac{\mathrm{d}^2\xi}{\mathrm{d}x^2} = -2\tanh(x)[1 - \tanh^2(x)] = -2\xi[1 - \xi^2]\, .

We need to define the functions

.. code:: ipython3

    pot = lambda x: 0.5*x**2
    fun = lambda xi: np.arctanh(xi)
    dxdxi = lambda xi: 1 - xi**2
    dxdxi2 = lambda xi: -2*xi*(1 - xi**2)

and run the function

.. code:: ipython3

    x, vals, vecs = mapped_FD(pot, fun, dxdxi, dxdxi2, npts=201)
    vals

And we obtain the following

.. parsed-literal::

    array([0.49989989, 1.4984226 , 2.49003572, 3.46934257, 4.46935021,
           5.59552989])

If we compare with the analytic values we get the following.

.. code:: ipython3

    plt.figure()
    plt.plot(anal_vals)
    plt.plot(vals, "o")
    plt.legend(["Analytic", "Finite differences"])
    plt.xlabel(r"$n$", fontsize=16)
    plt.ylabel(r"$E_n$", fontsize=16)
    plt.tight_layout();

.. image:: /images/infinite_fdm/eigvals_tanh.svg
   :width: 600 px
   :alt: Eigenvalues for the first transformation
   :align:  center

And the following are the eigenfunctions.

.. code:: ipython3

    plt.figure()
    plt.plot(x, np.abs(vecs[:, :3])**2)
    plt.xlim(-6, 6)
    plt.xlabel(r"$x$", fontsize=16)
    plt.ylabel(r"$|\psi_n(x)|^2$", fontsize=16)
    plt.yticks([])
    plt.tight_layout();


.. image:: /images/infinite_fdm/eigvecs_tanh.svg
   :width: 600 px
   :alt: Eigenfunctions for the first transformation
   :align:  center


Second transformation: :math:`\xi = \frac{2}{\pi}\mathrm{atan}(x)`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Let's consider first the transformation

.. math::

   \xi = \frac{2}{\pi}\mathrm{atan}(x)\, .

In this case

.. math::

   \frac{\mathrm{d}\xi}{\mathrm{d}x} = \frac{2}{\pi(1 + x^2)} = \frac{2 \cos^2\xi}{\pi} \, ,

and

.. math::

   \frac{\mathrm{d}^2\xi}{\mathrm{d}x^2} = -\frac{4x}{\pi(1 + x^2)^2} = -\frac{4 \cos^4\xi \tan \xi}{\pi}\, .


Once, again, we define the functions.

.. code:: ipython3

    pot = lambda x: 0.5*x**2
    fun = lambda xi: np.tan(0.5*np.pi*xi)
    dxdxi = lambda xi: 2/np.pi * np.cos(0.5*np.pi*xi)**2
    dxdxi2 = lambda xi: -4/np.pi * np.cos(0.5*np.pi*xi)**4 * np.tan(0.5*np.pi*xi)

and run the function

.. code:: ipython3

    x, vals, vecs = mapped_FD(pot, fun, dxdxi, dxdxi2, npts=201)
    vals

to obtain the following eigenvalues

.. parsed-literal::

    array([0.49997815, 1.49979632, 2.49930872, 3.49824697, 4.49627555,
           5.49295665])

with this plot

.. code:: ipython3

    plt.figure()
    plt.plot(anal_vals)
    plt.plot(vals, "o")
    plt.legend(["Analytic", "Finite differences"])
    plt.xlabel(r"$n$", fontsize=16)
    plt.ylabel(r"$E_n$", fontsize=16)
    plt.tight_layout();


.. image:: /images/infinite_fdm/eigvals_atan.svg
   :width: 600 px
   :alt: Eigenvalues for the second transformation
   :align:  center

and the following eigenfunctions.

.. code:: ipython3

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
   :alt: Eigenfunctions for the second transformation
   :align:  center


Conclusion
----------

The method works fine, although the differential equation is more
convoluted due to the change of variable. Although there are more
elegant methods to consider infinite domains, this is simple enough to
be solved in 10 lines of code.

We can see that the mapping :math:`\xi = \mathrm{atan}(x)`, covers
better the domain than :math:`\xi = \tanh(x)`, where most of the points
are placed in the center of the interval.


Thanks for reading!

.. raw:: html

  <small>
    <i>
      This post was written in the Jupyter notebook. You can
      <a href="./../../downloads/notebooks/finite_diff_map.ipynb">download</a>
      this notebook, or see a static view on
      <a href="http://nbviewer.jupyter.org/url/nicoguaro.github.io/downloads/notebooks/finite_diff_map.ipynb">nbviewer</a>.
    <i>
  </small>
