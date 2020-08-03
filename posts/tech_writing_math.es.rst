.. title: Escritura técnica: usando matemáticas
.. slug: tech_writing_math
.. date: 2020-08-02 18:00:00 UTC-05:00
.. tags: escritura, investigación, tipografía, libreoffice, latex, ms-word, matemáticas
.. category: Writing
.. link:
.. description: Consejos para escritura técnica con matemáticas.
.. type: text
.. has_math: yes
.. status:


En una `publicación anterior <../tech_writing>`_ mencioné algunos aspectos
generales de la escritura técnica. En este me gustaría hablar sobre la
inclusión de expresiones matemáticas en documentos técnicos.

Hay dos formas principales de incluir matemáticas en documentos:

- utilizando texto; y

- utilizando una interfaz gráfica.

Usar una interfaz gráfica, como el editor de ecuaciones en LibreOffice Writer o
MS Word, o `MathType <http://www.dessci.com/en/products/mathtype/>`_ es
conveniente. No es necesario memorizar nada y se pueden mirar las expresiones
mientras se crean. Sin embargo, puede ser algo lento en comparación con el uso
de entrada de texto —una vez que se está cómodo con la sintaxis—.

Hay dos tipos de ecuaciones utilizadas en Internet:

- `MathML <https://en.wikipedia.org/wiki/MathML>`_ es un
  `estándar W3C <https://en.wikipedia.org/wiki/World_Wide_Web_Consortium>`_
  para ecuaciones y está incluido en HTML5, por lo que funcionaría en todos los
  navegadores modernos El problema con este es que no está diseñado para ser
  escrito a mano. Por tanto, uno puede usarlo si tiene alguna forma automática
  de generar el código.

- `LaTeX <https://www.overleaf.com/learn/latex/Mathematical_expressions>`_
  es mi forma sugerida de escribir ecuaciones. La curva de aprendizaje podría
  ser un un poco empinada al principio pero vale la pena.

Una herramienta que ayuda con las ecuaciones es
`MathPix Snip <https://mathpix.com/>`_ que genera automáticamente código
LaTeX o MathML a partir de una imagen, incluso una escrita a mano. Otra
herramienta que es realmente útil es
`Detexify <http://detexify.kirelabs.org/classify.html>`_ que permite
dibujar un símbolo y proporciona la sintaxis de LaTeX de este.

En el resto de la publicación mostraré mis sugerencias para trabajar
con ecuaciones en LibreOffice y MS Word. Si estás utilizando LaTeX o
MarkDown/ReStructuredText para tus documentos ya estás utilizando
LaTeX para tus ecuaciones.


LibreOffice
===========

LibreOffice tiene su propio editor de ecuaciones con su propia sintaxis y
funciona bien para expresiones pequeñas, pero se complica para ecuaciones
grandes o largas manipulaciones algebraicas. Para LibreOffice sugeriría usar
`TexMaths <http://roland65.free.fr/texmaths/install.html>`_, es fácil de
usar y funciona para el procesador de textos (Writer) y presentaciones (Impress).
Supongo que también funciona para hojas de cálculo (Calc), pero no recuerdo
haber usado ecuaciones en una.

MS Office
=========

MS Office también tiene su propio editor de ecuaciones, funciona bien y es
fácil de usar. Sin embargo, el mismo problema aparece cuando quieres expresiones
largas. Una opción es usar directamente
`LaTeX en Office <https://docs.microsoft.com/en-us/archive/blogs/murrays/latex-math-in-office>`_
pero prefiero usar
`IguanaTex <http://www.jonathanleroux.org/software/iguanatex/download.html>`_.
Es un complemento que permite ingresar ecuaciones de forma similar a TexMaths en
LibreOffice.

También puede pegar directamente las ecuaciones MathML en MS Word (>2013 y Windows).


Usa SymPy
=========

Independientemente de la herramienta que use para escribir sus documentos,
sugiero usar un `CAS <https://es.wikipedia.org/wiki/Sistema_algebraico_computacional>`_
(del inglés Computer Algebra System), como Mathematica o SymPy. Estos programas
permiten la generación automática de LaTeX y MathML a partir de expresiones y
esto facilita mucho el proceso.

Veamos un ejemplo. Supongamos que tenemos la función

.. math:: f(x) = \exp(-x^2) \sin(3*x)

y queremos calcular su segunda derivada

.. math::

    f''(x) = \left(- 12 x \cos{\left(3 x \right)} + 2 \left(2 x^{2} - 1\right) \sin{\left(3 x \right)} - 9 \sin{\left(3 x \right)}\right) e^{- x^{2}}

El siguiente bloque de código nos da el código LaTex

.. code:: python

    from sympy import *
    init_session()
    f = exp(-x**2)*sin(3*x)
    fxx = diff(f, x, 2)
    print(latex(fxx))

que es

.. code:: latex

    \left(- 12 x \cos{\left(3 x \right)} + 2 \left(2 x^{2} - 1\right) \sin{\left(3 x \right)} - 9 \sin{\left(3 x \right)}\right) e^{- x^{2}}

Este corresponde con el código que usé arriba para representar la ecuación.

Si quisiéramos el código MathML de esa expresión podríamos usar
el siguiente fragmento de código

.. code:: python

    from sympy import *
    init_session()
    f = exp(-x**2)*sin(3*x)
    fxx = diff(f, x, 2)
    print(mathml(fxx, printer="presentation"))

observe el argumento opcional ``printer = "presentation"``. Si queremos agregar
esto a MS Word, por ejemplo, podríamos agregar la salida (que no voy a
mostrar porque es realmente larga) dentro del siguiente código

.. code:: xml

    <math xmlns = "http://www.w3.org/1998/Math/MathML">
    </math>


Cuando se usa Jupyter Notebook, esto se puede hacer gráficamente con un
clic derecho sobre la expresión. Y se muestra el siguiente menú.

.. image:: /images/jupyter_export_eqs.png


Referencias
===========

1. “How to Insert Equations in Microsoft Word.” WikiHow,
   https://www.wikihow.com/Insert-Equations-in-Microsoft-Word.
   Fecha de acceso: Agosto 3, 2020.

2. “Copy MathML into Word to Use as Equation.” Stack Overflow,
   https://stackoverflow.com/questions/25430775/copy-mathml-into-word-to-use-as-equation.
   Fecha de acceso: Agosto 3, 2020.

3. “Python - Output Sympy Equation to Word Using Mathml.” Stack Overflow,
   https://stackoverflow.com/questions/40921128/output-sympy-equation-to-word-using-mathml.
   Fecha de acceso: Agosto 3, 2020.
