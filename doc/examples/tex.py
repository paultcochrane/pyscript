from pyscript import *

defaults.units=UNITS['cm']

tex=TeX(r'$|\psi_t\rangle=e^{-iHt/\hbar}|\psi_0\rangle$',w=P(.5,0),fg=Color(1))

g=Group()
for ii in range(0,360,60):
    g.append(tex.copy().rotate(ii,P(0,0)))

render(Circle(r=.6+tex.width,bg=Color('midnightblue')),g,
       Circle(r=.4,bg=Color(1))
       ,file="tex.eps")

