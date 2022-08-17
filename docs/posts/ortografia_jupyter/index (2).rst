.. title: Spell Check in Jupyter Notebook
.. slug: ortografia_jupyter
.. date: 2019-08-20 14:45:41 UTC-05:00
.. tags: tutorial, data science, python, scientific computing,
.. category: Writing
.. link:
.. description: Describe how to highlight misspelled words in Spanish.
.. type: text


The purpose of this post is to show how to have automatic spell check in
Jupyter Notebook, as shown below.

.. image:: /images/ortografia_jupyter/ejemplo_ortografia.png
   :width: 600 px
   :alt: Example of spell checking in Jupyter Notebook.
   :align:  center

There are `several ways <https://stackoverflow.com/q/39324039/3358223>`__
to do this. However, the easiest way is through the (*nbextension*)
Spellchecker_. plugin.

Step by step
~~~~~~~~~~~~

The steps to follow are those:

1. Install Jupyter notebook extensions (nbextensions_). This includes
   Spellchecker_.

2. Locate the dictionaries in the folder where the plugin is. Dictionaries
   must use UTF-8 encoding.

3. Configure the path of the dictionaries. This can be a URL or a path
   relative to the folder where the plugin is located.

We will describe each step in detail below.

Step 1: Install nbextensions
-----------------------------

There is a list of plugins that add some commonly used functionality to
the Jupyter notebook.

Type the following in a terminal, to install it using PIP.

.. code:: bash

    pip install jupyter_contrib_nbextensions


However, if Anaconda is being used the **recommended method** is to use
``conda``, as shown below.

.. code:: bash

    conda install -c conda-forge jupyter_contrib_nbextensions

This should install the plugins and also the
`configuration interface <https://github.com/Jupyter-contrib/jupyter_nbextensions_configurator>`__.
In the main menu of Jupyter notebook a new tab named *Nbextension* will
appear. Here you can choose the add-ons to use. The appearance is
as follows.

.. image:: /images/ortografia_jupyter/interfaz_nbextensions.png
   :width: 600 px
   :alt: Graphical interface for Jupyter plugins.
   :align:  center

Some recommended plugins are:

- **Collapsible Headings:** that allows to hide sections of the documents.

- **RISE:** that turns notebooks into presentations.


Step 2: Dictionaries for Spanish
---------------------------------

The documentation of Spellchecker_ suggests using a Python script to
download dictionaries from project `Chromium <https://chromium.googlesource.com/chromium/deps/hunspell_dictionaries/+/master>`__.
However, these are encoded in  ISO-8859-1 (western) and it fails
for characters with accents or tildes. So, to avoid problems the
dictionary must be `UTF-8 <https://en.wikipedia.org/wiki/UTF-8>`__.
They can be downloaded at `this link </downloads/dict_es_ES.zip>`__.

Once you have the dictionaries, they must be located in the path of the
plugin. On my computer this would be

.. code::

  ~/.local/share/jupyter/nbextensions/spellchecker/


and within this we will place them in

.. code::

  ~/.local/share/jupyter/nbextensions/spellchecker/typo/dictionaries

This location is arbitrary, the important thing is that we need to know
the relative path to the plugin.


Step 3: Plugin Configuration
-----------------------------

Now, in the *Nbextensions* tab we select the plugin and fill the fields
with the information from our dictionary:

- language code to use with typo.js: ``es_ES``

- url for the dictionary .dic file to use: ``./typo/dictionaries/es_ES.dic``

- url for the dictionary .aff file to use: ``./typo/dictionaries/es_ES.aff``

This is shown below.

.. image:: /images/ortografia_jupyter/config_local.png
   :width: 600 px
   :alt: Configuration with local files.
   :align:  center

Another option is to use the URL for the files. The dictionaries of the
project `hunspell <https://hunspell.github.io/>`__ in UTF-8 are available
at https://github.com/wooorm/dictionaries. In this case, the configuration
would be:

- language code to use with typo.js: ``es_ES``

- url for the dictionary .dic file to use: ``https://raw.githubusercontent.com/wooorm/dictionaries/master/dictionaries/es/index.dic``

- url for the dictionary .aff file to use: ``https://raw.githubusercontent.com/wooorm/dictionaries/master/dictionaries/es/index.aff``

And it is shown below.

.. image:: /images/ortografia_jupyter/config_url.png
  :width: 600 px
  :alt: Configuration with remote files.
  :align:  center

.. _Spellchecker: <https://jupyter-contrib-nbextensions.readthedocs.io/en/latest/nbextensions/spellchecker/README.html
.. _nbextensions: https://github.com/ipython-contrib/jupyter_contrib_nbextensions
