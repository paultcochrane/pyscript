# Copyright (C) 2002  Alexei Gilchrist and Paul Cochrane
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.
'''
pyscript Presentation library (posters and talks)
'''

from pyscript import *

class Poster1:

    bg=None
    fg=Color('Lavender')

    thelogos=[]
    logo_height=.8
    
    title=""
    title_fg=Color('Yellow')
    title_scale=2

    authors=""
    authors_fg=Color(0)
    
    abstract=""
    abstract_fg=Color(0)
    
    logos=None

    box_bg=Color('Lavender')
    box_fg=Color(0)
    box_border=2

    references=""
    references_fg=Color(0)
    references_scale=.75
    
    def __init__(self):

        self.paper=Paper("a4")

        self.col1 = Align(a1="s",a2="n",angle=180,space=.4)
        self.col2 = Align(a1="s",a2="n",angle=180,space=.4)


    def tex(self,text,width=9,fg=None):
        if fg is None:
            fg=Color(0)
        return TeX(r'\begin{minipage}{%fcm}%s\end{minipage}'%(width,text),fg=fg)

    def addbox(self,col,*items):

        group=Align(a1="s",a2="n",angle=180,space=.2)
        apply(group.append,items)

        bbox=group.bbox()

        g=Group(
            Rectangle(sw=bbox.sw-P(.2,.2),
                      width=self.paper.width/2-.8,
                      height=bbox.height+.4,
                      bg=self.box_bg,
                      fg=self.box_fg,
                      linewidth=self.box_border,
                      c=group.c),
            group,
            )

        if col==1:
            self.col1.append(g)
        else:
            self.col2.append(g)

    def logos(self,*files):

        self.thelogos=[]

        for file in files:
            self.thelogos.append(Epsf(file,height=self.logo_height))

    def make_logos(self):

        if len(self.thelogos)==0:
            return Area(width=0,height=0)
        elif len(self.thelogos)==1:
            return Group(
                Area(width=self.paper.width,height=0,nw=P(0,0)),
                self.thelogos[0]
                )

        # a distribute class would be nice ....
        width=self.paper.width-\
             self.thelogos[0].bbox().width-\
             self.thelogos[-1].bbox().width-\
             .2
        
        for logo in self.thelogos[1:-1]:
            width-=logo.bbox().width

        space=width/(len(self.thelogos)-1)
        a=Align(a1="e",a2="w",angle=90,space=space)
        for logo in self.thelogos:
            a.append(logo)

        return a


    def make_title(self):
        return TeX(self.title,fg=self.title_fg).scale(self.title_scale,
                                                      self.title_scale)

    def make_abstract(self):
        return self.tex(self.abstract,16,fg=self.abstract_fg)

    def make_authors(self):
        return TeX(self.authors,fg=self.authors_fg)

    def make_references(self):

        s=self.references_scale

        # Should have an Area() of colwidth so it's left justified

        self.col2.append(
            self.tex(r"{\small %s}"%self.references,9./s,
                     fg=self.references_fg).scale(s,s)
            )
        
    def make(self,scale=1):

        # A0 = 4x A4
        
        self.make_references()
        
        self.col2.nw = self.col1.ne+P(.4,0)
        cols=Group(self.col1,self.col2)

        all=Align(a1="s",a2="n",angle=180,space=.4)

        all.append(
            self.make_logos(),
            self.make_title(),
            self.make_authors(),
            self.make_abstract(),
            cols,
            )

        all.n=self.paper.n-P(0,.1)

        back=Rectangle(sw=self.paper.sw,width=self.paper.width,
                       height=self.paper.height,
                       fg=None,
                       bg=self.bg
                       )

        p=self.paper.se+P(-.1,.1)
        signature=Text('Created with PyScript',size=6,
                       sw=p,fg=self.bg*.8).rotate(-90,p)

        All=Group(back,all,signature).scale(scale,scale) 


        return Group(All)

