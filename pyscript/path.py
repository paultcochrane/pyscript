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




class _bezier(object):
    '''
    A Bezier pathlette
    '''
    s=None
    e=None
    cs=None
    ce=None

    TOL=1e-4 #tolerance for linearising

    def __init__(self,s,cs,ce,e):
        self.s=s # start
        self.e=e # end
        self.cs=cs # start control
        self.ce=ce # end control

        self._cache()

    def body(self):
        return '%s %s %s %s curveto\n'%(self.s,self.cs,self.ce,self.e)

    def _cache(self):
        '''
        Split curve up into line segments and store length and the points
        '''

        Lold=(self.e-self.s).length

        pp=1
        while pp<=100:

            L=0
            dt=1.0/(pp+1)
            for ii in xrange(pp+1):
                L+=(self._t((ii+1)*dt)-self._t(ii*dt)).length 
            if abs((L-Lold)/float(Lold))<self.TOL: break
            Lold=L
            pp=pp+1 

        self.length=L
        self._points=[self.s]
        for ii in xrange(pp):
            self._points.append(self._t((ii+1)*dt))
        self._points.append(self.e)

        print pp, "points"
        
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


class Path(AffineObj):
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
    closed=0

    _pathlettes=[]

    def __init__(self,*path,**dict):

        apply(AffineObj.__init__,(self,),dict)

        path=list(path) # so we can use pop

        assert isinstance(path[0],P)
        cp=path.pop(0) # current point

        while 1:
            if len(path)==0: break
            p=path.pop(0)
            if isinstance(p,R):
                p=p+cp
                self._pathlettes.append(_line(cp,p))
                cp=p
            elif isinstance(p,P):
                self._pathlettes.append(_line(cp,p))
                cp=p
            elif isinstance(p,C):
                c=p
                # Get the next point
                p=path.pop()
                self._pathlettes.append(_bezier(cp,c.c1,c.c2,p))
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

        if self.linewidth!=defaults.linewidth:
            out.write("%g setlinewidth "%self.linewidth)

        if self.linecap!=defaults.linecap:
            out.write("%d setlinecap "%self.linecap)
            
        if self.linejoin!=defaults.linejoin:
            out.write("%d setlinejoin "%self.linejoin)

        if self.miterlimit!=defaults.miterlimit:
            out.write("%f setmiterlimit "%self.miterlimit)

        if self.dash!=defaults.dash:
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

