
### = we have the equivalent
#   = not yet implemented

#  zero    - replaces qubit with |0> state
#  discard - discard qubit (put "|" vertical bar on qubit wire)
#  slash   - put slash on qubit wire
#  Utwo    - two-qubit operation U
#  SS      - two-qubit gate, symmetric; open squares

# -----------------------------------------------------------------------------
'''
Package for drawing quantum circuit diagrams


'''

from pyscript import *
from types import *

# -------------------------------------------------------------------------
class Boxed(Group,Rectangle):
    '''
    Draws a box around an object,
    the box can be placed acording to standard Area tags

    @cvar pad: padding around object
    @cvar width: overide the width of the box
    @cvar height: override the height of the box
    
    '''

    fg=Color(0)
    bg=Color(1)
    pad=.2

    def __init__(self,obj,**dict):
        
        apply(Rectangle.__init__, (self,), dict)
        apply(Group.__init__, (self,), dict)

        bbox=obj.bbox()

        w=bbox.width+2*self.pad
        h=bbox.height+2*self.pad

        self.width=dict.get('width',w)
        self.height=dict.get('height',h)

        self.append(
            Rectangle(width=self.width,height=self.height,
                      bg=self.bg,fg=self.fg,
                      c=obj.c,
                      r=self.r,linewidth=self.linewidth,dash=self.dash),

            obj,
            )

# -------------------------------------------------------------------------
class Circled(Group,Circle):
    '''
    Draws a circle around an object,

    @cvar pad: padding around object
    @cvar r: overide the radius of the circle
    
    '''

    fg=Color(0)
    bg=Color(1)
    pad=.1

    def __init__(self,obj,**dict):
        
        apply(Circle.__init__, (self,), dict)
        apply(Group.__init__, (self,), dict)

        bbox=obj.bbox()

        w=bbox.width+2*self.pad
        h=bbox.height+2*self.pad

        self.r=dict.get('r',max(w,h)/2.)

        self.append(
            Circle(r=self.r,
                   bg=self.bg,fg=self.fg,
                   c=obj.c,
                   linewidth=self.linewidth,dash=self.dash),

            obj,
            )


# -------------------------------------------------------------------------
class Gate(Group):

    control=None
    target=None
    
    dot_r=.1
   
    # target object get set in __init__
    targetobj=None
    controlobj=None


    def __init__(self,tobj,**dict):
        
        Group.__init__(self,**dict)

        # XXX should we take a copy???
        self.targetobj=tobj.copy()

        if self.controlobj is None:
            self.controlobj=Dot(r=self.dot_r)

        # fix up target and control points    
        if type(self.target) in (type(()),type([])):
            pass
        elif isinstance(self.target,P):
            self.target=[self.target]
        elif self.target is None:
            self.target=[P(0,0)]
        else:
            raise "don't understand target structure for Gate"
            
        if type(self.control) in (type(()),type([])):
            pass
        elif isinstance(self.control,P):
            self.control=[self.control]
        elif self.control is None:
            self.control=[]
        else:
            raise "don't understand control structure for Gate"

        self._make()

    def settarget(self,*p):
        
        self.target=p
        self._make()
        
        
    def setcontrol(self,*p):

        self.control=p
        self._make()
        
    def _make(self):

        self.clear()
        
        # calc average target point
        tp=self.target[0]
        if len(self.target)>1:
            for tt in self.target[1:]:
                tp=tp+tt
            tp=tp/float(len(self.target))
        
        self.targetobj.c=tp

        #XXX should target adjust height here

        # add controls 
        for cc in self.control:
            self.append(Path(tp,cc))
            self.controlobj.c=cc
            self.append(self.controlobj.copy())

        self.append(self.targetobj)
            

# -------------------------------------------------------------------------
class GateBoxedTeX(Gate):
    def __init__(self,tex,**dict):
        apply(Gate.__init__, (self,Boxed(TeX(tex))) , dict)

