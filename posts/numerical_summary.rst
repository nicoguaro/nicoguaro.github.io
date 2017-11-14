.. title: Numerical methods challenge: Summary
.. slug: numerical_summary
.. date: 2017-11-14 11:22:23 UTC-05:00
.. tags: mathjax, numerical methods, python, julia, scientific computing
.. category: Scientific Computing
.. link:
.. description:
.. type: text

During October (2017) I wrote a program per day for some well-known numerical
methods in both Python and Julia. It was intended to be an exercise, then don't
expect the code to be good enough for real use. Also, I should mention that I
had almost no experience with Julia, so it probably is not idiomatic Julia but
more Python-like Julia.

Summary
=======

This post is a summary of that challenge. For the source code you can check
`the repository <https://github.com/nicoguaro/numerical_challenge_2017>`_.


The verdict
-----------

Since the challenge is with myself, and the main purpose was to learn some
Julia the verdict is: **success**. Nevertheless, I failed during day 26
with the Boundary Element Method.

The list of methods
-------------------

+-------------------------------+---------------------------------------------------+
| Day                           | Numerical method                                  |
+===============================+===================================================+
|  `01 <posts/numerical-01>`_   | Bisection                                         |
+-------------------------------+---------------------------------------------------+
|  `02 <posts/numerical-02>`_   | Regula falsi                                      |
+-------------------------------+---------------------------------------------------+
|  `03 <posts/numerical-03>`_   | Newton                                            |
+-------------------------------+---------------------------------------------------+
|  `04 <posts/numerical-04>`_   | Newton multivariate                               |
+-------------------------------+---------------------------------------------------+
|  `05 <posts/numerical-05>`_   | Broyden                                           |
+-------------------------------+---------------------------------------------------+
|  `06 <posts/numerical-06>`_   | Gradient descent                                  |
+-------------------------------+---------------------------------------------------+
|  `07 <posts/numerical-07>`_   | Nelder-Mead                                       |
+-------------------------------+---------------------------------------------------+
|  `08 <posts/numerical-08>`_   | Newton for optimization                           |
+-------------------------------+---------------------------------------------------+
|  `09 <posts/numerical-09>`_   | Lagrange interpolation                            |
+-------------------------------+---------------------------------------------------+
|  `10 <posts/numerical-10>`_   | Lagrange interpolation with Lobatto sampling      |
+-------------------------------+---------------------------------------------------+
|  `11 <posts/numerical-11>`_   | Lagrange interpolation using Vandermonde matrix   |
+-------------------------------+---------------------------------------------------+
|  `12 <posts/numerical-12>`_   | Hermite interpolation                             |
+-------------------------------+---------------------------------------------------+
|  `13 <posts/numerical-13>`_   | Spline interpolation                              |
+-------------------------------+---------------------------------------------------+
|  `14 <posts/numerical-14>`_   | Trapezoid quadrature                              |
+-------------------------------+---------------------------------------------------+
|  `15 <posts/numerical-15>`_   | Simpson quadrature                                |
+-------------------------------+---------------------------------------------------+
|  `16 <posts/numerical-16>`_   | Clenshaw-Curtis quadrature                        |
+-------------------------------+---------------------------------------------------+
|  `17 <posts/numerical-17>`_   | Euler integration                                 |
+-------------------------------+---------------------------------------------------+
|  `18 <posts/numerical-18>`_   | Runge-Kutta integration                           |
+-------------------------------+---------------------------------------------------+
|  `19 <posts/numerical-19>`_   | Verlet integration                                |
+-------------------------------+---------------------------------------------------+
|  `20 <posts/numerical-20>`_   | Shooting method                                   |
+-------------------------------+---------------------------------------------------+
|  `21 <posts/numerical-21>`_   | Finite differences with Jacobi method             |
+-------------------------------+---------------------------------------------------+
|  `22 <posts/numerical-22>`_   | Finite differences for eigenvalues                |
+-------------------------------+---------------------------------------------------+
|  `23 <posts/numerical-23>`_   | Ritz method                                       |
+-------------------------------+---------------------------------------------------+
|  `24 <posts/numerical-24>`_   | Finite element method in 1D                       |
+-------------------------------+---------------------------------------------------+
|  `25 <posts/numerical-25>`_   | Finite element method in 2D                       |
+-------------------------------+---------------------------------------------------+
|  `26 <posts/numerical-26>`_   | Boundary element method                           |
+-------------------------------+---------------------------------------------------+
|  `27 <posts/numerical-27>`_   | Monte-Carlo integration                           |
+-------------------------------+---------------------------------------------------+
|  `28 <posts/numerical-28>`_   | LU factorization                                  |
+-------------------------------+---------------------------------------------------+
|  `29 <posts/numerical-29>`_   | Cholesky factorization                            |
+-------------------------------+---------------------------------------------------+
|  `30 <posts/numerical-30>`_   | Conjugate gradient                                |
+-------------------------------+---------------------------------------------------+
|  `31 <posts/numerical-31>`_   | Finite element method with solver                 |
+-------------------------------+---------------------------------------------------+

Conclusions
-----------

- This was an exercise of code-kata to learn some of the details of Julia for
  scientific computing. As such, it was really useful for me to get my hands
  dirty with Julia.

- Implementing the Boundary Element Method in one day seems to be rough. I
  knew this beforehand, but I gave it a try anyways ... without succcess.

- Julia syntax is somewhat in a sweetspot between Python and MATLAB. This makes
  it really easy to use, although the documentation of some packages is at
  an arcane stage right now.

- I won't take a challenge like this in a while. It takes a lot of atttention
  to get it done.

