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
import types

from util import *

# -------------------------------------------------------------------------

class PsDict(UserDict.UserDict):
    """
    An extended dictionary with dynamic elements,
    this is the base class of may pyscript classes
    """
    type="PsDict"

    def __init__(self,**dict):

        self.natives(dict)

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
            
    def natives(self,dict={},**newnatives):
        '''
        this function allows the setting of default values
        NB: set native attributes MUST be done BEFORE initialisation
        of parent class!
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
        '''extended getitem to allow dynamic attributes
        
             1. first check internal dict for key
             2. second, return ._get_key() if method exists
             3. else raise KeyError
            
        '''
        if self.data.has_key(key):
            return self.data[key]
        try:
            return getattr(self,"_get_%s"%key)()
        except AttributeError:
            raise KeyError,key

    def __setitem__(self, key, item):
        '''extended setitem to allow dynamic attributes

             1. call ._set_key(item) if method exists
             2. else return data[key]
          
        '''
        try:
            getattr(self,"_set_%s"%key)(item)
        except AttributeError:
            self.data[key] = item        

    def copy(self,**dict):
        '''
        return a copy of this object
        with listed attributes modified

        eg::
          newobj=obj.copy(bg=Color(.3))
        '''
        # here for convenience
        obj=copy.deepcopy(self)

        for key,value in dict.items():
            obj[key]=value
        return obj
    
    def __repr__(self):
        return self.type+"("+str(self.data)+")"

    def set(self,**dict):
        '''
        Set a whole lot of attributes in one go

        eg::
          obj.set(bg=Color(.3),linewidth=2)

        @return: self 
        '''

        for key,value in dict.items():
            self[key]=value

        # for convenience return a reference to us
        return self

# -------------------------------------------------------------------------

class Color(PsDict):
    """
    Class to encode a postscript color
 
    There are four ways to specify the color:

     - Color(C,M,Y,K) =CMYKColor
     - Color(R,G,B) =RGBColor
     - Color(G) = Gray
     - Color('yellow') etc, see L{COLORS}
    """
    type="Color"

    COLORS={'red':(1,0,0),
            'green':(0,1,0),
            'blue':(0,0,1),
            'cyan':(1,0,0,0),
            'magenta':(0,1,0,0),
            'yellow':(0,0,1,0),
            'black':(0,),
            'white':(1,)}

    def __init__(self,*col,**dict):
      
        if type(col[0])==types.StringType:
            col=self.COLORS[col[0]]

        # some sanity checks
        assert len(col)>0 and len(col)<5
        for ii in col: assert ii>=0 and ii<=1
            
        self.natives(dict,color=col)
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
        '''
        colors can be multiplied by a numeric factor between 0 and 1.
        The effect is mostly to darken colors as they approach 0,
        but this depends on how the colors where specified.

        eg::
          Color(.2,.6,.6)*.5 = Color(.1,.3,.3)

        '''
        assert other>=0 and other<=1
        newcol=[]
        for ii in self['color']:
            newcol.append(ii*other)
        return apply(Color,tuple(newcol))

# -------------------------------------------------------------------------

# XXX fix!

class Postscript(PsDict):
    """
    Insert a raw postcript command in output
    """
    type="Postscript"

    def __init__(self,postscript,**dict):

        self.natives(dict,postscript=postscript)
        apply(PsDict.__init__,(self,),dict)


    def __str__(self):
        return " %(postscript)s "%self



