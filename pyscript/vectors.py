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


# Originally written by Mario Chemnitz (ucla@hrz.tu-chemnitz.de)
# Cut back and reworked to suit pyscript

from math import sqrt,acos,sin,cos
from util import *
from base import PsDict


class Matrix:
    '''
    2x2 matrix class
    '''
    type='Matrix'
 
    def __init__(self,a=0.0,b=0.0,c=0.0,d=0.0):
        # / a b \
        # \ c d /
        self.data=[a,b,c,d]
 
    def __repr__(s):
        return s.type+'('+repr(s[0])+","+repr(s[1])\
               +","+repr(s[2])+","+repr(s[3])+')'

    def __str__(s):
        '''
        print as postscript
        '''
        d=s.data
        
        #NB postscript uses transpose
        return "[%g %g %g %g]"%(d[0],d[2],d[1],d[3])

    def __add__(s,o):
        if pstype(o) == MatrixType:
            return Matrix(s[0]+o[0],s[1]+o[1],s[2]+o[2],s[3]+o[3])
        else:
            raise TypeError,"non-matrix in matrix addition"

    __radd__=__add__
  
    def __sub__(s,o):
        if pstype(o) == MatrixType:
            return Matrix(s[0]-o[0],s[1]-o[1],s[2]-o[2],s[3]-o[3])
        else:
            raise TypeError,"non-matrix in matrix subtraction"

    def __rsub__(s,o):
        if pstype(o) == MatrixType:
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
        if pstype(other)==MatrixType:
            tmp=Matrix()
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        tmp[i:j]=tmp[i:j]+self[i:k]*other[k:j]
            return tmp
        elif pstype(other) in (PType,RType):
            tmp=P()
            for i in range(2):
                for k in range(2):
                    tmp[i]=tmp[i]+self[i:k]*other[k]
            return tmp      
        elif pstype(other) in (FloatType,IntType):
            tmp=Matrix()
            for i in range(len(self)):
                tmp[i]=self[i]*other
            return tmp	
        else:
            raise TypeError,"m-n-error in matrix multiplication"
      
    # E operand for matrix multiplication is on the right (other*self):
    # -> matrix
    def __rmul__(self,other):
        if pstype(other)==MatrixType:
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
        n=float(n)
        tmp=Matrix()
        for i in range(len(self)):
            tmp[i]=self[i]/n
        return tmp
  


# -------------------------------------------------------------------------
# P = Vector (relative to origin) ie a point
# -------------------------------------------------------------------------
class P(PsDict):
    """
    A Vector (or point)
    operations always return type 'P' vectors
    """
    type='P'

    def __init__(self,x=0.0,y=0.0,**dict):
        self.point=[x,y]

        self.natives(dict,relative=0)
        apply(PsDict.__init__,(self,),dict)
        
    def __repr__(self):
        return self.type+'('+repr(self[0])+","+repr(self[1])+')'

    def __len__(self):
        return 2

    def __getitem__(self,i):

        if type(i)==type(""):
            return PsDict.__getitem__(self,i)
        
        if i < (len(self)):
            return self.point[i]
        else:
            raise IndexError,"index reading error"
    
    def __setitem__(self,i,other):
        if type(i)==type(""):
            return PsDict.__setitem__(self,i,other)

        if i < (len(self)):
            self.point[i]=other
        else:
            raise IndexError,"index writing error"

    def __add__(s,o):
        if pstype(o) in (PType,RType):
            return P(s[0]+o[0],s[1]+o[1])
        elif pstype(o) in (FloatType,IntType):
            return P(s[0]+o,s[1]+o)
        else:
            raise TypeError, "non-vector in vector addition"

    __radd__=__add__

    def __sub__(s,o):
        if pstype(o) in (PType,RType):
            return P(s[0]-o[0],s[1]-o[1])
        else:
            raise TypeError, "non-vector in vector subtraction"

    def __rsub__(s,o):
        if pstype(o) in (PType,RType):
            return P(o[0]-s[0],o[1]-s[1])
        else:
            raise TypeError, "non-vector in right vector subtraction"

    def __neg__(s):
        return P(-s[0],-s[1])

    def __mul__(s,o):
        if pstype(o) in (PType,RType):
            # Dot product
            return s[0]*o[0]+s[1]*o[1]
        elif pstype(o)==MatrixType:
            raise TypeError, "other must not be a matrix"
        else:
            return P(s[0]*o,s[1]*o)

    def __rmul__(s,o):
        return P(s[0]*o,s[1]*o)

    def __str__(self):
        "return postscript as string"
        return "%g uu %g uu"%tuple(self.point)

    def __div__(self,o):
        # only for numbers!
        if pstype(o) in (FloatType,IntType):
            n=float(o)
            return P(self[0]/o,self[1]/o)
        else:
            raise TypeError, "Only division by numbers implemented"

    def length(self):
        return sqrt(self*self)

    def cross(self,other):
        if pstype(o) in (PType,RType):
            tmp=P()
            tmp[0]=self[1]*other[2]-self[2]*other[1]
            tmp[1]=self[2]*other[0]-self[0]*other[2]
            return tmp
        else:
            raise TypeError, "non-vector in cross product"



# -------------------------------------------------------------------------
# R = Vector (relative to last point) function dependent!
# -------------------------------------------------------------------------

def R(*args,**dict):
    """
    Exactly the same as a P() but some functions interpret
    this as a relative direction
    """

    dict['relative']=1

    return apply(P,args,dict)

#E base vectors
