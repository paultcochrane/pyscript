from pyscript import *

r=Rectangle(width=2,height=2)
g=Group()

for a in [0,20,40]:
    p=P(a/7.,0)
    r2=r.copy(c=p).rotate(a,p)
    g.append(r2,Dot(r2.bbox().nw))

render(
    g,
    file="fig_position_eg2.eps",
    )
