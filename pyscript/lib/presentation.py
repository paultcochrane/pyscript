# Copyright (C) 2003-2006  Alexei Gilchrist and Paul Cochrane
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

# $Id$

'''
pyscript Presentation library (posters and talks)

There are some common useful component classes such as TeXBox and Box_1, 
followed by poster and talk classes
'''

__revision__ = '$Revision$'

from pyscript.defaults import defaults
from pyscript import Color, Group, Epsf, Area, P, Align, Rectangle, TeX, \
        Page, Distribute, Text, Pages
from pyscript.render import render
import os, types

class TeXBox(Group):
    '''
    Typeset some LaTeX within a fixed width box.
    
    @cvar fixed_width: the width of the box
    @type fixed_width: float

    @cvar tex_scale: The amount by which to scale the TeX
    @type tex_scale: float

    @cvar align: alignment of the LaTeX to box if it is smaller
    @type align: anchor string
    '''

    fixed_width = 9.4
    tex_scale = 0.7
    fg = Color(0)
    align = "w"
    text_style = ""

    def __init__(self, text, **options):
        Group.__init__(self, **options)

        width_pp = int(self.fixed_width/float(self.tex_scale)*defaults.units)

        al = Align(a1=self.align, a2=self.align, space=0)

        t = TeX(r'\begin{minipage}{%dpt}%s %s\end{minipage}' \
                % (width_pp, self.text_style, text), 
                fg=self.fg)

        t.scale(self.tex_scale, self.tex_scale)
        al.append(t)
        
        a = Area(width=self.fixed_width, height=0)
        al.append(a)

        self.append(al)
        apply(self, (), options)

class Box_1(Group):
    '''
    A box of fixed width. Items added to it are aligned vertically and
    separated by a specified padding
    
    @cvar border: width of the border (in pts)
    @type border: int

    @cvar fg: color of border
    @type fg: L{Color} object

    @cvar bg: color of box background
    @type bg: L{Color} object

    @cvar fixed_width: width of box
    @type fixed_width: float

    @cvar pad: vertical padding between items
    @type pad: float

    @cvar r: corner radius
    @type r: float
    '''
    
    bg = Color('Lavender')
    fg = Color(0)
    border = 1
    fixed_width = 9.6
    pad = 0.2
    r = 0

    def __init__(self, *items, **options):
        Group.__init__(self, **options)
        
        apply(self.append, items)

        Align(self, a1="s", a2="n", angle=180, space=self.pad)

        gb = self.bbox()

        r = Rectangle(n=gb.n+P(0, self.pad),
                    width=self.fixed_width,
                    height=gb.height+2*self.pad,
                    bg=self.bg,
                    fg=self.fg,
                    linewidth=self.border,
                    r=self.r,
                    )

        self.insert(0, r)

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
    
    @cvar address: TeX of address
    @cvar address_fg: fg color of address
    @cvar address_scale: scale of address TeX
    @cvar address_width: proportion of total width for address
    
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
    size = "A4"
    gutter = .2 # paper margin for A4 in cm

    bg = Color('DarkSlateBlue')

    title = ""
    title_fg = Color('Yellow')
    title_scale = 1.4
    title_width = .8

    address = ""
    address_fg = Color(0)
    address_scale = 1
    address_width = .8

    authors = ""
    authors_fg = Color(0)
    authors_scale = 1
    authors_width = .8
    
    abstract = ""
    abstract_fg = Color(0)
    abstract_scale = .8
    abstract_width = .8
    
    logo_height = .8
    logos = ()

    col1 = Group()
    col2 = Group()

    signature_fg = bg*0.8
    
    printing_area = None

    def __init__(self):

        Page.__init__(self)
        
        area = self.area()
        
        # subtract the gutter to get printing area
        self.printing_area = Area(
            sw=area.sw+P(1, 1)*self.gutter,
            width=area.width-2*self.gutter,
            height=area.height-2*self.gutter
            )

    def make_logos(self):

        #thelogos = Group()
        thelogos = Align(a1="e", a2="w", angle=90, space=None)
        for logo in self.logos:
            thelogos.append(Epsf(logo, height=self.logo_height))
            
        Distribute(thelogos, a1="e", a2="w",
                   p1=self.printing_area.nw,
                   p2=self.printing_area.ne)

        #Align(thelogos, a1="e", a2="w", angle=90, space=None)

        return thelogos


    def make_title(self):
        '''
        Return a title object
        '''

        return TeXBox(self.title, fg=self.title_fg,
                      fixed_width=self.printing_area.width*self.title_width,
                      tex_scale=self.title_scale,
                      align="c")

    def make_address(self):
        """
        Return an address object
        """
        return TeXBox(self.address,
                    fg=self.address_fg,
                    fixed_width=self.printing_area.width*self.address_width,
                    tex_scale=self.address_scale,
                    align="c")

    def make_abstract(self):
        '''
        Return the abstract object
        '''
        
        return TeXBox(self.abstract,
                      fixed_width=self.printing_area.width*self.abstract_width,
                      tex_scale=self.abstract_scale,
                      fg=self.abstract_fg, align="c")

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
        area = self.area()
        
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
        Align(self.col1, a1="s", a2="n", angle=180, space=None)
        Align(self.col2, a1="s", a2="n", angle=180, space=None)

        # Distribute the cols horizontally
        Distribute(Area(width=0, height=0),
                   self.col1, self.col2,
                   Area(width=0, height=0),
                   p1=self.printing_area.w,
                   p2=self.printing_area.e, a1="e", a2="w")
        
        
        # find the distance between the cols
        pad = (self.col2.bbox().w-self.col1.bbox().e)[0]

        # vertically align the column items
        Align(self.col1, a1="s", a2="n", angle=180, space=pad)
        Align(self.col2, a1="s", a2="n", angle=180, space=pad)        

        # align the two columns themselves
        cols = Align(self.col1, self.col2, 
                angle=90, space=None, a1="ne", a2="nw")
        
        all = Align(
            self.make_logos(),
            self.make_title(),
            self.make_authors(),
            self.make_address(),
            self.make_abstract(),
            cols,
            a1="s", a2="n", angle=180, space=pad
            )

        all.n = self.printing_area.n-P(0, .1)

        back = self.make_background()

        p = self.printing_area.se+P(0, 1.2)
        signature = Text(
                'Created with PyScript.  http://pyscript.sourceforge.net',
                size=6, sw=p, fg=self.signature_fg
                ).rotate(-90, p)

        self.append(back, all, signature)
        
        # return a reference for convenience
        return self


