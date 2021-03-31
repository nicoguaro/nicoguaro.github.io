.. title: Usando el lenguaje de Wolfram en Jupyter: Alternativa gratuita a Mathematica
.. slug: wolfram_jupyter
.. date: 2021-03-30 19:50:09 UTC-05:00
.. tags: jupyter, computer algebra system, wolfram engine, mathematica
.. category: Tutorial
.. link: 
.. description: 
.. type: text
.. has_math: yes

En esta publicación voy a describir cómo agregar Wolfram Language a
Jupyter. Esto proporciona una alternativa gratuita a Mathematica con,
prácticamente, la misma sintaxis. El uso de Wolfram Engine es gratuito en un
ambiente que no sea de producción como se describe en su sitio web:

   Wolfram Engine es gratuito para desarrolladores está disponible para
   aplicaciones que no son de producción. desarrollo de software.

   Puede utilizar este producto para:

   - desarrollar un producto para usted o su empresa
  
   - realizar proyectos personales en casa, en la escuela, en el trabajo
  
   - explorar Wolfram Language para futuros proyectos de producción


Instalación
------------

Para instalar debes seguir los siguientes pasos:

- `Descargar Wolfram Engine <https://www.wolfram.com/engine>`_.

- Crear una cuenta de Wolfram, si no tienes una.

- Ejecutar el instalador.

- Digitar lo siguiente en la terminal.

  .. code::

      wolframscript

y te debería preguntar por tu correo y contraseña.

Luego deberías estar en una terminal y ver lo siguiente

.. code::

    Wolfram Engine activated. See https://www.wolfram.com/wolframscript/ for more information.
    Wolfram Language 12.2.0 Engine for Linux x86 (64-bit)
    Copyright 1988-2021 Wolfram Research, Inc.

|

Y podemos probar que está funcionando

.. code:: mathematica

    In[1]:= $Version                                                                              

    Out[1]= 12.2.0 for Linux x86 (64-bit) (January 7, 2021)

    In[2]:= Integrate[1/(1 + x^2), x]                                                             

    Out[2]= ArcTan[x]

|

Ahora debemos instalar
`WolframLanguageForJupyter <https://github.com/WolframResearch/WolframLanguageForJupyter.git>`_.
Para esto debemos digitar lo siguiente en una terminal

.. code:: bash

    git clone https://github.com/WolframResearch/WolframLanguageForJupyter.git

    cd WolframLanguageForJupyter/

    ./configure-jupyter.wls add

|

Para probar que está instalado podemos digitar lo siguiente

.. code:: bash

    jupyter kernelspec list

y debería tener una salida similar a la siguiente

.. code:: bash

    wolframlanguage12.   /home/nicoguaro/.local/share/jupyter/kernels/wolframlanguage12.2

|

O también podemos intentar con

.. code:: bash

    jupyter notebook

y ver lo siguiente en el menú de kernel.

.. image:: /images/wolfram_menu.png
    :width: 400 px
    :alt: Menú de kernels luego de instalar  WolframLanguageForJupyter.
    :align:  center

|

Prueba
-----------

Probé algunas de las capacidades y puedes descargar el 
`notebook </downloads/notebooks/wolfram_notebook.ipynb>`_ o
ver una versión estática
`aquí <http://nbviewer.jupyter.org/url/nicoguaro.github.io/downloads/notebooks/wolfram_notebook.ipynb>`_.


Calculemos la integral

.. math::

    \int \frac{1}{1 + x^3}\mathrm{d}x\, .


.. code::

    sol:= Integrate[1/(1 + x^3), x]
    TeXForm[sol]

.. math::
    
    -\frac{1}{6} \log \left(x^2-x+1\right)+\frac{1}{3} \log (x+1)+\frac{\tan^{-1}\left(\frac{2 x-1}{\sqrt{3}}\right)}{\sqrt{3}}

|

Y realicemos un gráfico 3D.

.. code::

    fun:= Sin[Sqrt[x^2 + y^2]]/Sqrt[x^2 + y^2]
    Plot3D[fun, {x, -5*Pi, 5*Pi}, {y, -5*Pi, 5*Pi},
        PlotPoints -> 100, BoxRatios -> {1, 1, 0.2},
        PlotRange -> All]

.. image:: /images/wolfram_plot.png
    :width: 600 px
    :alt: Gráfico 3D en el notebook.
    :align:  center

|

En este caso no tenemos gráficos interactivos. Esto no está implementado aún,
pero si estás interesado peude ver el
`issue <https://github.com/WolframResearch/WolframLanguageForJupyter/issues/76>`_
sobre esto en GitHub.

