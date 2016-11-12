#!/usr/bin/env python

# plotting example

import sys
sys.path.append('../../')
sys.path.append('../../pyscript')
sys.path.append('../../pyscript/lib')

from Numeric import *
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

# start of plotting script
sigmaMin = sqrt(0.5 + 1.0/sqrt(2.0))
sigmaArr = arrayrange(0.1,10,0.1)
Fbar = zeros((len(sigmaArr),), Float)  # create a 1D array of zeros
for i in range(len(sigmaArr)):
    sigma = sigmaArr[i]
    if sigma > sigmaMin:
        Fbar[i] = (4.0*sigma*sigma+2.0)/(6.0*sigma*sigma+1.0)
    else:
        Fbar[i] = 1.0/((3.0 - 2.0*sqrt(2.0))*sigma*sigma + 1.0)

plot1 = Graph()
plot1.plot(sigmaArr, Fbar)
#           xMinVal=0.0, yMinVal=0.65,
#           xMaxVal=10.0, yMaxVal=1.0,
#           xTickSep=1, yTickSep=0.05)
plot1.xlabel(r"\Large $\sigma$")
plot1.ylabel(r"\Large $\bar{\mathcal{F}}$",angle=0)
    
# draw it!
render(plot1,file="plotExample.eps")

