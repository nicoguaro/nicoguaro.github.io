.. title: About teleportation in Star Trek
.. slug: teletransportacion-star-trek
.. date: 2013-04-18 03:40:00
.. tags: science fiction, back-of-the-envelope calculations, popular science, old blog
.. category: Popular science
.. has_math: yes

A friend once asked me about which of two methods was easier to
teleport people. One consisted of "deconfiguring" and "reconfiguring"
the person (as information, similar to `Start Trek <http://en.wikipedia.org/wiki/Transporter_%28Star_Trek%29>`_
and the other in "creating a shortcut" between two places in space-time to pass
to the person. Obviously, in both cases assuming that such things can be
done.

Regarding the creation of the shortcut in space-time, I think I have not
studied the equations of General Relativity to be able to do the math,
although perhaps in `Física Pasión <http://fisicapasion.blogspot.com/>`_
give us these calculations.

The first of the alternatives consists of, basically, the representation of a
person as information and its "deconfiguration" processing, transmission and
processing of "reconfiguration". Since as humans we are made, mostly,
of water we will assume a person of water for the calculations. We will also take
as reference mass :math:`70\, \mbox {kg}`.

Some data that we will use are:

- The molar mass of water is :math:`M_{H_2O}=18,01528\ \mbox{g/mol}`;
- Avogradro number is :math:`N_A=6,022 \times 10^{23}/\mbox{mol}`.

Then, we have that the number of moles in a person is

.. math::

    m_\text{persona} = \frac{70\ \mbox{kg}\ \mbox{moles}}
        {18,015\times 10^{-3} \text{kg}}
        =3885,7\ \mbox{moles}\, ,

and the number of molecules is

.. math::

    N_\text{moleculas} = N_A m_\text{persona} = 2,34\times 10^{27}\ \mbox{moleculas}\, .

Water has 12 vibrational and 6 translational modes, and furthermore 40 quantum
electronic numbers. This add up to 58 degrees of freedom for each molecule.
Thus, the total number of degrees of freedom is

.. math::

    N_{GDL} = 1,36\times 10^{29}\, .

In 2011 there was a `transmission record <https://goo.gl/YEvzpM>`_
of 186 Gb/s, considering this rate the time it would take to transmit
all data (assuming data represented as 32 bits real numbers)
would take :math:`2,3 \times 10^{16}\ \mbox {s}` or, equivalently,
:math:`1.70 \times 10^{10}` years (the estimated age of the universe is
:math:`1.37 \times 10^{10}` years).    

If we wanted this to happen really fast, say in 1 millisecond, the transmission
rate should be :math:`2.3 \times 10^{19}` faster than the record they reached
at CERN… something that is inconceivable for us today.