class Talk(Paper):
    """
    A talk class
    """
    bg = None
    fg = Color('lavender')

    thelogos = []
    logo_height = 0.8
    
    title = ""
    title_fg = Color('yellow')
    title_scale = 5

    footerScale = 1

    waitbar_fg = Color('red')
    waitbar_bg = Color('black')
    
    authors = ""
    authors_fg = Color('GoldenRod')
    authors_scale = 3

    mainAuthor = ""
    mainAuthor_fg = Color(0)
    
    logos = None

    box_bg = Color('lavender')
    box_fg = Color(0)
    box_border = 2
    
    headings_fgs = {
	    1 : Color('yellow'), 
	    2 : Color('yellow'), 
	    3 : Color('yellow'),
	    "default" : Color('yellow'),
	    }
    headings_scales = { 
	    1 : 3, 
	    2 : 2.5, 
	    3 : 2.2,
	    "default" : 1.5,
	    }
    headings_bullets = {
	    1 : r"$\bullet$", 
	    2 : r"--", 
	    3 : r"$\gg$",
	    "default" : r"$\cdot$",
	    }

    headings_indent = {
	    1 : 0,
	    2 : 0.5,
	    3 : 1,
	    "default" : 2,
	    }

    def __init__(self):
	
	self.paper = Paper("a4r")
	
    def tex(self, text, width=9, fg=None):
	if fg is None:
	    fg = Color(0)
	return TeX(r'\begin{minipage}{%fcm}%s\end{minipage}' % 
		    (width,text), fg=fg)

    def make(self, *slides):
	
	self.slides = slides
	numPages = len(slides)
	i = 1
	for slide in slides:
	    slide.pageNumber = i
	    temp = slide.make(self)
	    fname = '%s%02d%s' % ("slide",i,".eps")
	    render(temp,file=fname)
	    i += 1
	print "%i slides produced" % (i-1,)

