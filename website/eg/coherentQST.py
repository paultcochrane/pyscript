from pyscript import *

defaults.units=UNITS['mm']
defaults.linewidth=1
dashedline="[2 3] 0"

black = Color("Black")
grey = Color("LightGray")
laserCol = Color("OrangeRed")

def ScaledText(text,**dict):
    t=TeX(text).scale(2,2)
    apply(t,(),dict)
    return t

def arrowhead(n,wid,len,angle,col):
    
    L = P(0,len)
    W = P(wid,0)
    
    arrow = Path(n,n-L+W,n-L-W,n,bg=col).rotate(angle,p=n)
    
    return arrow

def loop(c,radius):

    return Circle(r=radius,c=c)

def fibre(c):

    loops = Group(
        loop(c+P(0,1),10),
        loop(c,10),
        loop(c-P(0,1),10)
        )

    l = 10
    x1 = P(0,l)
    x2 = P(0,1.5*l)
    x3 = P(-l/2,2*l)
    x4 = P(-l,2.5*l)

    return Group(
        Path(loops.e,
             loops.e+x1,
             C(loops.e+x2),
             loops.e+x3
             #loops.e+x4
             ),
        Path(loops.w,
             loops.w-x1,
             C(loops.w-x2),
             loops.w-x3
             #loops.w-x4
             ),
        loops
        ).rotate(-45,p=c)

def fibrecoupler(c,angle):

    boxW = 15
    boxH = 12
    nozzle = 3
    box = Rectangle(c=c+P(boxW/6,0),width=boxW,height=boxH)
    fibrepos = c
    lenspos = box.e-P(box.width/3,0)
    irispos = box.e-P(box.width/12,0)
    irisInside = P(0,1)
    irisOutside = P(0,5)
    iris = Group(
        Path(irispos+irisInside,
             irispos+irisOutside
             ),
        Path(irispos-irisInside,
             irispos-irisOutside
             )
        )

    coupler = Group(
        
        box,
        Path(box.w,fibrepos),
        Path(fibrepos,
             fibrepos-P(0,nozzle/2),
             fibrepos-P(nozzle,0),
             fibrepos+P(0,nozzle/2),
             fibrepos,
             bg=black
             ),
        Circle(r=4,c=lenspos).scale(0.3,1),
        iris
        ).rotate(angle,p=c)

    return coupler

def fibrecollimator(c,angle):

    rectW = c
    
    collimator = Group(
        Path(c,
             c+P(0,1.5),
             c+P(-3,0),
             c+P(0,-1.5),
             c,
             bg=black
             ),
        Rectangle(w=rectW,width=2,height=8,bg=black)
        ).rotate(angle,p=c)

    return collimator

def hologram(c,angle):

    platesize = P(0,6)
    plate = Path(c-platesize,c+platesize,linewidth=3)

    stageStart = 1.25*platesize
    stageFinish = 2.25*platesize
    arrowL = 2
    arrowW = 1
    offset = arrowL/4

    hologram = Group(
        plate,
        Path(c+stageStart,c+stageFinish-P(0,offset)),
        Circle(r=0.75,c=c+stageStart,bg=black),
        arrowhead(c+stageFinish,arrowW,arrowL,0,black),
        ScaledText(r"$x$",c=c+stageFinish-P(4,0)),
        ScaledText(r"$y$",c=c+stageStart-P(4,0))
        )

    return hologram

def laser(w):

    box = Rectangle(w=w,width=20,height=8,bg=grey)
    lasername = ScaledText(r'Laser',c=box.c,fg=Color("DarkRed"));

    #I want to do a squiggle with an arrow (the light symbol)

    return Group(
        box,
        lasername,
        )

imageM1 = Epsf("figures/families/LGVI0-1.eps",width=8,c=P(180,10))
imageM1.rotate(67.5,p=imageM1.c).rotate(-45,p=P(150,10))

imageM2 = Epsf("figures/families/LGVI00.eps",width=8,c=P(180,10))
imageM2.rotate(45,p=imageM2.c).rotate(-22.5,p=P(150,10))

imageM3 = Epsf("figures/families/LGVI01.eps",width=8,c=P(180,10))
imageM3.rotate(22.5,p=imageM3.c)
imageM4 = Epsf("figures/families/LGVI02.eps",width=8,c=P(180,10))
imageM4.rotate(22.5,p=P(150,10))
imageM5 = Epsf("figures/families/LGVI03.eps",width=8,c=P(180,10))
imageM5.rotate(-22.5,p=imageM5.c).rotate(45,p=P(150,10))

