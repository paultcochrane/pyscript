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

from base import *

from functions import *

import afm

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

class PsObject(PsDict):
    """
    A generic Postscript object
    """
    type="PsObject"

    def __init__(self,**dict):
        self.natives(dict,
                     o=P(0,0),
                     T=Matrix(1,0,0,1),
                     )
        apply(PsDict.__init__,(self,),dict)

    def concat(self,t,p=None):
        '''
        concat t to tranformation matrix
        @param t: a 2x2 Matrix dectribing Affine transformation
        @param p: the origin for the transformation
        @return: reference to self
        '''

        T=self["T"]
        self["T"]=t*T

        if p is not None:
            o=self['o'] # this is in external co-ords
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
            self['o']=self['o']+args[0]
        else:
            # assume we have dx,dy
            self["o"]=self["o"]+P(args[0],args[1])

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
        angle=angle/180.0*pi
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
        return self['T']*p_i+self['o']
        
    def etoi(self,p_e):
        '''
        convert external to internal co-ords
        @param p_e: external co-ordinate
        @return: internal co-ordinate
        '''
        return self['T'].inverse()*(p_e-self['o'])

    def prebody(self):
        T=self["T"]
        o=self["o"]
        S="gsave "
        if T==Matrix(1,0,0,1):
            S=S+"%s translate\n"%o 
        else:
            # NB postscript matrix is the transpose of what you'd expect!
            S=S+"[%g %g %g %g %s] concat\n"%(T[0],T[2],T[1],T[3],o)
        return S

    def body(self):
        return ""

    def postbody(self):
        return "grestore\n"

    def __str__(self):
        "return postscript as string"
        return self.prebody()+self.body()+self.postbody()


    def boundingbox(self):
        "return objects bounding box"
        
        # should be dynamically calculated and take
        # into account transformation matrix
        
        raise "Needs to be overridden!"

# -------------------------------------------------------------------------

class Area(PsObject):
    """
    A Rectangular area.
    
    defines the following compass points that can be set and retrived::

          nw--n--ne
          |       |
          w   c   e
          |       |
          sw--s--se

    The origin is the sw corner and the others are calculated from the
    width and height attributes
    """
    type="Area"

    def __init__(self,**dict):
        self.natives(dict,width=0,height=0)
        apply(PsObject.__init__,(self,),dict)

        # Dynamic locations ... retrival
    def _get_w(s):
        return s.itoe(P(0,s["height"]/2.))
    def _get_nw(s):
        return s.itoe(P(0,s["height"]))
    def _get_s(s):
        return s.itoe(P(s["width"]/2.,0))
    def _get_sw(s):
        return s.itoe(P(0,0))
    def _get_se(s):
        return s.itoe(P(s["width"],0))
    def _get_e(s):
        return s.itoe(P(s["width"],s["height"]/2.))
    def _get_ne(s):
        return s.itoe(P(s["width"],s["height"]))
    def _get_n(s):
        return s.itoe(P(s["width"]/2.,s["height"]))
    def _get_c(s):
        return s.itoe(P(s["width"]/2.,s["height"]/2.))


    # Dynamic locations ... setting
    def _set_n(s,pe):
        s.move(pe-s['n'])
    def _set_ne(s,pe):
        s.move(pe-s['ne'])
    def _set_e(s,pe):
        s.move(pe-s['e'])
    def _set_se(s,pe):
        s.move(pe-s['se'])
    def _set_s(s,pe):
        s.move(pe-s['s'])
    def _set_sw(s,pe):
        s.move(pe-s['sw'])
    def _set_w(s,pe):
        s.move(pe-s['w'])
    def _set_nw(s,pe):
        s.move(pe-s['nw'])
    def _set_c(s,pe):
        s.move(pe-s['c'])

    def boundingbox(self):

        SW=self['sw'].copy()
        NE=self['ne'].copy()
        for p in [self['sw'],self['nw'],self['ne'],self['se']]:
            SW[0]=min(SW[0],p[0])
            SW[1]=min(SW[1],p[1])
            NE[0]=max(NE[0],p[0])
            NE[1]=max(NE[1],p[1])


        return (SW,NE)

