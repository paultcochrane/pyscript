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