coupler2 = fibrecoupler(P(200,10),180)

LGVI01=Epsf("figures/families/LGVI01.eps",width=8,c=P(130,10))
analyser = Group(
    
    Path(P(110,10),P(150,10),linewidth=2,dash=dashedline,fg=laserCol),
    arrowhead(P(140,10),1,3,90,laserCol),
    LGVI01.rotate(22.5,p=LGVI01.c),

    Path(P(150,10),P(180,10),linewidth=2,dash=dashedline,fg=laserCol).rotate(-45,p=P(150,10)),
    Path(P(150,10),P(200,10),linewidth=2,dash=dashedline,fg=laserCol).rotate(-22.5,p=P(150,10)),
    Path(P(150,10),P(180,10),linewidth=2,dash=dashedline,fg=laserCol),
    Path(P(150,10),P(180,10),linewidth=2,dash=dashedline,fg=laserCol).rotate(22.5,p=P(150,10)),
    Path(P(150,10),P(180,10),linewidth=2,dash=dashedline,fg=laserCol).rotate(45,p=P(150,10)),

    hologram(P(150,10),0),

    imageM1,
    imageM2,
    imageM3,
    imageM4,
    imageM5,

    coupler2.rotate(-22.5,p=P(150,10))

    )

coll1 = fibrecollimator(P(70,10),0)

fibre1 = fibre(P(40,30))
fibre1.move(coll1.w-fibre1.itoe(fibre1[1].path[-1]))

lasersource = Group(

    laser(P(100,60)),
    
    Path(P(100,60),P(60,60),linewidth=2,dash=dashedline,fg=laserCol),
    arrowhead(P(80,60),1,3,270,laserCol),

    fibrecoupler(P(60,60),0)

)

circle1 = Circle(r=7,start=180,end=360,s=fibre1.itoe(fibre1[0].path[-1]))
lasersource.move(circle1.n-lasersource[3].w)

analyser.rotate(-22.5,p=P(110,10))
point1 = analyser.itoe(analyser[14].w)

fibre2 = fibre(P(220,10))
fibre2.move(point1+P(10,5)-fibre2.itoe(fibre2[0].path[-1]))

detector = Group(
    Rectangle(c=P(240,10),width=10,height=10,bg=black),
    Circle(r=5,c=P(245,10),bg=black),
)
detector.move(fibre2.itoe(fibre2[1].path[-1])-detector[1].w)



render(

    circle1,
    lasersource,
    ScaledText(r'coupler 1',s=lasersource[3].n+P(-5,2)),

    fibre1,
    Rectangle(width=20,height=7,c=fibre1.c,bg=Color(1)),
    ScaledText(r'SMF',c=fibre1.c),

    # insert fibre between fibre loop and collimator

    coll1,
    # label collimator

    Path(coll1.e,P(110,10),linewidth=2,dash=dashedline,fg=laserCol),
    Epsf("figures/families/LGVI00.eps",width=8,c=P(85,10)),
    arrowhead(P(100,10),1,3,90,laserCol),

    Path(P(110,10),P(140,10),linewidth=2,dash=dashedline,fg=laserCol),
    Epsf("figures/families/LGVI00.eps",width=8,c=P(140,10)),
    arrowhead(P(130,10),1,3,90,laserCol),

    analyser,
    # label analyser hologram
    # label coupler2
    ScaledText(r'holo 2',s=P(140,43)),

    ScaledText(r'coupler 2',s=point1+P(-5,5)),

    Path(
    point1,
    C(point1+P(5,5)),
    point1+P(10,5),
    ),

    hologram(P(110,10),0),
    ScaledText(r'holo 1',s=P(110,30)),
    # label preparation hologram

    # insert fibre between coupler and fibre loop

    fibre2,
    Rectangle(width=20,height=7,c=fibre2.c,bg=Color(1)),
    ScaledText(r'SMF',c=fibre2.c),

    # insert fibre between coupler and detector

    detector,
    ScaledText(r'detector',e=detector.itoe(detector[0].e)+P(0,-10)),
    # label detector
    file="coherentQST.eps"

    )
