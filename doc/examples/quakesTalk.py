from pyscript.lib.presentation import *

# define_bullet(level=1,...)
# define_heading(level=1,...)
# define_title()

# now wrap this stuff into a style and biff into ~/.pyscript/styles dir

defaults.tex_head+=r"\newcommand{\xmds}{\texttt{xmds}\xspace}"
defaults.tex_head+=r"\newcommand{\pyscript}{\textsf{PyScript}\xspace}"

abstract = r"""
Research science, and in particular computational science, benefits
greatly from advances in the software tools used in doing scientific
work.  In this talk I shall give an introduction to two software tools
which aid the scientist in their work: xmds and PyScript.

xmds is a code generator that integrates equations.  One writes them
down in human readable form in an XML file, and it goes away and
writes and compiles a C++ program that integrates those equations as
quickly as possible on your architecture.  xmds is a tool for carrying
out the initial phase of research; it models the system of interest
and generates results for further analysis and interpretation.  xmds
reduces code development time while maintaining fast execution of
simulations.

PyScript is a Python module for producing high quality postscript
drawings.  Rather than use a GUI to draw a picture, the picture is
programmed using Python and the PyScript objects.  This package
therefore comes at the end of the scientific process, for when the
research results are to be presented to the scientific community.
PyScript can be used to produce high quality figures and diagrams for
journal articles, and posters and seminars for conference
presentations.

Both of these tools allow the scientist to spend more time focussing
on the science, rather than on the 'donkey-work' of generating and
presenting the results.
"""

talk = Talk()
talk.title = r"""
\begin{center}
Software tools for research science:\\
{\small \xmds and \pyscript}
\end{center}
"""
talk.authors = r"\underline{Paul Cochrane}"
talk.speaker = r"Paul Cochrane"
talk.speaker_textstyle = r"\sf"

talk.address = r"""
\begin{center}
Australian Centre for Quantum-Atom Optics, Physics Dept.,\\
University of Queensland, Australia
\end{center}
"""

talk.title_fg = Color('white')
talk.title_bg = Color('white')
talk.title_textstyle = r"\bf\sf"

talk.address_fg = Color('white')
talk.address_textstyle = r"\sf"

talk.authors_fg = Color('white')
talk.authors_textstyle = r"\sf"

talk.slide_title_fg = Color('lightgray')
talk.slide_title_textstyle = r"\bf"

talk.headings_fgs[1] = Color('white')
talk.headings_textstyle[1] = r"\sf"
talk.headings_bullets[1] = Epsf(file="redbullet.eps").scale(0.2,0.2)

talk.headings_fgs[2] = Color('white')
talk.headings_textstyle[2] = r"\sf"
talk.headings_bullets[2] = Epsf(file="greenbullet.eps").scale(0.15,0.15)

talk.headings_fgs[3] = Color('white')
talk.headings_textstyle[3] = r"\sf"
talk.headings_bullets[3] = Epsf(file="yellowbullet.eps").scale(0.1,0.1)

# start of the slides

# titlepage
titlepage = Slide(talk)
titlepage.titlepage = True  # only call this for the first page

# introduction
intro = Slide(talk)
intro.title = r"Introduction"
intro.add_heading(1,r"Software tools in research science")
intro.add_heading(1,r"\xmds: the eXtensible Multi-Dimensional Simulator")
intro.add_heading(2,r"what is \xmds?")
intro.add_heading(2,r"who uses it?")
intro.add_heading(2,r"why is it useful?")
intro.add_heading(2,r"examples")
intro.add_heading(1,r"\pyscript: Postscript graphics in Python")
intro.add_heading(2,r"\pyscript overview")
intro.add_heading(2,r"uses of \pyscript")
intro.add_heading(2,r"examples")
intro.add_heading(1,r"Conclusion")

