from pyscript import *

# define our own dot
def dot(c):
    return Circle(r=.1,bg=Color('red'),c=c)

def s(angle):
    return U(angle)*.2

acol=Color('blue')
axis=Group(
    Path(P(-1,0),P(4,0),fg=acol),
    Path(P(0,-1),P(0,4),fg=acol),
    Text('(0,0)',ne=s(-135),fg=acol)
    )

# -----------------------------------------------------

r=Circle(r=3,linewidth=2)

dots=Group()
for ii in ['n','ne','e','se','s','sw','w','nw','c']:
    p=getattr(r,ii)
    dots.append(dot(p))
    dots.append(Text(str(ii),c=p-p/8.))

rad=Group(Path(P(0,0),P(0,3))).rotate(60)
radt=Text('r')
    
render(
    axis,
    r,
    dots,
    rad,
    radt.rotate(-30)(s=rad.c+U(-30,.2)),
    file="fig_circle.eps",
    )
