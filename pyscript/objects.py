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

"""
Base objects
"""
import os,string,re
import cStringIO,commands

from types import *

from math import cos,sin,pi

from defaults import *
from util import *
from vectors import *

from base import PsObj,Color


from functions import *

from afm import AFM

# -------------------------------------------------------------------------
# XXX
from base import PsDict
class PsObject: pass


# -------------------------------------------------------------------------
class AffineObj(PsObj):
    '''
    A base class for object that should implement affine
    transformations, this should apply to any object that draws
    on the page.
    '''

    o=P(0,0)
    T=Matrix(1,0,0,1)

    def concat(self,t,p=None):
        '''
        concat matrix t to tranformation matrix
        @param t: a 2x2 Matrix dectribing Affine transformation
        @param p: the origin for the transformation
        @return: reference to self
        '''

        self.T=t*self.T

        if p is not None:
            o=self.o # o is in external co-ords
            self.move(p-o)
            self.move(t*(o-p))
        
        return self

    def move(self,*args):
        '''
        translate object by a certain amount
        @param args: amount to move by, can be given as
         - dx,dy
         - P
        @return: reference to self
        '''
        if len(args)==1:
            # assume we have a point
            self.o+=args[0]
        else:
            # assume we have dx,dy
            self.o+=P(args[0],args[1])

    	return self
	    
    def rotate(self,angle,p=None):
        """
        rotate object, 
        the rotation is around p when supplied otherwise
        it's the objects origin

        @param angle: angle in degrees, clockwise
        @param p: point to rotate around (external co-ords)
        @return: reference to self
        """ 
        angle=angle/180.0*pi # convert angle to radians
        t=Matrix(cos(angle),sin(angle),-sin(angle),cos(angle))
        self.concat(t,p)

        return self

    def scale(self,sx,sy,p=None):
        '''
        scale object size (towards objects origin or p)
        @param sx sy: scale factors for each axis
        @param p: point around which to scale
        @return: reference to self
        '''

        t=Matrix(sx,0,0,sy)
        self.concat(t,p)
        
        return self

        
    def itoe(self,p_i):
        '''
        convert internal to external co-ords
        @param p_i: intrnal co-ordinate
        @return: external co-ordinate
        '''
        assert isinstance(p_i,P), "object not a P()"

        return self.T*p_i+self.o
        
    def etoi(self,p_e):
        '''
        convert external to internal co-ords
        @param p_e: external co-ordinate
        @return: internal co-ordinate
        '''
        assert isinstance(p_e,P), "object not a P()"

        return self.T.inverse()*(p_e-self.o)


    def prebody(self):
        '''
        set up transformation of coordinate system
        '''
        T=self.T
        o=self.o
        S="gsave "
        if T==Matrix(1,0,0,1):
            S=S+"%s translate\n"%o
        else:
            # NB postscript matrix is the transpose of what you'd expect!
            S=S+"[%g %g %g %g %s] concat\n"%(T[0],T[2],T[1],T[3],o())
        return S

    def postbody(self):
        '''
        undo coordinate system transformation
        '''
        return "grestore\n"


# -------------------------------------------------------------------------

