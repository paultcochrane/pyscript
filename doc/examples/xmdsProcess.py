#!/usr/bin/env pyscript

from pyscript import *
from pyscript.lib.presentation import Box_1,TeXBox

defaults.tex_head+=r"\newcommand{\xmds}{\textsc{xmds}\xspace}"

def Box(item, bg=Color('LightSteelBlue')*1.1):
    bg=bg
    fg=Color('black')*0.4
    border=1
    fixed_width=5
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
    bg=Color('OldLace')*1.1
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

def CodeBox(item):
    bg=Color('Orange')*1.3
    fg=Color('black')*0.4
    border=0.75
    fixed_width=2.5
    pad=0.2
    dogear=0.25
    gb=item.bbox()
    h = gb.height
    w = gb.width

    r=Group()
    r.append(Path(
        P(-pad,-pad),
        P(-pad,h+pad),
        P(w+pad,h+pad),
        P(w+pad,-pad+dogear),
        P(w+pad-dogear,-pad),
        P(w+pad-dogear,-pad+dogear),
        P(w+pad,-pad+dogear),
        P(w+pad-dogear,-pad),
        P(-pad,-pad),
        bg=bg,
        fg=fg,
        linewidth=border,
        miterlimit=1.0,
        )
             )
    r.append(item)
    return r

dist = 0.5
scale = 0.6

diag = Group()

diag.append(Align(
    Align(
    Rectangle(width=0.5,height=0.5,bg=Color('LightSteelBlue')*1.1),
    TeX(r'= Performed by \xmds'),
    a1="e", a2="w", angle=90, space=0.1).scale(scale,scale),
    Align(
    Rectangle(width=0.5,height=0.5,bg=Color('SandyBrown')*1.2),
    TeX(r'= Performed by simulation'),
    a1="e", a2="w", angle=90, space=0.1).scale(scale,scale),
    a1="sw", a2="nw", angle=180, space=0.1,
    ))

input = Box(
    Align(
    TeX(r"Input script"),
    CodeBox(
    TeX(r'''
    \noindent
    \texttt{<?xml version="1.0"?>}\\
    \texttt{<simulation>}\\
    \texttt{...}\\
    \texttt{</simulation>}
    ''').scale(0.5,0.5)
    ), a1="e", a2="w", angle=90, space=0.2,
    )
    )
input.n = diag.s - P(0,0.2)
diag.append(input)
diag.append(Arrow(diag.s,diag.s-P(0,dist)))

parser = Box(
    TeX(r"XML parser")
    )
parser.n = diag.s
diag.append(parser)
diag.append(Arrow(diag.s,diag.s-P(0,dist)))

kernel = Box(
    TeX(r"\xmds kernel")
    )
kernel.n = diag.s
diag.append(kernel)
diag.append(Arrow(diag.s,diag.s-P(0,dist)))

code = Box(
    Align(
    TeX(r"C/C++ code"),
    CodeBox(
    TeX(r'''
    \noindent
    \texttt{int main() \{}\\
    \texttt{...}\\
    \texttt{\}}
    ''').scale(0.5,0.5)
    ), a1="e", a2="w", angle=90, space=0.2,
    )
    )
code.n = diag.s
diag.append(code)
diag.append(Arrow(diag.s,diag.s-P(0,dist)))

compile = Box(
    TeX(r"Compile")
    )
compile.n = diag.s
diag.append(compile)
diag.append(Arrow(diag.s,diag.s-P(0,dist)))

run = Box(
    TeX(r"Run simulation"), bg=Color('SandyBrown')*1.2,
    )
run.n = diag.s
diag.append(run)
diag.append(Arrow(diag.s,diag.s-P(0,dist)))

output = Box(
    Align(
    TeX(r"Output"),
    CodeBox(
    TeX(r'''
    \noindent
    \texttt{<?xml version="1.0"?>}\\
    \texttt{<xsil>}\\
    \texttt{...}\\
    \texttt{</xsil>}
    ''').scale(0.5,0.5)
    ), a1="e", a2="w", angle=90, space=0.2,
    ), bg=Color('SandyBrown')*1.2,
    )
output.n = diag.s
diag.append(output)

# draw it!
print "Rendering picture..."
render(
    diag,
    file="xmdsProcess.eps",
    )

