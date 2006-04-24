from pyscript.lib.presentation import Poster_1,Box_1,TeXBox,CodeBox

defaults.tex_head+=r"\newcommand{\xmds}{\textsc{xmds}\xspace}"

def add_fig(fname,width=5.0):
    
    fig = Epsf(fname)
    rect1 = Rectangle(c=fig.c,
	    width=fig.bbox().width+0.1,
	    height=fig.bbox().height+0.1,
	    fg=Color('black'),
	    bg=Color('white'),
	    linewidth=0.5,
	    )
    out_fig = Group(rect1,fig)
    out_fig.scale(width/out_fig.bbox().width,width/out_fig.bbox().width)
    return out_fig

def CodeBox_1(item):
    # bg=Color('Plum')*1.3
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

class Box(Box_1):
    fg=Color('black')*.4
    bg=Color('LightGoldenRod')*1.1
    border=1
    pad=.2
    fixed_width = 9.9

class Title(TeXBox):
    tex_scale=1.1
    fg=Color('orangered')*0.95
    align='n'
    fixed_width = 9.4
    text_style=r"\sf"

class Poster(Poster_1):

    abstract_fg = Color('gold')*1.1
    abstract_scale = 0.8
    abstract_width = 0.92
    
    authors_fg = Color('yellow')
    
    address_fg = Color('yellow')
    address_scale = 0.9

    title_fg = Color('yellow')*2
    title_scale = 1.4
    
    bg = Color('royalblue')*0.8

    signature_fg = Color('white') # bg*2.0

    logo_height = 1.2
    logos=("ARC_COE_crop.eps","uq_logo_new.eps")

    title=r'''
    \large \sf \xmds: the eXtensible Multi-Dimensional Simulator
    '''