class Area(AffineObj):
    """
    A Rectangular area defined by sw corner and width and height.
    
    defines the following compass points that can be set and retrived::

          nw--n--ne
          |       |
          w   c   e
          |       |
          sw--s--se

    The origin is the sw corner and the others are calculated from the
    width and height attributes.

    If a subclass should have the origin somewhere other than sw then
    overide the sw attribute to make it a function
    """

    #XXX allow the changing of sw corner away from origin eg Text

    sw=P(0,0)
    width=0
    height=0


    # Dynamic locations
    def _get_n(s):
        return s.itoe(P(s.width/2.,s.height))
    def _set_n(s,pe):
        s.move(pe-s.n)
    n = property(_get_n,_set_n)

    def _get_ne(s):
        return s.itoe(P(s.width,s.height))
    def _set_ne(s,pe):
        s.move(pe-s.ne)
    ne = property(_get_ne,_set_ne)

    def _get_e(s):
        return s.itoe(P(s.width,s.height/2.))
    def _set_e(s,pe):
        s.move(pe-s.e)
    e = property(_get_e,_set_e)

    def _get_se(s):
        return s.itoe(P(s.width,0))
    def _set_se(s,pe):
        s.move(pe-s.se)
    se = property(_get_se,_set_se)

    def _get_s(s):
        return s.itoe(P(s.width/2.,0))
    def _set_s(s,pe):
        s.move(pe-s.s)
    s = property(_get_s,_set_s)

    def _get_sw(s):
        return s.itoe(P(0,0))
    def _set_sw(s,pe):
        s.move(pe-s.sw)
    sw = property(_get_sw,_set_sw)

    def _get_w(s):
        return s.itoe(P(0,s.height/2.))
    def _set_w(s,pe):
        s.move(pe-s.w)
    w = property(_get_w,_set_w)

    def _get_nw(s):
        return s.itoe(P(0,s.height))
    def _set_nw(s,pe):
        s.move(pe-s.nw)
    nw = property(_get_nw,_set_nw)

    def _get_c(s):
        return s.itoe(P(s.width/2.,s.height/2.))
    def _set_c(s,pe):
        s.move(pe-s.c)
    c = property(_get_c,_set_c)

    def bbox(self):

        x1,y1=self.sw
        x2,y2=self.ne

        for p in [self.sw,self.nw,self.ne,self.se]:
            x1=min(x1,p[0])
            y1=min(y1,p[1])
            x2=max(x2,p[0])
            y2=max(y2,p[1])

        return Bbox(sw=P(x1,y1),width=x2-x1,height=y2-y1)

# -------------------------------------------------------------------------
# A TeX expression
# parses the output of dvips
# -------------------------------------------------------------------------
class TeX(Area):
    '''
    an Area object with a TeX expression within

    requires working latex and dvips systems
    
    '''

    text=""
    fg=Color(0)

    def __init__(self,text="",**dict):

        self.text=text


        TMP="temp"
        fp=open("%s.tex"%TMP,"w")
        fp.write(defaults.tex_head)
        fp.write(text)
        fp.write(defaults.tex_tail)
        fp.close()

        os.system(defaults.tex_command%TMP)

        os.system("dvips -h - -E -o %s.eps %s.dvi"%(TMP,TMP))
    
        fp=open("%s.eps"%TMP,"r")
        eps=fp.read(-1)
        fp.close()
    
        # grab boundingbox
        bbox_so=re.search("\%\%boundingbox:\s+(\d+)\s+(\d+)\s+(\d+)\s+(\d+)",
                          eps,re.I)
        bbox=[]
        for ii in bbox_so.groups():
            bbox.append(int(ii))

        self.width=(bbox[2]-bbox[0])/float(defaults.units)
        self.height=(bbox[3]-bbox[1])/float(defaults.units)

        apply(Area.__init__,(self,),dict)

        self.offset=-P(bbox[0],bbox[1])/float(defaults.units)
        # grab font encoding
        so=re.search("^(TeXDict begin \d.*?)\s*end",eps,re.S|re.M)
        fonts=so.group(1)
        
        # grab body (ignoring procsets and fonts)
        so=re.search("\%\%EndSetup\s*(.*?)\s*\%\%Trailer",eps,re.S)
        body=so.group(1)
        # clean it up a bit and add fonts
        body="%s\nTeXDict begin\n%s\nend\n"%(fonts,string.strip(body))

        self.bodyps=body
        


    def body(self):
        out=cStringIO.StringIO()

        out.write("%s translate "%self.offset)
        out.write("%s\n"%self.fg)
        out.write("%s\n"%self.bodyps)
        return out.getvalue()


# -------------------------------------------------------------------------

