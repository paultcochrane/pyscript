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

There are some common useful component classes such as TeXBox and Box_1, 
followed by poster and talk classes
'''

from pyscript import *

class  TeXBox(Group):
    '''
    Typeset some LaTeX within a fixed width box.
    
    @cvar fixed_width: the width of the box
    @cvar tex_scale: The abount by which to scale the tex
    @cvar align: alignment of the LaTeX to box if its smaller
    '''

    fixed_width=9.2
    
    tex_scale=.7

    fg=Color(0)

    align="w"
    
    def __init__(self,text,**dict):

        apply(Group.__init__,(self,),dict)

        width_pp=int(self.fixed_width/float(self.tex_scale)*defaults.units)

        t=TeX(r'\begin{minipage}{%dpt}%s\end{minipage}'%(width_pp,text),
              fg=self.fg)

        t.scale(self.tex_scale,self.tex_scale)
        
        a=Area(width=self.fixed_width,height=0)

        Align(t,a,a1=self.align,a2=self.align,space=0)

        self.append(a,t)
        

class Box_1(Group):
    '''
    A box with of fixed width. Items added to it are aligned 
    vertically and separated by a specified padding
    
    @cvar border: width of the border (in pts)
    @cvar fg: color of border
    @cvar bg: color of box background
    @cvar fixed_width: width of box
    @cvar pad: vertical padding between items
    '''
    
    bg=Color('Lavender')
    fg=Color(0)
    border=1
    fixed_width=9.6
    pad=.2

    def __init__(self,*items,**dict):

        apply(Group.__init__,(self,),dict)
        
        apply(self.append,items)

        Align(self,a1="s",a2="n",angle=180,space=self.pad)

        gb=self.bbox()

        r=Rectangle(n=gb.n+P(0,self.pad),
                    width=self.fixed_width,
                    height=gb.height+2*self.pad,
                    bg=self.bg,
                    fg=self.fg,
                    linewidth=self.border,
                    )

        self.insert(0,r)

class Poster_1(Page):
    '''
    A poster style, portrait orientation very similar to a 
    journal articles front page. Title, authors and abstract across
    top. two columns for boxes with details. It is set up for A4 paper
    which can then be scaled for A0 etc.
    
    @cvar bg: poster background
    
    @cvar gutter: nonprintable margin around entire poster
    
    @cvar title: TeX of title
    @cvar title_fg: fg color of title
    @cvar title_scale: scale of title TeX
    @cvar title_width: proportion of total width for title
    
    @cvar authors: TeX of authors
    @cvar authors_fg: fg color of authors
    @cvar authors_scale: scale of authors TeX
    @cvar authors_width: proportion of total width for authors
    
    @cvar abstract: TeX of abstract
    @cvar abstract_fg: fg color of abstract
    @cvar abstract_scale: scale of abstract TeX
    @cvar abstract_width: proportion of total width for abstract
    
    @cvar logos: a list of filenames for the logos
    @cvar logo_height: the height to which to scale the logos
    
    @cvar printing_area: an Area the size of the page minus the gutter
    
    @cvar col1: a Group() containing left column objects
    @cvar col2: a Group() containing right column objects

    '''
    size="A4"
    gutter=.2 # paper margin for A4 in cm

    bg=Color('DarkSlateBlue')

    title=""
    title_fg=Color('Yellow')
    title_scale=1.4
    title_width=.7

    authors=""
    authors_fg=Color(0)
    authors_scale=1
    authors_width=.8
    
    abstract=""
    abstract_fg=Color(0)
    abstract_scale=.8
    abstract_width=.8
    
    logo_height=.8
    logos=()

    col1 = Group()
    col2 = Group()
    
    printing_area=None

    def __init__(self):

        Page.__init__(self)
        
        area=self.area()
        
        # subtract the gutter to get printing area
        self.printing_area=Area(
            sw=area.sw+P(1,1)*self.gutter,
            width=area.width-2*self.gutter,
            height=area.height-2*self.gutter
            )

    def make_logos(self):

        thelogos=Group()
        for logo in self.logos:
            thelogos.append(Epsf(logo,height=self.logo_height))
            
        Distribute(thelogos,a1="e",a2="w",
                   p1=self.printing_area.nw,
                   p2=self.printing_area.ne)

        Align(thelogos,a1="e",a2="w",angle=90,space=None)

        return thelogos


    def make_title(self):
        '''
        Return a title object
        '''

        return TeXBox(self.title,fg=self.title_fg,
                      fixed_width=self.printing_area.width*self.title_width,
                      tex_scale=self.title_scale,
                      align="c")

    def make_abstract(self):
        '''
        Return the abstract object
        '''
        
        return TeXBox(self.abstract,
                      fixed_width=self.printing_area.width*self.abstract_width,
                      tex_scale=self.abstract_scale,
                      fg=self.abstract_fg,align="c")

    def make_authors(self):
        '''
        Return authorlist object
        '''

        return TeXBox(self.authors,
                      fg=self.authors_fg,
                      tex_scale=self.authors_scale,
                      fixed_width=self.printing_area.width*self.authors_width,
                      align="c")

    def make_background(self):
        '''
        Return background (block color)
        '''
        area=self.area()
        
        return Rectangle(width=area.width,
                         height=area.height,
                         fg=None,
                         bg=self.bg
                         )
    
        
    def make(self):
        '''
        Create the actual poster aligning everything up.
        calls make_title(), make_authors() etc
        '''

        # NB: A0 = 4x A4
        
        # vertically align the column items ... no spacing yet!
        Align(self.col1,a1="s",a2="n",angle=180,space=None)
        Align(self.col2,a1="s",a2="n",angle=180,space=None)

        # Distribute the cols horizontally
        Distribute(Area(width=0,height=0),
                   self.col1,self.col2,
                   Area(width=0,height=0),
                   p1=self.printing_area.w,
                   p2=self.printing_area.e,a1="e",a2="w")
        
        
        # find the distance between the cols
        pad=(self.col2.bbox().w-self.col1.bbox().e)[0]

        # vertically align the column items
        Align(self.col1,a1="s",a2="n",angle=180,space=pad)
        Align(self.col2,a1="s",a2="n",angle=180,space=pad)        

        # align the two columns themselves
        cols=Align(self.col1,self.col2,angle=90,space=None,a1="ne",a2="nw")
        
        all=Align(
            self.make_logos(),
            self.make_title(),
            self.make_authors(),
            self.make_abstract(),
            cols,
            a1="s",a2="n",angle=180,space=pad
            )

        all.n=self.printing_area.n-P(0,.1)

        back=self.make_background()

        p=self.printing_area.se+P(0,1.2)
        signature=Text('Created with PyScript',size=6,
                       sw=p,fg=self.bg*.8).rotate(-90,p)

        self.append(back,all,signature)
        
        # return a reference for convenience
        return self


class Talk(Paper):
    """
    A talk class
    """
    bg = Color('RoyalBlue')
    fg = bg

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

    talkAuthor = ""
    talkAuthor_fg = Color(0)
    
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
        self.talkAuthor = talk.talkAuthor
        self.waitbar_fg = talk.waitbar_fg
        self.headings = []
        self.epsf = []
        self.figs = []

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

    def add_fig(self,obj,**dict):
        """
        Chuck an arbitrary figure onto the page, with a white background
        """

        # there must be a better way to do this!!!
        if dict.has_key('e'):
            obj.e = dict['e']
        elif dict.has_key('se'):
            obj.se = dict['se']
        elif dict.has_key('s'):
            obj.s = dict['s']
        elif dict.has_key('sw'):
            obj.sw = dict['sw']
        elif dict.has_key('w'):
            obj.w = dict['w']
        elif dict.has_key('nw'):
            obj.nw = dict['nw']
        elif dict.has_key('n'): 
            obj.n = dict['n']
        elif dict.has_key('ne'):
            obj.ne = dict['nw']
        else:
            obj.sw = P(0.0,0.0)

        gutter = 0.1
        back = Rectangle(width=obj.bbox().width+gutter,
                    height=obj.bbox().height+gutter,
                    bg=Color('white'))
        back.sw = obj.bbox().sw-P(gutter/2.0,gutter/2.0)
        self.figs.append(Group(back,obj))

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
                        (talk.talkAuthor,self.pageNumber,self.pages)
        
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

    def make_figs(self):
        figs = Group()
        for fig in self.figs:
            figs.append(fig)
        return figs

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
                self.make_figs(),
                signature,
                self.make_footer(talk),
                self.make_waitbar()
                ).scale(scale,scale)

        return Group(All)