#\includegraphics[width=3cm]{xmdslogo.eps}

    address=r"""
	\sf Australian Centre for Quantum-Atom Optics, Physics Department,
	The University of Queensland, Brisbane, Australia
	"""

    authors=r'''
	\sf \underline{Paul~T.~Cochrane}, G.~Collecutt, P.~D.~Drummond, and J.~J.~Hope
	'''

    abstract=r'''{\em 
    Writing codes for the simulation of complex phenomena is an art and
    science unto itself.  What with finding and using good algorithms,
    actually writing the code, debugging the code and testing the code,
    not much time is left to actually investigate what it was you were
    initially out to look at.  This is where \xmds comes in.  \xmds allows
    you to write a high-level description of the problem you are
    trying to solve (usually a differential equation of some form) it goes
    away and writes low-level simulation code for you (trying hard to
    keep the code as efficient as possible), compiles and presents it,
    ready to be run.
    }'''

    references=r'''
\renewcommand*{\refname}{ }
\begin{thebibliography}{14}
\expandafter\ifx\csname natexlab\endcsname\relax\def\natexlab#1{#1}\fi
\expandafter\ifx\csname bibnamefont\endcsname\relax
  \def\bibnamefont#1{#1}\fi
\expandafter\ifx\csname bibfnamefont\endcsname\relax
  \def\bibfnamefont#1{#1}\fi
\expandafter\ifx\csname citenamefont\endcsname\relax
  \def\citenamefont#1{#1}\fi
\expandafter\ifx\csname url\endcsname\relax
  \def\url#1{\texttt{#1}}\fi
\expandafter\ifx\csname urlprefix\endcsname\relax\def\urlprefix{URL }\fi
\providecommand{\bibinfo}[2]{#2}
\providecommand{\eprint}[2][]{\url{#2}}

\setlength{\itemsep}{-2mm}

\bibitem{Ceperley:1999:1}
\bibinfo{author}{\bibfnamefont{D.~M.} \bibnamefont{Ceperley}},
  \bibinfo{journal}{Rev. Mod. Phys.} \textbf{\bibinfo{volume}{71}},
  \bibinfo{pages}{438} (\bibinfo{year}{1999}).

\bibitem{Drummond:1983:1}
\bibinfo{author}{\bibfnamefont{P.~D.} \bibnamefont{Drummond}},
  \bibinfo{journal}{Comp. Phys. Comm.} \textbf{\bibinfo{volume}{29}},
  \bibinfo{pages}{211} (\bibinfo{year}{1983}).

\bibitem{xmdsweb}
\emph{\bibinfo{title}{\xmds home page}},
  \urlprefix\url{http://www.xmds.org}.

\bibitem{fftwweb}
\emph{\bibinfo{title}{FFTW home page}},
  \urlprefix\url{http://www.fftw.org}.

\end{thebibliography}
        '''    

    col1=Group(
        Box(
        Title(r'What is \xmds?'),
        TeXBox(r"""
        \begin{itemize}
        \setlength{\itemsep}{-1mm}
        \item \xmds = e\underline{X}tensible \underline{M}ulti-\underline{D}imensional \underline{S}imulator
        \item \xmds is open source software; released under the GNU General Public License
        \item Has applications in physics, mathematics, weather, chemistry, economics \ldots
        \item One writes a high-level description of a problem in XML
        \item \xmds converts XML to C language code, which is then compiled to produce an executable
        which solves the problem about as quickly as code written by an expert
        \item \xmds gives people doing simulations structure, organisation and standardisation
        \item Provides a convenient framework for describing simulations of a system be it in
        a scientific or industrial setting
        \item Keeps the ideas behind a simulation well laid out and, importantly, documented for others to see and use
        \item \xmds gives a common ground from which scientists can compare their numerical work;
        something lacking in an area at the interface between theory and experiment, which already
        have a well-ingrained culture of comparison and verification~\cite{Ceperley:1999:1}
        \end{itemize}
        """).make(),
        ),
        Box(
	Rectangle(height=0.2,fg=Box.bg,bg=Box.bg),
        Title('Overview'),
	Rectangle(height=0.2,fg=Box.bg,bg=Box.bg),
        TeXBox(r'''
        \begin{itemize}
        \setlength{\itemsep}{-2mm}
        \item \xmds is designed to integrate the following general PDE:
        \vspace*{-3mm}
        \begin{align}
        \frac{\partial}{\partial x^0}\vect{a}(\vect{x}) & =
        \vect{\mathcal{N}}\left(\vect{x}, \vect{a}(\vect{x}), \vect{p}(\vect{x}),
        \vect{b}(\vect{x}),\;\vect{\xi}(\vect{x})\right),\\ 
        p^i(\vect{x}) & = \mathcal{F}^{-1}\left[\Sigma_j
        \mathcal{L}^{ij}\left(x^0,\vect{k_\bot}\right)
        \mathcal{F}\left[a^j(\vect{x})\right]\right],\\
        \frac{\partial}{\partial x^{c}}\vect{b}(\vect{x}) & =
        \vect{\mathcal{H}}\left(\vect{x}, \vect{a}(\vect{x}), 
        \vect{b}(\vect{x})\right)
        \label{eq:xmdsPdeEx}
        \end{align}
        \vspace*{-4mm}
        \item $\vect{a}(\vect{x})$ : main field, $\vect{b}(\vect{x})$ : cross-propagating field,
        $\vect{p}(\vect{x})$ : field in Fourier space,\\ $\xi(\vect{x})$ : noise terms
        \item \xmds integrates ODEs, PDEs, and stochastic ODEs and PDEs
        \end{itemize}
        '''),
        Align(TeXBox(r'''
        \begin{itemize}
        \item \xmds solves DEs with two methods:
          \begin{itemize}
          \setlength{\itemsep}{-1.5mm}
          \vspace*{-3mm}
          \item fourth-order Runge-Kutta,
          \item split-step semi-implicit method~\cite{Drummond:1983:1}
          \end{itemize}
        \end{itemize}
        ''', fixed_width=5.1).make(),
        TeXBox(r'''
        \begin{itemize}
        \item \xmds can handle any number of:
        \vspace*{-3mm}
          \begin{itemize}
          \setlength{\itemsep}{-1.5mm}
          \item components
          \item dimensions
          \item random variables
          \end{itemize}
        \end{itemize}
        ''',fixed_width=4.5).make(),
              a1='ne', a2='nw', angle=90, space=-0.2),
        TeXBox(r'''
	\vspace*{-3mm}
        \begin{itemize}
        \setlength{\itemsep}{-2mm}
        \item Performs automatic numerical error checking
        \item Handles cross-propagating fields
        \item Calculates trajectory means and variances of stochastic simulations
        \item Automatically parallelises stochastic and deterministic problems
        using MPI
        \end{itemize}
        ''').make(),
	Rectangle(height=0.2,fg=Box.bg,bg=Box.bg),
	pad=0
        ),
        Box(
        Title(r'Why use \xmds?'),
        TeXBox(r'''
        \begin{itemize}
        \setlength{\itemsep}{-1.5mm}
        \item \xmds reduces development time and user-introduced bugs
        \item Execution time closely approximates that of hand-written code
        \item Input file size dramatically smaller than hand-written code
        \item Open source and documentation (\texttt{http://www.xmds.org})~\cite{xmdsweb}
        \item Uses XSIL output format for easy and portable data interchange
        \item FFTW (Fastest Fourier Transform in the West) for highly efficient FFTs~\cite{fftwweb}
        \item Allows simple and transparent comparison of simulations
        with other researchers
        \item The script documents the simulation
        \item Simulation script (and therefore parameters) are output with the
        simulation data, so the data and the variables that generated it are
        kept together for future reference
        \end{itemize}
        ''').make(),
        ),
	Box(
        Title(r"Nonlinear Schr\"{o}dinger Equation"),
        TeXBox(r"""
        \begin{equation}
        \frac{\partial \phi}{\partial z } = i\left[\frac{1}{2} \frac{\partial ^{2}
        \phi}{\partial t ^{2}} + |\phi|^{2} \phi + i \Gamma (t) \phi
        \right]
        \end{equation}
        Where $\phi$ is the field, $z$ is the spatial dimension,
        $t$ is time and $\Gamma(t)$ is a damping term.
        """).make(),
        Align(
        #add_fig("nlse.eps",width=4.29),
        CodeBox(
        TeX(r'''\begin{verbatim}
  <simulation>  <!-- outline xmds code; greatly compressed for space -->
  <name>nlse</name> <prop_dim>z</prop_dim>
  <field>  <!-- field to be integrated over -->
    <dimensions> t </dimensions>
    <vector>  <components>phi</components>
      <![CDATA[  phi = pcomplex(amp*exp(-t*t/w0/w0),vel*t);  ]]>
    </vector>
  </field>
  <sequence>  <!-- sequence of integrations to perform -->
    <integrate>  <algorithm>RK4IP</algorithm>
      <k_operators>
        <![CDATA[  L = rcomplex(0,-kt*kt/2);  ]]>
      </k_operators>
      <![CDATA[  dphi_dz =  L[phi] + i*~phi*phi*phi - phi*damping;  ]]>
    </integrate>
  </sequence>
  <output>  <!-- output to generate -->
    <group>
      <sampling>
        <moments>pow_dens</moments>
        <![CDATA[  pow_dens=~phi*phi;  ]]>
      </sampling>
    </group>
  </output>
  </simulation>
        \end{verbatim}''').scale(0.3,0.3),
        ),
        a1="ne", a2="nw", angle=90, space=0.3),
	),
        Box(
        Title('Future Features'),
        TeXBox(r'''
        \begin{itemize}
        \setlength{\itemsep}{-2mm}
        \item More algorithms, user-defined libraries of routines
        \item Improved load balancing of parallel stochastic simulations
        \item Timed output of simulation data to monitor data on-the-fly 
	\item Reimplementation and generalisation of \xmds engine
        %\item breakpoints: binary output of entire simulation state at end of
        %simulation so that can restart the simulation from this point at next run
        %of the simulation
        \end{itemize}
        ''').make(),
        ),
        )
    
    col2=Group(
        Box(
        Title('Fibre Optic Laser Field'),
        TeXBox(r"""
        Equation~(\ref{eq:fibre}) describes a one dimensional
        damped field subject to a complex noise.\\ This is a stochastic PDE.
        \begin{equation}
        \frac{\partial \phi}{\partial t} = -i \frac{\partial^{2}
        \phi}{\partial x^{2}} - \gamma \phi + \frac{\beta}{\sqrt{2}}
        \left[\xi_1(x,t) + i\xi_2(x,t)\right].
        \label{eq:fibre}
        \end{equation}
        """).make(),
        Align(
        Align(
        add_fig("fibre1.eps",width=4),
        TeX(r"single path").scale(0.52,0.52),
        a1="s", a2="n", angle=180, space=0.1
        ),
        Align(
        add_fig("fibre2.eps",width=4),
        TeX(r"1024 path mean").scale(0.52,0.52),
        a1="s", a2="n", angle=180, space=0.1
        ),a1="ne", a2="nw", angle=90, space=0.3),
	),
        Box(
        Title('Process and Functionality'),
        TeXBox(r'''
        The figures below describe the processes involved in creating an
        \xmds simulation (left-hand diagram) and operating within an \xmds simulation
        (right-hand diagram).  \xmds reads the XML script, parses it, generates
        C/C++ code and then compiles the simulation binary using a C++ compiler.
        The simulation when executed generates XSIL output, which can
        then be converted for display in your favourite graphing package.
        ''').make(),
        Align(
        add_fig("xmdsProcess.eps",width=3),
        add_fig("xmdsFunctionality.eps",width=3),
        a1="ne", a2="nw", angle=90, space=0.4),
        ),
        Box(
        Title('Other Features'),
        Align(
        Group(
        TeXBox(r'''
        \begin{itemize}
        \setlength{\itemsep}{-2mm}
        \item ASCII and binary output
        \item Benchmarking of simulations
        \item User-defined preferences
        \end{itemize}
        ''',fixed_width=4.5).make(),
        TeXBox(r'''
        \begin{itemize}
        \setlength{\itemsep}{-2mm}
        \item Field initialisation from file
        \item Command line arguments to simulations
        \item \xmds script template output
        \end{itemize}
        ''',fixed_width=5).make(),
        ), a1="ne", a2="nw", angle=90, space=0.1,
        ),
        ),
        Box(
        Title('Take-home message'),
        TeXBox(r'''
        \xmds will save you time by solving your problems very quickly.
        So why not give it a go?  See \texttt{http://www.xmds.org} and try it out.
        ''').make(),
        ),
	Box(
        Title('References'),
        TeXBox(references).make(),
	),
        )
# -------------------------------------------------------------


poster=Poster()
poster.size = "a4"

print "Rendering picture..."
render(
    poster.make(),
    #poster.make().scale(4.0,4.0),
    file="xmdsPoster.eps",
    )