# software tools in research science
tools = Slide(talk)
tools.title = r"Software tools in research science"
tools.add_heading(1,r"Three general phases of research")
tools.add_heading(2,r"doing the work and getting the results")
tools.add_heading(3,r"e.g. \xmds, C, Fortran, Python, Matlab, \ldots")
tools.add_heading(2,r"visualising and interpreting the data")
tools.add_heading(3,r"e.g. Matlab, Scilab, Gnuplot, \ldots")
tools.add_heading(2,r"presenting the results, and interpretation to the scientific\\ community")
tools.add_heading(3,r"e.g. \pyscript, \LaTeX, PowerPoint, \ldots")
tools.add_heading(1,r"Developing tools for doing research\\ facilitates more effective research")  # enabling technology
tools.add_heading(1,
                  r"""
                  Make scientists' life easier so they can focus
                  on science, and not the ``donkey-work''
                  """)

# xmds logo
xmds_logo = Slide(talk)
xmds_logo.add_fig(Epsf(file="xmds_logo.eps").scale(2.5,2.5),bg=None,c=xmds_logo.area.c)

# what is xmds?
xmds_what = Slide(talk)
xmds_what.title = r"What is \xmds?"
xmds_what.add_heading(1,r"eXtensible Multi-Dimensional Simulator")
xmds_what.add_heading(2,r"any number of components")
xmds_what.add_heading(2,r"any number of dimensions")
xmds_what.add_heading(2,r"any number of random variables")
xmds_what.add_heading(1,r"A system for integrating differential equations:")
xmds_what.add_heading(2,r"one writes a high-level description of simulation in XML")
xmds_what.add_heading(2,r"\xmds converts the XML into C language code")
xmds_what.add_heading(2,
                      r"""the C code is compiled into a binary executable, which runs about as fast
                      as code hand-written by an expert
                      """)
xmds_what.add_heading(1,r"\xmds provides a way of both performing and\\ documenting a simulation")

# xmds: who uses it?
xmds_who = Slide(talk)
xmds_who.title = r"\xmds: who uses it?"
xmds_who.add_heading(1,r"Anyone who models systems via differential equations")
xmds_who.add_heading(1,r"This includes:")
xmds_who.add_heading(2,r"physicists")
xmds_who.add_heading(2,r"geophysicists and earth scientists")
xmds_who.add_heading(2,r"chemists")
xmds_who.add_heading(2,r"biologists")
xmds_who.add_heading(2,r"weather forecasters")
xmds_who.add_heading(2,r"economists")
xmds_who.add_heading(2,r"risk analysts")
xmds_who.add_heading(2,r"\ldots")

# xmds: why use it?
xmds_why = Slide(talk)
xmds_why.title = r"Why use \xmds?"
xmds_why.add_heading(2,r"fast development time, and fast execution time")
xmds_why.add_heading(2,r"reduces user-introduced bugs")
xmds_why.add_heading(2,r"solves ODEs, PDEs, and stochastic ODEs and PDEs")
xmds_why.add_heading(2,r"automatic parallelisation of stochastic and deterministic problems")
xmds_why.add_heading(2,r"allows simple and transparent comparison of simulations with other researchers")
#xmds_why.add_heading(2,r"the script documents the simulation")
xmds_why.add_heading(2,
                     r"""simulation script (and therefore parameters) are output with the
                     simulation data, so the data and the variables that generated it are
                     kept together for future reference""")
xmds_why.add_heading(2,
                     r"""open source and documentation, see
                     \texttt{http://www.xmds.org/}""")

# xmds details
xmds_details = Slide(talk)
xmds_details.title = r"\xmds details"
xmds_details.add_heading(1,r"\xmds is designed to integrate PDEs of the general form:")
xmds_details.add_heading("equation",
                         r"""
                         \begin{align}
                         \frac{\partial}{\partial x^0}\vect{a}(\vect{x}) & =
                         \vect{\mathcal{N}}\left(\vect{x}, \vect{a}(\vect{x}), \vect{p}(\vect{x}),
                         \vect{b}(\vect{x}),\;\vect{\xi}(\vect{x})\right),\nonumber\\ 
                         p^i(\vect{x}) & = \mathcal{F}^{-1}\left[\Sigma_j
                         \mathcal{L}^{ij}\left(x^0,\vect{k_\bot}\right)
                         \mathcal{F}\left[a^j(\vect{x})\right]\right],\nonumber\\
                         \frac{\partial}{\partial x^{c}}\vect{b}(\vect{x}) & =
                         \vect{\mathcal{H}}\left(\vect{x}, \vect{a}(\vect{x}), 
                         \vect{b}(\vect{x})\right)\nonumber
                         \end{align}
                         """)
