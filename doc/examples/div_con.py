#!/usr/bin/env pyscript

from pyscript import *
from pyscript.lib.qi import *

g1=Assemble(Gate(Boxed(TeX(r'$\mathcal{E}_1$'),height=1.5)),1.5,
        Gate(Boxed(TeX(r'$\mathcal{E}_2$'),height=1.5)),2.5,
        Gate(Boxed(TeX(r'$\mathcal{E}_3$'),height=1.5)),1.5,
        wires=[QWire,QWire,QWire],
        )

g21=Assemble(Gate(Boxed(TeX(r'$\mathcal{E}_1$'),height=1.5)),1.5,
        wires=[QWire,QWire,QWire],
        )
g22=Assemble(Gate(Boxed(TeX(r'$\mathcal{E}_2$'),height=1.5)),2.5,
        wires=[QWire,QWire,QWire],
        )
g23=Assemble(Gate(Boxed(TeX(r'$\mathcal{E}_3$'),height=1.5)),1.5,
        wires=[QWire,QWire,QWire],
        )

g31=Assemble(Gate(Boxed(TeX(r'$\mathcal{E}_1$'),height=1.5)),1.5,
        wires=[QWire,QWire],
        )
g32=Assemble(Gate(Boxed(TeX(r'$\mathcal{E}_2$'),height=1.5)),1.5,
        wires=[QWire,QWire],
        )
g33=Assemble(Gate(Boxed(TeX(r'$\mathcal{E}_3$'),height=1.5)),1.5,
        wires=[QWire,QWire],
        )

m1=TeX(r'\Large $\le$')
m2=TeX(r'\Large $+$')
m3=TeX(r'\Large $+$')
m4=TeX(r'\Large $=$')
m5=TeX(r'\Large $+$')
m6=TeX(r'\Large $+$')

Align(g1,m1,m2,m3,m4,m5,m6,g31,g32,g33, a1="e",a2="w",angle=90)

divnconk=Distribute(
        g1,
        m1,
        g21,m2,g22,
        m3,g23,
        m4,
        g31,m5,g32,m6,g33,
        a1="e",a2="w",p1=P(0,0),p2=P(15,0),
        )

t1=TeX(r'\Large (by chaining)',n=P(g22.s.x,divnconk.s.y-.2))
        
t2=TeX(r'\Large (by stability)',n=P(g32.s.x,divnconk.s.y-.2))

divnconk.append(t1,t2).scale(.7)

render(
        divnconk,
        file="div_con.eps"
        )

