"""
Module for reading and writing AFM files.
"""

# It does not implement the full spec (Adobe Technote 5004, Adobe Font Metrics
# File Format Specification). Still, it should read most "common" AFM files.
# Taken and adapted from afmLib.py in fonttools by Just van Rossum

import re,os,string,types,cPickle


FONTDIR="."

# every single line starts with a "word"
identifierRE = re.compile("^([A-Za-z]+).*")

# regular expression to parse char lines
charRE = re.compile(
    "(-?\d+)"			# charnum
    "\s*;\s*WX\s+"		# ; WX 
    "(\d+)"			# width
    "\s*;\s*N\s+"		# ; N 
    "([.A-Za-z0-9_]+)"	        # charname
    "\s*;\s*B\s+"		# ; B 
    "(-?\d+)"			# left
    "\s+"			# 
    "(-?\d+)"			# bottom
    "\s+"			# 
    "(-?\d+)"			# right
    "\s+"			# 
    "(-?\d+)"			# top
    "\s*;\s*"			# ; 
    )

# regular expression to parse kerning lines
kernRE = re.compile(
    "([.A-Za-z0-9_]+)"	# leftchar
    "\s+"		# 
    "([.A-Za-z0-9_]+)"	# rightchar
    "\s+"		# 
    "(-?\d+)"		# value
    "\s*"		# 
    )

# regular expressions to parse composite info lines of the form:
# Aacute 2 ; PCC A 0 0 ; PCC acute 182 211 ;
compositeRE = re.compile(
    "([.A-Za-z0-9_]+)"	# char name
    "\s+"		# 
    "(\d+)"		# number of parts
    "\s*;\s*"		# 
    )
componentRE = re.compile(
    "PCC\s+"		# PPC
    "([.A-Za-z0-9_]+)"	# base char name
    "\s+"		# 
    "(-?\d+)"		# x offset
    "\s+"		# 
    "(-?\d+)"		# y offset
    "\s*;\s*"		# 
    )


class error(Exception): pass

class ConvertAFM:
    _keywords = ['StartFontMetrics',
                 'EndFontMetrics',
                 'StartCharMetrics',
                 'EndCharMetrics',
                 'StartKernData',
                 'StartKernPairs',
                 'EndKernPairs',
                 'EndKernData',
                 'StartComposites',
                 'EndComposites',
                 ]
	
    def __init__(self, filename):

        self._attrs = {}
        self._chars = {}
        self._kerning = {}
        self._comments = []
        self._composites = {}

        self.parse(filename)


    def parse(self,path):

	f = open(path, 'rb')
	data = f.read()
	f.close()
	# read any text file, regardless whether it's
        # formatted for Mac, Unix or Dos
	sep = ""
	if '\r' in data:
		sep = sep + '\r'	# mac or dos
	if '\n' in data:
		sep = sep + '\n'	# unix or dos
	lines=string.split(data, sep)

        for line in lines:
            if not string.strip(line):
                continue
            m = identifierRE.match(line)
            if m is None:
                raise error, "syntax error in AFM file: " + `line`

            pos = m.regs[1][1]
            word = line[:pos]
            rest = string.strip(line[pos:])
            if word in self._keywords:
                continue
            if word == "C":
                self.parsechar(rest)
            elif word == "KPX":
                self.parsekernpair(rest)
            elif word == "CC":
                self.parsecomposite(rest)
            else:
                self.parseattr(word, rest)

    def write(self,filename):

        afm=AFM()

        afm._attrs=self._attrs
        afm._chars=self._chars
        afm._kerning=self._kerning
        afm._comments=self._comments
        afm._composites=self._composites

        fp=open(filename,"w")
        cPickle.dump(afm,fp)
        fp.close()
	
    def parsechar(self, rest):
        m = charRE.match(rest)
        if m is None:
            raise error, "syntax error in AFM file: " + `rest`
        things = []
        for fr, to in m.regs[1:]:
            things.append(rest[fr:to])
        charname = things[2]
        del things[2]
        charnum, width, l, b, r, t = map(string.atoi, things)
        # width l b r t
        self._chars[charnum] = width,l, b, r, t

    def parsekernpair(self, rest):
        m = kernRE.match(rest)
        if m is None:
            raise error, "syntax error in AFM file: " + `rest`
        things = []
        for fr, to in m.regs[1:]:
            things.append(rest[fr:to])
        leftchar, rightchar, value = things

        value = string.atoi(value)
        #self._kerning[(leftchar, rightchar)] = value
        # fix for all kernings
        if len(leftchar)==len(rightchar)==1:
            self._kerning[(ord(leftchar),ord(rightchar))]=value
	
    def parseattr(self, word, rest):
        if word == "FontBBox":
            l, b, r, t = map(string.atoi, string.split(rest))
            self._attrs[word] = l, b, r, t
        elif word == "Comment":
            self._comments.append(rest)
        else:
            try:
                value = string.atoi(rest)
            except (ValueError, OverflowError):
                self._attrs[word] = rest
            else:
                self._attrs[word] = value
	
    def parsecomposite(self, rest):
        m = compositeRE.match(rest)
        if m is None:
            raise error, "syntax error in AFM file: " + `rest`
        charname = m.group(1)
        ncomponents = int(m.group(2))
        rest = rest[m.regs[0][1]:]
        components = []
        while 1:
            m = componentRE.match(rest)
            if m is None:
                raise error, "syntax error in AFM file: " + `rest`
            basechar = m.group(1)
            xoffset = int(m.group(2))
            yoffset = int(m.group(3))
            components.append((basechar, xoffset, yoffset))
            rest = rest[m.regs[0][1]:]
            if not rest:
                break
        assert len(components) == ncomponents
        self._composites[charname] = components
	
	
