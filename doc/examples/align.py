import sys
sys.path.insert(0,"../")

from pyscript import *

defaults.units=UNITS['cm']

r1=Rectangle(width=2,height=1,c=P(0,0))
r2=Rectangle(width=1,height=2,c=P(2,1))
c1=Circle(c=P(3,2))
c2=Circle(r=2,c=P(6,3))

# record where they started in red
orig=Group(r1.copy(fg=Color('Red')),
           r2.copy(fg=Color('Red')),
           c1.copy(fg=Color('Red')),
           c2.copy(fg=Color('Red')),
)

# now align them horiz. with 1cm e-w
#a=Align(r1,r2,c1,c2, a1="e",a2="w",space=1,angle=90,anchor=2)

a=Group(r1,r2,c1,c2)
Align(a,a1="e",a2="w",space=1,angle=90,anchor=2)

# this will align them horiz without changing their horiz. dist
#a=Align(r1,r2,c1,c2, a1="e",a2="w",space=None,angle=90)

render(
    orig,
    a,
    file="align.eps",
    )
    
