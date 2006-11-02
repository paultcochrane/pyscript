
from pyscript import *

defaults.tex_head=r"""
\documentclass{article}
\pagestyle{empty}
\usepackage{color}
\begin{document}
"""



# test scaling
class T(TeX):
	iscale=2

g=VAlign(T('\\LaTeX'),TeX('\\LaTeX',iscale=1.5),TeX('\\LaTeX'),space=.2)
g.move(1.5,0)

# test positional points
eq=TeX(r'$i\hbar \partial_t\psi = H \psi$')
eq.scale(.8,2).move(2,2.3).rotate(30)

#something more complex
para=TeX(r'''
Once upon a time
\begin{enumerate}
\item \label{first} there
\item was 
\item {\bf \textcolor{red}{f}\textcolor{green}{o}\textcolor{blue}{x}}
\item see \ref{first}
\end{enumerate}
''') 
para.move(0,-1)

render(

	para,
	g,
	eq, Dot(eq.ne), Dot(eq.n), Dot(eq.nw), Dot(eq.w), Dot(eq.sw), Dot(eq.s), Dot(eq.se), Dot(eq.e), Dot(eq.c), 

	# test fg
	eq.copy(fg=Color('green')),

	file='test_tex.eps'

	)