class AFM:
	
    def __init__(self):

        self._attrs = {}
        self._chars = {}
        self._kerning = {}
        self._comments = []
        self._composites = {}
	
    def has_kernpair(self, pair):
        return self._kerning.has_key(pair)
	
    def kernpairs(self):
        return self._kerning.keys()
	
    def has_char(self, char):
        return self._chars.has_key(char)
	
    def chars(self):
        return self._chars.keys()
	
    def comments(self):
        return self._comments
	
    def addComment(self, comment):
        self._comments.append(comment)
	
    def __getattr__(self, attr):
        if self._attrs.has_key(attr):
            return self._attrs[attr]
        else:
            raise AttributeError, attr
		
    def __getitem__(self, key):
        if type(key) == types.TupleType:
            # key is a tuple, return the kernpair
            return self._kerning.get(key,0)
        else:
            # return the metrics instead
            return self._chars[key]
	
    def __repr__(self):
        if hasattr(self, "FullName"):
            return '<AFM object for %s>' % self.FullName
        else:
            return '<AFM object at %x>' % id(self)


def load(fontname):

    fontpath=os.path.join(FONTDIR,fontname)

    fp = open(fontpath+".font")
    font = cPickle.load(fp)
    fp.close()

    return font

if __name__ == "__main__":

	str=" ... pretty good Ay! .. WA"

        #c=ConvertAFM('Times-Roman.afm')
        #c.write('Times-Roman.font')
        #import sys
        #sys.exit()

	font=load('Times-Roman')

        #cPickle.dump(font,open("Times-Roman.font","w"))

        #font=cPickle.load(open("Times-Roman.font"))

        print font

	chars=map(ord,list(str))

	#tot=0
	#for cc in xrange(len(chars)):
	#	tot+=font[chars[cc]][0]

	# order: width l b r t

	# use reduce as it's a built in function written in C

	# add up all the widths
	width= reduce(lambda x, y: x+font[y][0],chars,0)

	# subtract the kerning
	if len(chars)>1:
	    kern=reduce(lambda x,y:x+y,
		    map(lambda x,y:font[(x,y)] ,chars[:-1],chars[1:]))
	    print kern
	    #width+=kern

	# get rid of the end bits
	start=font[chars[0]][1]
	f=font[chars[-1]]
	width = width-start-(f[0]-f[3])


	# accumulate maximum height
	top = reduce(lambda x, y: max(x,font[y][4]),chars,0)

	# accumulate lowest point
	bottom = reduce(lambda x, y: min(x,font[y][2]),chars,font[chars[0]][2])

	height=top-bottom
	
	print f
	print f[1],f[2],f[3]-f[1],f[4]-f[2]
	print start,bottom,width,height

	sc=124/1000.

	w2=width*sc
	h2=height*sc
	s=start*sc
	b=bottom*sc

	import sys
	sys.path.insert(0,'../')
	
	from pyscript import *
	t=Text(str,scale="124")
	w,h=t['ne']-t['sw']

	print s,b,w2,h2
	render(
		Rectangle(width=w,height=h,sw=t['sw'],fg=Color('green')),
		Rectangle(width=w2,height=h2,sw=P(s,b),fg=Color('red')),
		t,
		file='tmp.eps',
		)