class Text(Area):
    '''
    A single line text object within an Area object
    '''
    
    text=''
    font="Times-Roman"
    size=12
    fg=Color(0)
    bg=None
    kerning=1
    
    def __init__(self,text="",**dict):
        '''
        @param text: the string to typeset
        @param dict:
         - font:one of the standard postscript fonts eg "Times-Roman"
         - scale: a number giving the pointsize of the font
         - fg: color object
        '''

        self.text=text


        # get the bbox
        # first need font and scale
        # Can't use base mechanism ... property items might get called
        self.font=dict.get('font',self.font)
        self.size=dict.get('size',self.size)
        self.kerning=dict.get('kerning',self.kerning)

        settext,x1,y1,x2,y2=self._typeset(text)

        self.settext=settext
        self.offset=-P(x1,y1)/float(defaults.units)
        self.width=(x2-x1)/float(defaults.units)
        self.height=(y2-y1)/float(defaults.units)

        apply(Area.__init__,(self,),dict)

    def _typeset(self,string):
        
        font=AFM(self.font)
        size=self.size
        sc=size/1000.


	chars=map(ord,list(string))

	# order: width l b r t

	# use 'reduce' and 'map' as they're written in C

	# add up all the widths
	width= reduce(lambda x, y: x+font[y][0],chars,0)

	# subtract the kerning
        if self.kerning==1:
            if len(chars)>1:
                kerns=map(lambda x,y:font[(x,y)] ,chars[:-1],chars[1:])
                
                charlist=list(string)

                out="("
                for ii in kerns:
                    if ii!=0:
                        out+=charlist.pop(0)+") %s ("%str(ii*sc)
                    else:
                        out+=charlist.pop(0)
                out+=charlist.pop(0)+")"
                
                settext=out

                kern=reduce(lambda x,y:x+y,kerns)
                            
                width+=kern
            else:
                # this is to catch the case when there are no characters
                # in the string, but self.kerning==1
                settext="("+string+")"

        else:
            settext="("+string+")"

	# get rid of the end bits
	start=font[chars[0]][1]
	f=font[chars[-1]]
	width = width-start-(f[0]-f[3])

	# accumulate maximum height
	top = reduce(lambda x, y: max(x,font[y][4]),chars,0)

	# accumulate lowest point
	bottom = reduce(lambda x, y: min(x,font[y][2]),chars,font[chars[0]][2])

	xl=start*sc
	yb=bottom*sc
	xr=xl+width*sc
	yt=top*sc

        return settext,xl,yb,xr,yt
        

    def body(self):
        out=cStringIO.StringIO()

        ATTR={'font':self.font,
              'size':self.size,
              'fg':self.fg,
              'settext':self.settext,
              'offset':self.offset}
        
        out.write("%(offset)s moveto\n"%ATTR)
        out.write("/%(font)s %(size)s selectfont %(fg)s \n"%ATTR)
        out.write("mark %(settext)s kernshow\n"%ATTR)
        
        return out.getvalue()


# -------------------------------------------------------------------------
# Text class ... requires 'gs -sDEVICE=bbox'
# -------------------------------------------------------------------------
##class Text_gs_XXX(Area):
##    '''
##    single line text object that requires "gs -sDEVICE=bbox"
##    '''
        
##    def __init__(self,text="",**dict):

##        # this is a bit ugly ... we need a
##        # minimal text object with no transformations
##        # in order to grab the bounding box
        
##        font="Times-Roman"
##        scale=12
##        if dict.has_key('font'): font=dict['font']
##        if dict.has_key('scale'): font=dict['scale']

##        temp=Text_nobbox(text=text,scale=scale,font=font)

##        # get the bbox
##        SW,NE=gsbbox(temp)

##        # Now create the real text object
##        self.natives(dict,
##                     bg=None,
##                     fg=Color(0),
##                     text=text,
##                     font="Times-Roman",
##                     scale=12,
##                     width=NE[0]-SW[0],
##                     height=NE[1]-SW[1],
##                     )

##        self.offset=-SW

##        apply(Area.__init__,(self,),dict)


##    def body(self):
##        out=cStringIO.StringIO()
        
##        out.write("%s moveto\n"%self.offset)
##        out.write("/%(font)s findfont\n%(scale)d scalefont setfont\n"%self)
##        out.write("%(fg)s (%(text)s) show\n"%self)
        
##        return out.getvalue()



# -------------------------------------------------------------------------
# Text class that has 1pp bounding box ...
# (but doesn't rely on gs)
# -------------------------------------------------------------------------

##class Text_nobbox_XXX(PsObject):
##    """
##    Text class with broken bbox
##    (doesn't require gs)
##    """
##    def __init__(self,text="",**dict):

##        self.natives(dict,
##                     bg=None,
##                     fg=Color(0),
##                     o=P(0,0),
##                     text=text,
##                     font="Helvetica",
##                     scale=12
##                     )
##        apply(PsObject.__init__,(self,),dict)

##    def body(self):
##        out=cStringIO.StringIO()
        
##        out.write("0 0 moveto\n")
##        out.write("/%(font)s findfont\n%(scale)d scalefont setfont\n"%self)
##        out.write("%(fg)s (%(text)s) show\n"%self)
        
##        return out.getvalue()

##    def bbox(self):
##        "return objects bounding box"

##        # return corners for now + 1point to take
##        # into account the line widths
##        sw = self["o"]-R(1,1)*(1/float(defaults.units))
##        ne = self["o"]+R(1,1)*(1/float(defaults.units))
##        return (sw,ne)

# -------------------------------------------------------------------------
# Rectangle
# -------------------------------------------------------------------------
class Rectangle(Area):
    """
    Draw a rectangle 

        @param dict:
                     - linewidth: the line thickness in points
                     - dash: the dash pattern to use (string ala postscript)
                     - fg: line color
                     - bg: fill color or None for empty

    """
    bg=None
    fg=Color(0)
    linewidth=defaults.linewidth
    dash=defaults.dash

    def body(self):
        
        out=cStringIO.StringIO()
        
        if self.linewidth!=defaults.linewidth:
            out.write("%f setlinewidth "%self.linewidth)

        if self.dash!=defaults.dash:
            out.write("%s setdash "%self.dash)
        
        ATTR={'bg':self.bg,
              'fg':self.fg,
              'width':self.width,
              'height':self.height}
        
        if self.bg is not None:
            out.write("%(bg)s 0 0 %(width)g uu %(height)g uu rectfill\n"%ATTR)
        if self.fg is not None:
            out.write("%(fg)s 0 0 %(width)g uu %(height)g uu rectstroke\n"%ATTR)
                        
        return out.getvalue()


# -------------------------------------------------------------------------
class Circle(AffineObj):
    """
    Draw a circle, or part of

    get ellipses by scaling. The origin is the center
    
        @param dict:
                     - r: radius
                     - start: starting angle for arc
                     - end: end angle for arc
                     - c, n, ne, ... as for L{Area.__init__} but on circumference
                     - fg,bg:  foreground and background colors
                     - linewidth, dash: usual
    """


    bg=None
    fg=Color(0)
    r=1.0
    start=0
    end=360
    linewidth=defaults.linewidth
    dash=defaults.dash
    

    def locus(self,angle):
        '''
        return a point on the edge at a particular angle
        (degrees, clockwise from vertical)
        '''
        r=self.r
        x=r*sin(angle/180.0*pi)
        y=r*cos(angle/180.0*pi)

        return self.itoe(P(x,y))

    def __getitem__(self,i):
        '''
        Get a point on the circumference
        
        @param i: an angle in degrees
        @return: point on circumference at that angle
                       (degrees clockwise from north)
        '''

        return self.locus(i)  
    
    def __setitem__(self,i,other):
        '''
        Set a point on the circumference
        '''

        pcurrent=self.locus(i)

        self.move(other-pcurrent)
        return self

    # some named locations
    def _get_n(s):
        return s[0]
    def _set_n(s,pe):
        s[0]=pe
    n = property(_get_n,_set_n)

    def _get_ne(s):
        return s[45]
    def _set_ne(s,pe):
        s[45]=pe
    ne = property(_get_ne,_set_ne)

    def _get_e(s):
        return s[90]
    def _set_e(s,pe):
        s[90]=pe
    e = property(_get_e,_set_e)

    def _get_se(s):
        return s[135]
    def _set_se(s,pe):
        s[135]=pe
    se = property(_get_se,_set_se)

    def _get_s(s):
        return s[180]
    def _set_s(s,pe):
        s[180]=pe
    s = property(_get_s,_set_s)

    def _get_sw(s):
        return s[235]
    def _set_sw(s,pe):
        s[235]=pe
    sw = property(_get_sw,_set_sw)

    def _get_w(s):
        return s[270]
    def _set_w(s,pe):
        s[270]=pe
    w = property(_get_w,_set_w)

    def _get_nw(s):
        return s[315]
    def _set_nw(s,pe):
        s[315]=pe
    nw = property(_get_nw,_set_nw)

    def _get_c(s):
        return s.o
    def _set_c(s,pe):
        s.move(pe-s.o)
    c = property(_get_c,_set_c)

    def body(self):

        out = cStringIO.StringIO()

        if self.linewidth!=defaults.linewidth:
            out.write("%f setlinewidth "%self.linewidth)

        if self.dash!=defaults.dash:
            out.write("%s setdash "%self.dash)

        # By default postscript goes anti-clockwise
        # and starts from 'e' ... fix it so it goes
        # clockwise and starts from 'n'

        ATTR={'bg':self.bg,
              'fg':self.fg,
              'r':self.r,
              'start':self.start,
              'end':self.end}

        if self.bg is not None:
            out.write("%(bg)s 0 0 %(r)g uu 360 %(start)g -1 mul add 90 add 360 %(end)g -1 mul add 90 add arcn fill\n" % ATTR)

        if self.fg is not None:
            out.write("%(fg)s 0 0 %(r)g uu 360 %(start)g -1 mul add 90 add 360 %(end)g -1 mul add 90 add arcn stroke\n" % ATTR)

        return out.getvalue()


    def bbox(self):

        #grab a tight boundingbox by zipping around circumference

        SW=self.locus(0)
        NE=self.locus(0)
        for ii in xrange(self.start,self.end+10,10):
            p=self.locus(ii)

            SW[0]=min(SW[0],p[0])
            SW[1]=min(SW[1],p[1])
            NE[0]=max(NE[0],p[0])
            NE[1]=max(NE[1],p[1])


        return Bbox(sw=SW,width=NE[0]-SW[0],height=NE[1]-SW[1])

# -------------------------------------------------------------------------
class Dot(Circle):
    '''
    draw a dot at the given location
    '''
    r=.05
    bg=Color(0)
    fg=None

    def __init__(self,c,**dict):
        apply(Circle.__init__,(self,),dict)
        self.c=c

# -------------------------------------------------------------------------
# Path elements
# -------------------------------------------------------------------------

class C:
    """
    Defines control points for besier spline
    """

    def __init__(self,*points):

        self.points=points
        if len(points)==1:
            self.c1=points[0]
            self.c2=points[0]
        elif len(points)==2:
            if type(points[0])==type(P()):
                self.c1=points[0]
                self.c2=points[1]
            else:
                self.c1=P(points[0],points[1])
                self.c2=P(points[0],points[1])
        elif len(points)==4:
            self.c1=P(points[0],points[1])
            self.c2=P(points[2],points[3])
            
        else:
            raise "Don't inderstand arguments to C()"

    def copy(self):
        return copy.deepcopy(self)

    def controls(self):
        # is this necessary?
        return self.c1,self.c2

class Path(Area):
    """
    A Path
    """
    
    fg=Color(0)
    bg=None
    linewidth=defaults.linewidth
    linecap=defaults.linecap
    linejoin=defaults.linejoin
    miterlimit=defaults.miterlimit
    dash=defaults.dash
    
    def __init__(self,*path,**dict):

        apply(Area.__init__,(self,),dict)

        if len(path)==0:
            path=[P(0,0),P(0,0)]
        else:
            path=list(path)

