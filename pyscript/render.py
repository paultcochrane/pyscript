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
Create the actual postscript
"""

import sys,os
import cStringIO
import time

from defaults import *
from util import *
from objects import *
from groups import *
from version import version

# we need to double up the comment %'s
# The BoundingBox and EndComments will be added later
EPSheader="""%%!PS-Adobe-2.0 EPSF-2.0
%%%%Creator: PyScript %s
%%%%CreationDate: %s
"""%(version,time.ctime(time.time()))

PSheader="""%%!PS-Adobe-2.0
%%%%Creator: PyScript %s
%%%%CreationDate: %s
%%%%Page: 1 1
"""%(version,time.ctime(time.time()))

PSMacros="""%%BeginProcSet: pyscript
/PyScriptDict 10 dict def PyScriptDict begin
%%show text with kerning if supplied
/kernshow { 0 2 2 counttomark 2 sub { -2 roll } for
counttomark 2 idiv { exch show 0 rmoveto} repeat pop
} bind def
/BeginEPSF { 
/b4_Inc_state save def 
/dict_count countdictstack def 
/op_count count 1 sub def      
userdict begin                 
/showpage { } def              
0 setgray 0 setlinecap         
1 setlinewidth 0 setlinejoin
10 setmiterlimit [ ] 0 setdash newpath
/languagelevel where           
{pop languagelevel             
1 ne                           
{false setstrokeadjust false setoverprint
} if
} if
} bind def
/EndEPSF { 
count op_count sub {pop} repeat 
countdictstack dict_count sub {end} repeat
b4_Inc_state restore
} bind def
/PyScriptStart {} def
/PyScriptEnd {} def
/showpage {} def
end
%%EndProcSet
"""

import os,re

def collecttex(objects,tex=[]):
    '''
    Collect the TeX objects in the order theyre rendered
    '''
    for object in objects:
        if isinstance(object,TeX):
            tex.append(object)
        elif isinstance(object,Group):
            tex=collecttex(object.objects,tex)
    return tex


def TeXstuff(objects):
    '''
    Get the actual postscript code and insert it into
    the tex objects. Also grab prolog
    '''

    objects=collecttex(objects)
    if len(objects)==0:
        return ""
    
    print "Collecting postscript for TeX objects ..."
    
    file="temp.tex"
    fp=open(file,"w")
    fp.write(defaults.tex_head)
    for tex in objects:
        fp.write('\\special{ps:PyScriptStart}\n')
        fp.write(tex.text)
        fp.write('\n\\special{ps:PyScriptEnd}\n')
        fp.write('\\newpage\n')
    fp.write(defaults.tex_tail)
    fp.close()

    ##os.system(defaults.tex_command%file+'> pyscript.log 2>&1')
    #(fi,foe) = os.popen4(defaults.tex_command%file)
    #fi.close()
    #sys.stderr.writelines(str(foe.readlines()))
    #sys.stderr.write('\n')
    #foe.close()

    # TeX it twice ... only pay attention to the 2nd one
    os.popen(defaults.tex_command%file)
    foe = os.popen(defaults.tex_command%file)
    sys.stderr.write(foe.read(-1))
    sys.stderr.write('\n')
    # Help the user out by throwing the latex log to stderr
    if os.path.exists("%s.log"%file):
        fp=open("%s.log"%file,'r')
        sys.stderr.write(fp.read(-1))
        fp.close()
    if foe.close() is not None:
        raise "Latex Error"
    
    (fi,foe) = os.popen4("dvips -q -tunknown %s -o temp.ps temp.dvi"%defaults.dvips_options)
    fi.close()
    err=foe.read(-1)
    sys.stderr.write(err)
    sys.stderr.write('\n')
    foe.close()
    if len(err)>0:
        raise "dvips Error"

    fp=open("temp.ps","r")
    ps=fp.read(-1)
    fp.close()

    # Now rip it appart .. use string rather than re which
    # gets caught on recursion limits
    
    # grab prolog dvips dosn't use %%BeginProlog!
    start=string.index(ps,"%%EndComments")+14
    end=string.index(ps,"%%EndProlog")
    prolog=ps[start:end]

    tt=[]
    pos1=end
    while 1:
        pos1=string.find(ps,"PyScriptStart",pos1)
        if pos1 <0:break
        pos2=string.find(ps,"PyScriptEnd",pos1)
        
        tt.append("TeXDict begin 1 0 bop\n%s\neop end"%ps[pos1+14:pos2])
        pos1=pos2
    
    assert len(tt)==len(objects)

    for ii in range(len(objects)):
        objects[ii].bodyps=tt[ii]


    # remove showpage
    # no we don't ... this kills some things
    #defs=re.sub("(?m)showpage","",defs)

    # Cant's seem to set a paper size of 0x0 without tinkering with
    # dvips config files. We need this so it matches with -E offsets.
    # the closest is the 'unknown' paper format which unfortunately
    # introduces some postript code that uses 'setpageparams' and 
    # 'setpage' for size. Can't seem to overide
    # those def easily so hunt out that code and kill it:
    # defs=re.sub("(?s)statusdict /setpageparams known.*?if } if","",defs)

    return prolog



# ---------------------------------------------------------------------------
# Create the actual postscript
# ---------------------------------------------------------------------------

class Eps(Group):
    '''
    Create the EPS
    '''
    
    # extra padding around EPS bbox to absorb effect
    # of line thicknesses etc (in pt)
    pad=2
    
    
    def write(self,fp,title="PyScriptEPS"):
        '''
        write a self-contained EPS file
        '''
        # XXX do translation here!

        # --- Header Comments ---
        
        # We conform DSC 3.0...
        fp.write("%!PS-Adobe-3.0 EPSF-3.0\n")
        SW,NE=self.bbox_pp()
        fp.write("%%%%BoundingBox: %d %d %d %d\n"%(SW[0],SW[1],NE[0],NE[1]))
        fp.write("%%%%Creator: PyScript %s\n"%version)
        fp.write("%%%%CreationDate: %s\n"%time.ctime(time.time()))
        # Color() can use CMYK ... don't need this with level 2 spec below
        # fp.write("%%Extensions: CMYK\n")
        # we've used some level 2 ops:
        fp.write("%%LanguageLevel: 2\n")
        fp.write("%%%%Title: %s\n"%title)
        # Say it's a single page:
        fp.write("%%Pages: 1\n") 
        fp.write("%%EndComments\n")

        # --- Prolog ---
        fp.write("%%BeginProlog\n")
        fp.write(PSMacros)
        # insert TeX prolog & fonts here
        fp.write(TeXstuff(self))
        fp.write("%%EndProlog\n")

        # --- Setup ---
        #fp.write("%%BeginSetup\n")
        # XXX set default mitre limits etc
        #fp.write("%%EndSetup\n")

        # --- Code ---
        fp.write("%%Page: 1 1\n")
        fp.write("PyScriptDict begin\n")
        fp.write('/uu {%f mul} def '%defaults.units)
        fp.write('%f setlinewidth '%defaults.linewidth)
        fp.write(self.prebody())
        fp.write(Group.body(self))
        fp.write(self.postbody())
        fp.write("end %PyScriptDict\n") # does this go after Trailer?
        fp.write("showpage\n") # where should this go?

        # --- Trailer ---
        fp.write("%%Trailer\n") 
        fp.write("%%EOF\n") 
        
    def __str__(self):
        '''
        Eps file with correct pre- and post- code for embeding
        '''
        out=cStringIO.StringIO()

        out.write("BeginEPSF\n")
        out.write("%%BeginDocument: PyScriptEPS\n")
        self.write(out)
        out.write("%%EndDocument\n")
        out.write("EndEPSF\n")
        
        return out.getvalue()

    def bbox_pp(self):
        '''
        Return the bbox in pp
        '''
        
        if len(self)==0:
            raise "No Objects for boundingbox"
        
        # Grab the groups bounding box
        b=self.bbox()
        
        p=P(self.pad,self.pad)

        # Make the sw corner (0,0) since some brain-dead previewers 
        # don't understand bounding-boxes
        self.move( P(0,0)-b.sw+p/float(defaults.units))

        SW=P(0,0)
        x=round(b.width*defaults.units)
        y=round(b.height*defaults.units)
        
        NE=P(x,y)+2*p
        
        return SW,NE
        
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

# -------------------------------------------------------------------------

def render(*objects,**opts):
    '''
    render the file
    '''

    if not opts.has_key('file'):
        raise "No filename given"

    out=open(opts['file'],"w")

    if len(objects)==0:
        raise "No objects to render!"
    elif len(objects)==1:
        if isinstance(objects[0],Eps):
            obj=objects[0]
        else:
            obj=apply(Eps,objects)
    else:
        obj=apply(Eps,objects)
        
    obj.write(out)
    out.close()

    print "Wrote",opts['file']











