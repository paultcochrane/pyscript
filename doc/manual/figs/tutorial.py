from pyscript import *
from pyscript.lib.quantumcircuits import *

defaults.units=UNITS['cm']

defaults.tex_head=r"""
\documentclass{article}
\pagestyle{empty}
\usepackage{amsmath}

\newcommand{\ket}[1]{\mbox{$|#1\rangle$}}
\newcommand{\bra}[1]{\mbox{$\langle #1|$}}
\newcommand{\braket}[2]{\mbox{$\langle #1|#2\rangle$}}
\newcommand{\ketbra}[2]{\mbox{|#1$\rangle\langle #2|$}}
\newcommand{\op}[1]{\mbox{\boldmath $\hat{#1}$}}
\newcommand{\R}[3]{%
\renewcommand{\arraystretch}{.5}
$\begin{array}{@{}c@{}}{#1}\\{#2}\end{array}{#3}$
\renewcommand{\arraystretch}{1}
}
\begin{document}
"""

blue=Color(.65,.65,1)
green=Color(.65,1,.65)

def BellDet(c=P(0,0)):

    H=P(0,.8)
    W=P(.5,0)

    D=Group(Path(c+H,
           C(c+H+W,c+H+W),
           c+W,
           C(c-H+W,c-H+W),
           c-H,bg=blue,
           ))

    return Group(
        Path(c-H,c+H,linewidth=2),
        D,
        TeX(r'$\mathcal{B}$',c=D.c)
        )

offline=Rectangle(height=4,width=5.5,e=P(3.5,1.5),
                  dash='[3 ] 0',bg=Color(.85))

render(
    offline,
    TeX('offline',nw=offline.nw+P(.1,-.1)),

    Path(P(5,0),P(-.3,0),P(-.6,.5),P(-.3,1),P(2,1)),
    Path(P(2,2),P(-.3,2),P(-.6,2.5),P(-.3,3),P(3.7,3)),
    Path(P(-1,4),P(3.7,4)),

    Dot(P(-.6,.5)),
    Dot(P(-.6,2.5)),

    classicalpath(Path(P(2.1,1.5),P(4.5,1.5),P(4.5,0)),
                  Path(P(3,1.5),P(3,0)),
                  Path(P(3.8,3.5),P(4.5,3.5),P(4.5,1.5)),
                  ),

    BellDet(P(2,1.5)),
    BellDet(P(3.7,3.5)),

    Boxed(TeX(r'$D\left(\frac{i\theta}{2\alpha^2}\right)$'),c=P(1,2),bg=green),

    Boxed(TeX('$X$'),c=P(3,0),bg=green),
    Boxed(TeX('$Z$'),c=P(4.5,0),bg=green),

    TeX(r'$\ket{B_{00}}$',e=P(-.7,.5)),
    TeX(r'$\ket{B_{00}}$',e=P(-.7,2.5)),
    TeX(r'$\ket{Q}$',e=P(-1.1,4)),

    file="tutorial.eps",
    )


