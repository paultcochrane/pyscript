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
import copy
import types

# -------------------------------------------------------------------------

class PsDict: pass

class PsObj(object):
    """
    Base Class that most pyscript objects should subclass
    """

    def __init__(self,**dict):
        '''
        can pass a dict of atributes to set
        '''
        apply(self,(),dict)
        

    def __call__(self,**dict):
        '''
        Set a whole lot of attributes in one go
        
        eg::
          obj.set(bg=Color(.3),linewidth=2)

        @return: self 
        '''

        for key,value in dict.items():
            self.__class__.__setattr__(self,key,value)

        # for convenience return a reference to us
        return self
        

    def copy(self,**dict):
        '''
        return a copy of this object
        with listed attributes modified

        eg::
          newobj=obj.copy(bg=Color(.3))
        '''
        # here for convenience
        obj=copy.deepcopy(self)

        apply(obj,(),dict)

        return obj
    
    def __repr__(self):
        return str(self.__class__)

    def __str__(self):
        '''
        return actual postscript string to generate object
        '''
        return self.prebody()+self.body()+self.postbody()

    def prebody(self):
        '''
        convenience function to allow clean subclassing
        '''
        return ''

    def body(self):
        '''
        subclasses should overide this for generating postscipt code
        '''
        return ''

    def postbody(self):
        '''
        convenience function to allow clean subclassing
        '''
        return ''


    def bbox(self):
        """
        return objects bounding box
        9this can be a Null Bbox() if object doesn't
        draw anything on the page.)

        NB that the bbox should be dynamically calculated and take
        into account the transformation matrix if it applies
        """

        return Bbox()


# -------------------------------------------------------------------------

class Color(PsObj):
    """
    Class to encode a postscript color
 
    There are four ways to specify the color:

     - Color(C,M,Y,K) =CMYKColor
     - Color(R,G,B) =RGBColor
     - Color(G) = Gray
     - Color('yellow') etc, see L{COLORS}
    """

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
        
        self.color=col
            
        apply(PsObj.__init__,(self,),dict)
        
        
    def body(self):

        color=self.color
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

##class Postscript(PsObj):
##    """
##    Insert a raw postcript command in output
##    """
##    type="Postscript"

##    def __init__(self,postscript,**dict):

##        self.natives(dict,postscript=postscript)
##        apply(PsObj.__init__,(self,),dict)


##    def __str__(self):
##        return " %(postscript)s "%self



