from pyscript import *

def s(angle):
    "spacing"
    return U(angle)*.2

# define our own dot
def dot(c):
    return Circle(r=.1,bg=Color('red'),c=c)

acol=Color('blue')
axis=Group(
    Path(P(-1,0),P(4,0),fg=acol),
    Path(P(0,-1),P(0,4),fg=acol),
    Text('(0,0)',ne=s(-135),fg=acol)
    )

r=Rectangle(width=3,height=3,linewidth=2)

dots=Group()
for ii in ['n','ne','e','se','s','sw','w','nw','c']:
    p=getattr(r,ii)
    dots.append(dot(p))
    dots.append(Text(ii,sw=p+P(.2,.2)))
    
h=Text('height',s=U(-90,.4)+r.w)
render(
    axis,
    r,
    dots,
    Text('width',n=U(180,.4)+r.s),
    h.rotate(-90,h.s),
    
    file="fig_rectangle.eps",
    )
