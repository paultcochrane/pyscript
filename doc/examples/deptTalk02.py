from presentation import *

# define_bullet(level=1,...)
# define_heading(level=1,...)
# define_title()

# now wrap this stuff into a style and biff into ~/.pyscript/styles dir


talk = Talk()
talk.title = r"""
\begin{center}
Tailoring Teleportation\\ to the Quantum Alphabet
\end{center}
"""
talk.authors = r"\underline{Paul Cochrane} and Tim Ralph"
talk.talkAuthor = r"Paul Cochrane"
talk.talkAuthor_textstyle = r"\sf"

talk.address = r"""
\begin{center}
Centre for Quantum Computer Technology, Physics Dept.,\\
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

talk.headings_fgs[2] = Color('white')
talk.headings_textstyle[2] = r"\sf"

# start of the slides

# this is the titlepage, so one doesn't need to do much
slide1 = Slide(talk)
slide1.titlepage = True  # should just need to call this for the first page

# other slides can be a bit more involved
slide2 = Slide(talk)
slide2.title = r"Introduction"
slide2.add_heading(1,r"Teleportation")
slide2.add_heading(1,r"Tailored teleportation")
slide2.add_heading(1,r"Coherent states on a line")
slide2.add_heading(1,r"Results")
slide2.add_heading(1,r"Outlook")

# slide 3
slide3 = Slide(talk)
slide3.title = r"Teleportation explained\ldots"
slide3.add_heading(1,r" Victoria (verifier), Alice (sender), Bob (receiver)")
slide3.add_heading(1,r"Alice and Bob share an entanglement resource")
slide3.add_heading(1,r"Victoria gives target state to Alice")
slide3.add_heading(1,r"Target state kept secret from Alice and Bob")
slide3.add_heading(1,r"""
Alice makes joint local
measurements on the target state and her part of the entanglement resource
""")
#slide3.add_heading(1,r"""
#\sf Alice makes \textcolor[named]{Red}{joint} \textcolor[named]{Orange}{local}
#measurements on the target state and her part of the entanglement resource
#""")

slide4 = Slide(talk)
slide4.title = slide3.title
slide4.add_heading(1,r"""
Alice sends the measurements to Bob via a classical channel
""")
slide4.add_heading(1,r"""
Bob makes local unitary
transformations on his part of the entanglement resource
""")
#slide4.add_heading(1,r"""
#\sf Bob makes \textcolor[named]{Orange}{local} 
#\textcolor[named]{Red}{unitary}
#transformations on his part of the entanglement resource
#""")
slide4.add_heading(1,r"The target state is reproduced at Bob's location")
slide4.add_heading(1,r"""
Victoria verifies that output state is a good reproduction of input 
state""")

slide5 = Slide(talk)
slide5.title = slide4.title
# I'll need to change this figure to pyscript...
slide5.add_epsf(file="teleDiag.ps",width=22,c=slide5.area.c-P(0,1))

slide6 = Slide(talk)
slide6.title = r"Alice and Bob"
slide6.add_epsf(file="AliceBob.ps",
		    width=17,c=slide6.area.c-P(0,0.7))

slide7 = Slide(talk)
slide7.title = slide6.title
circ = Circle(r=1.5,fg=Color('black'),bg=Color('white'))
a = Text('A',font="helvetica").scale(4.5,4.5)
b = Text('B',font="helvetica").scale(4.5,4.5)
a.c = circ.c
b.c = circ.c
left = Group(circ,a)
right = Group(circ,b)

ttext = TeXBox(r"\sf Theoretically\ldots",fg=Color('white'),tex_scale=5)
slide7.add_fig(ttext,
	    w=slide7.area.nw+P(4,-5),
	    bg=None,
	    )
slide7.add_fig(left,bg=None,c=slide7.area.c+P(-5,1))
slide7.add_fig(right,bg=None,c=slide7.area.c+P(8,1))

slide8 = slide7.copy()
slide8.add_fig(TeXBox(r"""
\sf In theory, theory and practice are the
same\ldots\\ In practice, they're not.
""",fg=Color('white'),tex_scale=3,fixed_width=20),
		w=slide8.area.sw+P(4,3),
		bg=None,
		)

slide9 = Slide(talk)
slide9.title = slide7.title
ttext = TeXBox(r"\sf Experimentally\ldots",fg=Color('white'),tex_scale=5)
slide9.add_fig(ttext,w=slide9.area.nw+P(4,-5),bg=None)
slide9.add_epsf(file="Alice.ps",width=13,e=slide9.area.c+P(0,-1))
slide9.add_epsf(file="Bob.ps",width=13,w=slide9.area.c+P(0,-1))

slide10 = Slide(talk)
slide10.title = r"Alice and Bob (and Ted and Carol?)"
slide10.add_epsf(file="BobCarolTedAlice.ps",width=9.5,c=slide10.area.c+P(0,-1))

slide11 = Slide(talk)
ttext = TeXBox(r"\bf Now entering boring section of talk\ldots\\ Please feel free to fall asleep.",
	fg=slide11.title_fg,
	tex_scale=3.5,
	fixed_width=24)
