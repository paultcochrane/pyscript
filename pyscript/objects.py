# Copyright (C) 2002  Alexei Gilchrist
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
import UserDict,os,string,re,copy
import cStringIO,commands

from types import *

from math import cos,sin,pi

from defaults import *
from util import *
from vectors import *


# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

class Color:
    """
    (C,M,Y,K)=CMYKColor or (R,G,B)=RGBColor or (G)=Gray or 'yellow' etc 
    """
    def __init__(self,*col):
      
        if type(col[0])==StringType:
            col=COLORS[col[0]]

        assert len(col)>0 and len(col)<5
        
        for ii in col:
            assert ii>=0 and ii<=1
            
        self.color=col
        
    def __str__(self):
        "return postscript as string"

        color=self.color
        if len(color)==1:
            ps=" %f setgray "%color
        elif len(color)==3:
            ps=" %f %f %f setrgbcolor "%color
        elif len(color)==4:
            ps=" %f %f %f %f setcmykcolor "%color
        else:
            raise "Unknown color"
        return ps
    
    def copy(self):
        return copy.deepcopy(self)

    def __mul__(self,other):
        assert other>=0 and other<=1
        newcol=[]
        for ii in self.color:
            newcol.append(ii*other)
        return apply(Color,tuple(newcol))

# -------------------------------------------------------------------------
# Pass through abritrary postcript
# -------------------------------------------------------------------------

class Postscript:
    """
    Insert a raw postcript command in output
    """
    type="Postscript"

    def __init__(self,command):
        self.command=command

        def __str__(self):
            return " %s "%self.command

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------


class PsObject(UserDict.UserDict):
    """
    Base class, A generic Postscript object
    implements a dict with
    some dynamic elements
    """
    type="PsObject"

    def __init__(self,**dict):
        # create the dict structures
        UserDict.UserDict.__init__(self)

        setkeys(dict,{"o":P(0,0),
                      "T":Matrix(1,0,0,1)})

        # Add critical items first
        critical=dict.get("__natives__",{})
        criticalkeys=critical.keys()
        criticalkeys.append("__natives__")
        for key,value in critical.items():
            self[key]=value

        # Add rest
        for key,value in dict.items():
            if key in criticalkeys: continue
            self[key]=value

    def __getitem__(self, key):
        "get dict or attribute"
        if self.data.has_key(key):
            return self.data[key]
        try:
            return getattr(self,"_get_%s"%key)()
        except AttributeError:
            print "hello"
            raise KeyError,key

    def __setitem__(self, key, item):
        "set attribute or dict"
        try:
            getattr(self,"_set_%s"%key)(item)
        except AttributeError:
            self.data[key] = item        

    def copy(self):
        return copy.deepcopy(self)

    def concat(self,t):

        T=self["T"]
        self["T"]=t*T#[a,b,c,d]

    def move(self,dx,dy):
        self["o"]=self["o"]+P(dx,dy)

    def rotate(self,angle):
        angle=angle/180.0*pi
        t=Matrix([cos(angle),sin(angle),-sin(angle),cos(angle)])
        self.concat(t)

    def scale(self,sx,sy):
        self.concat(Matrix([sx,0,0,sy]))

    def prebody(self):
        T=self["T"]
        o=self["o"]
        S="gsave\n"
        if T!=None and o!=P(0,0):
            S=S+"[%f %f %f %f %s] concat "%(T[0],T[1],T[2],T[3],o)
        return S

    def postbody(self):
        return "grestore\n"

    def __str__(self):
        "return postscript as string"
        return self.prebody()+self.body()+self.postbody()

    def body(self):
        return ""

    def boundingbox(self):
        "return objects bounding box"
        
        # should be dynamically calculated abd take
        # into account transformation matrix
        
        raise "Needs to be overridden!"

    def get_fonts(self,fontdict):
        """
        Return any font definitions to be included at begining of output
        """
        # Not implemented
        pass

    def get_defs(self,order,defdict):
        """
        Get any postscript definitions that will be used in output
        """
        pass

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------

class Area(PsObject):
    """
    A Rectangular area.
    """
    type="Area"

    def __init__(self,**dict):
        setkeys(dict,{"width":0,"height":0})
        apply(PsObject.__init__,(self,),dict)


        # Dynamic locations ... retrival
    def _get_w(self):
        return self["o"]+P(0,self["height"]/2.)
    def _get_nw(self):
        return self["o"]+P(0,self["height"])
    def _get_s(self):
        return self["o"]+P(self["width"]/2.,0)
    def _get_sw(self):
        return self["o"]
    def _get_se(self):
        return self["o"]+P(self["width"],0)
    def _get_e(self):
        return self["o"]+P(self["width"],self["height"]/2.)
    def _get_ne(self):
        return self["o"]+P(self["width"],self["height"])
    def _get_n(self):
        return self["o"]+P(self["width"]/2.,self["height"])
    def _get_c(self):
        return self["o"]+P(self["width"]/2.,self["height"]/2.)


    # Dynamic locations ... setting
    def _set_n(self,p):
        self["o"]=self["o"]+p-self["n"]
    def _set_ne(self,p):
        self["o"]=self["o"]+p-self["ne"]
    def _set_e(self,p):
        self["o"]=self["o"]+p-self["e"]
    def _set_se(self,p):
        self["o"]=self["o"]+p-self["se"]
    def _set_s(self,p):
        self["o"]=self["o"]+p-self["s"]
    def _set_sw(self,p):
        self["o"]=self["o"]+p-self["sw"]
    def _set_w(self,p):
        self["o"]=self["o"]+p-self["w"]
    def _set_nw(self,p):
        self["o"]=self["o"]+p-self["nw"]
    def _set_c(self,p):
        self["o"]=self["o"]+p-self["c"]

    def boundingbox(self):
        "return objects bounding box"

        # return corners for now + 1point to take
        # into account the line widths
        sw = self["sw"]-R(1,1)*(1/float(defaults.units))
        ne = self["ne"]+R(1,1)*(1/float(defaults.units))

        # TODO
        # should be dynamically calculated and take
        # into account transformation matrix

        return (sw,ne)

# -------------------------------------------------------------------------
# A TeX expression
# parses the output of dvips
# -------------------------------------------------------------------------
class TeX(Area):
    '''
    an Area object for a TeX expression
    
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
        self.bbox=[]
        for ii in bbox_so.groups():
            self.bbox.append(int(ii))

        setkeys(dict,
                {"width":(self.bbox[2]-self.bbox[0])/float(defaults.units),
                 "height":(self.bbox[3]-self.bbox[1])/float(defaults.units),
                 "fg":Color(0)
                 })
        apply(Area.__init__,(self,),dict)

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

        out.write("%d %d translate %s\n"%(-self.bbox[0],-self.bbox[1],
                                          self["fg"]) )
        out.write("%s\n"%self.bodyps)
        return out.getvalue()


class Text1(Area):
        
    def __init__(self,text="",**dict):

        # get the bbox
        # first need font and scale
        font=dict.get("font","Helvetica")
        scale=dict.get("scale","12")


        fp=open("temp.eps","w")
        fp.write('/%s findfont'%font +
                 ' %s scalefont setfont'%scale +
                 ' 0 0 moveto (%s) '%text +
                 'false charpath flattenpath pathbbox stack')
        fp.close()

        BBOX=commands.getoutput('gs -q -dNODISPLAY -dBATCH -dNOPAUSE %s'%"temp.eps")
        BBOX=string.split(BBOX,"\n")
        BBOX.reverse()
        
        self.bbox=map(float,BBOX)

        setkeys(dict,
                {"bg":None,
                 "fg":Color(0),
                 "o":P(0,0),
                 "text":text,
                 "font":font,
                 "scale":scale
                 })
        apply(PsObject.__init__,(self,),dict)



    def body(self):
        out=cStringIO.StringIO()
        
        out.write("0 0 moveto\n")
        out.write("/%(font)s findfont\n%(scale)s scalefont setfont\n"%self)
        out.write("(%(text)s) show\n"%self)
        
        return out.getvalue()

    def boundingbox(self):
        "return objects bounding box"

        # return corners for now + 1point to take
        # into account the line widths
        sw = P(self.bbox[0],self.bbox[1])
        ne = P(self.bbox[2],self.bbox[3])
        return (sw,ne)


class Text2(Area):
        
    def __init__(self,text="",**dict):

        # get the bbox
        # first need font and scale
        font=dict.get("font","Helvetica")
        scale=dict.get("scale","12")


        fp=open("temp.eps","w")
        fp.write('/%s findfont'%font +
                 ' %s scalefont setfont'%scale +
                 ' 0 10 moveto (%s) show showpage quit'%text)
        fp.close()

        BBOX=commands.getoutput('gs -q -sDEVICE=bbox -dBATCH -dNOPAUSE %s'%"temp.eps")
        
        so=re.search("HiResBoundingBox:\s*([\d.\-]+)\s*([\d.\-]+)\s*([\d.\-]+)\s*([\d.\-]+)",BBOX,re.M)
        self.bbox=[float(so.group(1)),float(so.group(2))-10,
                   float(so.group(3)),float(so.group(4))-10]

        setkeys(dict,
                {"bg":None,
                 "fg":Color(0),
                 "o":P(0,0),
                 "text":text,
                 "font":font,
                 "scale":scale
                 })
        apply(PsObject.__init__,(self,),dict)



    def body(self):
        out=cStringIO.StringIO()
        
        out.write("0 0 moveto\n")
        out.write("/%(font)s findfont\n%(scale)s scalefont setfont\n"%self)
        out.write("(%(text)s) show\n"%self)
        
        return out.getvalue()

    def boundingbox(self):
        "return objects bounding box"

        # return corners for now + 1point to take
        # into account the line widths
        sw = P(self.bbox[0],self.bbox[1])
        ne = P(self.bbox[2],self.bbox[3])
        return (sw,ne)

class Text(PsObject):
        
    def __init__(self,text="",**dict):

        setkeys(dict,
                {"bg":None,
                 "fg":Color(0),
                 "o":P(0,0),
                 "text":text,
                 "font":"Helvetica",
                 "scale":"12"
                 })
        apply(PsObject.__init__,(self,),dict)

    def body(self):
        out=cStringIO.StringIO()
        
        out.write("0 0 moveto\n")
        out.write("/%(font)s findfont\n%(scale)s scalefont setfont\n"%self)
        out.write("(%(text)s) show\n"%self)
        
        return out.getvalue()

    def boundingbox(self):
        "return objects bounding box"

        # return corners for now + 1point to take
        # into account the line widths
        sw = self["o"]-R(1,1)*(1/float(defaults.units))
        ne = self["o"]+R(1,1)*(1/float(defaults.units))
        return (sw,ne)

# -------------------------------------------------------------------------
# -------------------------------------------------------------------------
class Box(Area):
    """
    Draw a box
    """
    type="Box"

    def __init__(self,**dict):
        
        setkeys(dict,
                {"bg":None,
                 "fg":Color(0)})
        apply(Area.__init__,(self,),dict)


    def body(self):
        
        out=cStringIO.StringIO()
        
        if self["bg"] is not None:
            out.write("%(bg)s 0 0 %(width)s uu %(height)s uu rectfill\n"%self)
        out.write("%(fg)s 0 0 %(width)s uu %(height)s uu rectstroke\n"%self)
                        
        return out.getvalue()
                

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

        setkeys(dict,
                {"path":path,
                 "fg":Color(0),
                 "bg":None,
                 "width":ne[0]-sw[0],
                 "height":ne[1]-sw[1],
                 "o":sw,
                 "linewidth":defaults.linewidth,
                 "linecap":defaults.linecap,
                 "linejoin":defaults.linejoin,
                 "miterlimit":defaults.miterlimit,
                 "dash":defaults.dash
                 })

        
        self.offset=-sw
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
        #setkeys(dict,
                 #"width":ne[0]-sw[0],
                 #"height":ne[1]-sw[1],
                 #"o":sw,
                 #})

        apply(PsObject.__init__,(self,),dict)


    def boundingbox(self):
        """
        Gather together common bounding box for group
        """
        SW,NE=self.objects[0].boundingbox()
        for obj in self.objects[1:]:
            sw,ne=obj.boundingbox()
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
    
