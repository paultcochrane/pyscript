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
    
class Align(Group):

    anchor=None

    space=None
    angle=0

    a1="c"
    a2="c"

    def __init__(self,*objs,**dict):

        # first grap the keys that define the alignment
        self.space=dict.get("space",None)
        self.a1=dict.get("a1","c")
        self.a2=dict.get("a2","c")
        self.angle=dict.get("angle",0)
        
        apply(Group.__init__,(self,objs),dict)

        assert self.a1 in ["n","ne","e","se","s","sw","w","nw","c"]
        assert self.a2 in ["n","ne","e","se","s","sw","w","nw","c"]
        
    def append(self,*objs):
        '''
        append object(s) to group
        '''

        for obj in objs:

            if self.anchor is None:
                self.objbox.union(obj.bbox())
                self.objects.append(obj)
                self.anchor=obj
                continue

            # if we're appending, the obj is p2
            p2=getattr(obj.bbox(),self.a2)
            p1=getattr(self.objects[-1].bbox(),self.a1)

            if self.space is not None:
                obj.move(E(self.angle,self.space)-(p2-p1))

            else:
                # Don't touch the spacing in the angle direction
                # adjust in othogonal direction instead

                obj.move((E(self.angle+90)*(p2-p1))*E(self.angle-90))


            self.objbox.union(obj.bbox())
            self.objects.append(obj)

        # update size
        if self.objbox.is_set():
            self.isw=self.objbox.sw
            self.width=self.objbox.width
            self.height=self.objbox.height

