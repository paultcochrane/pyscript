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

VERSION="0.0.1"

import sys,os
import cStringIO
import time

from defaults import *
from util import *
from objects import *
from groups import *

# we need to double up the comment %'s
# The BoundingBox and EndComments will be added later
EPSheader="""%%!PS-Adobe-2.0 EPSF-2.0
%%%%Creator: pyscript v%s
%%%%CreationDate: %s
"""%(VERSION,time.ctime(time.time()))

PSheader="""%%!PS-Adobe-2.0
%%%%Creator: pyscript v%s
%%%%CreationDate: %s
%%%%Page: 1 1
"""%(VERSION,time.ctime(time.time()))

# NB and 'end' was added to EndEPSF
PSMacros="""%% show text with kerning if supplied
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
"""

import os,re
##def TeXdefs(text=""):
##    '''
##    get font & stuff headers out of dvips
##    '''

##    file="temp.tex"
##    fp=open(file,"w")
##    fp.write(defaults.tex_head)
##    fp.write(text)
##    fp.write(defaults.tex_tail)
##    fp.close()

##    os.system(defaults.tex_command%file)

##    os.system("dvips -E -o temp.eps temp.dvi")

##    fp=open("temp.eps","r")
##    eps=fp.read(-1)
##    fp.close()

##    # grab headers
##    so=re.search("(\%\%BeginProcSet.*)\s*TeXDict begin \d",eps,re.S)
##    defs=so.group(1)

##    # remove showpage
##    defs=re.sub("(?m)showpage","",defs)

##    return "\n%s\n"%defs


def TeXstuff(objects):
    '''
    Get the actual postscript code and insert it into
    the tex objects. Also grab fonts and defs
    '''

    file="temp.tex"
    fp=open(file,"w")
    fp.write(defaults.tex_head)
    for tex in objects:
        fp.write(tex.text)
        fp.write('\\newpage\n')
    fp.write(defaults.tex_tail)
    fp.close()

    os.system(defaults.tex_command%file)

    os.system("dvips -tunknown -o temp.ps temp.dvi")

    fp=open("temp.ps","r")
    ps=fp.read(-1)
    fp.close()

    #grab tex
    tt=re.findall('(?s)\%\%Page:.*?TeXDict(.*?)end',ps)

    assert len(tt)==len(objects)

    for ii in range(len(objects)):
        objects[ii].bodyps="TeXDict %s end"%tt[ii]

    # grab headers
    start=string.index(ps,"%DVIPSSource")
    end=string.index(ps,"%%Page:")
    defs=ps[start:end]

    # remove showpage
    defs=re.sub("(?m)showpage","",defs)

    # Cant's seem to set a paper size of 0x0 without tinkering with
    # dvips config files. We need this so it matches with -E offsets.
    # the closest is the 'unknown' paper format which unfortunately
    # introduces some postript code
    # that uses 'setpageparams' and 'setpage' for size. Can't seem to overide
    # those def easily so hunt out that code and kill it:
    defs=re.sub("(?s)statusdict /setpageparams known.*?if } if","",defs)

    return "\n%s\n"%defs


#def collecttex(objects,tex):
#    for object in objects:
#        if isinstance(object,TeX):
#            tex=tex+object.text
#        elif isinstance(object,Group):
#            tex=collecttex(object.objects,tex)
#    return tex

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

# ---------------------------------------------------------------------------
# Create the actual postscript
# ---------------------------------------------------------------------------

##def render(*objects,**opts):
##    '''
##    render the file
##    '''

##    filetype=opts.get('type','eps')

##    if not opts.has_key('file'):
##        opts['file']=sys.argv[0]+".eps"
        
        
##    if opts['file']=='-':
##        out=sys.stdout
##    else:
##        print "Writing",opts['file']
##        out=open(opts['file'],"w")

##    # step through and accumulate postscript
##    # and auxillary information

##    tex=collecttex(objects,"")
    
##    defs=""
##    if len(tex)>0:
##        defs=TeXdefs(tex)


##    # put all objects into group
##    #if len(objects)>1:
##    #    objects=Group(objects)

##    if type(objects)==type(()):
##        objects=apply(Group,objects)

##    # Make the sw corner (0,0) since some brain-dead previewers 
##    # don't understand bounding-boxes
##    objects.sw=P(0,0)
    
##    bbox=objects.bbox()

##    if not bbox.is_set():
##        print "No objects to render!"
##        return
##    SW=bbox.sw
##    NE=bbox.ne


##    pad=5 # no. of points to pad bbox with
##    # convert bbox to points
##    SW[0]=round(SW[0]*defaults.units)-pad
##    SW[1]=round(SW[1]*defaults.units)-pad
##    NE[0]=round(NE[0]*defaults.units)+pad
##    NE[1]=round(NE[1]*defaults.units)+pad


##    if filetype=='ps':
##        out.write(PSheader)

##    else:
##        out.write(EPSheader)
##        out.write('%%%%BoundingBox: %d %d %d %d\n%%%%EndComments\n'%\
##                  (SW[0],SW[1],NE[0],NE[1]))

##    out.write(PSMacros)
##    out.write('/uu {%f mul} def '%defaults.units)
##    out.write('%f setlinewidth '%defaults.linewidth)
##    out.write(defs)
    
##    out.write(str(objects))
    
##    if filetype=='ps':
##        out.write('\nshowpage\n')

##    out.close()

def render(*objects,**opts):
    '''
    render the file
    '''

    filetype=opts.get('type','eps')

    if not opts.has_key('file'):
        opts['file']=sys.argv[0]+".eps"
        
        
    if opts['file']=='-':
        out=sys.stdout
    else:
        print "Writing",opts['file']
        out=open(opts['file'],"w")

    # step through and accumulate postscript
    # and auxillary information

    tex=collecttex(objects)

    defs=""
    if len(tex)>0:
        defs=TeXstuff(tex)


    # put all objects into group
    #if len(objects)>1:
    #    objects=Group(objects)

    if type(objects)==type(()):
        objects=apply(Group,objects)

    # Make the sw corner (0,0) since some brain-dead previewers 
    # don't understand bounding-boxes
    objects.sw=P(0,0)
    
    bbox=objects.bbox()

    if not bbox.is_set():
        print "No objects to render!"
        return
    SW=bbox.sw
    NE=bbox.ne


    pad=5 # no. of points to pad bbox with
    # convert bbox to points
    SW[0]=round(SW[0]*defaults.units)-pad
    SW[1]=round(SW[1]*defaults.units)-pad
    NE[0]=round(NE[0]*defaults.units)+pad
    NE[1]=round(NE[1]*defaults.units)+pad


    if filetype=='ps':
        out.write(PSheader)

    else:
        out.write(EPSheader)
        out.write('%%%%BoundingBox: %d %d %d %d\n%%%%EndComments\n'%\
                  (SW[0],SW[1],NE[0],NE[1]))

    out.write(PSMacros)
    out.write('/uu {%f mul} def '%defaults.units)
    out.write('%f setlinewidth '%defaults.linewidth)
    out.write(defs)
    
    out.write(str(objects))
    
    if filetype=='ps':
        out.write('\nshowpage\n')

    out.close()










