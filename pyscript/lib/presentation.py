# Copyright (C) 2003  Alexei Gilchrist and Paul Cochrane
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

class Poster_paper:

    gutter=.5 # paper margin for A4 in cm

    bg=Color('DarkSlateBlue')
    fg=Color('Lavender')

    thelogos=[]
    logo_height=.8
    
    title=""
    title_fg=Color('Yellow')
    title_scale=2

    authors=""
    authors_fg=Color(0)
    authors_scale=1.4
    
    abstract=""
    abstract_fg=Color(0)
    
    logos=None

    box_bg=Color('Lavender')
    box_fg=Color(0)
    box_border=1
    box_pad=.2

    header_fg=Color('Navy')
    header_scale=1.3

    references=""
    references_fg=Color(0)
    references_scale=.75

    pad=.4
    tex_scale=.7

    #  (20.9903   ,29.7039),

    col1 = Group()
    col2 = Group()

    
    def __init__(self):

        # everything is going to be based around a4 paper
        self.paper_true=Paper("a4")
        self.paper=Area(
            sw=self.paper_true.sw+P(1,1)*self.gutter,
            width=self.paper_true.width-2*self.gutter,
            height=self.paper_true.height-2*self.gutter
            )


    def tex(self,text,width=None,fg=None,scale=None,align="w"):
        if fg is None:
            fg=Color(0)
        if width is None:
            width=(self.paper.width-3*self.pad)/2.-2*self.box_pad
        if scale is None:
            scale=self.tex_scale

        t=TeX(r'\begin{minipage}{%fcm}%s\end{minipage}'%(width/float(scale),text),fg=fg).scale(scale,scale)

        all=Align(Area(width=width,height=0,e=t.e),
                    t,
                    a1=align,a2=align,space=0)

        return all

    def header(self,text,align="c",scale=None):

        if scale is None:
            scale=self.header_scale

        scale=scale*self.tex_scale
        
        return self.tex(text,fg=self.header_fg,align=align,scale=scale)


    def addbox(self,col,*items):

        group=Group()
        apply(group.append,items)

        Align(group,a1="s",a2="n",angle=180,space=self.box_pad)

        bbox=group.bbox()

        g=Group(
            Rectangle(n=bbox.n-P(0,-self.box_pad),
                      width=(self.paper.width-3*self.pad)/2.,
                      height=bbox.height+2*self.box_pad,
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

        self.thelogos=Group()

        for file in files:
            self.thelogos.append(Epsf(file,height=self.logo_height))

    def make_logos(self):

        if len(self.thelogos)==0:
            return Area(width=0,height=0)

        Distribute(self.thelogos,a1="e",a2="w",
                   p1=self.paper.nw,p2=self.paper.ne)

        Align(self.thelogos,a1="e",a2="w",angle=90,space=None)

        return self.thelogos


    def make_title(self):

        scale=self.tex_scale*self.title_scale

        return self.tex(self.title,fg=self.title_fg,
                        scale=scale,width=self.paper.width*.8,align="c")

    def make_abstract(self):
        return self.tex(self.abstract,16,fg=self.abstract_fg,align="c")

    def make_authors(self):

        scale=self.tex_scale*self.authors_scale
        
        return self.tex(self.authors,fg=self.authors_fg,
                        scale=scale,width=self.paper.width*.8,align="c")

    def make_references(self):

        s=self.references_scale*self.tex_scale

        self.col2.append(
            self.tex(r"{\small %s}"%self.references,
                     fg=self.references_fg,scale=s)
            )
        
    def make(self,scale=1):

        # A0 = 4x A4
        
        self.make_references()

        col1=Align(self.col1,a1="s",a2="n",angle=180,space=self.pad)        
        col2=Align(self.col2,a1="s",a2="n",angle=180,space=self.pad)        

        col2.nw = col1.ne+P(self.pad,0)
        cols=Group(col1,col2)

        all=Align(
            self.make_logos(),
            self.make_title(),
            self.make_authors(),
            self.make_abstract(),
            cols,
            a1="s",a2="n",angle=180,space=self.pad
            )

        all.n=self.paper.n-P(0,.1)

        back=Rectangle(width=self.paper_true.width,
                       height=self.paper_true.height,
                       fg=None,
                       bg=self.bg
                       )

        p=self.paper.se+P(-.1,.1)
        signature=Text('Created with PyScript',size=6,
                       sw=p,fg=self.bg*.8).rotate(-90,p)

        All=Group(back,all,signature).scale(scale,scale) 

        return All

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
	a = Align(self.thelogos, a1="e", a2="w", angle=90, space=space)

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
	heading_block = Group()
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
			fg=heading_fg).scale(heading_scale,heading_scale)
	    padding = Area(sw=tex.sw,width=heading_indent,height=0)
	    heading_proper = Group(padding,tex)
	    Align(heading_proper, a1="e", a2="w", angle=90, space=0)
	    heading_block.append(heading_proper)

	Align(heading_block, a1="sw", a2="nw", angle=180, space=0.4)
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
	
	footerTeX = Group(
		    TeX(text=talk.title,
			fg=self.title_fg,
			).scale(self.footerScale,self.footerScale),
		    TeX(
			text=footerText,
			fg=self.title_fg
			).scale(self.footerScale,self.footerScale),
		    )
	footer = Align(footerTeX, a1="e", a2="w", angle=90, space=0.1)
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
        
	all = Group(self.make_logos(),self.make_title())
        
	if self.authors is not None:
	    all.append(self.make_authors())
        
        Align(all, a1="s", a2="n", angle=180, space=0.4)

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