xmds_details.add_heading(2,r"$\vect{x}$ : spatial dimension")
xmds_details.add_heading(2,r"$\vect{a}(\vect{x})$ : main field")
xmds_details.add_heading(2,r"$\vect{b}(\vect{x})$ : cross-propagating field")
xmds_details.add_heading(2,r"$\vect{p}(\vect{x})$ : field defined in Fourier space")
xmds_details.add_heading(2,r"$\xi(\vect{x})$ : noise terms")

# xmds processes
xmds_processes = Slide(talk)
xmds_processes.title = r"\xmds processes"
xmds_processes.add_fig(Epsf(file="xmdsProcess.eps").scale(1.5,1.5),
                       c=xmds_processes.area.c+P(-5,0))
xmds_processes.add_fig(Epsf(file="xmdsFunctionality.eps").scale(1.25,1.25),
                       c=xmds_processes.area.c+P(5,))

# xmds examples
xmds_eg = Slide(talk)
xmds_eg.title = r"\xmds examples"
xmds_eg.add_heading(1,r"Nonlinear Schr\"odinger Equation")
# turn this into add_equation someday...
xmds_eg.add_heading("equation", r"""
        \begin{equation}
        \frac{\partial \phi}{\partial z } = i\left[\frac{1}{2} \frac{\partial ^{2}
        \phi}{\partial t ^{2}} + |\phi|^{2} \phi + i \Gamma (t) \phi
        \right]\nonumber
        \end{equation}
        """)
xmds_eg.add_heading(3,
                    r"""where $\phi$ is the field, $z$ is the spatial dimension,
                    $t$ is time and $\Gamma(t)$ is a damping term.""")
xmds_eg.add_epsf(file="nlse.eps",width=15,c=xmds_eg.area.c+P(0,-4.5))

# xmds demonstration
xmds_demo = Slide(talk)
xmds_demo.title = r"\xmds demonstration"
xmds_demo.add_heading(1,r"Nonlinear Schr\"odinger Equation")
xmds_demo.add_heading(2,r"You've seen the equation, you've seen the results,\\ now see \xmds in action")

# nlse.xmds

# fibre optic field
xmds_eg2 = Slide(talk)
xmds_eg2.title = r"\xmds examples (cont.)"
xmds_eg2.add_heading(1,r"Fibre Optic Laser Field")
xmds_eg2.add_heading("equation", r"""
        \begin{equation}
        \frac{\partial \phi}{\partial t} = -i \frac{\partial^{2}
        \phi}{\partial x^{2}} - \gamma \phi + \frac{\beta}{\sqrt{2}}
        \left[\xi_1(x,t) + i\xi_2(x,t)\right]\nonumber
        \end{equation}
        """)
xmds_eg2.add_heading(2,r"this is a stochastic simulation")
xmds_eg2.add_epsf(file="fibre1.eps", width=12, n=xmds_eg2.area.n+P(-6.7, -9))
xmds_eg2.add_epsf(file="fibre2.eps", width=12, n=xmds_eg2.area.n+P(6.7, -9))
xmds_eg2.add_fig(TeX(r"single path",fg=Color('white')).scale(2,2),
                 bg=None,
                 s=xmds_eg2.area.s+P(-6.7,1.7))
xmds_eg2.add_fig(TeX(r"1024 path mean",fg=Color('white')).scale(2,2),
                 bg=None,
                 s=xmds_eg2.area.s+P(6.7,1.7))

# xmds features
xmds_features = Slide(talk)
xmds_features.title = r"Bestiary of \xmds features"
xmds_features.add_heading(2,r"Automatic numerical error checking")
xmds_features.add_heading(2,r"Automatic parallelisation of stochastic and deterministic problems")
xmds_features.add_heading(2,r"Handles cross-propagating fields")
xmds_features.add_heading(2,r"Calculates trajectory means and variances of stochastic simulations")
xmds_features.add_heading(2,r"ASCII and binary output")
xmds_features.add_heading(2,r"Benchmarking of simulations")
xmds_features.add_heading(2,r"\xmds script template output")
xmds_features.add_heading(2,r"Field initialisation from file")
xmds_features.add_heading(2,r"Command line arguments to simulations")
xmds_features.add_heading(2,r"User-defined preferences (for custom compiler flags etc.)")
xmds_features.add_heading(2,r"\ldots")

# pyscript logo
pyscript_logo = Slide(talk)
pyscript_logo.add_fig(Epsf(file="logo.eps").scale(2,2),c=pyscript_logo.area.c)

# what is pyscript?
pyscript_what = Slide(talk)
pyscript_what.title = r"What is \pyscript?"
pyscript_what.add_heading(1,
                          r"""
                          Generate Postscript figures/diagrams/documents using the Python
                          programming language
                          """)
pyscript_what.add_heading(1,r"Instead of using a mouse to draw objects, write code to draw objects")
 # not a new idea, eg ps, but python more accessible
pyscript_what.add_heading(1,r"Have full use of the Python language and modules")
pyscript_what.add_heading(1,r"Produces small file-size, high-quality Postscript output")
pyscript_what.add_heading(1,r"Uses \LaTeX{} to produce high quality fonts")
pyscript_what.add_heading(1,r"Free software, released under the GPL")
pyscript_what.add_heading(1,r"\texttt{http://pyscript.sourceforge.net}")

# pyscript uses
pyscript_use = Slide(talk)
pyscript_use.title = r"The uses and features of \pyscript"
pyscript_use.add_heading(1,r"\pyscript uses:")
pyscript_use.add_heading(2,r"figures and diagrams in journal articles")
pyscript_use.add_heading(2,r"posters and seminars for conferences")
pyscript_use.add_heading(2,r"amaze your colleauges with the size of your Postscript files")
pyscript_use.add_heading(1,r"\pyscript features:")
pyscript_use.add_heading(2,r"scaling, rotating, translating, any affine transformation")
pyscript_use.add_heading(2,r"embed EPS graphics")
pyscript_use.add_heading(2,r"embed \LaTeX{} graphics and symbols")
pyscript_use.add_heading(2,r"properly kerned text objects")
pyscript_use.add_heading(2,r"scriptable and accurate control of object location")
pyscript_use.add_heading(2,r"expanding suite of libraries for common objects and tasks")

# pyscript examples
pyscript_eg = Slide(talk)
pyscript_eg.title = r"\pyscript examples"
pyscript_eg.add_fig(TeX(r"""
\begin{verbatim}
from pyscript import *

tex=TeX(r'$|\psi_t\rangle=e^{-iHt/\hbar}|\psi_0\rangle$',w=P(.5,0))

g=Group()
for ii in range(0,360,60):
    g.append(tex.copy().rotate(ii,P(0,0)))

render(g,file=...)
\end{verbatim}
""").scale(1.1,1.1),w=pyscript_eg.area.w+P(1,0))
pyscript_eg.add_fig(Epsf(file="fig_tex_eg.eps").scale(1.8,1.8),c=pyscript_eg.area.c+P(6.5,0))

# another example
pyscript_eg2 = Slide(talk)
pyscript_eg2.title = r"\pyscript examples (cont.)"
pyscript_eg2.add_fig(TeX(r"""
\begin{verbatim}
from pyscript import *

p0=P(2,1)
p1=P(4,2)
c1=R(4,2)
c2=R(-4,-2)/2.
p2=P(4,4)
p3=P(6,5)

path=Path(p0,p1,C(c1,c2),p2,p3,fg=Color('red'),linewidth=.8)

g=Group()
delta=1/20.
for p in range(21):
    g.append(Dot(path.P(p*delta)))

render(path,g,file=...)
\end{verbatim}
"""),w=pyscript_eg2.area.w+P(2,0))
pyscript_eg2.add_fig(Epsf(file="fig_path_eg.eps").scale(2,2),c=pyscript_eg2.area.c+P(6,0))

