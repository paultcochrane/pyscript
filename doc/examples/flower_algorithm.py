#!/usr/bin/env pyscript

# $Id$

"""
Quite a complex example of using the quantumcircuits library.  This shows
the quantum circuit of the flower algorithm.
"""

from pyscript import *
import pyscript.lib.quantumcircuits as qc


#-----------------------------------------------------------------------------
defaults.units=UNITS['cm']

defaults.tex_head=r"""
\documentclass{article}
\pagestyle{empty}

\newcommand{\ket}[1]{\mbox{$|#1\rangle$}}
\newcommand{\bra}[1]{\mbox{$\langle #1|$}}
\newcommand{\braket}[2]{\mbox{$\langle #1|#2\rangle$}}
\newcommand{\op}[1]{\mbox{\boldmath $\hat{#1}$}}
\begin{document}
"""

p1=Path(P(-.8,0),P(11,0),linewidth=2)
p2=Path(P(0,2),P(6.7,2))
p3=Path(P(0,4),P(6.7,4))
p4=Path(P(0,5),P(6.7,5))



r=Rectangle(c=P(6,3.5),width=.8,height=4.2,bg=Color(1))
t=TeX(r'QFT$^\dagger$')
t.rotate(-90)
t.c=r.c
qft=Group(r, t )

ket0=TeX(r'\ket{0}')

det=qc.detector()

dots=TeX(r'$\cdots$')
vdots=TeX(r'$\vdots$')

H=qc.Boxed(TeX(r'H'))

anc=TeX('$q$ ancilla qubits')
anc.rotate(-90)

render(p1,p2,p3,p4,
       
       Rectangle(s=P(2.7,-.2),height=5.4,width=.5,bg=Color(1),fg=Color(1)),
       dots.copy(c=P(2.7,0)),
       dots.copy(c=P(2.7,2)),
       dots.copy(c=P(2.7,4)),
       dots.copy(c=P(2.7,5)),
       vdots.copy(c=P(-.2,3)),
       vdots.copy(c=P(1,3)),
       vdots.copy(c=P(6.8,3)),

       H.copy(c=P(1,2)),
       H.copy(c=P(1,4)),
       H.copy(c=P(1,5)),

       qc.classicalpath(Path(P(6.7,2),P(7.5,2),P(7.5,5),P(6.7,5)),
                        Path(P(6.7,4),P(7.5,4)),
                        Path(P(7.5,3),P(9,3),P(9,0)),
                        ),


       qc.cbox(TeX(r'$\;U^{2^0}\;$'),1.8,0,2),
       qc.cbox(TeX(r'$U^{2^{q-2}}$'),3.8,0,4),
       qc.cbox(TeX(r'$U^{2^{q-1}}$'),5,0,5),

       det.copy(c=p2.end),
       det.copy(c=p3.end),
       det.copy(c=p4.end),

       qc.Boxed(TeX(r'$\mathcal{D}$'),c=P(9,0)),
       TeX(r'\renewcommand{\arraycolsep}{1mm}$\left\{\begin{array}{ccc}0&\mathrm{w.p.}&1-p(E_j)\\1&\mathrm{w.p.}&p(E_j)\end{array}\right.$',w=P(9.1,3)),
       qc.Boxed(TeX(r'$\phi_j$'),c=P(7.5,3)),
       qc.Dot(P(9,3)),

       ket0.copy(e=p2.start),
       ket0.copy(e=p3.start),
       ket0.copy(e=p4.start),
       TeX(r'$\rho$',e=p1.start-P(.1,0)),
       TeX(r'$\mathcal{E}(\rho)$',w=p1.end+P(.1,0)),

       
       TeX(r'\ket{E_j}',s=P(7.5,0.1)),

       anc(c=P(-1,3.5)),

       qft,
       file="flower_algorithm.eps")


# vim: expandtab shiftwidth=4:
