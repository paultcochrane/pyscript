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
from objects import Group

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

import os,re
def TeXdefs(text=""):
    '''
    get font & stuff headers out of dvips
    '''

    file="temp.tex"
    fp=open(file,"w")
    fp.write(defaults.tex_head)
    fp.write(text)
    fp.write(defaults.tex_tail)
    fp.close()

    os.system(defaults.tex_command%file)

    os.system("dvips -E -o temp.eps temp.dvi")

    fp=open("temp.eps","r")
    eps=fp.read(-1)
    fp.close()

    # grab headers
    so=re.search("(\%\%BeginProcSet.*)\s*TeXDict begin \d",eps,re.S)
    defs=so.group(1)

    # remove showpage
    defs=re.sub("(?m)showpage","",defs)

    return "\n%s\n"%defs

def collecttex(objects,tex):
    for object in objects:
        if pstype(object)==TeXType:
            tex=tex+object.text
        elif pstype(object)==GroupType:
            tex=collecttex(object.objects,tex)
    return tex

# ---------------------------------------------------------------------------
# Create the actual postscript
# ---------------------------------------------------------------------------


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

    tex=collecttex(objects,"")
    
    # XXX Doesn't handle nested groups!!!

    defs=""
    if len(tex)>0:
        defs=TeXdefs(tex)

    # put all objects into group
    #if len(objects)>1:
    #    objects=Group(objects)

    if type(objects)==type(()):
        objects=apply(Group,objects)

    SW,NE=objects.boundingbox()
    
    if not SW or not NE:
        print "No objects to render!"
        return

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

    out.write('/uu {%f mul} def '%defaults.units)
    out.write('%f setlinewidth '%defaults.linewidth)
    out.write(defs)
    
    out.write(str(objects))
    
    if filetype=='ps':
        out.write('\nshowpage\n')

    out.close()











