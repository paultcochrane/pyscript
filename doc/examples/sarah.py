from pyscript import *
from math import *

defaults.units=UNITS['cm']

def arrow(s,e,**dict):
    # don't yet have an arrow object so define one here
    gap=.05

    d=e-s
    length=d.length
    theta=-atan2(e[1]-s[1],e[0]-s[0])/pi*180

    dict['bg']=Color(0)

    p00=P(0,0)
    dh=.05
    dl=.2
    ah2=apply(Path,(p00,P(-dl,-dh),P(-dl,dh),p00),dict)

    ah2.move(length,0)

    g=Group(
        apply(Path,(P(0,0),P(length,0)),dict),
        ah2,
        )
    g.rotate(theta)
    g.move(s[0],s[1])

    return g

render(
    arrow(P(0,0),P(0,4)),
    arrow(P(0,0),P(5,0)),
    Path(P(2,3.8),P(2,0),dash='[ 2] 0',fg=Color(.5)),

    Path(P(.5,2),P(2,2),linewidth=1),
    Path(P(4,3.7),
         C(P(3,3.5),P(2,3)),
         P(2,2),
         C(P(2,1),P(3,.5)),
         P(4,.3),linewidth=1),
    Path(P(2,2),P(4,2),dash='[ 3] 0',linewidth=1),

    TeX(r'$\bar{\lambda}_c$',n=P(2,-.1)),

    TeX(r'$\bar{\lambda}$',ne=P(4.8,-.1)),
    
    file="sarah.eps",
    )