class Talk(Pages):
    """
    A talk class
    """

    def __init__(self, style=None):
        Pages.__init__(self)

        self.slides = []

        self.bg = Color('RoyalBlue')*0.9
        self.fg = self.bg

        self.logos = []
        self.logo_height = 0.8
        
        self.title = ""
        self.title_fg = Color('white')
        self.title_scale = 5
        self.title_textstyle = ""

        self.slide_title = ""
        self.slide_title_fg = Color('white')
        self.slide_title_scale = 5
        self.slide_title_textstyle = ""

        self.footerScale = 1

        self.waitbar_fg = Color('orangered')
        self.waitbar_bg = Color('black')
        
        self.authors = ""
        self.authors_fg = Color('white')
        self.authors_scale = 3
        self.authors_textstyle = ""

        self.speaker = ""   # i.e. who's actually giving the talk
        self.speaker_fg = Color(0)
        self.speaker_textstyle = ""

        self.address = ""
        self.address_fg = Color('white')
        self.address_scale = 2
        self.address_textstyle = ""
        
        self.box_bg = Color('lavender')
        self.box_fg = Color(0)
        self.box_border = 2

        self.text_scale = 3
        self.text_fg = Color(0)
        self.text_textstyle = ""
        
        self.headings_fgs = {
                1 : Color('white'), 
                2 : Color('white'), 
                3 : Color('white'),
                "equation" : Color('white'),
                "default" : Color('white'),
                "space" : self.fg,
                }
        self.headings_scales = { 
                1 : 3, 
                2 : 2.5, 
                3 : 2.2,
                "equation" : 2.5,
                "default" : 1.5,
                "space" : 3,
                }
        self.headings_bullets = {
                1 : TeX(r"$\bullet$"), 
                2 : TeX(r"--"), 
                3 : TeX(r"$\gg$"),
                "equation" : Rectangle(height=1, fg=self.bg, bg=self.bg),
                "default" : TeX(r"$\cdot$"),
                "space" : Rectangle(height=1, fg=self.bg, bg=self.bg),
                }
        self.headings_indent = {
                1 : 0,
                2 : 0.5,
                3 : 1,
                "equation" : 2,
                "default" : 2,
                "space" : 0,
                }
        self.headings_textstyle = {
                1 : "",
                2 : "",
                3 : "",
                "equation" : "",
                "default" : "",
                "space" : "",
                }

        # process the style option
        if style is not None:
            # make sure the file exists in either the .pyscript/styles
            # directory, or the current directory
            styleFname = style + ".py"
            HOME = os.path.expandvars("$HOME")
            if os.path.exists(HOME + "/.pyscript/styles/" + styleFname):
                print "Found %s in .pyscript/styles dir" % style
                self.read_style(HOME + "/.pyscript/styles/" + styleFname)
            elif os.path.exists(styleFname):
                print "Found %s in current dir" % style
                self.read_style(styleFname)
            else:
                # barf
                raise ValueError, "Style %s not found!" % style

    def read_style(self, styleFname):
        """
        Read the talk style file

        @param styleFname: The name of the style file to process
        @type styleFname: string
        """
        # slurp in the text
        fp = open(styleFname, "r")
        lines = fp.readlines()
        fp.close()

        # make one big string...
        styleText = ""
        for line in lines:
            styleText += line

        # exec the text
        exec(styleText)

    def set_title(self, title):
        """
        Set the title of the talk as a whole

        @param title: the title of the talk
        @type title: string
        """
        self.title = title
        return

    def set_authors(self, authors):
        """
        Set the authors of the talk

        @param authors: the author list for the talk
        @type authors: string
        """
        self.authors = authors
        return

    def set_speaker(self, speaker):
        """
        Set the name of the person actually giving the talk/presentation

        @param speaker: the name of the person giving the talk
        @type speaker: string
        """
        self.speaker = speaker
        return

    def set_address(self, address):
        """
        Set the address for the institution (or equivalent) of the speaker
        
        @param address: the address to use
        @type address: string
        """
        self.address = address
        return

    def add_logo(self, logo, height=None):
        """
        Add a logo to the talk

        @param logo: eps file name of logo
        @type logo: string
        """
        if height is None:
            height = self.logo_height

        self.logos.append(Epsf(file=logo, height=height))

    def make_authors(self):
        """
        Generate the authors text on the titlepage
        """
        ttext = "%s %s" % (self.authors_textstyle, self.authors)
        return TeX(ttext, fg=self.authors_fg
            ).scale(self.authors_scale, self.authors_scale)

    def make_address(self):
        """
        Generate the address text on the titlepage
        """
        if isinstance(self.address, types.StringType):
            ttext = "%s %s" % (self.address_textstyle, self.address)
            return TeX(ttext, fg=self.address_fg
                ).scale(self.address_scale, self.address_scale)
        else:
            #raise ValueError, "Can't handle non-string arguments yet"
            return self.address

    def make(self, *slides, **options):
        """
        Routine to collect all of slides together and render them all as
        the one document
        """
        # create the titlepage automatically
        titlepage = Slide(self)
        titlepage.set_titlepage()
        self.slides.append(titlepage)
        
        # create the list of slides
        for slide in slides:
            self.slides.append(slide)

        # add all the slides to the talk
        i = 1
        temp = Pages()
        for slide in self.slides:
            slide.pageNumber = i
            print 'Adding slide', str(i), '...'
            temp.append(slide.make(self))
            i += 1

        # determine the file name to use
        if not options.has_key('file'):
            raise ValueError, "No filename given"
        file = options['file']
        
        # render it!
        render(temp, file=file)