# -------------------------------------------------------------------------
# A TeX expression
# parses the output of dvips
# -------------------------------------------------------------------------
class TeX(Area):
    '''
    an Area object with a TeX expression within

    requires working latex and dvips systems
    
    '''
    type="TeX"

    def __init__(self,text="",**dict):

        TMP="temp"
        fp=open("%s.tex"%TMP,"w")
        fp.write(defaults.tex_head)
        fp.write(text)
        fp.write(defaults.tex_tail)
        fp.close()
        self.text=text

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

        self.natives(dict,
                     width=(bbox[2]-bbox[0])/float(defaults.units),
                     height=(bbox[3]-bbox[1])/float(defaults.units),
                     fg=Color(0)
                     )
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
        out.write("%s\n"%self['fg'])
        out.write("%s\n"%self.bodyps)
        return out.getvalue()


# -------------------------------------------------------------------------

class Text(Area):
    '''
    A single line text object within an Area object
    '''
        
    def __init__(self,text="",**dict):
        '''
        @param text: the string to typeset
        @param dict:
         - font:one of the standard postscript fonts eg "Times-Roman"
         - scale: a number giving the pointsize of the font
         - fg: color object
        '''

        # get the bbox
        # first need font and scale
        fontname=dict.get('font',"Times-Roman")
        scale=dict.get('scale',12)

        font=afm.load(fontname)

        x1,y1,x2,y2=font.boundingbox(text,scale=scale)

        # Now create the real text object
        self.natives(dict,
                     bg=None,
                     fg=Color(0),
                     text=text,
                     font="Times-Roman",
                     scale="12",
                     width=(x2-x1)/float(defaults.units),
                     height=(y2-y1)/float(defaults.units),
                     )

        self.offset=-P(x1,y1)/float(defaults.units)

        apply(Area.__init__,(self,),dict)


    def body(self):
        out=cStringIO.StringIO()
        
        out.write("%s moveto\n"%self.offset)
        out.write("/%(font)s findfont\n%(scale)s scalefont setfont\n"%self)
        out.write("%(fg)s (%(text)s) show\n"%self)
        
        return out.getvalue()

# -------------------------------------------------------------------------
# Text class ... requires 'gs -sDEVICE=bbox'
# -------------------------------------------------------------------------
class Text_gs(Area):
    '''
    single line text object that requires "gs -sDEVICE=bbox"
    '''
        
    def __init__(self,text="",**dict):

        # this is a bit ugly ... we need a
        # minimal text object with no transformations
        # in order to grab the bounding box
        
        font="Times-Roman"
        scale=12
        if dict.has_key('font'): font=dict['font']
        if dict.has_key('scale'): font=dict['scale']

        temp=Text_nobbox(text=text,scale=scale,font=font)

        # get the bbox
        SW,NE=gsbbox(temp)

        # Now create the real text object
        self.natives(dict,
                     bg=None,
                     fg=Color(0),
                     text=text,
                     font="Times-Roman",
                     scale=12,
                     width=NE[0]-SW[0],
                     height=NE[1]-SW[1],
                     )

        self.offset=-SW

        apply(Area.__init__,(self,),dict)


    def body(self):
        out=cStringIO.StringIO()
        
        out.write("%s moveto\n"%self.offset)
        out.write("/%(font)s findfont\n%(scale)d scalefont setfont\n"%self)
        out.write("%(fg)s (%(text)s) show\n"%self)
        
        return out.getvalue()


# -------------------------------------------------------------------------
# Text class with alternative calculation of bbox ....
# doesn't rely on gs -bbox  but requires postscript level 2 ?
# -------------------------------------------------------------------------

class Text_alt(Area):
        
    def __init__(self,text="",**dict):

        # get the bbox
        # first need font and scale
        font=dict.get("font","Helvetica")
        scale=dict.get("scale",12)


        fp=open("temp.eps","w")
        fp.write('/%s findfont'%font +
                 ' %d scalefont setfont'%scale +
                 ' 0 0 moveto (%s) '%text +
                 'false charpath flattenpath pathbbox stack')
        fp.close()

        BBOX=commands.getoutput('gs -q -dNODISPLAY -dBATCH -dNOPAUSE %s'%"temp.eps")
        BBOX=string.split(BBOX,"\n")
        BBOX.reverse()
        
        self.bbox=map(float,BBOX)

        self.natives(dict,
                     bg=None,
                     fg=Color(0),
                     o=P(0,0),
                     text=text,
                     font=font,
                     scale=scale
                     )
        apply(PsObject.__init__,(self,),dict)



    def body(self):
        out=cStringIO.StringIO()
        
        out.write("0 0 moveto\n")
        out.write("/%(font)s findfont\n%(scale)d scalefont setfont\n"%self)
        out.write("%(fg)s (%(text)s) show\n"%self)
        
        return out.getvalue()

    def boundingbox(self):
        "return objects bounding box"

        # return corners for now + 1point to take
        # into account the line widths
        sw = P(self.bbox[0],self.bbox[1])
        ne = P(self.bbox[2],self.bbox[3])
        return (sw,ne)


# -------------------------------------------------------------------------
# Text class that has 1pp bounding box ...
# (but doesn't rely on gs)
# -------------------------------------------------------------------------

class Text_nobbox(PsObject):
    """
    Text class with broken bbox
    (doesn't require gs)
    """
    def __init__(self,text="",**dict):

        self.natives(dict,
                     bg=None,
                     fg=Color(0),
                     o=P(0,0),
                     text=text,
                     font="Helvetica",
                     scale=12
                     )
        apply(PsObject.__init__,(self,),dict)

    def body(self):
        out=cStringIO.StringIO()
        
        out.write("0 0 moveto\n")
        out.write("/%(font)s findfont\n%(scale)d scalefont setfont\n"%self)
        out.write("%(fg)s (%(text)s) show\n"%self)
        
        return out.getvalue()

    def boundingbox(self):
        "return objects bounding box"

        # return corners for now + 1point to take
        # into account the line widths
        sw = self["o"]-R(1,1)*(1/float(defaults.units))
        ne = self["o"]+R(1,1)*(1/float(defaults.units))
        return (sw,ne)

# -------------------------------------------------------------------------
# Rectangle
# -------------------------------------------------------------------------
class Rectangle(Area):
    """
    Draw a rectangle 
    """
    type="Rectangle"

    def __init__(self,**dict):
        '''
        @param dict:
                     - linewidth: the line thickness in points
                     - dash: the dash pattern to use (string ala postscript)
                     - fg: line color
                     - bg: fill color or None for empty
        '''
        self.natives(dict,
                     bg=None,
                     fg=Color(0),
                     linewidth=defaults.linewidth,
                     dash=defaults.dash,
                     )
        apply(Area.__init__,(self,),dict)


    def body(self):
        
        out=cStringIO.StringIO()
        
        if self['linewidth']!=defaults.linewidth:
            out.write("%(linewidth)f setlinewidth "%self)

        if self['dash']!=defaults.dash:
            out.write("%(dash)s setdash "%self)

        if self["bg"] is not None:
            out.write("%(bg)s 0 0 %(width)g uu %(height)g uu rectfill\n"%self)
        out.write("%(fg)s 0 0 %(width)g uu %(height)g uu rectstroke\n"%self)
                        
        return out.getvalue()

# -------------------------------------------------------------------------
# Circle
# -------------------------------------------------------------------------

class Circle(PsObject):
    """
    Draw a circle, or part of

    get ellipses by scaling. The origin is the center
    
    """
    type="Circle"

    namedangles={'n':0,'ne':45,'e':90,'se':135,
                 's':180,'sw':235,'w':270,'nw':315}

    def __init__(self, **dict):
        '''
        @param dict:
                     - r: radius
                     - start: starting angle for arc
                     - end: end angle for arc
                     - c, n, ne, ... as for L{Area.__init__}
                     - 0-360: point on circumference at that angle
                       (degrees clockwise from n)
                     - fg,bg:  foreground and background colors
                     - linewidth, dash:

        
        '''
        self.natives(dict,
                     bg=None,
                     fg=Color(0),
                     r=1.0,
                     start=0,
                     end=360,
                     linewidth=defaults.linewidth,
                     dash=defaults.dash,
                     )
        apply(PsObject.__init__, (self,), dict)

    def locus(self,angle):
        '''
        return a point on the edge at a particular angle
        (degrees, clockwise from vertical)
        '''
        r=self['r']
        x=r*sin(angle/180.0*pi)
        y=r*cos(angle/180.0*pi)

        return self.itoe(P(x,y))

    def __getitem__(self,i):

        if self.namedangles.has_key(i):
            return self.locus(self.namedangles[i])

        if type(i)==type(""):
            return PsObject.__getitem__(self,i)
        
        return self.locus(i)  
    
    def __setitem__(self,i,other):

        if self.namedangles.has_key(i):
            pcurrent=self.locus(self.namedangles[i])
            self.move(other-pcurrent)

        if type(i)==type(""):
            return PsObject.__setitem__(self,i,other)

        pcurrent=self.locus(i)

        self.move(other-pcurrent)

    def _get_c(s):
        return s['o']

    def _set_c(s,pe):
        s.move(pe-s['o'])

    def body(self):

        out = cStringIO.StringIO()

        if self['linewidth']!=defaults.linewidth:
            out.write("%(linewidth)f setlinewidth "%self)

        if self['dash']!=defaults.dash:
            out.write("%(dash)s setdash "%self)

        # By default postscript goes anti-clockwise
        # and starts from 'e' ... fix it so it goes
        # clockwise and starts from 'n'
        
        if self["bg"] is not None:
            out.write("%(bg)s 0 0 %(r)g uu 360 %(start)g -1 mul add 90 add 360 %(end)g -1 mul add 90 add arcn fill\n" % self)

        out.write("%(fg)s 0 0 %(r)g uu 360 %(start)g -1 mul add 90 add 360 %(end)g -1 mul add 90 add arcn stroke\n" % self)

        return out.getvalue()



    def boundingbox(self):

        #grab a tight boundingbox by zipping around circumference

        SW=self.locus(0)
        NE=self.locus(0)
        for ii in xrange(self['start'],self['end']+10,10):
            p=self.locus(ii)

            SW[0]=min(SW[0],p[0])
            SW[1]=min(SW[1],p[1])
            NE[0]=max(NE[0],p[0])
            NE[1]=max(NE[1],p[1])


        return SW,NE

# -------------------------------------------------------------------------
# Path
# -------------------------------------------------------------------------

class C:
    """
    Defines control points for besier spline
    """

    type='C'

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
    type='Path'
    
    def __init__(self,*path,**dict):

        if len(path)==0:
            path=[P(0,0),P(0,0)]
        else:
            path=list(path)

        path=self.make_relative(path)
        sw,ne=self.extent(path)
        self.offset=-sw

        self.natives(dict,
                     path=path,
                     fg=Color(0),
                     bg=None,
                     width=ne[0]-sw[0],
                     height=ne[1]-sw[1],
                     o=sw,
                     linewidth=defaults.linewidth,
                     linecap=defaults.linecap,
                     linejoin=defaults.linejoin,
                     miterlimit=defaults.miterlimit,
                     dash=defaults.dash
                     )
        apply(Area.__init__,(self,),dict)

    def closed(self):
        "Is the path a closed one?"
        p=self['path']
        if p[-1].type=='C' or p[-1] is p[0]:
            return 1
        else:
            return 0
                
    def _get_start(self):
        "return start point"
        return self["path"][0]

    def _get_end(self):
        "return end point"
        P=self['path']
        p=P[-1]
        if p.type=='C':
            p=P[0]
        return p
        
    def body(self):

        out=cStringIO.StringIO()

        P=self["path"][:]

        out.write("%s translate "%self.offset)


        if self['linewidth']!=defaults.linewidth:
            out.write("%(linewidth)f setlinewidth "%self)

        if self['linecap']!=defaults.linecap:
            out.write("%(linecap)d setlinecap "%self)
            
        if self['linejoin']!=defaults.linejoin:
            out.write("%(linejoin)d setlinejoin "%self)

        if self['miterlimit']!=defaults.miterlimit:
            out.write("%(miterlimit)f setmiterlimit "%self)

        if self['dash']!=defaults.dash:
            out.write("%(dash)s setdash "%self)

        out.write("newpath %s moveto\n"%P[0])

        p=None
        while len(P)>1:
            pp=p
            p=P.pop(1)
            if p.type=='P':
                out.write("%s lineto\n"%p)
            elif p.type=='C':
                c1,c2=p.controls()
                pn=P.pop(1%len(P))
                out.write("%s %s %s curveto\n"%(c1,c2,pn))

        if self.closed():
            out.write(' closepath ')

        
        if self["bg"] is not None:
            out.write("gsave %(bg)s fill grestore\n"%self)
        
        if self["fg"] is not None:
            out.write("%(fg)s stroke\n"%self)

        return out.getvalue()


    def make_relative(self,path):
        "Return a path with all relative elements"
        return path

    def extent(self,path):
        "a boundingbox"

        boundpoints=[]
        L=len(path)
        for ii in range(L):
            p=path[ii]
            if p.type=="P":
                boundpoints.append(p)
            elif p.type=="C":
                pn=path[(ii+1)%L]
                pp=path[(ii-1)%L]
                assert pn.type=="P" and pp.type=="P"
                c1,c2=p.controls()
                if c1==None or c2==None: continue

                divisions=10
                for d in range(1,divisions):
                    t=d/float(divisions)
                    p=(1-t)**3*pp+3*(1-t)**2*t*c1+3*(1-t)*t**2*c2+t**3*pn
                    boundpoints.append(p)
                    

        SW=P(0,0)
        NE=P(0,0)
        NE[0]=SW[0]=boundpoints[0][0]
        NE[1]=SW[1]=boundpoints[0][1]


        for p in boundpoints:
            SW[0]=min(SW[0],p[0])
            SW[1]=min(SW[1],p[1])
            NE[0]=max(NE[0],p[0])
            NE[1]=max(NE[1],p[1])

        return SW,NE

# -------------------------------------------------------------------------
# Group
# -------------------------------------------------------------------------

class Group(PsObject):
    """
    Groups together a list of objects
    """
    type="Group"
    
    def __init__(self,*objects,**dict):
        if len(objects)==1 and type(objects[0]) in (TupleType,ListType):
            self.objects=list(objects[0])
        else:
            self.objects=list(objects)


        apply(PsObject.__init__,(self,),dict)

    def __getitem__(self,i):

        # If it's type string pass it on
        if type(i)==type(""):
            return PsObject.__getitem__(self,i)

        return self.objects[i]
        
    def __setitem__(self,i,other):

        # If it's type string pass it on
        if type(i)==type(""):
            return PsObject.__setitem__(self,i,other)

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

    def boundingbox(self):
        """
        Gather together common bounding box for group
        """

        # We need to do the calculation in the 
        # external co-ordinates (that's where the
        # bounding box will be used)
        
        if len(self.objects)==0:
            return None,None

        # first grap initial values
        for obj in self.objects:
            sw,ne=obj.boundingbox()
            if not sw or not ne:
                # some objects may not return a boundingbox
                continue
            else:
                SW=self.itoe(sw)
                NE=self.itoe(ne)

        for obj in self.objects:
            sw,ne=obj.boundingbox()
            if sw and ne: # some objects return None
                sw,ne=bbox_itoe(sw,ne,self.itoe)

                SW[0]=min(sw[0],SW[0])
                SW[1]=min(sw[1],SW[1])
                NE[0]=max(ne[0],NE[0])
                NE[1]=max(ne[1],NE[1])
        return SW,NE

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
        
        self.natives(dict,
                     width=w*UNITS['cm']/float(defaults.units),
                     height=h*UNITS['cm']/float(defaults.units),
                     )

        apply(Area.__init__,(self,),dict)
















