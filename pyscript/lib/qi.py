
### = we have the equivalent
#   = not yet implemented

###  def     - define a custom controlled single-qubit operation, with
###            opname  = name of gate operation
###            nctrl   = number of control qubits
###            texsym  = latex symbol for the target qubit operation
###  defbox  - define a custom muti-qubit-controlled multi-qubit operation, with
###            opname  = name of gate operation
###            nbits   = number of qubits it acts upon
###            nctrl   = number of control qubits
###            texsym  = latex symbol for the target qubit operation
###  qubit   - define a qubit with a certain name (all qubits must be defined)
###            name    = name of the qubit, eg q0 or j2 etc
###            initval = initial value (optional), eg 0
###  cbit    - define a cbit with a certain name (all cbits must be defined)
###            name    = name of the cbit, eg c0
###            initval = initial value (optional), eg 0
###  H       - single qubit operator ("hadamard")
###  X       - single qubit operator 
###  Y       - single qubit operator 
###  Z       - single qubit operator
###  S       - single qubit operator
###  T       - single qubit operator
###  nop     - single qubit operator, just a wire
###  space   - single qubit operator, just an empty space
###  dmeter  - measure qubit, showing "D" style meter instead of rectangular box
#  zero    - replaces qubit with |0> state
#  discard - discard qubit (put "|" vertical bar on qubit wire)
#  slash   - put slash on qubit wire
###  measure - measurement of qubit, gives classical bit (double-wire) output
###  cnot    - two-qubit CNOT
###  c-z     - two-qubit controlled-Z gate
###  c-x     - two-qubit controlled-X gate
#  swap    - two-qubit swap operation 
###  Utwo    - two-qubit operation U
###  ZZ      - two-qubit controlled-Z gate, symmetric notation; two filled circles
#  SS      - two-qubit gate, symmetric; open squares
###  toffoli - three-qubit Toffoli gate

# -----------------------------------------------------------------------------
'''
Package for drawing quantum circuit diagrams


'''

from pyscript import *


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

    target=P(0,0)
    control=None
    dot_r=.1
    
    def __init__(self,obj,**dict):
        
        apply(Group.__init__, (self,), dict)

        self.obj=obj

        if type(self.control) in (type(()),type([])):
            for p in self.control:
                self.addcontrol(p)
                
        elif isinstance(self.control,P):
            self.addcontrol(self.control)

        obj.c=self.target

        self.append(
            obj,
            )

    def addcontrol(self,p):

        self.append(Path(self.target,p))
        self.append(Dot(p,r=self.dot_r))
        


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

def Rx(arg,**dict): return GCT('$R_x(%s)$'%arg,**dict)
def Ry(arg,**dict): return GCT('$R_y(%s)$'%arg,**dict)
def Rz(arg,**dict): return GCT('$R_z(%s)$'%arg,**dict)

# -------------------------------------------------------------------------
def Not(**dict):
    r=.2
    return Gate(
        Group(Circle(r=r),Path(P(0,r),P(0,-r)),Path(P(-r,0),P(r,0))),
        **dict)
# -------------------------------------------------------------------------
def CSIGN(**dict):
    return Gate(Dot(r=Gate.dot_r),**dict)

ZZ=CSIGN
# -------------------------------------------------------------------------
#def Swap(**dict):
#    return Gate(Dot(r=Gate.dot_r),**dict)
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
class Qubit(Path):

	def __init__(self):
		# these will get tweaked afterwards
		pass

class Bit(ClassicalPath):

	def __init__(self):
		# these will get tweaked afterwards
		pass

class T:
	'''
	Time-slice labeling object
	'''
	def __init__(self,t=1):
		self.t=t
# -------------------------------------------------------------------------
class Qasm(Group):

    def __init__(self,*qubits,**dict):

        apply(Group.__init__, (self,), dict)

	# create wires ...
	if len(qubits)==1 and isinstance(qubits[0],Integer):
		n = qubits[0]

		wires=[]
		for w in range(n):
			wires.append(Qubit())

	else:
		wires=qubits
			

    def add(self,gate):
	'''
	Add gates to the quantum circuit
	'''
        pass

# -------------------------------------------------------------------------
# misc other items
# -------------------------------------------------------------------------

class Meter(Group):
    """
    A meter object as in Mike'n'Ike
     
    """
    height=1
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
                P(w-.3,.1),C(0,0),P(.3,.1),
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


