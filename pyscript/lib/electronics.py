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
pyscript Electronics objects library

thanks to Adrian Jonstone's lcircuit macros from CTAN for the ideas and names
"""

from pyscript import *

# AND gate
def AndGate(
    sw=P(0,0),
    direction='e',
    height=2.0,
    width=3.0,
    pinLength=0.5,
    label=None,
    labelPinIn1=None,
    labelPinIn2=None,
    labelPinOut=None
    ):
    """
    Generates an AND gate
    @param sw: the position of the sw reference point
    @param direction: the direction of the gate
    @param height: vertical extent of gate
    @param width: horizontal extent of gate (equivalent to length)
    @param pinLength: length of pins into and out of gate
    @param label: overall label
    @param labelPinIn1: label for input pin 1 (the top one for default
	direction)
    @param labelPinIn2: label for input pin 2 (th bottom one for default
	direction)
    @param labelPinOut: label for output pin
    @return: a Group() object of the gate
    """
    
    buff = 0
    pinEdgeDist = 0.1*height
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    gateBody = Group(Path(sw+P(pinLength,buff+0), 
	sw+P(pinLength,buff+bodyHeight), 
	sw+P(pinLength+bodyWidth/2.,buff+bodyHeight)),
        Circle(c=sw+P(pinLength+bodyWidth/2.,buff+bodyHeight/2.), 
		r=bodyHeight/2., start=0, end=180),
        Path(sw+P(pinLength+bodyWidth/2.,buff+0), sw+P(pinLength,buff+0)))
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist), 
	sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Path(sw+P(bodyWidth+pinLength,bodyHeight/2.), 
	sw+P(bodyWidth+2.*pinLength,bodyHeight/2.))

    if direction == 'e':
	angle = 0
    elif direction == 'n':
	angle = -90
    elif direction == 's':
	angle = 90
    elif direction == 'w':
 	angle = 180
    else:
	print "Incorrect direction entered, 'e' used..."
	angle = 0

    if label is not None:
	obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
	return obj.rotate(angle,p=obj.c)
    else:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)
	return obj.rotate(angle,p=obj.c)

# NAND gate
def NandGate(
	sw=P(0,0), 
	direction='e', 
	height=2.0, 
	width=3.0, 
	pinLength=0.5, 
	label=None, 
	labelPinIn1=None, 
	labelPinIn2=None, 
	labelPinOut=None,
	):
    """
    Generates a NAND gate
    @param sw: the position of the sw reference point
    @param direction: the direction of the gate
    @param height: vertical extent of gate
    @param width: horizontal extent of gate (equivalent to length)
    @param pinLength: length of pins into and out of gate
    @param label: overall label
    @param labelPinIn1: label for input pin 1 (the top one for default
        direction)
    @param labelPinIn2: label for input pin 2 (th bottom one for default
        direction)
    @param labelPinOut: label for output pin
    @return: a Group() object of the gate
    """

    buff = 0
    pinEdgeDist = 0.1*height
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = Group(Path(sw+P(pinLength,buff+0), 
	sw+P(pinLength,buff+bodyHeight), 
	sw+P(pinLength+bodyWidth/2.,buff+bodyHeight)),
        Circle(c=sw+P(pinLength+bodyWidth/2.,buff+bodyHeight/2.), 
		r=bodyHeight/2., start=0, end=180),
        Path(sw+P(pinLength+bodyWidth/2.,buff+0), sw+P(pinLength,buff+0)))
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist), 
		sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Group(
        Circle(c=P(bodyWidth+pinLength+rad,bodyHeight/2.),r=rad),
        Path(sw+P(bodyWidth+pinLength+2.*rad,bodyHeight/2.), 
		sw+P(bodyWidth+2.*rad+2.*pinLength,bodyHeight/2.)))

    if direction == 'e':
        angle = 0
    elif direction == 'n':
        angle = -90
    elif direction == 's':
        angle = 90
    elif direction == 'w':
        angle = 180
    else:
        print "Incorrect direction entered, 'e' used..."
        angle = 0

    if label is not None:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
	return obj.rotate(angle,p=obj.c)
    else:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)
	return obj.rotate(angle,p=obj.c)

# OR gate
def OrGate(
	sw=P(0,0), 
	direction='e', 
	height=2.0, 
	width=3.0, 
	pinLength=0.5, 
	label=None, 
	labelPinIn1=None, 
	labelPinIn2=None, 
	labelPinOut=None):
    """
    Generates an OR gate
    @param sw: the position of the sw reference point
    @param direction: the direction of the gate
    @param height: vertical extent of gate
    @param width: horizontal extent of gate (equivalent to length)
    @param pinLength: length of pins into and out of gate
    @param label: overall label
    @param labelPinIn1: label for input pin 1 (the top one for default
        direction)
    @param labelPinIn2: label for input pin 2 (th bottom one for default
        direction)
    @param labelPinOut: label for output pin
    @return: a Group() object of the gate
    """
    # should it be direction or dir?
    pinEdgeDist = 0.1*height
    pinBackDist = -0.08*width
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = Path(sw-P(pinBackDist,pinEdgeDist),
		C(sw+P(pinLength+bodyWidth/2.,0)),
		sw+P(1.25*bodyWidth,bodyHeight/2.),
		C(sw+P(pinLength+bodyWidth/2.,bodyHeight)),
		sw+P(-pinBackDist,bodyHeight+pinEdgeDist),
		C(sw+P(2.0*pinLength,bodyHeight/2.)),
		sw-P(pinBackDist,pinEdgeDist),
		)
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist), 
		sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Path(gateBody.e,gateBody.e+P(pinLength,0))

    if direction == 'e':
        angle = 0
    elif direction == 'n':
        angle = -90
    elif direction == 's':
        angle = 90
    elif direction == 'w':
        angle = 180
    else:
        print "Incorrect direction entered, 'e' used..."
        angle = 0

    if label is not None:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
	return obj.rotate(angle,p=obj.c)
    else:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)
	return obj.rotate(angle,p=obj.c)

# NOR gate
def NorGate(
        sw=P(0,0),
        direction='e',
        height=2.0,
        width=3.0,
        pinLength=0.5,
        label=None,
        labelPinIn1=None,
        labelPinIn2=None,
        labelPinOut=None):
    """
    Generates a NOR gate
    @param sw: the position of the sw reference point
    @param direction: the direction of the gate
    @param height: vertical extent of gate
    @param width: horizontal extent of gate (equivalent to length)
    @param pinLength: length of pins into and out of gate
    @param label: overall label
    @param labelPinIn1: label for input pin 1 (the top one for default
        direction)
    @param labelPinIn2: label for input pin 2 (th bottom one for default
        direction)
    @param labelPinOut: label for output pin
    @return: a Group() object of the gate
    """
    pinEdgeDist = 0.1*height
    pinBackDist = -0.08*width
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = Path(sw-P(pinBackDist,pinEdgeDist),
                C(sw+P(pinLength+bodyWidth/2.,0)),
                sw+P(1.25*bodyWidth,bodyHeight/2.),
                C(sw+P(pinLength+bodyWidth/2.,bodyHeight)),
                sw+P(-pinBackDist,bodyHeight+pinEdgeDist),
                C(sw+P(2.0*pinLength,bodyHeight/2.)),
                sw-P(pinBackDist,pinEdgeDist),
                )
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist),
                sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Group(
		Circle(w=gateBody.e,r=0.1),
		Path(gateBody.e+P(0.2,0),gateBody.e+P(pinLength+0.2,0)),
		)

    if direction == 'e':
        angle = 0
    elif direction == 'n':
        angle = -90
    elif direction == 's':
        angle = 90
    elif direction == 'w':
        angle = 180
    else:
        print "Incorrect direction entered, 'e' used..."
        angle = 0

    if label is not None:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
	return obj.rotate(angle,p=obj.c)
    else:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)
	return obj.rotate(angle,p=obj.c)

# XOR gate
def XorGate(
        sw=P(0,0),
        direction='e',
        height=2.0,
        width=3.0,
        pinLength=0.5,
        label=None,
        labelPinIn1=None,
        labelPinIn2=None,
        labelPinOut=None):
    """
    Generates an XOR gate
    @param sw: the position of the sw reference point
    @param direction: the direction of the gate
    @param height: vertical extent of gate
    @param width: horizontal extent of gate (equivalent to length)
    @param pinLength: length of pins into and out of gate
    @param label: overall label
    @param labelPinIn1: label for input pin 1 (the top one for default
        direction)
    @param labelPinIn2: label for input pin 2 (th bottom one for default
        direction)
    @param labelPinOut: label for output pin
    @return: a Group() object of the gate
    """
    pinEdgeDist = 0.1*height
    pinBackDist = -0.08*width
    xBit = 0.2
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = Group(
		Path(sw+P(-pinBackDist+xBit,-pinEdgeDist),
                	C(sw+P(pinLength+xBit+bodyWidth/2.,0)),
                	sw+P(1.4*bodyWidth,bodyHeight/2.),
                	C(sw+P(pinLength+xBit+bodyWidth/2.,bodyHeight)),
                	sw+P(-pinBackDist+xBit,bodyHeight+pinEdgeDist),
                	C(sw+P(2.0*pinLength+xBit,bodyHeight/2.)),
                	sw+P(-pinBackDist+xBit,-pinEdgeDist),
                	),
		Path(sw+P(-pinBackDist,bodyHeight+pinEdgeDist),
                        C(sw+P(2.0*pinLength,bodyHeight/2.)),
                        sw+P(-pinBackDist,-pinEdgeDist)
			),
		)
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist),
                sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Path(gateBody.e,gateBody.e+P(pinLength,0))

    if direction == 'e':
        angle = 0
    elif direction == 'n':
        angle = -90
    elif direction == 's':
        angle = 90
    elif direction == 'w':
        angle = 180
    else:
        print "Incorrect direction entered, 'e' used..."
        angle = 0

    if label is not None:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
	return obj.rotate(angle,p=obj.c)
    else:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)
	return obj.rotate(angle,p=obj.c)

# NXOR gate
def NxorGate(
        sw=P(0,0),
        direction='e',
        height=2.0,
        width=3.0,
        pinLength=0.5,
        label=None,
        labelPinIn1=None,
        labelPinIn2=None,
        labelPinOut=None):
    """ 
    Generates a NXOR gate
    @param sw: the position of the sw reference point
    @param direction: the direction of the gate
    @param height: vertical extent of gate
    @param width: horizontal extent of gate (equivalent to length)
    @param pinLength: length of pins into and out of gate
    @param label: overall label
    @param labelPinIn1: label for input pin 1 (the top one for default
        direction)
    @param labelPinIn2: label for input pin 2 (th bottom one for default
        direction)
    @param labelPinOut: label for output pin
    @return: a Group() object of the gate
    """
    pinEdgeDist = 0.1*height
    pinBackDist = -0.08*width
    xBit = 0.2
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = Group(
                Path(sw+P(-pinBackDist+xBit,-pinEdgeDist),
                        C(sw+P(pinLength+xBit+bodyWidth/2.,0)),
                        sw+P(1.4*bodyWidth,bodyHeight/2.),
                        C(sw+P(pinLength+xBit+bodyWidth/2.,bodyHeight)),
                        sw+P(-pinBackDist+xBit,bodyHeight+pinEdgeDist),
                        C(sw+P(2.0*pinLength+xBit,bodyHeight/2.)),
                        sw+P(-pinBackDist+xBit,-pinEdgeDist),
                        ),
                Path(sw+P(-pinBackDist,bodyHeight+pinEdgeDist),
                        C(sw+P(2.0*pinLength,bodyHeight/2.)),
                        sw+P(-pinBackDist,-pinEdgeDist)
                        ),
                )
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist),
                sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Group(
		Circle(w=gateBody.e,r=0.1),
		Path(gateBody.e+P(0.2,0),gateBody.e+P(pinLength+0.2,0)),
		)

    if direction == 'e':
        angle = 0
    elif direction == 'n':
        angle = -90
    elif direction == 's':
        angle = 90
    elif direction == 'w':
        angle = 180
    else:
        print "Incorrect direction entered, 'e' used..."
        angle = 0

    if label is not None:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
	return obj.rotate(angle,p=obj.c)
    else:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)
	return obj.rotate(angle,p=obj.c)

# NOT gate
def NotGate(
        sw=P(0,0), 
        direction='e', 
        height=2.0,
        width=3.0,
        pinLength=0.5,
        label=None,
        labelPinIn1=None,
        labelPinIn2=None,
        labelPinOut=None,
        ):
    """
    Generates a NOT gate
    @param sw: the position of the sw reference point
    @param direction: the direction of the gate
    @param height: vertical extent of gate
    @param width: horizontal extent of gate (equivalent to length)
    @param pinLength: length of pins into and out of gate
    @param label: overall label
    @param labelPinIn1: label for input pin 1 (the top one for default
        direction)
    @param labelPinIn2: label for input pin 2 (th bottom one for default
        direction)
    @param labelPinOut: label for output pin
    @return: a Group() object of the gate
    """

    buff = 0
    pinEdgeDist = 0.1*height
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = Path(sw+P(pinLength,buff+0),
		sw+P(pinLength,buff+bodyHeight),
        	sw+P(pinLength+0.707106781*bodyWidth,buff+bodyHeight/2.),
		sw+P(pinLength,buff+0))
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist),
                sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Group(
        Circle(w=gateBody.e,r=rad),
        Path(gateBody.e+P(2.*rad,0),gateBody.e+P(2.*rad+pinLength,0))
	)

    if direction == 'e':
        angle = 0
    elif direction == 'n':
        angle = -90
    elif direction == 's':
        angle = 90
    elif direction == 'w':
        angle = 180
    else:
        print "Incorrect direction entered, 'e' used..."
        angle = 0

    if label is not None:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
	return obj.rotate(angle,p=obj.c)
    else:
        obj = Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)
	return obj.rotate(angle,p=obj.c)


# resistor
def Resistor(
	w=P(0,0),
	direction='ew',
	resLength=3.0,
	resWidth=1.0,
	pinLength=0.5,
	label=None,
	labelPinIn=None,
	labelPinOut=None,
	):
    """
    Generates a box resistor
    @param w: the position of the sw reference point
    @param direction: the direction of the resistor (ew is horizontal)
    @param resLength: length of resistor
    @param resWidth: width of resistor
    @param pinLength: length of pins into and out of resistor
    @param label: overall label
    @param labelPinIn: label for input pin
    @param labelPinOut: label for output pin
    @return: a Group() object
    """

    pinIn = Path(w,w+P(pinLength,0))
    resistor = Rectangle(w=pinIn.e,width=resLength,height=resWidth)
    pinOut = Path(resistor.e,resistor.e+P(pinLength,0))

    if direction == 'ew':
	angle = 0
    elif direction == 'ns':
	angle = 90
    else:
	angle = 0
	print "please enter either ew or ns, ew used in this case"

    if label is not None:
	obj = Group(pinIn, pinOut, resistor, label)
	return obj.rotate(angle,p=obj.c)
    else:
	obj = Group(pinIn, pinOut, resistor)
	return obj.rotate(angle,p=obj.c)

# capacitor
def Capacitor(
        w=P(0,0),
        direction='ew',
        capHeight=1.0,
        capSep=0.25,
        pinLength=0.5,
        label=None,
        labelPinIn=None,
        labelPinOut=None,
        ):
    """
    Generates a capacitor
    @param w: the position of the sw reference point
    @param direction: the direction of the capacitor (ew is horizontal)
    @param capHeight: height of capacitor
    @param capSep: separation of the plates of the capacitor
    @param pinLength: length of pins into and out of capacitor
    @param label: overall label
    @param labelPinIn: label for input pin
    @param labelPinOut: label for output pin
    @return: a Group() object
    """

    pinIn = Path(w,w+P(pinLength,0))
    cap = Group(
	Path(pinIn.e+P(0,-capHeight/2.0),pinIn.e+P(0,capHeight/2.0)),
	Path(pinIn.e+P(capSep,-capHeight/2.0),pinIn.e+P(capSep,capHeight/2.0)),
	)
    pinOut = Path(cap.e,cap.e+P(pinLength,0))

    if direction == 'ew':
	angle = 0
    elif direction == 'ns':
	angle = 90
    else:
	angle = 0
	print "please enter either ew or ns, ew used in this case"

    if label is not None:
        obj = Group(pinIn, pinOut, cap, label)
	return obj.rotate(angle,p=obj.c)
    else:
        obj = Group(pinIn, pinOut, cap)
	return obj.rotate(angle,p=obj.c)


