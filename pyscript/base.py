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
import UserDict,copy
from types import *

#os,string,re,copy
#import cStringIO,commands
#from math import cos,sin,pi

#from defaults import *
from util import *
#from vectors import *

# -------------------------------------------------------------------------
# PsDict: implement a dynamic dictionary
# -------------------------------------------------------------------------

class PsDict(UserDict.UserDict):
    """
    Base class, 
    implements a dict with dynamic elements
    """
    type="PsDict"

    def __init__(self,**dict):

        self.natives({},dict)

        # create the dict structures
        UserDict.UserDict.__init__(self)

        # set native attributes
        for key,value in self._natives.items():
            self[key]=value

        # Add rest
        natives=self._natives.keys()
        for key,value in dict.items():
            if key not in natives:
                self[key]=value
            
    def natives(self,newnatives={},dict={}):
        '''
        set native attributes
        MUST be done BEFORE initialisation!
        '''
        # need to set natives attribute (may not be initialised yet!)
        if not self.__dict__.has_key('_natives'):
            self._natives={}
        
        # first accumulated the natives...
        # Add old natives to new since old will
        # be higher up inheritance tree
        # (accumulated overide defaults)
        for key,value in self._natives.items():
            newnatives[key]=value

        # override defaults with user supplied values
        for key in dict.keys():
            if newnatives.has_key(key):
                newnatives[key]=dict[key]
        # store natives
        self._natives=newnatives
        

    def __getitem__(self, key):
        "get dict or attribute"
        if self.data.has_key(key):
            return self.data[key]
        try:
            return getattr(self,"_get_%s"%key)()
        except AttributeError:
            raise KeyError,key

    def __setitem__(self, key, item):
        "set attribute or dict"
        try:
            getattr(self,"_set_%s"%key)(item)
        except AttributeError:
            self.data[key] = item        

    def copy(self,**dict):
        '''
        return a copy of this object
        with listed attributes modified
        '''
        # here for convenience
        obj=copy.deepcopy(self)

        for key,value in dict.items():
            obj[key]=value
        return obj


# -------------------------------------------------------------------------
# Color
# -------------------------------------------------------------------------

class Color(PsDict):
    """
    (C,M,Y,K)=CMYKColor or (R,G,B)=RGBColor or (G)=Gray or 'yellow' etc 
    """
    def __init__(self,*col,**dict):
      
        if type(col[0])==StringType:
            col=COLORS[col[0]]

        # some sanity checks
        assert len(col)>0 and len(col)<5
        for ii in col: assert ii>=0 and ii<=1
            
        self.natives({"color":col},dict)
        apply(PsDict.__init__,(self,),dict)
        
        
    def __str__(self):
        "return postscript as string"

        color=self['color']
        if len(color)==1:
            # grayscale color
            ps=" %g setgray "%color
        elif len(color)==3:
            # rgb color
            ps=" %g %g %g setrgbcolor "%color
        elif len(color)==4:
            # cmyk color
            ps=" %g %g %g %g setcmykcolor "%color
        else:
            raise "Unknown color"
        return ps
    
    def __mul__(self,other):
        assert other>=0 and other<=1
        newcol=[]
        for ii in self['color']:
            newcol.append(ii*other)
        return apply(Color,tuple(newcol))

# -------------------------------------------------------------------------
# Pass through abritrary postcript
# -------------------------------------------------------------------------


# XXX fix!

class Postscript(PsDict):
    """
    Insert a raw postcript command in output
    """
    type="Postscript"

    def __init__(self,postscript,**dict):

        self.natives({"postscript":postscript},dict)
        apply(PsDict.__init__,(self,),dict)


    def __str__(self):
        return " %(postscript)s "%self



