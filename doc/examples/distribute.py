#import sys
#sys.path.insert(0,"../")

from pyscript import *


defaults.units=UNITS['cm']

p1=P(-3,0)
p2=P(3,0)

o1=Rectangle(width=.5,height=1)
o2=Circle(r=.5)
o3=Rectangle(width=.5,height=.5)
o4=Rectangle(width=2,height=.5)

oc=Group(o1.copy(),o2.copy(),o3.copy()).apply(fg=Color('Red'))


render(
#    oc,
    Distribute(o1,o2,o3,o4,p1=p1,p2=p2,a1='c',a2='c',as='w',ae='e'),
    Path(p1,p2,fg=Color('red')),

    Dot(c=o1.c), Dot(c=o2.c), Dot(c=o3.c),Dot(c=o4.c),

    
    file="distribute.eps"
    )
