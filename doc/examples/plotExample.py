#!/usr/bin/env python

# state sniffing in a cryptography scheme with a quantum cloner diagram

import sys
sys.path.append('../../')
sys.path.append('../../pyscript')
sys.path.append('../../pyscript/lib')

from pyscript import *
from plot import *

#----------------------------------------------------------------------------------------------
defaults.units=UNITS['cm']

defaults.tex_head=r"""
\documentclass{article}
\pagestyle{empty}

\newcommand{\ket}[2]{\mbox{$|#1\rangle_{#2}$}}
\newcommand{\bra}[1]{\mbox{$\langle #1|$}}
\newcommand{\braket}[2]{\mbox{$\langle #1|#2\rangle$}}
\newcommand{\op}[1]{\mbox{\boldmath $\hat{#1}$}}
\begin{document}
"""




# draw it!
render(plot1,file="plotExample.eps")