# and another
pyscript_eg3 = Slide(talk)
pyscript_eg3.title = r"\pyscript examples (cont.)"
pyscript_eg3.add_fig(TeX(r"""
\begin{verbatim}
offline=Rectangle(height=4,width=5.5,e=P(3.5,1.5),
                  dash='[3 ] 0',bg=Color(.85))

render(
    offline,
    TeX('offline',nw=offline.nw+P(.1,-.1)),

    Path(P(5,0),P(-.3,0),P(-.6,.5),P(-.3,1),P(2,1)),
    Path(P(2,2),P(-.3,2),P(-.6,2.5),P(-.3,3),P(3.7,3)),
    Path(P(-1,4),P(3.7,4)),

    Dot(P(-.6,.5)),
    Dot(P(-.6,2.5)),

    classicalpath(Path(P(2.1,1.5),P(4.5,1.5),P(4.5,0)),
                  Path(P(3,1.5),P(3,0)),
                  Path(P(3.8,3.5),P(4.5,3.5),P(4.5,1.5)),
                  ),

    BellDet(P(2,1.5)),
    BellDet(P(3.7,3.5)),

    Boxed(TeX(r'$D\left(\frac{i\theta}{2\alpha^2}\right)$'),
              c=P(1,2),bg=green),

    Boxed(TeX('$X$'),c=P(3,0),bg=green),
    Boxed(TeX('$Z$'),c=P(4.5,0),bg=green),

    TeX(r'$\ket{B_{00}}$',e=P(-.7,.5)),
    TeX(r'$\ket{B_{00}}$',e=P(-.7,2.5)),
    TeX(r'$\ket{Q}$',e=P(-1.1,4)),

    file=...,
    )
\end{verbatim}
"""),w=pyscript_eg3.area.w+P(1,0))
pyscript_eg3.add_fig(Epsf(file="tutorial.eps").scale(1.8,1.8),c=pyscript_eg3.area.c+P(5,0))
pyscript_eg3.add_fig(TeX(r"(18K---try doing that in Illustrator)",fg=Color('white')).scale(2,2),
                     bg=None,c=pyscript_eg3.area.c+P(5,-6))

# pyscript logo
pyscript_eg4 = Slide(talk)
pyscript_eg4.title = r"\pyscript examples (cont.)"
pyscript_eg4.add_fig(Epsf(file="logo.eps").scale(2,2),c=pyscript_eg4.area.c)

# conclusion
conclusion = Slide(talk)
conclusion.title = r"Conclusion"
conclusion.add_heading(1,r"\xmds and \pyscript are:")
conclusion.add_heading(2,r"two software tools to aid research science")
conclusion.add_heading(2,r"enabling technologies")
conclusion.add_heading(2,r"able to let scientists focus on science")
conclusion.add_heading(1,r"\xmds will solve your problems quickly")
conclusion.add_heading(1,r"\pyscript will make the results look good")


# acknowledgements
thanks = Slide(talk)
thanks.title = r"Acknowledgements"
thanks.add_heading(1,r"\xmds (\texttt{http://www.xmds.org})")
thanks.add_heading(2,r"Greg Collecutt, Peter Drummond, Joe Hope")
thanks.add_heading(1,r"\pyscript (\texttt{http://pyscript.sourceforge.net})")
thanks.add_heading(2,r"Alexei Gilchrist")

# building software tools for scientists, in much the same vein
# as more physical tools (such as measurement apparatus),
# stuff like that

# doing the research, and making the results
# visualising the data
# presenting the research and results to the community

# draw it!
talk.make(
    titlepage,
    intro,
    tools,
    xmds_logo,
    xmds_what,
    xmds_who,
    xmds_why,
    xmds_details,
    xmds_processes,
    xmds_eg,
    xmds_demo,
    xmds_eg2,
    xmds_features,
    pyscript_logo,
    pyscript_what,
    pyscript_use,
    pyscript_eg,
    #pyscript_eg2,
    pyscript_eg3,
    pyscript_eg4,
    conclusion,
    thanks,
    file="quakesTalk.ps",
    )

