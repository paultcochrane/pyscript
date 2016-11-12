#!/usr/bin/env pyscript
# $Id$

from pyscript import *
from pyscript.lib.presentation import Box_1,TeXBox

def Box(item):
    bg=Color('LightSteelBlue')*1.1
    fg=Color('black')*0.4
    border=1
    fixed_width=4.5
    pad=.2
    gb=item.bbox()

    r=Group()
    r.append(Rectangle(n=gb.n+P(0,pad),
                width=fixed_width,
                height=gb.height+2*pad,
                bg=bg,
                fg=fg,
                linewidth=border,
                )
             )
    r.append(item)
    return r

def RoundedBox(item):
    bg=Color('LawnGreen')*1.1
    fg=Color('black')*0.4
    border=1
    fixed_width=2.5
    pad=.2
    gb=item.bbox()

    h = gb.height+2*pad
    w = fixed_width

    r=Group(Path(P(0,0),
                 C(P(-0.5,0),P(-0.5,h)),
                 P(0,h),
                 P(w,h),
                 C(P(w+0.5,h),P(w+0.5,0)),                 
                 P(w,0),
                 P(0,0),
                 linewidth=border, fg=fg, bg=bg))
    item.c = r.c
    return Group(r,item)

def DecisionBox(item):
    bg=Color('Orange')*1.3
    fg=Color('black')*0.4
    border=1
    fixed_width=2.1
    pad=.2
    gb=item.bbox()

    h = fixed_width  # gb.width+2*pad
    w = fixed_width  # h

    r=Group(Path(P(0,0),
                 P(-w/2.0,h/2.0),
                 P(0,h),
                 P(w/2.0,h/2.0),
                 P(0,0),
                 linewidth=border, fg=fg, bg=bg))
    item.c = r.c
    return Group(r,item)


dist = 0.5

begin = RoundedBox(
    TeX(r"Begin Simulation")
    )

init = Box(
    TeX(r"Initialise segments \texttt{1..n}")
    )
init.n = begin.s - P(0,dist)

process = Box(
    TeX(r"Process segment \texttt{i}")
    )
process.n = init.s - P(0,dist)

sample = Box(
    TeX(r"Sample segment \texttt{i}")
    )
sample.n = process.s - P(0,dist)

postprocess = Box(
    TeX(r"Post-process")
    )
postprocess.n = sample.s - P(0,dist)

finished = Group(DecisionBox(
    TeX(r"Finished?")
    ))
finished.n = postprocess.s - P(0,dist)

finishedY = Text("Y")
finishedY.c = finished.s + P(0.25,-0.2)
finishedN = Text("N")
finishedN.c = finished.e + P(0.2,0.25)

ipp = TeX(r"\texttt{i++}")
ipp.nw = finished.e + P(0.7,-0.15)

means_etc = Box(
    TeX(r"Compute means \& std dev")
    )
means_etc.n = finished.s - P(0,dist)

halfstep = Group(DecisionBox(
    TeX(r"Do $\frac{1}{2}$ step?")
    ))
halfstep.n = means_etc.s - P(0,dist)

halfstepN = Text("N")
halfstepN.c = halfstep.s + P(0.25,-0.2)
halfstepY = Text("Y")
halfstepY.c = halfstep.w - P(0.2,-0.25)

error = Box(
    TeX(r"Compute step error")
    )
error.n = halfstep.s - P(0,dist)

output = Box(
    TeX(r"Write output")
    )
output.n = error.s - P(0,dist)

end = RoundedBox(
    TeX(r"End Simulation")
    )
end.n = output.s - P(0,dist)

arrows = Group(
    Arrow(begin.s,init.n),
    Arrow(init.s,process.n),
    Arrow(process.s,sample.n),
    Arrow(sample.s,postprocess.n),
    Arrow(postprocess.s,finished.n),
    Arrow(finished.s,means_etc.n),
    Arrow(means_etc.s,halfstep.n),
    Arrow(halfstep.s,error.n),
    Arrow(error.s,output.n),
    Arrow(output.s,end.n),
    )

arrowFinishedNo = Group(
    Path(finished.e,
         finished.e+P(process.width/2.0-finished.width/2.0+0.5,0),
         process.e+P(0.5,0)),
    Arrow(process.e+P(0.5,0),process.e),
    )

arrowHalfstepYes = Group(
    Path(halfstep.w,
         halfstep.w-P(init.width/2.0-halfstep.width/2.0+0.5,0),
         init.w-P(0.5,0)),
    Arrow(init.w-P(0.5,0),init.w),
    )

diag = Group(
    begin,
    init,
    process,
    sample,
    postprocess,
    finished,
    finishedY,finishedN,ipp,
    means_etc,
    halfstep,
    halfstepY,halfstepN,
    error,
    output,
    end,
    arrows,
    arrowFinishedNo,
    arrowHalfstepYes,
    )

# draw it!
print "Rendering picture..."
render(
    diag,
    file="xmdsFunctionality.eps",
    )