class Slide(Talk):
    """
    A slide class
    """

    pageNumber = None
    authors = None
    titlepage = False

    def __init__(self,talk):
	
	self.bg = talk.bg
	self.fg = talk.fg
	self.paper = talk.paper
	self.footerScale = talk.footerScale
	self.mainAuthor = talk.mainAuthor
	self.waitbar_fg = talk.waitbar_fg
	self.headings = []
	self.epsf = []

    def logos(self,*files):
	
	self.thelogos = []
	
	for file in files:
	    self.thelogos.append(Epsf(file, height=self.logo_height))

    def make_logos(self):
	
	if len(self.thelogos) == 0:
	    return Area(width=0, height=0)
	elif len(self.thelogos) == 1:
	    return Group(
		Area(width=self.paper.width, height=0, nw=P(0,0)),
		self.thelogos[0]
		)

	width = self.paper.width -\
		self.thelogos[0].bbox().width -\
		self.thelogos[-1].bbox().width -\
		0.2

	for logo in self.thelogos[1:-1]:
	    width -= logo.bbox().width

	space = width/(len(self.thelogos)-1)
	a = Align(a1="e", a2="w", angle=90, space=space)
	for logo in self.thelogos:
	    a.append(logo)

	return a

    def make_authors(self):
        return TeX(
	    self.authors,fg=self.authors_fg
	    ).scale(self.authors_scale,self.authors_scale)

    def make_title(self):
        return TeX(self.title,fg=self.title_fg).scale(self.title_scale,
                                                      self.title_scale)

    def add_heading(self,level,text):
	temp = [ level, text ]
	self.headings.append(temp)

    def make_headings(self):
	heading_block = Align(a1="sw", a2="nw", angle=180, space=0.4)
	for heading in self.headings:
	    heading_text = heading[1]
	    heading_level = heading[0]
	    if not self.headings_bullets.has_key(heading_level):
		heading_level = "default"
	    heading_bullet = self.headings_bullets[heading_level]
	    heading_fg = self.headings_fgs[heading_level]
	    heading_scale = self.headings_scales[heading_level]
	    heading_indent = self.headings_indent[heading_level]

	    tex = TeX(text=heading_bullet + ' ' + heading_text,
			fg=heading_fg
			).scale(heading_scale,heading_scale)
	    tex.offset = tex.offset + P(heading_indent,0.0)
	    heading_block.append(tex)

	return heading_block
	    
    def make_waitbar(self):
	waitBarBack = Rectangle(se=self.paper.se+P(-0.8,0.4),
			width=2.5,
			height=0.5,
			fg=self.waitbar_bg,
			bg=self.waitbar_bg)

	offset = 0.05
	waitBarFront = Rectangle(w=waitBarBack.w+P(offset,0),
			width=(waitBarBack.width-2*offset)*\
				self.pageNumber/self.pages,
			height=waitBarBack.height-2*offset,
			fg=self.waitbar_fg,
			bg=self.waitbar_fg)
	waitBar = Group(waitBarBack,waitBarFront)
	return  waitBar

    def make_footer(self,talk):
	footerText = " - %s; page %i of %i" %  \
			(talk.mainAuthor,self.pageNumber,self.pages)
	
	footer = Align(a1="e", a2="w", angle=90, space=0.1)
	footer.append(
		    TeX(text=talk.title,
			fg=self.title_fg,
			).scale(self.footerScale,self.footerScale)
		    )
	footer.append(
		    TeX(
			text=footerText,
			fg=self.title_fg
			).scale(self.footerScale,self.footerScale)
		    )
	footer.sw = self.paper.sw+P(0.4,0.4)
	return footer

    def add_epsf(self,file="",**dict):
	if dict.has_key('width'):
	    picture = Epsf(file,width=dict['width'])
	elif dict.has_key('height'):
	    picture = Epsf(file,height=dict['height'])
	elif dict.has_key('width') and dict.has_key('height'):
	    picture = Epsf(file,width=dict['width'],height=dict['height'])
	else:
	    picture = Epsf(file)

	# there must be a better way to do this!!!
	if dict.has_key('e'):
	    picture.e = dict['e']
	elif dict.has_key('se'):
	    picture.se = dict['se']
	elif dict.has_key('s'):
	    picture.s = dict['s']
	elif dict.has_key('sw'):
	    picture.sw = dict['sw']
	elif dict.has_key('w'):
	    picture.w = dict['w']
	elif dict.has_key('nw'):
	    picture.nw = dict['nw']
	elif dict.has_key('n'):
	    picture.n = dict['n']
	elif dict.has_key('ne'):
	    picture.ne = dict['nw']
	else:
	    picture.sw = P(0.0,0.0)

	offset = 0.2
	background = Rectangle(width=picture.bbox().width+offset,
				height=picture.bbox().height+offset,
				bg=Color('white'),
				fg=Color('white'),
				)
	background.sw = picture.sw-P(offset/2.0,offset/2.0)
	figure = Group(background,picture)
	self.epsf.append(figure)

    def make_epsf(self):
	pictures = Group()
	for file in self.epsf:
	    pictures.append(file)
	return pictures

    def make(self, talk, scale=1):
        
        all=Align(a1="s", a2="n", angle=180, space=0.4)
        
        all.append(
            self.make_logos(),
            self.make_title()
            )

	if self.authors is not None:
	    all.append(self.make_authors())
        
	if self.titlepage:
	    all.c = self.paper.c + P(0.0,0.8)
	else:
	    all.n = self.paper.n - P(0,0.2)

	# I'm aware that this isn't a good way to do this, but
	# it's late at night, and I want to get *something* going

	headings = self.make_headings()
	headings.nw = self.paper.nw + P(3.0,-3.0)
    
        back = Rectangle(sw = self.paper.sw,
                        width = self.paper.width,
                        height = self.paper.height,
                        fg = None,
                        bg = self.bg
                        )
        
        p = self.paper.se + P(-0.1,0.1)
        signature = Text('Created with PyScript',
                            size=15,
                            sw=p,
                            fg=self.bg*0.8
                        ).rotate(-90,p)

	self.pages = len(talk.slides)

        All = Group(
		back,
		all,
		headings,
		self.make_epsf(),
		signature,
		self.make_footer(talk),
		self.make_waitbar()
		).scale(scale,scale)

        return Group(All)

