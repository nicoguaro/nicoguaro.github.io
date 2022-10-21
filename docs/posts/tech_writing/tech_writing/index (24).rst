.. title: Technical writing
.. slug: tech_writing
.. date: 2020-05-28 15:53:40 UTC-05:00
.. tags: writing, research, typography, libreoffice, latex
.. category: Writing
.. link:
.. description: Give some tips on technical writing.
.. type: text
.. status:

This is the first post about technical writing [*]_ from a series that
I will be creating and uploading. Technical writing is
something that most of us have to deal with in different contexts. For
example, in college coursework, research publications, software documentation.
The main idea of the series is to mention some of the tricks that I have
learned over the years and some tools that might come in handy.

Future posts will (probably) be about:

- `Using equations <../tech_writing_math>`_;

- `Using figures <../tech_writing_figs>`_;

- Using tables; and

- Managing bibliographic references.

The current post
================

As mentioned above, technical writing is something that a lot of persons
have to deal with. This is a skill that is sometimes overlooked,
but it should not. According to the
`U.S. Bureau of Labor Statistics <https://www.bls.gov/ooh/media-and-communication/technical-writers.htm>`_

  Technical writers prepare instruction manuals, how-to guides,
  journal articles, and other supporting documents to communicate complex and
  technical information more easily.

And it is a desired skill in the workplace. Its demand is expected to grow
around 10% in the current decade.

Typography
----------

The first thing that I should mention is that writing documents is
typography. "Putting documents" together is typography because
we are *designing with text* (Butterick, 2019). So, we should consider
ourselves typographers since we are constantly designing documents.

I would suggest taking a look at "Butterick's Practical Typography"
since it is a really good book about it and it reads smoothly. I will
mention some important points here according to Butterick's
"Typography in ten minutes":

1. The most important typographic selection is on the body text.
   This is due to the fact that it is most of the document.

2. Choose a point size between 10-12 points for printed documents
   and 15-25 pixels for digital documents.

3. Line spacing should be between 120-145 % of the point size.

4. Line length should be between 45-90 characters. This is roughly
   2 or 3 small caps alphabets:

   abcdefghijklmnopqrstuvwxyzabcdefghijklmnopqrstuvwxyzabcd

5. Mind the selection of your font. Try to avoid default fonts such as
   Arial, Calibri or Times New Roman.

Editors
--------

Another point that I want to touch in this post is about editors. The first
question that arises is "what editor should I use?". The short answer is:
**use whatever your peers are using**. That's my best advice; that way you
have people to discuss with you about your doubts.

The long answer … is that each editor has its weak and strong points. I
have written scientific papers in LaTeX, LibreOffice Writer and MS Word;
all of them look professional. So, in the end, you can write your
documents in several ways and achieve a similar result. I prefer to use
LaTeX for long documents since it is centered in the structure of the
document instead of the appearance and this is the way one should manage
a long document like a dissertation, in my opinion.

If you just want me to pick one editor and suggest it to you, I would
say that you should ride with `LibreOffice <https://www.libreoffice.org/>`_.
A good reference for it is "Designing with LibreOffice". Once you learn
how to use styles you will ask how have you been writing documents all
this time.

There are two main flavors for editors that I am going to discuss:
WYSIWYG (What You See Is What You Get) and markup-based editors.

- WYSIWYG. This category is the one that most people is familiar with.
  Two examples are:

  - LibreOffice writer; and

  - Microsoft Word.

- Markup-based editors rely on marks on the "text" to differentiate
  sections and styles. In this case, your text looks like code, as seen
  in the following image

  .. image:: /images/rst_code.png

  Some examples are:

  - LaTeX;

  - `Markdown <https://www.markdownguide.org/getting-started>`_; and

  - `reStructuredtext <https://docutils.sourceforge.io/rst.html>`_.


Independently of what your main editor is I suggest that you use
`Pandoc <https://pandoc.org/>`_. It allows you to convert between several
formats, making the process a little bit easier. There is even an editor
based completely on it named `Panwriter <https://panwriter.com/>`_.


References
----------

1. Matthew Butterick (2019). `Butterick's Practical Typography <https://practicaltypography.com/>`_.
   Second edition, Matthew Butterick.

2. Wikibooks contributors. (2020). `LaTeX <https://en.wikibooks.org/wiki/LaTeX>`_.
   Wikibooks, The Free Textbook Project.

3. Bruce Byfield (2016). `Designing with LibreOffice <https://designingwithlibreoffice.com/>`_.
   Friends of OpenDocument, Inc.

4. Deville, S. (2015).
   `Writing academic papers in plain text with Markdown and Jupyter notebook
   <https://sylvaindeville.net/2015/07/17/writing-academic-papers-in-plain-text-with-markdown-and-jupyter-notebook/>`_.
   Sylvain Deville.

5. Eric Holscher (2016).
   `An introduction to Sphinx and Read the Docs for Technical Writers
   <https://www.ericholscher.com/blog/2016/jul/1/sphinx-and-rtd-for-writers/>`_.


.. [*] This post is (somewhat) related to a
   `previous post <../herramientas-investigacion/>`__
   where I discussed research tools that most of us need but are not
   commonly taught in a formal fashion.