slide11.add_fig(ttext,w=slide11.area.w+P(3,-1),bg=None)

slide12 = Slide(talk)
slide12.title = r"Tailored teleportation"
slide12.add_heading(1,r"Tailored displacement only")
slide12.add_epsf(file="tailoredDispDiag.ps",width=20,c=slide12.area.c+P(0,-1.5))

slide13 = Slide(talk)
slide13.title = slide12.title
slide13.add_heading(1,r"Best displacement Bob should make is")
ttext = TeXBox(r"WARNING: Gratuitous equation!!!",
	    fg=Color('white'),tex_scale=3,fixed_width=17)
slide13.add_fig(ttext,c=slide13.area.c+P(0,5),bg=None)

slide14 = Slide(talk)
slide14.title = slide13.title
slide14.add_heading(1,r"Best displacement Bob should make is")
eqn = TeXBox(r"$\epsilon = (1-\lambda) \alpha + \lambda \beta$",
	fg=Color('white'),
	tex_scale=3,
	fixed_width=8)
slide14.add_fig(eqn,c=slide14.area.c+P(0,5.5),bg=None)

slide15 = slide14.copy()
slide15.add_heading("space",r" ")
slide15.add_heading(2,r"$\beta = x_- + i p_+$ is Alice's measurement result")
slide15.add_heading(2,r"""
\sf $\lambda$ is the squeezing parameter ($\lambda=0$: no squeezing;
$\lambda=1$: infinite squeezing)""")
slide15.add_heading(2,r"$\alpha$ is the best guess of the target state")

slide16 = slide15.copy()
slide16.add_heading(1,r"guess contribution")
# somehow put an arrow to \alpha and put a circle around it.

slide17 = slide16.copy()
slide17.add_heading(1,r"normal teleportation contribution")
# again put arrow to circled element (in this caes \beta)

slide18 = Slide(talk)
slide18.title = r"Tailored measurement teleportation"
slide18.add_heading(1,r"Tailored measurement as well")
slide18.add_epsf(file="adapTeleDiag.ps",width=20,c=slide18.area.c+P(0,-1.5))

slide19 = Slide(talk)
slide19.title = r"Coherent states on a line"
slide19.add_heading(1,r"""
Coherent states only exist along real axis in phase space""")
slide19.add_heading(1,r"""
States of known phase, unknown amplitude""")
slide19.add_epsf(file="cohStateOnALine.ps",width=20,c=slide19.area.c+P(0,-3))

slide20 = Slide(talk)
slide20.title = r"How well does it work??"
slide20.add_epsf(file="fidelityLambdaAll.ps",width=20,c=slide20.area.c+P(0,-1))
ttext = TeXBox(r"\sf standard teleportation",
	    fg=Color('red'),
	    tex_scale=3,
	    fixed_width=10)
slide20.add_fig(ttext,w=slide20.area.c-P(1,4),bg=None)
# need to chuck arrow on it.

slide21 = slide20.copy()
ttext = TeXBox(r"\sf tailored displacement",
	    fg=Color('red'),
	    tex_scale=3,
	    fixed_width=10)
slide21.add_fig(ttext,w=slide21.area.c-P(1,1),bg=None)
# now need to add arrow

slide22 = slide21.copy()
ttext = TeXBox(r"\sf tailored measurement and displacement",
	    fg=Color('red'),
	    tex_scale=3,
	    fixed_width=18)
slide22.add_fig(ttext,w=slide21.area.c+P(-7.5,6),bg=None)
# now need to add arrow

slide23 = Slide(talk)
slide23.title = r"Beam me up, mate!"
slide23.add_heading("space","")
slide23.add_heading(1,r"""
CBS news coverage of the ANU teleportation experiment""")
slide23.add_heading(1,r"""
This protocol could easily be added to the ANU teleportation experiment""")
slide23.add_epsf(file="starTrek.ps",width=5,ne=slide23.area.ne-P(0.5,0.5))

slide24 = slide23.copy()
slide24.add_epsf(file="drinking.ps",width=14,c=slide24.area.c+P(0,-4.5))

slide25 = slide23.copy()
slide25.add_epsf(file="working.ps",width=9.5,c=slide25.area.c+P(0,-4.5))

slide26 = Slide(talk)
slide26.title = r"Conclusion/Outlook"
slide26.add_heading(1,r"""
Have shown how to tailor teleportation to the known properties of the
target states""")
slide26.add_heading(1,r"""
This gives a great improvement over current continuous variable
teleportation""")
slide26.add_heading(1,r"""
This protocol could be implemented in the ANU teleportation experiment""")


# draw it!
talk.make(
	slide1, 
	slide2,
	slide3,
	slide4,
	slide5,
	slide6,
	slide7,
	slide8,
	slide9,
	slide10,
	slide11,
	slide12,
	slide13,
	slide14,
	slide15,
	slide16,
	slide17,
	slide18,
	slide19,
	slide20,
	slide21,
	slide22,
	slide23,
	slide24,
	slide25,
	slide26,
        file="deptTalk02.ps",
	)

