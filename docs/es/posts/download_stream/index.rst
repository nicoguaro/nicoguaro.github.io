.. title: Descargar videos de MS Stream
.. slug: download_stream
.. date: 2020-06-12 15:31:22 UTC-05:00
.. tags: tutorial, nodejs, videos
.. category: Tutorial
.. link:
.. description:
.. type: text

Esta semana un estudiante me preguntó acerca de descargar los videos de uno
de los cursos de MS Stream. El problema es que si no eres propietario
del video no puedes descargarlo. Entonces, voy a mostrar una opción para
descargar videos sin ser propietario de los mismos.

**Descargo de responsabilidad:** puede ser una buena idea preguntar a tu
organización sobre los derechos de autor de los videos.

Prerrequisitos
--------------

Vas a necesitar lo siguiente:

- `git <https://git-scm.com/downloads>`_;

- `ffmpeg <https://www.ffmpeg.org/download.html>`_; and

- `Node.js <https://nodejs.org/en/download/>`_.

Instalación de ``destreamer``
-----------------------------

Después de obtener los requisitos previos, puedes descargar
`destreamer <https://github.com/snobu/destreamer>`_ usando

.. code:: bash

  $ git clone https://github.com/snobu/destreamer
  $ cd destreamer
  $ npm install
  $ npm run build

en una terminal.

Si no se quiere jugar con
`variables de entorno <https://en.wikipedia.org/wiki/Environment_variable>`_,
sugiero agregar ``ffmpeg`` a la misma carpeta en donde se encuentra
``destreamer``.

Descarga
---------

Después de eso, debe navegar a la carpeta donde descargaste ``destreamer`` y

.. code:: bash

  $ ./destreamer.sh -i "https://web.microsoftstream.com/video/VIDEO_ID"

en Mac o Linux,

.. code:: bash

  $ destreamer.cmd -i "https://web.microsoftstream.com/video/VIDEO_ID"

en el *command prompt* en Windows, y

.. code:: bash

  $ destreamer.ps1 -i "https://web.microsoftstream.com/video/VIDEO_ID"

en PowerShell. ``VIDEO_ID`` se refiere al identificador del video
en MS Stream.


Si deseas descargar varios archivos (como un curso completo),
puedes crear un archivo con las URL y usar

.. code:: bash

  $ destreamer.cmd -f filename.txt
