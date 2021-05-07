.. title: Revisión ortográfica en Jupyter Notebook
.. slug: ortografia_jupyter
.. date: 2019-08-20 14:45:41 UTC-05:00
.. tags: tutorial, ciencia de datos, python, computación científica,
.. category: Writing
.. link:
.. description: Describe cómo tener resaltado de palabras mal escritas en español.
.. type: text


El objetivo de esta publicación es mostrar cómo tener revisión automática
de ortografía en Jupyter Notebook, como se muestra a continuación.

.. image:: /images/ortografia_jupyter/ejemplo_ortografia.png
   :width: 600 px
   :alt: Ejemplo de corrección ortográfica en Jupyter Notebook.
   :align:  center


Existen `varias formas <https://stackoverflow.com/q/39324039/3358223>`__ de
realizar esto. Sin embargo, la forma más fácil es a través del complemento
(*nbextension*) Spellchecker_.


Paso a paso
~~~~~~~~~~~

Los pasos a seguir son los siguientes:

1. Instalar Jupyter notebook extensions (nbextensions_). Este incluye
   Spellchecker_.

2. Ubicar los diccionarios en la carpeta donde está el complemento. Los
   diccionarios deben usar la codificación UTF-8.

3. Configurar la ruta de los diccionarios. Esta puede ser una URL o
   una ruta relativa respecto a la carpeta en donde se encuentra el complemento.


A continuación describiremos en detalle cada paso.

Paso 1: Instalación de nbextensions
------------------------------------

Existe una lista de complementos que agregan algunas funcionalidades
comúnmente usadas a Jupyter notebook.

Escriba lo siguiente en una terminal, para instalarlo usando PIP.

.. code:: bash

    pip install jupyter_contrib_nbextensions


Sin embargo, si se está usando Anaconda el **método recomendado** es usar
``conda``, como se muestra a continuación.

.. code:: bash

    conda install -c conda-forge jupyter_contrib_nbextensions


Esto debe instalar los complementos y también la
`interfaz de configuración <https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator>`__.
En el menú principal de Jupyter notebook aparecerá una nueva pestaña
nombrada *Nbextensions* en donde se pueden elegir los complementos a usar.
La apariencia es la siguiente.

.. image:: /images/ortografia_jupyter/interfaz_nbextensions.png
   :width: 600 px
   :alt: Interfaz gráfica para los complementos de Jupyter.
   :align:  center

Algunos complementos recomendados son:

- **Collapsible Headings:** que permite ocultar secciones de los documentos.

- **RISE:** que convierte los notebooks en presentaciones.


Paso 2: Diccionarios para español
---------------------------------

La documentación de Spellchecker_ sugiere usar un script de Python para
descargar diccionarios del proyecto `Chromium <https://chromium.googlesource.com/chromium/deps/hunspell_dictionaries/+/master>`__.
Sin embargo, estos tienen como codificación ISO-8859-1 (occidente) y falla
para caracteres con tildes o virgulillas. Para que no haya problemas el
diccionario debe tener codificación `UTF-8 <https://en.wikipedia.org/wiki/UTF-8>`__.
Pueden descargarse en `este enlace </downloads/dict_es_ES.zip>`__.

Una vez que se tienen los diccionarios se deben ubicar en la ruta del
complemento. En mi computador esta sería

.. code::

  ~/.local/share/jupyter/nbextensions/spellchecker/


y dentro de esta los ubicaremos en

.. code::

  ~/.local/share/jupyter/nbextensions/spellchecker/typo/dictionaries

Esta ubicación es arbitraria, lo importante es que necesitamos conocer
la ruta relativa al complemento.


Paso 3: Configuración complementos
----------------------------------

Ahora, en la pestaña *Nbextensions* seleccionamos el complemento y llenamos
los campos con la información de nuestro diccionario:

- language code to use with typo.js: ``es_ES``

- url for the dictionary .dic file to use: ``./typo/dictionaries/es_ES.dic``

- url for the dictionary .aff file to use: ``./typo/dictionaries/es_ES.aff``

Esto se muestra a continuación.

.. image:: /images/ortografia_jupyter/config_local.png
   :width: 600 px
   :alt: Configuración con archivos locales.
   :align:  center


Otra opción es usar la URL para los archivos. En https://github.com/wooorm/dictionaries
están disponibles los diccionarios del proyecto `hunspell <https://hunspell.github.io/>`__
en UTF-8. En este caso, la configuración sería:

- language code to use with typo.js: ``es_ES``

- url for the dictionary .dic file to use: ``https://raw.githubusercontent.com/wooorm/dictionaries/master/dictionaries/es/index.dic``

- url for the dictionary .aff file to use: ``https://raw.githubusercontent.com/wooorm/dictionaries/master/dictionaries/es/index.aff``

Y se muestra a continuación.

.. image:: /images/ortografia_jupyter/config_url.png
  :width: 600 px
  :alt: Configuración con archivos remotos.
  :align:  center


.. _Spellchecker: <https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/spellchecker/README.html
.. _nbextensions: https://github.com/ipython-contrib/jupyter_contrib_nbextensions