GBT=GateBoxedTeX
# -------------------------------------------------------------------------
class GateCircledTeX(Gate):
    def __init__(self,tex,**dict):
        apply(Gate.__init__, (self,Circled(TeX(tex))) , dict)

GCT=GateCircledTeX
# -------------------------------------------------------------------------
def H(**dict): return GBT('$H$',**dict)
def X(**dict): return GBT('$X$',**dict)
def Y(**dict): return GBT('$Y$',**dict)
def Z(**dict): return GBT('$Z$',**dict)
def S(**dict): return GBT('$S$',**dict)
def T(**dict): return GBT('$T$',**dict)

def RX(arg,**dict): return GCT('$R_x(%s)$'%arg,**dict)
def RY(arg,**dict): return GCT('$R_y(%s)$'%arg,**dict)
def RZ(arg,**dict): return GCT('$R_z(%s)$'%arg,**dict)

# -------------------------------------------------------------------------
def NOT(**dict):
    r=.2
    return Gate(
        Group(Circle(r=r),Path(P(0,r),P(0,-r)),Path(P(-r,0),P(r,0))),
        **dict)
# -------------------------------------------------------------------------
def CSIGN(**dict):
    return Gate(Dot(r=Gate.dot_r),**dict)

ZZ=CSIGN
# -------------------------------------------------------------------------
def SWAP(**dict):
    x=Group(Path(P(-.1,.1),P(.1,-.1)),Path(P(-.1,-.1),P(.1,.1)))
    dict['controlobj']=dict.get('controlobj',x)
    return Gate(x,**dict)
    #return Gate(x,**dict)
# -------------------------------------------------------------------------

# XXX make this a class!
class ClassicalPath:
    pass

def classicalpath(*paths):
    '''
    @return: classical path
    @param paths: 1 or more Path() objects
    '''
    g=Group()

    for path in paths:
        g.append(path.copy(linewidth=2,fg=Color(0)))

    # reuse these paths
    for path in paths:
        g.append(path(linewidth=1,fg=Color(1)))

    return g


# -------------------------------------------------------------------------


class NoWire(Group):
    def __init__(self,**dict):
        Group.__init__(self,**dict)

    def set(self,y,e,w):
        return self
    
class QWire(NoWire):
    
    fg=Color(0)
    linewidth=None
    dash=None

    def set(self,y,e,w):
        path=Path(P(w,y),P(e,y),
                fg=self.fg,linewidth=self.linewidth,dash=self.dash)
        self.append(path)
        return self

class CWire(QWire):
    def set(self,y,e,w):
        path=Path(P(w,y),P(e,y),
                fg=self.fg,linewidth=self.linewidth,dash=self.dash)
        
        self.append(classicalpath(path))
        return self
    

