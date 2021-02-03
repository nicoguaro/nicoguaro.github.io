.. title: Reto de métodos numéricos: resumen
.. slug: numerical_summary
.. date: 2017-11-14 11:22:23 UTC-05:00
.. tags: métodos numéricos, python, julia, computación científica
.. category: Scientific Computing
.. type: text
.. has_math: yes

Durante octubre (2017) escribí un programa por día para algunos
métodos numéricos famosos en Python y Julia. Esto está pensado como
un ejercicio, no esperen que el código sea lo suficientemente bueno para
usarse en la "vida real". Además, también debo mencionar que casi que no
tenía experiencia con Julia, así que probablemente no escriba un Julia
idiomático y se parezca más a Python.

Resumen
=======

Esta publicación resume el reto. Para ver el código fuente pueden remitirse
`al repositorio <https://github.com/nicoguaro/numerical_challenge_2017>`_.


El veredicto
------------

Ya que el reto es conmigo mismo, y el propósito era aprender algo de
Julia, el veredicto es: **exitoso**. Sin embargo, fallé en el día 26
con el Método de Elementos de Frontera.

La lista de métodos
-------------------

+----------------------------+---------------------------------------------------+
| Día                        | Método numérico                                   |
+============================+===================================================+
|  `01 <../numerical-01>`_   | Bisección                                         |
+----------------------------+---------------------------------------------------+
|  `02 <../numerical-02>`_   | Regula falsi                                      |
+----------------------------+---------------------------------------------------+
|  `03 <../numerical-03>`_   | Newton                                            |
+----------------------------+---------------------------------------------------+
|  `04 <../numerical-04>`_   | Newton multivariable                              |
+----------------------------+---------------------------------------------------+
|  `05 <../numerical-05>`_   | Broyden                                           |
+----------------------------+---------------------------------------------------+
|  `06 <../numerical-06>`_   | Descenso del gradiente                            |
+----------------------------+---------------------------------------------------+
|  `07 <../numerical-07>`_   | Nelder-Mead                                       |
+----------------------------+---------------------------------------------------+
|  `08 <../numerical-08>`_   | Newton para optimización                          |
+----------------------------+---------------------------------------------------+
|  `09 <../numerical-09>`_   | Interpolación de Lagrange                         |
+----------------------------+---------------------------------------------------+
|  `10 <../numerical-10>`_   | Interpolación de Lagrange con muestreo de Lobatto |
+----------------------------+---------------------------------------------------+
|  `11 <../numerical-11>`_   |Interpolación de Lagrange con matriz de Vandermonde|
+----------------------------+---------------------------------------------------+
|  `12 <../numerical-12>`_   | Interpolación de Hermite                          |
+----------------------------+---------------------------------------------------+
|  `13 <../numerical-13>`_   | Interpolación spline                              |
+----------------------------+---------------------------------------------------+
|  `14 <../numerical-14>`_   | Cuadratura trapezoidal                            |
+----------------------------+---------------------------------------------------+
|  `15 <../numerical-15>`_   | Cuadratura de Simpson                             |
+----------------------------+---------------------------------------------------+
|  `16 <../numerical-16>`_   | Cuadratura de Clenshaw-Curtis                     |
+----------------------------+---------------------------------------------------+
|  `17 <../numerical-17>`_   | Integración de Euler                              |
+----------------------------+---------------------------------------------------+
|  `18 <../numerical-18>`_   | Integración de Runge-Kutta                        |
+----------------------------+---------------------------------------------------+
|  `19 <../numerical-19>`_   | Integración de Verlet                             |
+----------------------------+---------------------------------------------------+
|  `20 <../numerical-20>`_   | Método del disparo                                |
+----------------------------+---------------------------------------------------+
|  `21 <../numerical-21>`_   | Diferencias finitas con método de Jacobi          |
+----------------------------+---------------------------------------------------+
|  `22 <../numerical-22>`_   | Diferencias finitas para valores propios          |
+----------------------------+---------------------------------------------------+
|  `23 <../numerical-23>`_   | Método de Ritz                                    |
+----------------------------+---------------------------------------------------+
|  `24 <../numerical-24>`_   | Elementos finitos en 1D                           |
+----------------------------+---------------------------------------------------+
|  `25 <../numerical-25>`_   | Elementos finitos en 2D                           |
+----------------------------+---------------------------------------------------+
|  `26 <../numerical-26>`_   | Método de elementos de frontera                   |
+----------------------------+---------------------------------------------------+
|  `27 <../numerical-27>`_   | Integración Monte-Carlo                           |
+----------------------------+---------------------------------------------------+
|  `28 <../numerical-28>`_   | Factorización LU factorization                    |
+----------------------------+---------------------------------------------------+
|  `29 <../numerical-29>`_   | Factorización de Cholesky                         |
+----------------------------+---------------------------------------------------+
|  `30 <../numerical-30>`_   | Gradiente conjugado                               |
+----------------------------+---------------------------------------------------+
|  `31 <../numerical-31>`_   | Elementos finitos con solucionador                |
+----------------------------+---------------------------------------------------+

Conclusiones
------------

- Este era un ejercicio de kata de código para aprender algunos detalles sobre
  Julia para computación científica. Como tal, fue muy útil para mí ensuciarme
  las manos con Julia.

- Implementar el Método de Elementos de Frontera en un día parece algo difícil.
  Yo ya lo sabía de antemano, pero lo intenté de todas formas … sin éxito.

- La sintaxis de Julia está en un punto intermedio entre Python y Matlab. Esto
  hace que sea fácil de usar, aunque la documentación de algunas paquetes está
  en una etapa preliminar en este momento.

- No volveré a hacer un reto como estos en un rato. Requiere de mucha atención
  realizarlo.
