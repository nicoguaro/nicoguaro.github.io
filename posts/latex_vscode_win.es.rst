.. title: Usando MixTex con LaTeX Workshop en Windows
.. slug: latex_vscode_wind
.. date: 2022-09-23 12:00:00 UTC-05:00
.. tags: escritura, investigación, tiografía, latex, visual-studio-code
.. category: Escritura
.. description: Cómo configurar LaTeX con VS Code
.. type: text


Este es un post para mencionar cómo configurar Visual Studio Code
para LaTeX—a través de la extensión `LaTeX Workshop
<https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop>`_—.

En el pasado, he utilizado varios editores de texto y para LaTeX. Hace un par
de años sustituí `TeXstudio <https://www.texstudio.org/>`_ por VS Code, y creo
que funciona muy bien. `Visual Studio Code <https://code.visualstudio.com/>`_
es uno de los `IDE más usados ahora mismo
<https://insights.stackoverflow.com/survey/2019#development-environments-and-tools>`_.
Una ventaja de usar VS Code para escribir tus documentos es que puedes
configurarlo para adaptarse a tu flujo de trabajo y utilizarlo para varios
lenguajes/propósitos. También es multiplataforma, no tendrás que preocuparte
por tener diferentes flujos de trabajo en Linux o Windows.

Necesitas seguir estos pasos para hacerlo funcionar:

- Instala Perl. Puedes utilizar `Strawberry Perl <https://strawberryperl.com/>`_
  en Windows.
- Si no tienes privilegios de administrador puedes instalar la versión `portable
  <https://strawberryperl.com/releases.html>`_ y añadir la ruta al ejecutable
  a la variable de entorno PATH.
- Instala MikTeX. El creador de LaTeX Workshop sugiere usar TeX Live en su lugar
  porque ya viene con Perl y podrías saltarte un paso de esta lista.
  Las desventajas de usar TeX Live en lugar de MikTeX son más
  (vea `aquí <https://tex.stackexchange.com/questions/20036/what-are-the-advantages-of-tex-live-over-miktex>`_).
- Instala `LaTeX Workshop <https://marketplace.visualstudio.com/items?itemName=James-Yu.latex-workshop>`_.


Referencias
-----------

1. Cangemi, Denis. “The Reasons Why You Must Use Visual Studio Code.” Medium,
   13 de agosto de 2020, https://blog.devgenius.io/the-reasons-why-you-must-use-visual-studio-code-b522f946a849.

2. Wright, Joseph. “TeX on Windows: TeX Live versus MiKTeX Revisited.” Some TeX
   Developments, 18 de diciembre de 2016, https://www.texdev.net/2016/12/18/tex-on-windows-tex-live-versus-miktex-revisited/.

|