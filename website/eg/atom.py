from pyscript import *

defaults.units=UNITS['cm']

defaults.tex_head=r"""
\documentclass{article}
\pagestyle{empty}

\newcommand{\ket}[1]{\mbox{$|#1\rangle$}}
\newcommand{\bra}[1]{\mbox{$\langle #1|$}}
\newcommand{\braket}[2]{\mbox{$\langle #1|#2\rangle$}}
\newcommand{\ketbra}[2]{\mbox{|#1$\rangle\langle #2|$}}
\newcommand{\op}[1]{\mbox{\boldmath $\hat{#1}$}}
\begin{document}
"""

def level(x,y,label,**dict):

    w=1
    label.w=P(x+w/2.,y)

    return Group(
        apply(Path,(P(x-w/2.,y),P(x+w/2.,y)),dict),
        label,
        )

from math import atan2

def darrow(s,e,label,**dict):
    # don't yet have an arrow object ...

    gap=.05

    d=e-s
    length=d.length
    theta=-atan2(e[1]-s[1],e[0]-s[0])/pi*180
    label.s=P(length/2.,gap)

    p00=P(0,0)
    dh=.05
    dl=.2
    ah1=apply(Path,(p00,P(dl,dh),P(dl,-dh),p00),dict)
    ah2=apply(Path,(p00,P(-dl,-dh),P(-dl,dh),p00),dict)

    ah2.move(length,0)

    g=Group(
        apply(Path,(P(0,0),P(length,0)),dict),
        ah1,ah2,
        label,
        )
    g.rotate(theta)
    g.move(s[0],s[1])

    return g

render(
    
    level(0,0,TeX("$\ket{1}\equiv\ket{g}$")),
    level(2,0.3,TeX("$\ket{2}\equiv\ket{e}$")),
    level(.5,2,TeX("\ket{3}")),
    level(2.5,2.5,TeX("\ket{4}")),
    
    Path(P(0,1.7),P(1,1.7),dash='[2]0'),
    TeX(r'$\Delta\left\{\rule{0cm}{2.75mm}\right.$')(e=P(0,1.85)),

    darrow(P(0,0),P(.3,1.7),TeX('\small signal'),fg=Color('green'),bg=Color('green')),

    darrow(P(.6,1.7),P(1.8,.3),TeX('\small activation'),fg=Color('red'),bg=Color('red')),

    darrow(P(2.2,.3),P(2.5,2.5),TeX('\small read out'),fg=Color('blue'),bg=Color('blue')),

    file="atom.eps",
    )

