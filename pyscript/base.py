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
        this can be a Null Bbox() if object doesn't
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

    COLORS={
        "AliceBlue":(240,248,255),
        "AntiqueWhite":(250,235,215),
        "Aqua":(0,255,255),
        "Aquamarine":(127,255,212),
        "Azure":(240,255,255),
        "Beige":(245,245,220),
        "Bisque":(255,228,196),
        "Black":(0,0,0),
        "BlanchedAlmond":(255,235,205),
        "Blue":(0,0,255),
        "BlueViolet":(138,43,226),
        "Brown":(165,42,42),
        "BurlyWood":(222,184,135),
        "CadetBlue":(95,158,160),
        "Chartreuse":(127,255,0),
        "Chocolate":(210,105,30),
        "Coral":(255,127,80),
        "CornflowerBlue":(100,149,237),
        "Cornsilk":(255,248,220),
        "Crimson":(220,20,60),
        "Cyan":(0,255,255),
        "DarkBlue":(0,0,139),
        "DarkCyan":(0,139,139),
        "DarkGoldenrod":(184,134,11),
        "DarkGray":(169,169,169),
        "DarkGreen":(0,100,0),
        "DarkKhaki":(189,183,107),
        "DarkMagenta":(139,0,139),
        "DarkOliveGreen":(85,107,47),
        "DarkOrange":(255,140,0),
        "DarkOrchid":(153,50,204),
        "DarkRed":(139,0,0),
        "DarkSalmon":(233,150,122),
        "DarkSeaGreen":(143,188,143),
        "DarkSlateBlue":(72,61,139),
        "DarkSlateGray":(47,79,79),
        "DarkTurquoise":(0,206,209),
        "DarkViolet":(148,0,211),
        "DeepPink":(255,20,147),
        "DeepSkyBlue":(0,191,255),
        "DimGray":(105,105,105),
        "DodgerBlue":(30,144,255),
        "FireBrick":(178,34,34),
        "FloralWhite":(255,250,240),
        "ForestGreen":(34,139,34),
        "Fuchsia":(255,0,255),
        "Gainsboro":(220,220,220),
        "GhostWhite":(248,248,255),
        "Gold":(255,215,0),
        "Goldenrod":(218,165,32),
        "Gray":(128,128,128),
        "Green":(0,128,0),
        "GreenYellow":(173,255,47),
        "Honeydew":(240,255,240),
        "HotPink":(255,105,180),
        "IndianRed":(205,92,92),
        "Indigo":(75,0,130),
        "Ivory":(255,255,240),
        "Khaki":(240,230,140),
        "Lavender":(230,230,250),
        "LavenderBlush":(255,240,245),
        "LawnGreen":(124,252,0),
        "LemonChiffon":(255,250,205),
        "LightBlue":(173,216,230),
        "LightCoral":(240,128,128),
        "LightCyan":(224,255,255),
        "LightGoldenrodYellow":(250,250,210),
        "LightGreen":(144,238,144),
        "LightGrey":(211,211,211),
        "LightPink":(255,182,193),
        "LightSalmon":(255,160,122),
        "LightSeaGreen":(32,178,170),
        "LightSkyBlue":(135,206,250),
        "LightSlateGray":(119,136,153),
        "LightSteelBlue":(176,196,222),
        "LightYellow":(255,255,224),
        "Lime":(0,255,0),
        "LimeGreen":(50,205,50),
        "Linen":(250,240,230),
        "Magenta":(255,0,255),
        "Maroon":(128,0,0),
        "MediumAquamarine":(102,205,170),
        "MediumBlue":(0,0,205),
        "MediumOrchid":(186,85,211),
        "MediumPurple":(147,112,219),
        "MediumSeaGreen":(60,179,113),
        "MediumSlateBlue":(123,104,238),
        "MediumSpringGreen":(0,250,154),
        "MediumTurquoise":(72,209,204),
        "MediumVioletRed":(199,21,133),
        "MidnightBlue":(25,25,112),
        "MintCream":(245,255,250),
        "MistyRose":(255,228,225),
        "Moccasin":(255,228,181),
        "NavajoWhite":(255,222,173),
        "Navy":(0,0,128),
        "OldLace":(253,245,230),
        "Olive":(128,128,0),
        "OliveDrab":(107,142,35),
        "Orange":(255,165,0),
        "OrangeRed":(255,69,0),
        "Orchid":(218,112,214),
        "PaleGoldenrod":(238,232,170),
        "PaleGreen":(152,251,152),
        "PaleTurquoise":(175,238,238),
        "PaleVioletRed":(219,112,147),
        "PapayaWhip":(255,239,213),
        "PeachPuff":(255,218,185),
        "Peru":(205,133,63),
        "Pink":(255,192,203),
        "Plum":(221,160,221),
        "PowderBlue":(176,224,230),
        "Purple":(128,0,128),
        "Red":(255,0,0),
        "RosyBrown":(188,143,143),
        "RoyalBlue":(65,105,225),
        "SaddleBrown":(139,69,19),
        "Salmon":(250,128,114),
        "SandyBrown":(244,164,96),
        "SeaGreen":(46,139,87),
        "Seashell":(255,245,238),
        "Sienna":(160,82,45),
        "Silver":(192,192,192),
        "SkyBlue":(135,206,235),
        "SlateBlue":(106,90,205),
        "SlateGray":(112,128,144),
        "Snow":(255,250,250),
        "SpringGreen":(0,255,127),
        "SteelBlue":(70,130,180),
        "Tan":(210,180,140),
        "Teal":(0,128,128),
        "Thistle":(216,191,216),
        "Tomato":(255,99,71),
        "Turquoise":(64,224,208),
        "Violet":(238,130,238),
        "Wheat":(245,222,179),
        "White":(255,255,255),
        "WhiteSmoke":(245,245,245),
        "Yellow":(255,255,0),
        "YellowGreen":(154,205,50),
        }


    def __init__(self,*col,**dict):
      
        # some sanity checks
        if type(col[0])==types.StringType:
            col=self.COLORS[col[0]]
            # renormalise so that values are in [0,1]
            col = (col[0]/255.,col[1]/255.,col[2]/255.)
            
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
        colors can be multiplied by a numeric factor.
        factors less than 1 will darken the colors,
        factors grater than will will lighten the colors.
        (this depends on how the colors where specified)

        eg::
          Color(.2,.6,.6)*.5 = Color(.1,.3,.3)

        '''
        assert other>=0 #and other<=1
        newcol=[]
        for ii in self.color:
            newcol.append(min(1,ii*other))
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



