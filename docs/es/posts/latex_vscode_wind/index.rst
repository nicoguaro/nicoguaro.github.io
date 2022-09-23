.. title: Using MikTex with LaTeX Workshop on Windows
.. slug: latex_vscode_wind
.. date: 2022-09-23 12:00:00 UTC-05:00
.. tags: writing, research, typography, latex, visual-studio-code
.. category: Writing
.. link:
.. description: Setting LaTeX with VS Code
.. type: text

This is a post to mention how to setup Visual Studio Code for LaTeX—through
the `LaTeX Workshop extension
<https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop>`_.

In the past,  I have used several text editors and for LaTeX. A couple of years
ago I replaced `TeXstudio <https://www.texstudio.org/>`_ for VS Code, and I think
that it works just fine. `Visual Studio Code <https://code.visualstudio.com/>`_
is one of the `most used IDE right now
<https://insights.stackoverflow.com/survey/2019#development-environments-and-tools>`_.
One advantage of using VS Code to type your documents is that you can set it up
to fit your workflow and use it for several languages/purposes. It is also
cross-platform, you will not be worrying for having different workflows in
Linux or Windows.

You need to follow these steps to make it work:

- Install Perl. You can use `Strawberry Perl <https://strawberryperl.com/>`_ in
  Windows.
- If you don't have administrator privileges you can install the `portable
  version <https://strawberryperl.com/releases.html>`_ and add the path to the
  executable to the PATH environment variable.
- Install MikTeX. The creator of LaTeX Workshop suggests to use TeX Live instead
  because it already comes with Perl and you could skip one step in this list.
  The disadvantages of using TeX Live instead of MikTeX are more
  (see `here <https://tex.stackexchange.com/questions/20036/what-are-the-advantages-of-tex-live-over-miktex>`_).
- Install `LaTeX Workshop <https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop>`_.




References
----------

1. Cangemi, Denis. “The Reasons Why You Must Use Visual Studio Code.” Medium,
   13 Aug. 2020, https://blog.devgenius.io/the-reasons-why-you-must-use-visual-studio-code-b522f946a849.

2. Wright, Joseph. “TeX on Windows: TeX Live versus MiKTeX Revisited.” Some TeX
   Developments, 18 Dec. 2016, https://www.texdev.net/2016/12/18/tex-on-windows-tex-live-versus-miktex-revisited/.

|