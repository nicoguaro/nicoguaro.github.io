.. title: Downloading videos from MS Stream
.. slug: download_stream
.. date: 2020-06-12 15:31:22 UTC-05:00
.. tags: tutorial, nodejs, videos
.. category: Tutorial
.. link:
.. description:
.. type: text

This week a student asked me about downloading the videos from one of the
courses from MS Stream. The problem is that if you are not a proprietary
of the video you cannot download it. So, I will show you an option to
download videos without being a proprietary of them.

**Disclaimer:** It might be a good idea if you ask your organization about
the copyright of the videos.

Prerequisites
-------------

You will need the following:

- `git <https://git-scm.com/downloads>`_;

- `ffmpeg <https://www.ffmpeg.org/download.html>`_; and

- `Node.js <https://nodejs.org/en/download/>`_.

``destreamer`` installation
---------------------------

After getting the prerequisites you can download
`destreamer <https://github.com/snobu/destreamer>`_ using

.. code:: bash

  $ git clone https://github.com/snobu/destreamer
  $ cd destreamer
  $ npm install
  $ npm run build

in a terminal.

If you do not want to play with
`environment variables <https://en.wikipedia.org/wiki/Environment_variable>`_,
I suggest that you just add ``ffmpeg`` to the same folder as ``destreamer``.

Downloading
-----------

After that, you need to navigate to the folder where you downloaded
``destreamer`` and

.. code:: bash

  $ ./destreamer.sh -i "https://web.microsoftstream.com/video/VIDEO_ID"

in Mac or Linux,

.. code:: bash

  $ destreamer.cmd -i "https://web.microsoftstream.com/video/VIDEO_ID"

in the command prompt in Windows, and

.. code:: bash

  $ destreamer.ps1 -i "https://web.microsoftstream.com/video/VIDEO_ID"

in PowerShell.``VIDEO_ID`` refers to the identifier in MS Stream.

If you want to download several files (like a complete course), you
can create a file with the URLs and use

.. code:: bash

  $ destreamer.cmd -f filename.txt