class Slide(Page):
    """
    A slide class.  Use this class to generate the individual slides in a talk
    """
    pageNumber = None
    authors = None
    titlepage = False
    # size = "screen"
    size = "a4"
    orientation = "Landscape"

    def __init__(self, talk):
        Page.__init__(self)
        
        self.headings = []
        self.epsf = []
        self.figs = []
        self.area = self.area()
        self.title = None
        self.logos = talk.logos
        self.text_scale = talk.text_scale
        self.text_textstyle = talk.text_textstyle
        self.text_fg = talk.text_fg
        self.textObjs = []

    def make_logos(self):
        """
        Put the logos on the page
        """
        if len(self.logos) == 0:
            return Area(width=0, height=0)
        elif len(self.logos) == 1:
            return Group(
                Area(width=self.area.width-0.4, height=0),
                self.logos[0]
                )

        width = self.area.width -\
                self.logos[0].bbox().width -\
                self.logos[-1].bbox().width -\
                0.4

        for logo in self.logos[1:-1]:
            width -= logo.bbox().width

        space = width/(len(self.logos)-1)
        a = Align(a1="e", a2="w", angle=90, space=space)
        for logo in self.logos:
            a.append(logo)

        return a

    def add_fig(self, obj, **options):
        """
        Chuck an arbitrary figure onto the page, with a white background
        """

        # there must be a better way to do this!!!
        if options.has_key('e'):
            obj.e = options['e']
        elif options.has_key('se'):
            obj.se = options['se']
        elif options.has_key('s'):
            obj.s = options['s']
        elif options.has_key('sw'):
            obj.sw = options['sw']
        elif options.has_key('w'):
            obj.w = options['w']
        elif options.has_key('nw'):
            obj.nw = options['nw']
        elif options.has_key('n'): 
            obj.n = options['n']
        elif options.has_key('ne'):
            obj.ne = options['ne']
        elif options.has_key('c'):
            obj.c = options['c']
        else:
            obj.sw = P(0.0, 0.0)

        if options.has_key('bg'):
            backColor = options['bg']
        else:
            backColor = Color('white')

        if options.has_key('fg'):
            frontColor = options['fg']
        else:
            frontColor = None

        gutter = 0.1
        back = Rectangle(width=obj.bbox().width+gutter,
                    height=obj.bbox().height+gutter,
                    bg=backColor, fg=frontColor)
        back.sw = obj.bbox().sw-P(gutter/2.0, gutter/2.0)
        self.figs.append(Group(back, obj))

    def set_titlepage(self):
        """
        Set the current slide to be the titlepage
        """
        self.titlepage = True
        return

    def set_title(self, title=None):
        """
        Set the title of the slide
        """
        self.title = title
        return

    def make_title(self, talk):
        """
        Make the title of the slide (note that this is *not* the title of
        the talk)
        """
        if self.title is None or self.title == "":
            #print "######### title None or the empty string #######"
            # this is an ugly hack to try and fix a nasty bug:
            # whenever there isn't a title, or the text of it isn't long
            # enough, the slide is printed portrait once passed through
            # ps2pdf and viewed with xpdf or acroread.  Interestingly
            # enough, the postscript and pdf views fine with gv, and the
            # postscript views fine with pspresent.  Don't know 100% why
            # this is, and can't seem to fix it properly here.
            return TeX("------------------").scale(0.1,0.1)

        # if we just get a string, put it in a TeX object in the current style
        if isinstance(self.title, types.StringType):
            ttext = "%s %s" % (talk.title_textstyle, self.title)
            return TeX(ttext, fg=talk.title_fg).scale(talk.title_scale*0.8,
                                                      talk.title_scale)
        else:
            # just return the object itself
            return self.title
    
    def add_heading(self, level, text):
        """
        Add a heading to the slide

        @param level: the heading level as a number starting from 1 (the most
        significant level)
        @type level: int (1,2,3) or string ("space", "equation")

        @param text: the text to be used for the heading
        @type text: string
        """
        temp = [ level, text ]
        self.headings.append(temp)

    def add_text(self, text, **options):
        """
        Add, and arbitrarily place, text on the slide

        @param text: the text to place
        @type text: string, TeX object or Text object
        """
        # process options
        if options.has_key('bg'):
            backColor = options['bg']
        else:
            backColor = Color('white')

        if options.has_key('fg'):
            frontColor = options['fg']
        else:
            frontColor = self.text_fg

        if options.has_key('scale'):
            scale = options['scale']
        else:
            scale = self.text_scale

        # check for what kind of object we have...
        if isinstance(text, types.StringType):
            # prepend the style if it is just a string
            text = self.text_textstyle + " " + text
            obj = TeX(text, fg=frontColor).scale(scale, scale)
        else:
            raise ValueError, \
                    "Cannot yet handle non-string objects in Slide.add_text()"

        # there must be a better way to do this!!!
        if options.has_key('e'):
            obj.e = options['e']
        elif options.has_key('se'):
            obj.se = options['se']
        elif options.has_key('s'):
            obj.s = options['s']
        elif options.has_key('sw'):
            obj.sw = options['sw']
        elif options.has_key('w'):
            obj.w = options['w']
        elif options.has_key('nw'):
            obj.nw = options['nw']
        elif options.has_key('n'): 
            obj.n = options['n']
        elif options.has_key('ne'):
            obj.ne = options['ne']
        elif options.has_key('c'):
            obj.c = options['c']
        else:
            obj.sw = P(0.0, 0.0)

        #obj = TeX(r"test", fg=frontColor)
        #obj.c = self.area.c

        self.textObjs.append(obj)

    def make_headings(self, talk):
        """
        Make the headings
        """
        heading_block = Align(a1="sw", a2="nw", angle=180, space=0.5)
        for heading in self.headings:
            heading_level = heading[0]
            if not talk.headings_bullets.has_key(heading_level):
                heading_level = "default"
            heading_text = "%s %s"%(talk.headings_textstyle[heading_level]
                                                            , heading[1])
            heading_bullet = talk.headings_bullets[heading_level]
            heading_fg = talk.headings_fgs[heading_level]
            heading_scale = talk.headings_scales[heading_level]
            heading_indent = talk.headings_indent[heading_level]

            tex = Align(a1='ne', a2='nw', angle=90, space=0.2)
            tex.append(heading_bullet)
            tex.append(TeXBox(text=heading_text,
                            fixed_width=self.area.width-5,
                            fg=heading_fg,
                            tex_scale=heading_scale))
 
            padding = Area(sw=tex.sw, width=heading_indent, height=0)
            heading_proper = Align(a1="e", a2="w", angle=90, space=0)
            heading_proper.append(padding, tex)
            heading_block.append(heading_proper)

        return heading_block
            
    def make_waitbar(self, talk):
        """
        Make a waitbar
        """
        waitBarBack = Rectangle(se=self.area.se+P(-0.8, 0.4),
                        width=2.5,
                        height=0.5,
                        r=0.2,
                        fg=talk.waitbar_bg,
                        bg=talk.waitbar_bg)

        offset = 0.05
        waitBarFront = Rectangle(w=waitBarBack.w+P(offset, 0),
                        width=(waitBarBack.width-2*offset)*\
                                self.pageNumber/self.pages,
                        height=waitBarBack.height-2*offset,
                        r=0.2,
                        fg=talk.waitbar_fg,
                        bg=talk.waitbar_fg)
        waitBar = Group(waitBarBack, waitBarFront)
        return  waitBar

    def make_footer(self, talk):
        """
        Make the footer.  A text block giving the title and the name of the
        person giving the talk
        """
        pageOf = False
        if pageOf:
            footerText = " - %s; page %i of %i" %  \
                        (talk.speaker, self.pageNumber, self.pages)
        else:
            footerText = " - %s" % (talk.speaker, )
        
        footer = Align(a1="e", a2="w", angle=90, space=0.1)
        footer.append(TeX(text="%s %s"%(talk.title_textstyle, talk.title),
                        fg=talk.title_fg,
                        ).scale(talk.footerScale, talk.footerScale))
        footer.append(TeX(text="%s %s"%(talk.speaker_textstyle, footerText),
                        fg=talk.title_fg
                        ).scale(talk.footerScale, talk.footerScale))
        footer.sw = self.area.sw+P(0.4, 0.4)
        return footer

    def add_epsf(self, file="", **options):
        """
        Add an eps file to the slide

        @param file: the filename of the eps file
        @type file: string
        
        @keyword width: the width of the image in the current default units.  
        If only this variable is given, then the aspect ratio of the image is
        maintained.

        @keyword height: the height of the image in the current default
        units.  If only this variable is given, then the aspect ratio of 
        the image is maintainted.

        @keyword c, n, ne, e, se, s, sw, w, nw: the location of the anchor point
        """
        if options.has_key('width'):
            picture = Epsf(file, width=options['width'])
        elif options.has_key('height'):
            picture = Epsf(file, height=options['height'])
        elif options.has_key('width') and options.has_key('height'):
            picture = Epsf(file, width=options['width'], 
                    height=options['height'])
        else:
            picture = Epsf(file)

        # there must be a better way to do this!!!
        if options.has_key('e'):
            picture.e = options['e']
        elif options.has_key('se'):
            picture.se = options['se']
        elif options.has_key('s'):
            picture.s = options['s']
        elif options.has_key('sw'):
            picture.sw = options['sw']
        elif options.has_key('w'):
            picture.w = options['w']
        elif options.has_key('nw'):
            picture.nw = options['nw']
        elif options.has_key('n'):
            picture.n = options['n']
        elif options.has_key('ne'):
            picture.ne = options['ne']
        elif options.has_key('c'):
            picture.c = options['c']
        else:
            picture.sw = P(0.0, 0.0)

        offset = 0.2
        background = Rectangle(width=picture.bbox().width+offset,
                                height=picture.bbox().height+offset,
                                bg=Color('white'),
                                fg=Color('white'),
                                )
        background.sw = picture.sw-P(offset/2.0, offset/2.0)
        figure = Group(background, picture)
        self.epsf.append(figure)

    def make_epsf(self):
        """
        Collects all of the eps images together
        """
        pictures = Group()
        for file in self.epsf:
            pictures.append(file)
        return pictures

    def make_figs(self):
        """
        Collects all of the figures together
        """
        figs = Group()
        for fig in self.figs:
            figs.append(fig)
        return figs

    def make_textObjs(self):
        """
        Collects all the text objects together
        """
        textObjs = Group()
        for text in self.textObjs:
            textObjs.append(text)
        return textObjs

    def make_titlepage(self, talk):
        """
        Makes the titlepage of the talk
        """
        titlepage = Align(a1="s", a2="n", angle=180, space=0.4)

        if isinstance(talk.title, types.StringType):
            ttext = "%s %s" % (talk.title_textstyle, talk.title)
            titlepage.append(TeX(ttext,
                                fg=talk.title_fg)\
                                .scale(talk.title_scale, talk.title_scale))
        else:
            #raise ValueError, "Can't yet handle non-string arguments")
            titlepage.append(Text(ttext))

        if talk.authors is not None:
            titlepage.append(talk.make_authors())
        if talk.address is not None:
            titlepage.append(talk.make_address())

        return titlepage

    def make_background(self, talk):
        """
        Makes the background of the slide
        """
        back = Group()
        back.append(Rectangle(sw=self.area.sw,
                        width=self.area.width,
                        height=self.area.height,
                        fg=None,
                        bg=talk.bg,
                        )
                    )
        back.append(Rectangle(sw=self.area.sw,
                        width=2.5,
                        height=self.area.height,
                        fg=None,
                        bg=talk.bg*0.5,
                        )
                    )
        back.append(Rectangle(sw=self.area.sw,
                        width=self.area.width,
                        height=1.5,
                        fg=None,
                        bg=talk.bg*0.5,
                        )
                    )
        back.append(Rectangle(nw=self.area.nw,
                        width=self.area.width,
                        height=2.5,
                        fg=None,
                        bg=talk.bg*0.5,
                        )
                    )
        back.append(Rectangle(nw=self.area.nw,
                        width=2.5,
                        height=2.5,
                        fg=None,
                        bg=Color('firebrick'),
                        )
                    )

        return back
        
    def make(self, talk, scale=1):
        """
        Make the slide.  Collect all of the objects together into one Page()
        object ready for rendering.
        """
        
        if self.titlepage:
            all = self.make_titlepage(talk)
            all.c = self.area.c + P(0.0, 0.8)
        else:
            all = Align(a1="s", a2="n", angle=180, space=0.4)
            all.append(self.make_title(talk))
            all.nw = self.area.nw + P(2.5, -0.2)

        # I'm aware that this isn't a good way to do this, but
        # it's late at night, and I want to get *something* going

        headings = self.make_headings(talk)
        headings.nw = self.area.nw + P(3.0, -3.0)
    
        back = self.make_background(talk)

        p = self.area.se + P(-0.1, 0.1)
        signature = Text(
                'Created with PyScript.  http://pyscript.sourceforge.net', 
                size=15, 
                sw=p, 
                fg=talk.bg*0.8
                ).rotate(-90, p)

        logos = self.make_logos()
        logos.nw = self.area.nw + P(0.2,-0.2)

        self.pages = len(talk.slides)

        All = Group(
                back,
                all,
                headings,
                self.make_epsf(),
                self.make_figs(),
                self.make_textObjs(),
                signature,
                self.make_footer(talk),
                logos,
                self.make_waitbar(talk)
                ).scale(scale, scale)

        return Page(All, orientation=self.orientation)

# vim: expandtab shiftwidth=4:
