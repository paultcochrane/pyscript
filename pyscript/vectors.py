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


# Originally written by Mario Chemnitz (ucla@hrz.tu-chemnitz.de)
# Cut back and reworked to suit pyscript

from math import sqrt,acos,sin,cos,pi
from base import PsObj


class Matrix:
    '''
    2x2 matrix class
    '''
    type='Matrix'
 
    def __init__(self,a=0.0,b=0.0,c=0.0,d=0.0):
        # / a b \
        # \ c d /
        self.data=[a,b,c,d]
 

    def body(s):
        d=s.data
        
        #NB postscript uses transpose
        return "[%g %g %g %g]"%(d[0],d[2],d[1],d[3])

    def __add__(s,o):
        if isinstance(o,Matrix):
            return Matrix(s[0]+o[0],s[1]+o[1],s[2]+o[2],s[3]+o[3])
        else:
            raise TypeError,"non-matrix in matrix addition"

    __radd__=__add__
  
    def __sub__(s,o):
        if isinstance(o,Matrix):
            return Matrix(s[0]-o[0],s[1]-o[1],s[2]-o[2],s[3]-o[3])
        else:
            raise TypeError,"non-matrix in matrix subtraction"

    def __rsub__(s,o):
        if isinstance(o,Matrix):
            return Matrix(o[0]-s[0],o[1]-s[1],o[2]-s[2],o[3]-s[3])
        else:
            raise TypeError,"non-matrix in right matrix subtraction"

    def __neg__(s):
        return Matrix(-s[0],-s[1],-s[2],-s[3])
        
    def __len__(self):
        return 4

    def __getitem__(self,i):
        if i < (len(self)):
            return self.data[i]
        else:
            raise IndexError,"index reading error"
    
    def __setitem__(self,i,other):
        if i < (len(self)):
            self.data[i]=other
        else:
            raise IndexError,"index writing error"

    # reads entry from row i and column j: -> data element
    def __getslice__(self,i,j):
        if i<2 and j<2:
            return self.data[2*i+j]
        else:
            raise IndexError,"index reading error"

    # writes matrix element to row i and column j
    def __setslice__(self,i,j,wert):
        if i<2 and j<2:
            self.data[2*i+j]=wert
        else:
            raise IndexError,"index writing error"

    #E matrix multiplication (self*other): -> matrix or vector
    def __mul__(self,other):
        if isinstance(other,Matrix):
            tmp=Matrix()
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        tmp[i:j]=tmp[i:j]+self[i:k]*other[k:j]
            return tmp
        elif isinstance(other,P):
            tmp=P()
            for i in range(2):
                for k in range(2):
                    tmp[i]=tmp[i]+self[i:k]*other[k]
            return tmp      
        elif isinstance(other,(int,float)):
            tmp=Matrix()
            for i in range(len(self)):
                tmp[i]=self[i]*other
            return tmp	
        else:
            raise TypeError,"m-n-error in matrix multiplication"
      
    # E operand for matrix multiplication is on the right (other*self):
    # -> matrix
    def __rmul__(self,other):
        if isinstance(other,Matrix):
            tmp=Matrix()
            for i in range(len(self)):
                tmp[i]=other*self[i]
            return tmp	
        else:
            raise TypeError,"error in right matrix multiplication"

    def det(s):
        return s[0]*s[3]-s[1]*s[2]

    def inverse(s):

        d=s.det()

        if d==0 : raise "determinant=0, cannot calc inverse"

        return Matrix(s[3],-s[1],-s[2],s[0])/float(d)


    def __div__(self,n):
        # only for numbers!
        assert isinstance(n,(int,float)), "only division by numbers implemented"
        n=float(n)
        tmp=Matrix()
        for i in range(len(self)):
            tmp[i]=self[i]/n
        return tmp
  


# -------------------------------------------------------------------------
# P = Vector (relative to origin) ie a point
# -------------------------------------------------------------------------
class P(PsObj):
    """
    A Vector (or point)
    operations always return type 'P' vectors
    """

    point=[0,0]

    def __init__(self,x=0.0,y=0.0,**dict):

        self.point=[x,y]

        apply(PsObj.__init__,(self,),dict)
        
    def __len__(self):
        return 2

    def __getitem__(self,i):
        if i < (len(self)):
            return self.point[i]
        else:
            raise IndexError,"index reading error"
    
    def __setitem__(self,i,other):
        if i < (len(self)):
            self.point[i]=other
        else:
            raise IndexError,"index writing error"

    def __add__(s,o):
        if isinstance(o,P):
            return P(s[0]+o[0],s[1]+o[1])
        elif isinstance(o,(float,int)):
            return P(s[0]+o,s[1]+o)
        else:
            raise TypeError, "non-vector in vector addition"

    __radd__=__add__

    def __sub__(s,o):
        if isinstance(o,P):
            return P(s[0]-o[0],s[1]-o[1])
        else:
            raise TypeError, "non-vector in vector subtraction"

    def __rsub__(s,o):
        if isinstance(o,P):
            return P(o[0]-s[0],o[1]-s[1])
        else:
            raise TypeError, "non-vector in right vector subtraction"

    def __neg__(s):
        return P(-s[0],-s[1])

    def __mul__(s,o):
        if isinstance(o,P):
            # Dot product
            return s[0]*o[0]+s[1]*o[1]
        elif isinstance(o,Matrix):
            raise TypeError, "other must not be a matrix"
        else:
            return P(s[0]*o,s[1]*o)

    def __rmul__(s,o):
        return P(s[0]*o,s[1]*o)

    def body(self):
        "return postscript as string"
        return "%g uu %g uu"%tuple(self)

    def __div__(self,o):
        # only for numbers!
        if isinstance(o,(float,int)):
            n=float(o)
            return P(self[0]/o,self[1]/o)
        else:
            raise TypeError, "Only division by numbers implemented"

    def _get_x(self):
        return self[0]
    x = property(_get_x,None)

    def _get_y(self):
        return self[1]
    y = property(_get_y,None)

    def _get_length(self):
        '''
        Return length of this vector
        (distance from origin to point)
        '''
        return sqrt(self*self)
    length = property(_get_length,None)

    def _get_U(self):
        '''
        Return unit vector pointing in same direction
        '''
        return self/float(self.length)
    U = property(_get_U,None)


    def cross(self,other):
        if isinstance(o,P):
            tmp=P()
            tmp[0]=self[1]*other[2]-self[2]*other[1]
            tmp[1]=self[2]*other[0]-self[0]*other[2]
            return tmp
        else:
            raise TypeError, "non-vector in cross product"



# -------------------------------------------------------------------------
# R = Vector (relative to last point) function dependent!
# -------------------------------------------------------------------------

class R(P):

    def __add__(s,o):
        if isinstance(o,(float,int)):
            return R(s[0]+o,s[1]+o)
        else:
            return P.__add__(s,o)
        
    def __mul__(s,o):
        if isinstance(o,(float,int)):
            return R(s[0]*o,s[1]*o)
        else:
            return P.__mul__(s,o)
        
    def __rmul__(s,o):
        
        return R(s[0]*o,s[1]*o)

    def __div__(self,o):
        # only for numbers!
        if isinstance(o,(float,int)):
            n=float(o)
            return R(self[0]/o,self[1]/o)
        else:
            raise TypeError, "Only division by numbers implemented"
    def __neg__(s):
        return R(-s[0],-s[1])

#def R(*args,**dict):
#    """
#    Exactly the same as a P() but some functions interpret
#    this as a relative direction
#    """

#return apply(P,args,{'relative':1})
# -------------------------------------------------------------------------
# Unit vector
# -------------------------------------------------------------------------

def U(angle,r=1):
    '''
    return a relative vector of length r in the given direction
    '''
    x=r*sin(angle/180.0*pi)
    y=r*cos(angle/180.0*pi)

    return R(x,y)

# -------------------------------------------------------------------------
# Unit vector
# -------------------------------------------------------------------------
def Cusp(p1,p2):
    '''
    Alignment aid returns P(p1.x,p2.y)
    '''
    return P(p1[0],p2[1])
    
    
# -------------------------------------------------------------------------

def Identity(p):
    '''
    function which does nothing
    '''
    # do it this way so we return a copy
    return P(p[0],p[1])


# -------------------------------------------------------------------------
class Bbox(object):
    """
    A Rectangular area defined by sw corner and width and height.
    which specifies a boundingbox.

    Has the same attributes (but read only) as Area::
    
          nw--n--ne
          |       |
          w   c   e
          |       |
          sw--s--se

    """

    sw=None
    width=0
    height=0 

    def __init__(self,**dict):
        '''
        can pass a dict of atributes to set
        '''

        # this will raise an exception if class doesn't have attribute
        # I think this is good.
        prop=[]
        for key,value in dict.items():
            if isinstance(eval('self.__class__.%s'%key),property):
                prop.append((key,value))
            else:
                self.__class__.__setattr__(self,key,value)


    def _get_n(s):
        return s.sw+P(s.width/2.,s.height)
    n = property(_get_n)

    def _get_ne(s):
        return s.sw+P(s.width,s.height)
    ne = property(_get_ne)

    def _get_e(s):
        return s.sw+P(s.width,s.height/2.)
    e = property(_get_e)

    def _get_se(s):
        return s.sw+P(s.width,0)
    se = property(_get_se)

    def _get_s(s):
        return s.sw+P(s.width/2.,0)
    s = property(_get_s)

    def _get_w(s):
        return s.sw+P(0,s.height/2.)
    w = property(_get_w)

    def _get_nw(s):
        return s.sw+P(0,s.height)
    nw = property(_get_nw)

    def _get_c(s):
        return s.sw+P(s.width/2.,s.height/2.)
    c = property(_get_c)

    def is_set(self):
        '''
        Is the bounding box set with a value?
        '''
        if self.sw is None:
            return 0
        else:
            return 1

    def union(self,bbox,itoe=Identity):
        '''
        Expand this boundingbox to include bbox,
        passing bbox through itoe if supplied
        '''

        if not bbox.is_set():
            # if the supplied bbox is not set we have
            # nothing to do
            return

        
        ne=itoe(bbox.ne)
        sw=itoe(bbox.sw)
        nw=itoe(bbox.nw)
        se=itoe(bbox.se)
        

        xmin=min(ne[0],nw[0],se[0],sw[0])
        xmax=max(ne[0],nw[0],se[0],sw[0])
        ymin=min(ne[1],nw[1],se[1],sw[1])
        ymax=max(ne[1],nw[1],se[1],sw[1])
        
        #if self.is_set():

            #x1=min(self.sw[0],sw[0])
            #y1=min(self.sw[1],sw[1])
            #x2=max(self.ne[0],ne[0])
            #y2=max(self.ne[1],ne[1])

            #self.sw=P(x1,y1)
            #self.width=x2-x1
            #self.height=y2-y1
            
        #else:

            #self.sw=sw
            #self.width,self.height=ne-sw

        if self.is_set():

            x1=min(self.sw[0],xmin)
            y1=min(self.sw[1],ymin)
            x2=max(self.ne[0],xmax)
            y2=max(self.ne[1],ymax)

            self.sw=P(x1,y1)
            self.width=x2-x1
            self.height=y2-y1
            
        else:

            self.sw=P(xmin,ymin)
            self.width=xmax-xmin
            self.height=ymax-ymin
            