class Assemble(Group):

    wirespacing=1
    gatespacing=.1
   
    wires=[]
    hang=.2
    starthang=hang
    endhang=hang

   
    def __init__(self,*gates,**dict):
       

        self.starthang=dict.get('hang',self.hang)
        self.endhang=dict.get('hang',self.hang)
        Group.__init__(self,**dict)
        
        sequence=list(gates)
        
        # parse the list ...
        wires=[]
        named={}
        basetime=0
        while len(sequence)>0:
            # the gate ...
            gate=sequence.pop(0)

            # the target ...
            t=sequence.pop(0)
            wires.append(t)

            # optional controls ...
            if len(sequence)>0 and isinstance(sequence[0],(IntType,FloatType)):
                c=sequence.pop(0)
                wires.append(c)
            elif len(sequence)>0 and isinstance(sequence[0],(TupleType,ListType)):
                c=sequence.pop(0)
                wires.extend(c)
            else:
                c=None

            g=self.setgate(gate,t,c)

            # optional time label ...
            if len(sequence)>0 and isinstance(sequence[0],StringTypes):
                l=sequence.pop(0)
                if named.has_key(l):
                    # group already exists
                    named[l].append(g)
                else:
                    # create new named group
                    G=named[l]=Group(g)
                    self.append(G)
            else:
                self.append(g)
       
        L=0
        for ii in self:
            L+=ii.width+self.gatespacing
        L-=self.gatespacing

        # XXX add distribute's options
        Distribute(self,p1=P(0,0),p2=P(L,0))            
        self.recalc_size()

        # XXX should check wires are ints

        # add wires ...
        x0=self.w.x-self.starthang
        x1=self.e.x+self.endhang
        if len(self.wires) == 0:
            for w in range(-min(wires),-max(wires)-1,-1):
                wire=QWire().set(w*self.wirespacing,x0,x1)
                self.insert(0,wire)
                self.wires.append(wire)
            print self.wires
        else:
            #w=-int(min(wires))
            w=-1
            wirestmp=[]
            for wire in self.wires:
                # if it already an instance this will have no effect
                # otherwise create an instance
                wire=apply(wire,())
                wire.set(w*self.wirespacing,x0,x1)
                self.insert(0,wire)
                wirestmp.append(wire)
                w-=1
            self.wires=wirestmp

        
    def setgate(self,gate,target,control=None):

        # if it already an instance this will have no effect
        # otherwise create an instance
        gate=apply(gate)
        
        # XXX multi target qubits
        gate.settarget(P(0,-target))
       
        if isinstance(control,(IntType,FloatType)):
            gate.setcontrol(P(0,-control))
        elif isinstance(control,(TupleType,ListType)):
            tmp=[]
            for cc in control:
                tmp.append(P(0,-cc))
            apply(gate.setcontrol,tmp)

        return gate

# -------------------------------------------------------------------------
# misc other items
# -------------------------------------------------------------------------

class Meter(Group):
    """
    A meter object as in Mike'n'Ike
     
    """
    height=.7
    width=1.8*height

    angle=45
    bg=Color(1)
    mcolor=Color(.8)
    
    def __init__(self,**args):

        Group.__init__(self,**args)

        h=self.height
        w=self.width
		
        
        self.append(Rectangle(width=1.8*h,height=h,bg=self.bg))
        
        p=Path(
                P(.1,.1),C(0,0),P(w-.1,.1),
                P(w-.2,.1),C(0,0),P(.2,.1),
                closed=1,bg=self.mcolor,fg=None)
        
        self.append(p,
            Path(P(w/2.,.1),U(self.angle,h*.9)),
            )

# -------------------------------------------------------------------------
class Detector(Group):
    '''
    A D shaped detector, can be given an object to surround
    '''

    height=.8
    width=height/2.
    bg=Color(1)
    fg=Color(0)
    pad=.1
	
    def __init__(self,object=None,**dict):
		
        if object is not None:
            # use the objects boundingbox when width and height not supplied
            bb=object.bbox()
            w=bb.width+2*self.pad
            h=bb.height+2*self.pad

            self.width=dict.get("width",max(w,self.width))
            self.height=dict.get("height",max(h,self.height))
        Group.__init__(self,**dict)

        if self.width>self.height:
            p=Path(
                P(0,0),P(0,self.height),
                P(self.width-self.height/2.,self.height),C(90,0),
                P(self.width,self.height/2.), C(180,90),
                P(self.width-self.height/2.,0),
                closed=1)
        else:
			
            p=Path(
                P(0,0),P(0,self.height),  C(90,0),
                P(self.width,self.height/2.), C(180,90),
                closed=1)
		
        p(bg=dict.get("bg",self.bg),fg=dict.get("fg",self.fg))

        self.append(p)
        if object is not None:
            # object looks better if it's slightly off centre
            # since one side is curved. pad/3 is about right
            object.c=P(self.width/2.-self.pad/3.,self.height/2.)
            self.append(object)

