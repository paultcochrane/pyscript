#!/usr/bin/env pyscript

# $Id$

"""
State swapping quantum computing circuit diagram.  Uses the
quantumcircuits library.
"""

from pyscript import *
from pyscript.lib.quantumcircuits import *

#----------------------------------------------------------------------------------------------

defaults.tex_head=r"""
\documentclass{article}
\pagestyle{empty}

\newcommand{\ket}[2]{\mbox{$|#1\rangle_{#2}$}}
\newcommand{\bra}[1]{\mbox{$\langle #1|$}}
\newcommand{\braket}[2]{\mbox{$\langle #1|#2\rangle$}}
\newcommand{\op}[1]{\mbox{\boldmath $\hat{#1}$}}
\begin{document}
"""

# define the rails
rail1 = Rail(w=P(0,0), length=3.0, labelIn=r'\ket{\psi}{}', labelOut=r'\ket{\phi}{}')
rail2 = Rail(w=P(0,1), length=3.0, labelIn=r'\ket{\phi}{}', labelOut=r'\ket{\psi}{}')

# three controlled nots
cnot1 = Cnot(c=P(0.5,0), targetDist=1.0, direction="up")
cnot2 = Cnot(c=P(1.5,1), targetDist=1.0, direction="down")
cnot3 = Cnot(c=P(2.5,0), targetDist=1.0, direction="up")

# draw it!
render(rail1,rail2,cnot1,cnot2,cnot3,file="stateSwap.eps")

# vim: expandtab shiftwidth=4:

