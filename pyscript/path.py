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

from defaults import *
from vectors import *
from base import PsObj,Color,PyScriptError,FontError
from objects import *

# -------------------------------------------------------------------------
# Pathlettes ... components of path, not used by themselves
# -------------------------------------------------------------------------

class _line(object):
    '''
    A line pathlette
    '''
    s=None
    e=None

    def __init__(self,s,e):
        self.s=s
        self.e=e

    def _get_start(self):
        "return start point"
        return self.s
    start = property(_get_start)

    def _get_end(self):
        "return end point"
        return self.e
    end = property(_get_end)

    def _get_length(self):
        return (self.e-self.s).length
    length = property(_get_length)

    def P(self,f):
        '''
        return point at fraction f of length
        '''
        return (self.s+(self.e-self.s)*f)

    def body(self):
        return '%s lineto\n'%self.e

    def bbox(self,itoe=Identity):

        p0=itoe(self.s)
        p1=itoe(self.e)

        x0=min(p0[0],p1[0])
        x1=max(p0[0],p1[0])
        y0=min(p0[1],p1[1])
        y1=max(p0[1],p1[1])

        return Bbox(sw=P(x0,y0),width=x1-x0,
                    height=y1-y0)

# -------------------------------------------------------------------------

class _bezier(object):
    '''
    A Bezier pathlette
    '''
    s=None
    e=None
    cs=None
    ce=None
    length=None
    
    TOL=None #tolerance for linearising

    def __init__(self,s,cs,ce,e,TOL=5e-3,temporary=False):
        self.s=s # start
        self.e=e # end
        self.cs=cs # start control
        self.ce=ce # end control
        self.TOL=TOL
        
        # for efficiency don't do this unless we intend to
        # keep this pathlette
        if not temporary:
            self._points=self.straighten()
            self.set_length()

    def _is_straight(self):
        '''
        is this curve straight?
        '''

        L1=(self.cs-self.s).length+\
          (self.ce-self.cs).length+\
          (self.e-self.ce).length
        L2=(self.e-self.s).length
        
        if abs(L1-L2)/float(L1)<=self.TOL:
            return True
        else:
            return False

    def straighten(self):
        
        if self._is_straight():
            return (self.s,self.e)
        else: 
            c1,c2=self._bisect(temporary=True)
            
            return (c1.straighten()+c2.straighten())
        
    def _bisect(self,t=.5,temporary=False):
        '''
        Divide this bezier into two
        '''
        p01   = self.s * (1-t) + self.cs * t
        p12   = self.cs * (1-t) + self.ce * t
        p23   = self.ce * (1-t) + self.e * t
        p012  = p01  * (1-t) + p12  * t
        p123  = p12  * (1-t) + p23  * t
        p0123 = p012 * (1-t) + p123 * t

        return (_bezier(self.s.copy(), p01, p012, p0123,temporary=temporary),
                _bezier(p0123.copy(), p123, p23, self.e.copy(),temporary=temporary) )       

    
    def set_length(self):
        L=0
        p0=self.s
        for p in self._points:
            L+=(p-p0).length
            p0=p
        self.length=L

    def body(self):
        return '%s %s %s curveto\n'%(self.cs,self.ce,self.e)


    def _t(self,t):
        '''
        Return point on curve parametrised by t [0-1]
        This is exact
        '''
        a1=3*(self.cs-self.s)
        a2=3*(self.s-2*self.cs+self.ce)
        a3=-self.s+3*self.cs-3*self.ce+self.e
        
        return a3*t**3+a2*t**2+a1*t+self.s

    def _get_start(self):
        "return start point"
        return self.s
    start = property(_get_start)

    def _get_end(self):
        "return end point"
        return self.e
    end = property(_get_end)

    def P(self,f):
        '''
        return point on curve at fraction f of length
        '''
        assert 0<=f<=1

        #if self.length is None:
        #    self._cache()

        
        if f==0:
            return self.s
        elif f==1:
            return self.e
        
        Lf=self.length*f

        L=0
        p0=self.s
        for p in self._points:
            l=(p-p0).length
            if L+l>=Lf: break
            L+=l
            p0=p

        # XXX Add a correction here so it's actually on the curve!
        # Newton Rapson?

        return (p-p0).U*(Lf-L) +p0

    def bbox(self,itoe=Identity):
        # run through the list of points to get the bounding box
        
        #if self.length is None:
        #    self._cache()

        p0=itoe(self.s)
        x0,y0=p0
        x1,y1=p0

        for p in self._points:
        
            p1=itoe(p)

            x0=min(x0,p1[0])
            x1=max(x1,p1[0])
            y0=min(y0,p1[1])
            y1=max(y1,p1[1])

        return Bbox(sw=P(x0,y0),width=x1-x0,
                    height=y1-y0)

# -------------------------------------------------------------------------
# Curve specifier
# -------------------------------------------------------------------------

class C:
    """
    Specifier and generator for curves
    """

    # The type of the curve
    # 0 = bezier
    _type=None
    
    def __init__(self,c1=None,c2=None):
        '''
        store curve parameters
        '''

        if c1 is not None and c2 is not None:
            self.c1=c1
            self.c2=c2
            self._type=0
        elif c1 is not None and c2 is None:
            self.c1=c1
            self.c2=c1
            self._type=0
        else:
            raise "Don't inderstand arguments to C()"

    def copy(self):
        return copy.deepcopy(self)

    #def controls(self):
    #    # is this necessary?
    #    return self.c1,self.c2
    
    def curve(self,p1,p2):
        '''
        return pathlette object corresponding to curve
        '''
        if self._type==0:
            c1=self.c1
            c2=self.c2
            if isinstance(c1,R):
                c1=p1+c1
            if isinstance(c2,R):
                c2=p2+c2
            return _bezier(p1,c1,c2,p2)
        else:
            raise "Couldn't contruct curve"
# -------------------------------------------------------------------------
# Path object
# -------------------------------------------------------------------------

class Path(AffineObj):
    """
    A Path
    """
    
    fg=Color(0)
    bg=None
    linewidth=None
    linecap=None
    linejoin=None
    miterlimit=None
    dash=None
    closed=0

    #_pathlettes=[]

    def __init__(self,*path,**dict):

        self._pathlettes=[]

        apply(AffineObj.__init__,(self,),dict)

        path=list(path) # so we can use pop
        
        # first point must be, well a point
        assert isinstance(path[0],P)
        cp=path.pop(0) # current point

        while 1:
            if len(path)==0: break

            p=path.pop(0)
            if isinstance(p,R):
                p=cp+p
                self._pathlettes.append(_line(cp,p))
                cp=p
            elif isinstance(p,P):
                self._pathlettes.append(_line(cp,p))
                cp=p
            elif isinstance(p,C):
                c=p
                # Get the next point
                #p=path[0]
                p=path.pop(0)
                if isinstance(p,R):
                    p=cp+p
                self._pathlettes.append(c.curve(cp,p))
                cp=p
                
            else:
                raise "Unknown path control"


    def bbox(self):
        b=Bbox()
        for pl in self._pathlettes:
            b.union(pl.bbox(self.itoe))
        return b

    def _get_start(self):
        "return start point"
        return self.itoe(self._pathlettes[0].start)
    start = property(_get_start)

    def _get_end(self):
        "return end point"
        return self.itoe(self._pathlettes[-1].end)
    end = property(_get_end)

    def _get_length(self):

        l=0
        for pl in self._pathlettes:
            l+=pl.length
        return l
    length = property(_get_length)
        
    def P(self,f):
        '''
        Return the point at fraction f along the path
        '''

        assert 0<=f<=1

        Lf=self.length*f

        L=0
        for pl in self._pathlettes:
            l=pl.length
            if L+l>=Lf: break
            L+=l
        return self.itoe(pl.P((Lf-L)/float(l)))


    def body(self):

        out=cStringIO.StringIO()

        if self.linewidth is not None:
            out.write("%g setlinewidth "%self.linewidth)

        if self.linecap is not None:
            out.write("%d setlinecap "%self.linecap)
            
        if self.linejoin is not None:
            out.write("%d setlinejoin "%self.linejoin)

        if self.miterlimit is not None:
            out.write("%f setmiterlimit "%self.miterlimit)

        if self.dash is not None:
            out.write("%s setdash "%self.dash)

        out.write('newpath %s moveto\n'%self._pathlettes[0].start)

        for pl in self._pathlettes:
            out.write(pl.body())

        if self.closed:
            out.write(' closepath ')

        
        if self.bg is not None:
            out.write("gsave %s fill grestore\n"%self.bg)
        
        if self.fg is not None:
            out.write("%s stroke\n"%self.fg)

        return out.getvalue()

