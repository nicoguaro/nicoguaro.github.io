.. title: Gráficos isométricos en Inkscape
.. slug: isometric_inkscape
.. date: 2018-05-24 15:42:02 UTC-05:00
.. tags: inkscape, gráficos por computador, álgebra lineal, tutorial
.. category: Computer graphics
.. description: Cómo hacer isométricos usando Inkscape.
.. type: text
.. has_math: yes

A veces me encuentro en la necesidad de hacer un diagrama usando una
`proyección isométrica <https://en.wikipedia.org/wiki/Isometric_projection>`__.
Cuando el diagrama es complicado la mejor opción es usar algún software de
CAD como `FreeCAD <https://freecadweb.org/>`__, pero a veces sólo se necesita
un diagrama simple. Otra situación en la que esto es común
es en `videojuegos <https://en.wikipedia.org/wiki/Isometric_graphics_in_video_games_and_pixel_art>`__,
donde se el `arte isométrico <https://youtu.be/toWMFcWB4HA>`__ y
`arte pixelado <https://en.wikipedia.org/wiki/Pixel_art>`__ son bastante comunes.

Lo que queremos se muestra en la siguiente figura.

.. image:: /images/isometric_inkscape/isometric_example.svg
   :width: 400 px
   :alt: Ejemplo de isométrico.
   :align:  center


Es decir, queremos comenzar con cierto dibujo, o
escrito en el caso del ejemplo, y queremos saber cómo se
vería en una de las caras de una bloque isométrico.

A continuación, describiré brevemente las transformaciones involucradas en este
proceso. Si sólo está interesado en la receta para hacer esto en Inkscape, pase
al final de este post.

Transformaciones involucradas
-----------------------------

Como estamos trabajando en una pantalla de computador, estamos hablando de 2
dimensiones. Por lo tanto, todas las transformaciones están representadas por
matrices 2×2. En el ejemplo de interés en este post necesitamos las
siguientes transformaciones:

1. Escalado vertical
2. Inclinación horizontal
3. Rotación

Las siguientes son las matrices de transformación.

Escalado en la dirección vertical
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

La matriz está dada por

.. math::

   M_\text{scaling} = \begin{bmatrix} 1 &0\\ 0 &a\end{bmatrix}\, ,

donde :math:`a` es el factor de escalamiento.


Inclinación horizontal
~~~~~~~~~~~~~~~~~~~~~~~

La matriz está dada por

.. math::

   M_\text{skew} = \begin{bmatrix} 1 &\tan a\\ 0 &1\end{bmatrix}\, ,

donde :math:`a` es el ángulo de inclinación.


Rotación
~~~~~~~~~

La matriz está dada por

.. math::

   M_\text{rotation} = \begin{bmatrix} \cos a &-\sin a\\ \sin a &\cos a\end{bmatrix}\, ,

donde :math:`a` es el ángulo de rotación.


Transformación completa
~~~~~~~~~~~~~~~~~~~~~~~

La transformación completa está dada por

.. math::

   M_\text{complete} = M_\text{rotation} M_\text{skew} M_\text{scaling}\, ,

particularmente,

.. math::

   &M_\text{side} =
     \frac{1}{2}\begin{bmatrix} \sqrt{3} & 0\\ -1 &2\end{bmatrix}\approx
     \begin{bmatrix} 0.866 & 0.000\\ -0.500 &1.000\end{bmatrix}\, , \\
   &M_\text{front} = \frac{1}{2}\begin{bmatrix} \sqrt{3} & 0\\ 1 &2\end{bmatrix}\approx
     \begin{bmatrix} 0.866 & 0.000\\ 0.500 &1.000\end{bmatrix}\, , \\
   &M_\text{plant} = \frac{1}{2}\begin{bmatrix} \sqrt{3} & -\sqrt{3}\\ -1 &1\end{bmatrix}\approx
     \begin{bmatrix} 0.866 & -0.866\\ 0.500 &0.500\end{bmatrix}\, .

Estos valores parecen un poco arbitrarios, pero pueden obtenerse de la
`proyección isométrica <https://en.wikipedia.org/wiki/Isometric_projection#Mathematics>`__
misma. Pero esta explicación sería un poco larga para este post.


Tranformación en Inskcape
~~~~~~~~~~~~~~~~~~~~~~~~~

Ya tenemos las matrices de transformación y podemos usarlas en Inkscape.
Pero primero, necesitamos entender cómo funciona. Inkscape usa
`SVG <https://en.wikipedia.org/wiki/Scalable_Vector_Graphics>`__, el estándar
web para gráficos vectoriales.
`Las transformaciones <https://developer.mozilla.org/en-US/docs/Web/SVG/Attribute/transform>`__
en SVG se realizan utilizando la siguiente matriz

.. math::

   \begin{bmatrix} a &c &e\\ b &d &f\\ 0 &0 &1\end{bmatrix}\, ,

que usa `coordenadas homogéneas <https://en.wikipedia.org/wiki/Homogeneous_coordinates>`__.
Entonces, se puede presionar ``Shift + Ctrl + M`` y digitar
las componentes de las matrices que se obtuvieron anteriormente
para :math:`a`, :math:`b`, :math:`c`, y :math:`d`; dejando
:math:`e` y :math:`f` con el valor 0.

Sin embargo, mi método preferido es aplicar cada transformación después de
otro en el cuadro de diálogo `Transformar` (``Shift + Ctrl + M``).
Y este es el método presentado en el resumen al final de esta publicación.


TL;DR
-----
Si solo está interesado en las transformaciones necesarias en Inkscape
Puedes consultar el resumen a continuación. Utiliza el tercer cuadrante como se
presenta abajo.

.. image:: /images/isometric_inkscape/third_angle.svg
   :width: 400 px
   :alt: Nombres para la representación en tercer cuadrante.
   :align:  center

Resumen
~~~~~~~~~~

Tenga en cuenta que Inkscape trata la rotación en sentido horario como
positiva. Opuesto a la notación común en matemáticas.

.. image:: /images/isometric_inkscape/isometric_instructions.svg
   :width: 500 px
   :alt: Resumen para diagramas isométricos en Inkscape.
   :align:  center
