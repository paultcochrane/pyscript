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
import string

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

        # first do non-property ones
        # this will raise an exception if class doesn't have attribute
        # I think this is good.
        prop=[]
        for key,value in dict.items():
            if isinstance(eval('self.__class__.%s'%key),property):
                prop.append((key,value))
            else:
                self.__class__.__setattr__(self,key,value)

        # now the property ones
        # (which are functions of the non-property ones)
        for key,value in prop:
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
            'white':(1,),
            'greenyellow':   (0.15,0,0.69,0),
            'yellow':        (0,0,1,0),
            'goldenrod':     (0,0.10,0.84,0),
            'dandelion':     (0,0.29,0.84,0),
            'apricot':       (0,0.32,0.52,0),
            'peach':         (0,0.50,0.70,0),
            'melon':         (0,0.46,0.50,0),
            'yelloworange':  (0,0.42,1,0),
            'orange':        (0,0.61,0.87,0),
            'burntorange':   (0,0.51,1,0),
            'bittersweet':   (0,0.75,1,0.24),
            'redorange':     (0,0.77,0.87,0),
            'mahogany':      (0,0.85,0.87,0.35),
            'maroon':        (0,0.87,0.68,0.32),
            'brickred':      (0,0.89,0.94,0.28),
            'orangered':     (0,1,0.50,0),
            'rubinered':     (0,1,0.13,0),
            'wildstrawberry':(0,0.96,0.39,0),
            'salmon':        (0,0.53,0.38,0),
            'carnationpink': (0,0.63,0,0),
            'magenta':       (0,1,0,0),
            'violetred':     (0,0.81,0,0),
            'rhodamine':     (0,0.82,0,0),
            'mulberry':      (0.34,0.90,0,0.02),
            'redviolet':     (0.07,0.90,0,0.34),
            'fuchsia':       (0.47,0.91,0,0.08),
            'lavender':      (0,0.48,0,0),
            'thistle':       (0.12,0.59,0,0),
            'orchid':        (0.32,0.64,0,0),
            'darkorchid':    (0.40,0.80,0.20,0),
            'purple':        (0.45,0.86,0,0),
            'plum':          (0.50,1,0,0),
            'violet':        (0.79,0.88,0,0),
            'royalpurple':   (0.75,0.90,0,0),
            'blueviolet':    (0.86,0.91,0,0.04),
            'periwinkle':    (0.57,0.55,0,0),
            'cadetblue':     (0.62,0.57,0.23,0),
            'cornflowerblue':(0.65,0.13,0,0),
            'midnightblue':  (0.98,0.13,0,0.43),
            'navyblue':      (0.94,0.54,0,0),
            'royalblue':     (1,0.50,0,0),
            'cerulean':      (0.94,0.11,0,0),
            'cyan':          (1,0,0,0),
            'processblue':   (0.96,0,0,0),
            'skyblue':       (0.62,0,0.12,0),
            'turquoise':     (0.85,0,0.20,0),
            'tealblue':      (0.86,0,0.34,0.02),
            'aquamarine':    (0.82,0,0.30,0),
            'bluegreen':     (0.85,0,0.33,0),
            'emerald':       (1,0,0.50,0),
            'junglegreen':   (0.99,0,0.52,0),
            'seagreen':      (0.69,0,0.50,0),
            'forestgreen':   (0.91,0,0.88,0.12),
            'pinegreen':     (0.92,0,0.59,0.25),
            'limegreen':     (0.50,0,1,0),
            'yellowgreen':   (0.44,0,0.74,0),
            'springgreen':   (0.26,0,0.76,0),
            'olivegreen':    (0.64,0,0.95,0.40),
            'rawsienna':     (0,0.72,1,0.45),
            'sepia':         (0,0.83,1,0.70),
            'brown':         (0,0.81,1,0.60),
            'tan':           (0.14,0.42,0.56,0),
            'gray':          (0,0,0,0.50),
            }

    def __init__(self,*col,**dict):
      
        if type(col[0])==types.StringType:
            col=self.COLORS[string.lower(col[0])]

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