#        path=self.make_relative(path)
        sw,ne=self.extent(path)
        self.offset=-sw

        self.sw=sw
        self.width=ne[0]-sw[0]
        self.height=ne[1]-sw[1]
        self.path=path
        

    def closed(self):
        "Is the path a closed one?"
        p=self.path
        if isinstance(p[-1],C) or p[-1] is p[0]:
            return 1
        else:
            return 0
                
    def _get_start(self):
        "return start point"
        return self.path[0]

    def _get_end(self):
        "return end point"
        P=self.path
        p=P[-1]
        if isinstance(p,C):
            p=P[0]
        return p
        
    def body(self):

        out=cStringIO.StringIO()

        path=self.path[:]

        out.write("%s translate "%self.offset)


        if self.linewidth!=defaults.linewidth:
            out.write("%f setlinewidth "%self.linewidth)

        if self.linecap!=defaults.linecap:
            out.write("%d setlinecap "%self.linecap)
            
        if self.linejoin!=defaults.linejoin:
            out.write("%d setlinejoin "%self.linejoin)

        if self.miterlimit!=defaults.miterlimit:
            out.write("%f setmiterlimit "%self.miterlimit)

        if self.dash!=defaults.dash:
            out.write("%s setdash "%self.dash)

        out.write("newpath %s moveto\n"%path[0])

        p=None
        while len(path)>1:
            pp=p
            p=path.pop(1)
            if isinstance(p,P):
                out.write("%s lineto\n"%p)
            elif isinstance(p,C):
                c1,c2=p.controls()
                pn=path.pop(1%len(path))
                out.write("%s %s %s curveto\n"%(c1,c2,pn))

        if self.closed():
            out.write(' closepath ')

        
        if self.bg is not None:
            out.write("gsave %s fill grestore\n"%self.bg)
        
        if self.fg is not None:
            out.write("%s stroke\n"%self.fg)

        return out.getvalue()


#    def make_relative(self,path):
#        "Return a path with all relative elements"
#        return path

    def extent(self,path):
        "a boundingbox in internal co-ords"

        # first collect a whole lot of points on the path
        boundpoints=[]
        L=len(path)
        for ii in range(L):
            p=path[ii]
            if isinstance(p,P):
                boundpoints.append(p)
            elif isinstance(p,C):
                pn=path[(ii+1)%L]
                pp=path[(ii-1)%L]
                assert isinstance(pn,P)
                c1,c2=p.controls()
                if c1==None or c2==None: continue

                divisions=10
                for d in range(1,divisions):
                    t=d/float(divisions)
                    p=(1-t)**3*pp+3*(1-t)**2*t*c1+3*(1-t)*t**2*c2+t**3*pn
                    boundpoints.append(p)
                    

        SW=boundpoints[0].copy()
        NE=boundpoints[0].copy()
        #SW=P(0,0)
        #NE=P(0,0)
        #NE[0]=SW[0]=boundpoints[0][0]
        #NE[1]=SW[1]=boundpoints[0][1]


        for p in boundpoints:
            SW[0]=min(SW[0],p[0])
            SW[1]=min(SW[1],p[1])
            NE[0]=max(NE[0],p[0])
            NE[1]=max(NE[1],p[1])

        return SW,NE

# -------------------------------------------------------------------------

class Group(AffineObj):
    """
    Groups together a list of objects
    """
    
    def __init__(self,*objects,**dict):
        if len(objects)==1 and type(objects[0]) in (TupleType,ListType):
            self.objects=list(objects[0])
        else:
            self.objects=list(objects)

        apply(PsObj.__init__,(self,),dict)

    def __getitem__(self,i):
        return self.objects[i]
        
    def __setitem__(self,i,other):
        self.objects[i]=other

    def __getslice__(self,i,j):
        return self.objects[i:j]

    def __setslice__(self,i,j,wert):
        self.objects[i:j]=wert

    def append(self,*objs):
        '''
        append object(s) to group
        '''
	for obj in objs:
	    self.objects.append(obj)

    def bbox(self):
        """
        Gather together common bounding box for group
        """

        # We need to do the calculation in the 
        # external co-ordinates (that's where the
        # bounding box will be used)

        # first a null Bbox
        bbox=Bbox()
        
        for obj in self.objects:
            bbox.union(obj.bbox(),self.itoe)

        return bbox

    def body(self):
        out=cStringIO.StringIO()
        for obj in self.objects:
            out.write(str(obj))
        return out.getvalue()
    

