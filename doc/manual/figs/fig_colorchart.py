#from pyscript import *

#defaults.units=UNITS['cm']

# first grab all the colors in a list so we can sort them
# also find the longest name
cols=[]
max=0
max_name=""

for name,rgb in Color.COLORS.items():
    if len(name)>max:
        max=len(name)
        max_name=name
    cols.append((name,rgb))

from math import *

def hue(c):
    '''
    Calculate the hue (reasonably accurate)
    '''
    r,g,b=c[0]/255.,c[1]/255.,c[2]/255.

    C1=r-g/2.-b/2.
    C2=sqrt(3)/2.*(b-g)
    C=sqrt(C1**2+C2**2)
    
    if C==0:
        return -1

    if C2<=0:
        return acos(C1/C)
    else:
        return 2*pi-acos(C1/C)

def bri(c):
    '''
    Calculate the brightness/luminance (reasonably accurate)

    ...The luminance is the radiant intensity per unit projected area 
    weighted by the spectral sensitivity associated with the 
    brightness sensation of human vision...
    '''
    r,g,b=c[0]/255.,c[1]/255.,c[2]/255.
    return 0.2125*r+0.7154*g+0.0721*b


def bri_srt(c1,c2):
    '''
    Sort according to brightness
    '''
    b1=bri(c1[1])
    b2=bri(c2[1])

    if b1>b2: return -1
    elif b1<b2: return 1
    else: return 0


def hue_srt(c1,c2):
    '''
    Sort according to Hue
    '''
    h1=hue(c1[1])
    h2=hue(c2[1])

    if h1>h2: return -1
    elif h1<h2: return 1
    else: 
        # if they are the same sort by brightness
        return bri_srt(c1,c2)
    
cols.sort(hue_srt)

#for c in cols:
#    print hue(c)


# create the longest name and grab its size
t=Text(max_name)
width=t.width+.1
height=t.height+.2


#assume 140 cols: 140=35x4
H=35*height

print str(len(cols))

chart = Group()
ii=0
for xx in xrange(4):
    x=xx*width

    for yy in xrange(35):
        y=yy*height

        name,c=cols[ii]

        # switch the text color when its too dark
        if bri(c) < .4:
            tc=Color(1)
        else:
            tc=Color(0)
     
        chart.append(
            Rectangle(width=width,height=height,c=P(H-x,y),
                      fg=None,bg=Color(name)),
            Text(name,c=P(H-x,y),fg=tc)
            )

        ii+=1

render(chart,file="fig_colorchart.eps")
