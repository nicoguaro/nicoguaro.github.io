.. title: Gráficos isométricos en Inkscape: Parte 2
.. slug: isometric_inkscape2
.. date: 2018-05-30 12:40:57 UTC-05:00
.. tags: inkscape, gráficos por computador, tutorial
.. category: Computer graphics
.. description: Cómo hacer isométricos usando Inkscape.
.. type: text
.. has_math: yes

`La semana pasada <../ isometric_inkscape>`__ publiqué una guía rápida
sobre dibujos isométricos dibujar usando `Inkscape <https://inkscape.org/en/>`__.
En ese post, mostré cómo obtener imágenes que se proyectan a las caras de
un bloque isométrico.

Después de mi publicación, `Biswajit Banerjee <https://twitter.com/parresianz>`__
me preguntó en `Twitter <https://twitter.com/parresianz/status/999787980658126848>`__
si podría repetir el proceso con un ejemplo más complejo, y él sugirió
el siguiente diagramaa

.. image:: https://upload.wikimedia.org/wikipedia/commons/thumb/6/69/Beam_moment_plain.svg/512px-Beam_moment_plain.svg.png
   :alt: Cálculo del momento de inercia para una viga.
   :align:  center

que, creo, se creó en Inkscape usando la opción "Crear caja 3D".

En esta publicación, haré lo siguiente:

1. Usar el mismo enfoque de la semana pasada para recrear este esquema.
2. Sugerir mi enfoque preferido para dibujar este esquema.


Primer enfoque
--------------

Repetiré el resumen de la semana pasada. Hay que tener en cuenta que
Inkscape trata la rotación en sentido horario como positiva.

.. image:: /images/isometric_inkscape/isometric_instructions.svg
   :width: 500 px
   :alt: Resumen para esquemas isométricos en Inkscape.
   :align:  center


Luego, para crear una caja con las dimensiones deseadas, primero creamos
cada rectángulo con las dimensiones correctas (en proyecciones paralelas).
En el siguiente ejemplo, usamos caras con relaciones de aspecto 3:2,
2:1 y 4:3. La caja de la derecha es la cifra obtenida después de aplicar
las transformaciones descritas en el esquema anterior.

.. image:: /images/isometric_inkscape/isometric_ex2.svg
   :width: 500 px
   :alt: Orthogonal views and final isometric figure
   :align:  center

Ahora podemos proceder, para recrear la figura deseada. No conozco las
dimensiones exactas de la caja; supongo que la sección transversal era
un cuadrado y la relación de aspecto era 5:1. Después de aplicar las
transformaciones para cada rectángulo obtenemos lo siguiente
(agregando algunos ajustes aquí y allá).

.. image:: /images/isometric_inkscape/isometric_beam.svg
   :width: 500 px
   :alt: Figura usando el enfoque descrito.
   :align:  center
   
Segundo enfoque
---------------

Para este tipo de esquema, preferiría crear una cuadrícula axonométrica
(``Archivo > Propiedades de documento > Cuadrículas``). Después de
agregar la cuadrícula a nuestro lienzo es bastante sencillo dibujar las
figuras en vista isométrica. El lienzo debe ser similar a la siguiente
imagen.

.. image:: /images/isometric_inkscape/screenshot_inkscape.png
   :width: 500 px
   :alt: Segundo enfoque: usando una rejilla axonométrica.
   :align:  center

Luego podemos dibujar cada cara usando la cuadrícula. Si queremos ser
más precisos podemos activar ``Ajustar a nodos cúspides``. La siguiente
animación muestra la construcción paso a paso.


.. image:: /images/isometric_inkscape/isometric_construction.gif
   :width: 500 px
   :alt: Construcción del isométrico paso a paso.
   :align:  center

Y obtenemos la siguiente imagen.

.. image:: /images/isometric_inkscape/isometric_beam2.svg
   :width: 500 px
   :alt: Figura usando el segundo enfoque.
   :align:  center
   
Conclusión
----------

Como mencioné, Inkscape se puede usar para dibujar figuras simples en
proyección isométrica. Sin embargo, sugiero utilizar un CAD como
`FreeCAD <https://freecadweb.org/>`__ para geometrías más complicadas.

