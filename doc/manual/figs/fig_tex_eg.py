from pyscript import *

tex=TeX(r'$|\psi_t\rangle=e^{-iHt/\hbar}|\psi_0\rangle$',w=P(.5,0))

g=Group()
for ii in range(0,360,60):
    g.append(tex.copy().rotate(ii,P(0,0)))

render(g,file="fig_tex_eg.eps")
