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
Groupies
"""

import cStringIO 

from types import *
from vectors import *
from objects import Area
from defaults import defaults


# -------------------------------------------------------------------------

class Group(Area):
    """
    Groups together a list of objects
    """

    def __init__(self,*objects,**dict):

        self.objects=[]
        self.objbox=Bbox()
        
        if len(objects)==1 and type(objects[0]) in (TupleType,ListType):
            apply(self.append,objects[0])
        else:
            apply(self.append,objects)

        apply(Area.__init__,(self,),dict)

    def __getitem__(self,i):
        return self.objects[i]
        
    def __setitem__(self,i,other):
        self.objects[i]=other

    def __getslice__(self,i,j):
        return self.objects[i:j]

    def __setslice__(self,i,j,wert):
        self.objects[i:j]=wert

    def __len__(self):
        return len(self.objects)

    def insert(self,idx,obj):

        self.objbox.union(obj.bbox())
        self.objects.insert(idx,obj)

    def append(self,*objs):
        '''
        append object(s) to group
        '''
        for obj in objs:
            self.objbox.union(obj.bbox())
            self.objects.append(obj)

        # update size
        if self.objbox.is_set():
            self.isw=self.objbox.sw
            self.width=self.objbox.width
            self.height=self.objbox.height

    def apply(self,**dict):
        '''
        apply attributes to all objects
        '''
        # do this by attributes since they 
        # might not all get accepted

        for key,value in dict.items():
            dict1={key:value}
            for obj in self.objects:
                try:
                    apply(obj,(),dict1)            
                except AttributeError:
                    # skip objects that don't have the attribute
                    pass
        # we don't know if the sizes where changes so recalculate them
        self.recalc_size()

        # for convenience return reference to group
        return self

    def recalc_size(self):
        '''
        recalculate internal container size based on objects within
        '''
        self.objbox=Bbox()
        for obj in self.objects:
            self.objbox.union(obj.bbox())

        if self.objbox.is_set():
            self.isw=self.objbox.sw
            self.width=self.objbox.width
            self.height=self.objbox.height
        
            
    def body(self):
        out=cStringIO.StringIO()
        for obj in self.objects:
            out.write(str(obj))
        return out.getvalue()


    def bbox(self):
        """
        Gather together common bounding box for group
        Don't use Area's bbox as transformations may
        mean a tighter bbox (eg a circle)
        """

        # We need to do the calculation in the 
        # external co-ordinates (that's where the
        # bounding box will be used)

        # first a null Bbox
        bbox=Bbox()
        
        for obj in self.objects:
            bbox.union(obj.bbox(),self.itoe)

        return bbox

# -------------------------------------------------------------------------
    
def Align(*items,**dict):
    '''
    Function to align a group of objects.

    @param anchor: The item number of the object that remain fixed
    @param a1: The first anchor point to align to eg "e", "c"
    @param a2: The second anchor point for aligning
    @param space: the amount of space to enforce between the anchor points, if None then only movement perpendicular to angle is possible
    @param angle: the angle of the line between anchor points
    @return: a reference to the group containing the objects
    '''

    anchor=dict.get('anchor',0)
    a1=dict.get('a1','c')
    a2=dict.get('a2','c')
    space=dict.get('space',None)
    angle=dict.get('angle',0)
    
    if len(items)==1:
        if not isinstance(items[0],Group):
            # Nothing to do here ...
            return apply(Group,objects) 
        objects=items[0]
        if len(objects) <= 1:
            return objects
    else:
        # create a group around the objects
        objects=Group(items)

    # keep a reference to the anchor ... we'll
    # move it back later
    anchor_bbox_sw=objects[anchor].bbox().sw
    
    assert a1 in ["n","ne","e","se","s","sw","w","nw","c"]
    assert a2 in ["n","ne","e","se","s","sw","w","nw","c"]

    # need to implement a length for group
    for ii in range(1,len(objects)):

        obj=objects[ii]
        p1=getattr(objects[ii-1].bbox(),a1)
        p2=getattr(obj.bbox(),a2)
        

        if space is not None:
            obj.move(U(angle,space)-(p2-p1))

        else:
            # Don't touch the spacing in the angle direction
            # adjust in othogonal direction instead

            obj.move((U(angle+90)*(p2-p1))*U(angle-90))

        
        p1=p2

    offset=anchor_bbox_sw-objects[anchor].bbox().sw

    # Can't really move group since it might be fake
    for obj in objects:
        obj.move(offset)

    if isinstance(objects,Group):
        objects.recalc_size()

        # for convenience ..
        return objects
    else:
        # create a group (though it may not be used)
        # for convenience
        return apply(Group,objects) 

# -------------------------------------------------------------------------

def Distribute(*items,**dict):
    '''
    Function to distribute a group of objects.

    @param p1: first point of the line along which to distribute
    @param p2: second point of the line along which to distribute
    @param a1: The first anchor point to use for spacing to eg "e", "c"
    @param a2: The second anchor point for spacing
    @param as: anchor point for first item (overides a2 if present)
    @param ae: anchor point for last item (overides a1 if present)
    @return: a reference to a group containing the objects
    '''

    a1=dict.get('a1','c')
    a2=dict.get('a2','c')

    assert a1 in ["n","ne","e","se","s","sw","w","nw","c"]
    assert a2 in ["n","ne","e","se","s","sw","w","nw","c"]

    # note the swap:
    as=dict.get('as',a2)
    ae=dict.get('ae',a1)

    assert as in ["n","ne","e","se","s","sw","w","nw","c"]
    assert ae in ["n","ne","e","se","s","sw","w","nw","c"]

    # these two have to be present
    p1=dict['p1']
    p2=dict['p2']

    pv=p2-p1

    if len(items)==1:
        if isinstance(items[0],Group):
            items=items[0]

    # A vector giving the direction to distribute things
    pv=p2-p1


    if len(items)==1:
        # place item in the centre
        
        ov=( getattr(items[0].bbox(),a1)+getattr(items[0].bbox(),a2) )/2. -p1

        # how much we need to move by
        mv=(pv.length/2.-pv.U*ov)*pv.U

        items[0].move(mv)

    else:

        # work out the amount of space we have to play with
        space=pv.length

        # place items at the edges
        # ---first object----
        ov=getattr(items[0].bbox(),as)-p1

        # how much we need to move by
        mv=-pv.U*ov*pv.U
        items[0].move(mv)

        space -= abs(( getattr(items[0].bbox(),a1)-getattr(items[0].bbox(),as) )*pv.U)

        # ---second object---
        ov=getattr(items[-1].bbox(),ae)-p2

        # how much we need to move by
        mv=-pv.U*ov*pv.U
        items[-1].move(mv)

        space -= abs(( getattr(items[-1].bbox(),ae)-getattr(items[-1].bbox(),a2) )*pv.U)

        if len(items)>2:

            # take out the length of each item in this dir
            for item in items[1:-1]:
                # abs? XXX
                space -= abs(( getattr(item.bbox(),a2)-getattr(item.bbox(),a1) )*pv.U)

            ds=space/float((len(items)-1))

            for ii in range(1,len(items)-1):
                p1=getattr(items[ii-1].bbox(),a1)
                p2=getattr(items[ii].bbox(),a2)

                mv=(ds-(p2-p1)*pv.U)*pv.U
                items[ii].move(mv)
            
        
    if isinstance(items,Group):
        items.recalc_size()

        # for convenience ..
        return items
    else:
        # create a group (though it may not be used)
        # for convenience
        return apply(Group,items) 



# -------------------------------------------------------------------------

class Page(Group):
    '''
    A postscript page
    '''

    size='a4'
    orientation="portrait"
    
    # From gs_statd.ps which defines the paper sizes for gs:
    # Define various paper formats.  The Adobe documentation defines only these:
    # 11x17, a3, a4, a4small, b5, ledger, legal, letter, lettersmall, note.
    # These procedures are also accessed as data structures during initialization,
    # so the page dimensions must be the first two elements of the procedure.

    PAPERSIZES={
        # Page sizes defined by Adobe documentation
        "11x17":(792,1224),
        # a3 see below
        # a4 see below
        # a4small should be a4 with an ImagingBBox of [25 25 570 817].
        # b5 see below
        "ledger":(1224,792), # 11x17 landscape
        "legal":(612,1008),
        "letter":(612,792),
        # lettersmall should be letter with an ImagingBBox of [25 25 587 767].
        # note should be letter (or some other size) with the ImagingBBox
        # shrunk by 25 units on all 4 sides.

        # ISO standard paper sizes
        "a0":(2380,3368),
        "a1":(1684,2380),
        "a2":(1190,1684),
        "a3":(842,1190),
        "a4":(595,842),
        "a5":(421,595),
        "a6":(297,421),
        "a7":(210, 297),
        "a8":(148, 210),
        "a9":(105, 148),
        "a10":(74, 105),
        # ISO and JIS B sizes are different....
        # first ISO
        "b0":(2836, 4008),
        "b1":(2004, 2836),
        "b2":(1418, 2004),
        "b3":(1002, 1418),
        "b4":(709, 1002),
        "b5":(501, 709),
        "b6":(354, 501),
        "jisb0":(2916, 4128),
        "jisb1":(2064, 2916),
        "jisb2":(1458, 2064),
        "jisb3":(1032, 1458),
        "jisb4":(729, 1032),
        "jisb5":(516, 729),
        "jisb6":(363, 516),
        "c0":(2600, 3677),
        "c1":(1837, 2600),
        "c2":(1298, 1837),
        "c3":(918, 1298),
        "c4":(649, 918),
        "c5":(459, 649),
        "c6":(323, 459),
        # U.S. CAD standard paper sizes
        "archE":(2592, 3456),
        "archD":(1728, 2592),
        "archC":(1296, 1728),
        "archB":(864, 1296),
        "archA":(648, 864),
        # Other paper sizes
        "flsa":(612, 936), # U.S. foolscap
        "flse":(612, 936), # European foolscap
        "halfletter":(396, 612),
        }
    
    def area(self):
        '''
        return an area object same size as page in default units
        '''
        w,h=self.PAPERSIZES[self.size]
        if self.orientation=="landscape": h,w=w,h

        w,h=w/float(defaults.units),h/float(defaults.units)
        
        return Area(sw=P(0,0),width=w,height=h)
        
    def recalc_size(self):
        pass

    def bbox(self):
        
        area=self.area()
        return Bbox(sw=area.sw,width=area.width,height=area.height)

    def prebody(self):

        w,h=self.PAPERSIZES[self.size]
        out='''
        %%PageBoundingBox: 0 0 %(w)d %(h)d
        %%BeginFeature: *PageSize %(size)s
        <</PageSize [%(w)d %(h)d] /ImagingBBox null>> setpagedevice
        %%EndFeature
        
        /PyScriptDict 1 dict def
        PyScriptDict begin
        /showpage {} def
        '''%{'w':w,'h':h,'size':self.size}
        
        return out+Group.prebody(self)

    def postbody(self):

        out='''
        end
        showpage
        '''
        return Group.prebody(self)+out

    