# pyscript Electronics objects library
# thanks to Adrian Jonstone's lcircuit macros from CTAN for the ideas and names

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
    AND gate
    """
    
    # should it be direction or dir?
    buff = 0
    pinEdgeDist = 0.1*height
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    gateBody = Group(Path(sw+P(pinLength,buff+0), sw+P(pinLength,buff+bodyHeight), sw+P(pinLength+bodyWidth/2.,buff+bodyHeight)),
                     Circle(c=sw+P(pinLength+bodyWidth/2.,buff+bodyHeight/2.), r=bodyHeight/2., start=0, end=180),
                     Path(sw+P(pinLength+bodyWidth/2.,buff+0), sw+P(pinLength,buff+0)))
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist), sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Path(sw+P(bodyWidth+pinLength,bodyHeight/2.), sw+P(bodyWidth+2.*pinLength,bodyHeight/2.))

    if label is not None:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
    else:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)

# NAND gate
def NandGate(sw=P(0,0), direction='e', height=2.0, width=3.0, pinLength=0.5, label=None, labelPinIn1=None, labelPinIn1=None, labelPinOut=None):
    """
    NAND gate
    """
    
    # should it be direction or dir?
    buff = 0
    pinEdgeDist = 0.1*height
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = Group(Path(sw+P(pinLength,buff+0), sw+P(pinLength,buff+bodyHeight), sw+P(pinLength+bodyWidth/2.,buff+bodyHeight)),
                     Circle(c=sw+P(pinLength+bodyWidth/2.,buff+bodyHeight/2.), r=bodyHeight/2., start=0, end=180),
                     Path(sw+P(pinLength+bodyWidth/2.,buff+0), sw+P(pinLength,buff+0)))
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist), sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Group(
        Circle(c=P(bodyWidth+pinLength+rad,bodyHeight/2.),r=rad),
        Path(sw+P(bodyWidth+pinLength+2.*rad,bodyHeight/2.), sw+P(bodyWidth+2.*rad+2.*pinLength,bodyHeight/2.)))

    if label is not None:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
    else:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)

# OR gate
def OrGate(sw=P(0,0), direction='e', height=2.0, width=3.0, pinLength=0.5, label=None, labelPinIn1=None, labelPinIn1=None, labelPinOut=None):
    """
    OR gate
    """
    # should it be direction or dir?
    buff = 0
    pinEdgeDist = 0.1*height
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = 1
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist), sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Path(sw+P(bodyWidth+pinLength+2.*rad,bodyHeight/2.), sw+P(bodyWidth+2.*rad+2.*pinLength,bodyHeight/2.))

    if label is not None:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
    else:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)

# NOR gate
def NorGate(sw=P(0,0), direction='e', height=2.0, width=3.0, pinLength=0.5, label=None, labelPinIn1=None, labelPinIn1=None, labelPinOut=None):
    """
    NOR gate
    """
    # should it be direction or dir?
    buff = 0
    pinEdgeDist = 0.1*height
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = 1
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist), sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Path(sw+P(bodyWidth+pinLength+2.*rad,bodyHeight/2.), sw+P(bodyWidth+2.*rad+2.*pinLength,bodyHeight/2.))

    if label is not None:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
    else:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)

# XOR gate
def XorGate(sw=P(0,0), direction='e', height=2.0, width=3.0, pinLength=0.5, label=None, labelPinIn1=None, labelPinIn1=None, labelPinOut=None):
    """
    XOR gate
    """
    # should it be direction or dir?
    buff = 0
    pinEdgeDist = 0.1*height
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = 1
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist), sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Path(sw+P(bodyWidth+pinLength+2.*rad,bodyHeight/2.), sw+P(bodyWidth+2.*rad+2.*pinLength,bodyHeight/2.))

    if label is not None:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
    else:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)

# NXOR gate
def NxorGate(sw=P(0,0), direction='e', height=2.0, width=3.0, pinLength=0.5, label=None, labelPinIn1=None, labelPinIn1=None, labelPinOut=None):
    """
    NXOR gate
    """
    # should it be direction or dir?
    buff = 0
    pinEdgeDist = 0.1*height
    bodyHeight = height
    bodyWidth = width - 2.0*pinLength
    rad = 0.1
    gateBody = 1
    gatePinIn1 = Path(sw+P(0,bodyHeight-pinEdgeDist), sw+P(pinLength,bodyHeight-pinEdgeDist))
    gatePinIn2 = Path(sw+P(0,pinEdgeDist), sw+P(pinLength,pinEdgeDist))
    gatePinOut = Path(sw+P(bodyWidth+pinLength+2.*rad,bodyHeight/2.), sw+P(bodyWidth+2.*rad+2.*pinLength,bodyHeight/2.))

    if label is not None:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut, label)
    else:
        return Group(gateBody, gatePinIn1, gatePinIn2, gatePinOut)







