.. title: Using Wolfram Language in Jupyter: A free alternative to Mathematica
.. slug: wolfram_jupyter
.. date: 2021-03-30 19:50:09 UTC-05:00
.. tags: jupyter, computer algebra system, wolfram engine, mathematica
.. category: Tutorial
.. link: 
.. description: 
.. type: text
.. has_math: yes

In this post I am going to describe how to add the Wolfram Language to
the Jupyter notebook. This provides a free alternative to Mathematica with,
pretty much, the same syntax. The use of the Wolfram Engine is free for
non-production as described in their website:

  The Free Wolfram Engine for Developers is available for non-production
  software development.

  You can use this product to:

  - develop a product for yourself or your company
  
  - conduct personal projects at home, at school, at work
  
  - explore the Wolfram Language for future production projects


Installation
------------

To install you should do the following steps:

- `Download Wolfram Engine <https://www.wolfram.com/engine>`_.

- Create a Wolfram account, if you don't have one.

- Execute the installer.

- Type the following in a terminal

.. code::

    wolframscript

and you should be asked for your email and password.

After that you should be in a terminal and see the following

.. code::

    Wolfram Engine activated. See https://www.wolfram.com/wolframscript/ for more information.
    Wolfram Language 12.2.0 Engine for Linux x86 (64-bit)
    Copyright 1988-2021 Wolfram Research, Inc.

|

And we can try that it is working

.. code:: mathematica

    In[1]:= $Version                                                                              

    Out[1]= 12.2.0 for Linux x86 (64-bit) (January 7, 2021)

    In[2]:= Integrate[1/(1 + x^2), x]                                                             

    Out[2]= ArcTan[x]

|

Now we need to install
`WolframLanguageForJupyter <https://github.com/WolframResearch/WolframLanguageForJupyter.git>`_.
For that we can type the following in a terminal

.. code:: bash

    git clone https://github.com/WolframResearch/WolframLanguageForJupyter.git

    cd WolframLanguageForJupyter/

    ./configure-jupyter.wls add

|

To test that it is installed we can type the following in a terminal

.. code:: bash

    jupyter kernelspec list

and it should have an output that includes a line similar to the following

.. code:: bash

    wolframlanguage12.   /home/nicoguaro/.local/share/jupyter/kernels/wolframlanguage12.2

|

Or we could also try with

.. code:: bash

    jupyter notebook

and see the following in the kernel menu.

.. image:: /images/wolfram_menu.png
    :width: 400 px
    :alt: Kernel menu after installing WolframLanguageForJupyter.
    :align:  center

|

Test drive
-----------

I tested some of the capabilities and you can download the
`notebook </downloads/notebooks/wolfram_notebook.ipynb>`_ or
see a static version
`here <http://nbviewer.jupyter.org/url/nicoguaro.github.io/downloads/notebooks/wolfram_notebook.ipynb>`_.


Let's compute the integral

.. math::

    \int \frac{1}{1 + x^3}\mathrm{d}x\, .


.. code:: mathematica

    sol:= Integrate[1/(1 + x^3), x]
    TeXForm[sol]

.. math::
    
    -\frac{1}{6} \log \left(x^2-x+1\right)+\frac{1}{3} \log (x+1)+\frac{\tan^{-1}\left(\frac{2 x-1}{\sqrt{3}}\right)}{\sqrt{3}}

|

And make a 3D plot.

.. code::

    fun:= Sin[Sqrt[x^2 + y^2]]/Sqrt[x^2 + y^2]
    Plot3D[fun, {x, -5*Pi, 5*Pi}, {y, -5*Pi, 5*Pi},
        PlotPoints -> 100, BoxRatios -> {1, 1, 0.2},
        PlotRange -> All]

.. image:: /images/wolfram_plot.png
    :width: 600 px
    :alt: 3D plot in the notebook.
    :align:  center

|

In this case we don't have an interactive image. This is still not implemented,
but if you are interested there is an
`open issue <https://github.com/WolframResearch/WolframLanguageForJupyter/issues/76>`_
about it in GitHub.