class Paper(Area):
    '''
    returns an area object the size of one of the standard paper sizes
    '''

    # PAPERSIZES taken from gs man page (x cm,y cm)
    PAPERSIZES={
        "a0":         (83.9611   ,118.816),
        "a1":         (59.4078   ,83.9611),
        "a2":         (41.9806   ,59.4078),
        "a3":         (29.7039   ,41.9806),
        "a4":         (20.9903   ,29.7039),
        "a5":         (14.8519   ,20.9903),
        "a6":         (10.4775   ,14.8519),
        "a7":         (7.40833   ,10.4775),
        "a8":         (5.22111   ,7.40833),
        "a9":         (3.70417   ,5.22111),
        "a10":        (2.61056   ,3.70417),
        "b0":         (100.048   ,141.393),
        "b1":         (70.6967   ,100.048),
        "b2":         (50.0239   ,70.6967),
        "b3":         (35.3483   ,50.0239),
        "b4":         (25.0119   ,35.3483),
        "b5":         (17.6742   ,25.0119),
        "archA":      (22.86     ,30.48),
        "archB":      (30.48     ,45.72),
        "archC":      (45.72     ,60.96),
        "archD":      (60.96     ,91.44),
        "archE":      (91.44     ,121.92),
        "flsa":       (21.59     ,33.02),
        "flse":       (21.59     ,33.02),
        "halfletter": (13.97     ,21.59),
        "note":       (19.05     ,25.4 ),
        "letter":     (21.59     ,27.94),
        "legal":      (21.59     ,35.56),
        "11x17":      (27.94     ,43.18),
        "ledger":     (43.18     ,27.94),
        }

    def __init__(self,size,**dict):
        '''
        @param size: eg "a4","letter" etc. See L{PAPERSIZES} for sizes
        @return: An area object the size of the selected paper
                 with the sw corner on P(0,0)
        '''

        
        w,h=self.PAPERSIZES[size]
        
        self.width=w*UNITS['cm']/float(defaults.units)
        self.height=h*UNITS['cm']/float(defaults.units)

        apply(Area.__init__,(self,),dict)


class Epsf(Area):

    bbox_so=re.compile("\%\%boundingbox:\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)\s+(-?\d+)",re.I|re.S)

    linewidth=defaults.linewidth
    dash=defaults.dash
    fg=Color(0)


    def __init__(self,file,**dict):
        '''
        @param file: path to epsf file
        @return: The eps figure as an area object
        '''

        self.file=file

        fp=open(file,'r')
        self.all=fp.read(-1)
        fp.close()

        so=self.bbox_so.search(self.all)
        x1s,y1s,x2s,y2s=so.groups()

        d=float(defaults.units)
        x1=float(x1s)/d
        y1=float(y1s)/d
        x2=float(x2s)/d
        y2=float(y2s)/d

        print x1,y1,x2,y2
        self.offset=-P(x1,y1)
        print self.offset
        
        self.width=x2-x1
        self.height=y2-y1
        print self.width,self.height

        apply(Area.__init__,(self,),dict)
    

    def body(self):
        
        out=cStringIO.StringIO()
        
        if self.linewidth!=defaults.linewidth:
            out.write("%f setlinewidth "%self.linewidth)

        if self.dash!=defaults.dash:
            out.write("%s setdash "%self.dash)
        
        
        if self.fg is not None:
            out.write("%s\n"%self.fg)
            
        out.write("%s translate \n\n"%self.offset)

        out.write("%%%%BeginDocument: %s\n"%self.file)
        out.write(self.all)
        
        return out.getvalue()













