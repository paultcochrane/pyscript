#!/usr/bin/env python

from pyscript import *
from pyscript.lib.qi import *

g=Assemble(
        SWAP,1,2,
        NOT,2,1,
        H,1,
        X,3,2,
        Z,3,1,
        hang=.5,
        wires=[QWire,QWire,QWire],
        )

w=g.wires

render(
        g,
        TeX(r'$|\psi\rangle$',e=w[0].w),
        TeX(r'$|\psi\rangle$',w=w[2].e),
        TeX(r'$|\beta_{00}\rangle\left\{\rule{0cm}{7mm}\right.$',
            e=(w[2].w+w[1].w)/2.),
        Meter(w=w[0].e),
        Meter(w=w[1].e),
        file="teleport.eps"
        )
