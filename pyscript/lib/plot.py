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
'''
pyscript plotting functions
'''

from pyscript import *
from Numeric import *

class Graph(Group):

    def __init__(self):

        # the bottom left hand corner of the graph is (0,0)
        self.xGraphMin = 0.0
        self.yGraphMin = 0.0

        # the top right hand corner of the graph is (10,10)
        self.xGraphMax = 10.0
        self.yGraphMax = 10.0

    def plot(self,
             xData,yData,
             xMinVal=None, xMaxVal=None,
             yMinVal=None, yMaxVal=None,
             xTickSep=None, yTickSep=None):

        # check inputs for correct type!!

        xGraphMin = self.xGraphMin
        yGraphMin = self.yGraphMin
        xGraphMax = self.xGraphMax
        yGraphMax = self.yGraphMax
        
        # the min and max parts of the curve
        xMin = min(xData)
        xMax = max(xData)
        yMin = min(yData)
        yMax = max(yData)

        # sort of automatic settings for min and max axis values
        # only really a stop-gap in case the relevant values are None
        # need to improve!!
        if xMinVal is None:
            xMinVal = xMin
        if xMaxVal is None:
            xMaxVal = xMax
        if yMinVal is None:
            yMinVal = yMin
        if yMaxVal is None:
            yMaxVal = yMax

        # sort of automatic settings for the tick separation values
        # in case the relevant values are None
        # need to improve!!
        if xTickSep is None:
            xTickSep = (xMaxVal - xMinVal)/11.0
        if yTickSep is None:
            yTickSep = (yMaxVal - yMinVal)/11.0
            
        # the x and y axes
        xAxis = Path(P(xGraphMin,yGraphMin),P(xGraphMax,yGraphMin))
        yAxis = Path(P(xGraphMin,yGraphMin),P(xGraphMin,yGraphMax))
        
        # length of the ticks
        xTickLen = 0.2 # in graph coordinates
        yTickLen = 0.2
        
        # min and max number of ticks for the x and y axes
        maxXTicks = 11
        minXTick = 5
        maxYTicks = 11
        minYTicks = 5

        # somehow I need to work out the number of ticks to use
        # and the values that are there.  In the interim, I'm going
        # to define xNumTicks and xTickSep manually, and maybe have
        # an automatic procedure for determining them if they aren't
        # specified in the calling script
        xNumTicks = round((xMaxVal - xMinVal)/xTickSep)
        
        if xTickSep is None:
            # try and split x data up into maxXTicks equal points and see if the numbers look "nice"
            xTickSep = (xMax - xMin)/xNumTicks

        xTicksVals = arrayrange(xMinVal,xMaxVal+xTickSep,xTickSep)
        xTicksPos = (xGraphMax/xNumTicks)*arrayrange(0,xNumTicks+1,1)
        # ### just for testing...
        #xTicksVals = [-10, -8, -6, -4, -2, 0, 2, 4, 6, 8, 10]
        #xTicksPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        xTicks = Group()
        for i in range(len(xTicksPos)):
            xTicks.append(Path(P(xGraphMin+xTicksPos[i],yGraphMin),
                               P(xGraphMin+xTicksPos[i],yGraphMin+xTickLen)))
        
        # try and split y data up into maxYTicks equal points and see if the numbers look "nice"
        yNumTicks = round((yMaxVal - yMinVal)/yTickSep)
        
        if yTickSep is None:
            # try and split x data up into maxXTicks equal points and see if the numbers look "nice"
            yTickSep = (yMax - yMin)/yNumTicks
        
        yTicksVals = arrayrange(yMinVal,yMaxVal+yTickSep,yTickSep)
        yTicksPos = (yGraphMax/yNumTicks)*arrayrange(0,yNumTicks+1,1)
        # ### just for testing...
        #yTicksVals = [-1, -0.8, -0.6, -0.4, -0.2, 0.0, 0.2, 0.4, 0.6, 0.8, 0.10]
        #yTicksPos = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        yTicks = Group()
        for i in range(len(yTicksPos)):
            yTicks.append(Path(P(xGraphMin,yGraphMin+yTicksPos[i]),
                               P(xGraphMin+yTickLen,xGraphMin+yTicksPos[i])))

        # ## now put the x values on the graph
        # I need to work out the bounding box for all of the text area
        # that the values take up
        xTicksValsText = Group()
        for i in range(len(xTicksVals)):
            xTicksValsText.append(TeX(s=P(xGraphMin+xTicksPos[i],yGraphMin-1.0),
                                      text=str(xTicksVals[i])))

        # now grab the height of the text, subtract 2*(some padding)
        # and translate the xTicksVals object down by that amount
        xTicksValsHeight = xTicksValsText.bbox().height
        xTicksValsPadding = 0.075
        # this seems like a waste of time, but at least it will work
        # I've made the text, found its bounding box and now
        # I can properly position the text
        xTicksValsText = Group()
        for i in range(len(xTicksVals)):
            xTicksValsText.append(TeX(s=P(xGraphMin+xTicksPos[i],yGraphMin-xTicksValsHeight-2.0*xTicksValsPadding),
                                      text=("%0.2f" % xTicksVals[i])))

        # ## now put the y values on the graph
        # I need to work out the bounding box for all of the text area
        # that the values take up
        yTicksValsText = Group()
        for i in range(len(yTicksVals)):
            yTicksValsText.append(TeX(e=P(xGraphMin-1.0,yGraphMin+yTicksPos[i]),
                                      text=("%0.2f" % yTicksVals[i])))

        # now grab the width of the text, subtract 2*(some padding)
        # and translate the yTicksVals object left by that amount
        yTicksValsWidth = yTicksValsText.bbox().width
        yTicksValsPadding = 0.1
        # this seems like a waste of time, but at least it will work
        # I've made the text, found its bounding box and now
        # I can properly position the text
        yTicksValsText = Group()
        for i in range(len(yTicksVals)):
            yTicksValsText.append(TeX(e=P(xGraphMin-2.0*yTicksValsPadding,yGraphMin+yTicksPos[i]),
                                      text=("%0.2f" % yTicksVals[i])))

        # ### believe it or not, now we put the curve on

        # the min and max parts of the curve
        xMin = min(xData)
        xMax = max(xData)
        yMin = min(yData)
        yMax = max(yData)

        print "\nYou will probably need extrema values of about"
        print "xMin = " + str(xMin) + ", xMax = " + str(xMax)
        print "yMin = " + str(yMin) + ", yMax = " + str(yMax)
        print ""

        # now scale the x and y values to these extremes
        xScale = xGraphMax/(xMaxVal - xMinVal)  # need to check if xMax - xMin is too small!!
        yScale = yGraphMax/(yMaxVal - yMinVal)
        xGraphData = xScale*(xData - xMinVal)
        yGraphData = yScale*(yData - yMinVal)
        
        linecolour = 'blue'
        curve = Group()
        # curve.fg = Color('blue')   # this doesn't work !! why???
        # curve.bg = Color('blue')
        for i in range(len(yGraphData)-1):
            # ## workaround for colour issue
            segment = Path(P(xGraphData[i],yGraphData[i]),
                           P(xGraphData[i+1],yGraphData[i+1]))
            if linecolour is not None:
                segment.fg = Color(linecolour)
                
            curve.append(segment)
            # ## end of workaround
            
            # original code
            #    curve.append(Path(P(xGraphData[i],yGraphData[i]),
            #                      P(xGraphData[i+1],yGraphData[i+1])))
            
            
            
        self.objects = Group(xAxis, yAxis, xTicks, yTicks, curve,
                        xTicksValsText, yTicksValsText)
        self.graphArea = self.objects
        self.axesArea = Group(xAxis, yAxis, xTicks, yTicks)
        return self.objects, self.graphArea, self.axesArea

    def xlabel(self,label):
    
        xGraphMin = self.xGraphMin
        yGraphMin = self.yGraphMin
        xGraphMax = self.xGraphMax
        yGraphMax = self.yGraphMax
        axesGraphDiff = self.graphArea.bbox().height - self.axesArea.bbox().height

        xLabelPadding = 0.075
        # ## now put an xlabel on it
        xLabelText = TeX(n=P((xGraphMax-xGraphMin)/2.0,yGraphMin-axesGraphDiff-xLabelPadding),
                         text=label)

        return self.objects.append(xLabelText)

    def ylabel(self,label,angle=-90):
        
        xGraphMin = self.xGraphMin
        yGraphMin = self.yGraphMin
        xGraphMax = self.xGraphMax
        yGraphMax = self.yGraphMax
        axesGraphDiff = self.graphArea.bbox().width - self.axesArea.bbox().width

        yLabelPadding = 0.075
        # ## now put an ylabel on it
        yLabelText = TeX(e=P(xGraphMin-axesGraphDiff-yLabelPadding,(yGraphMax-yGraphMin)/2.0),
                             text=label)
        yLabelText.rotate(angle)

        return self.objects.append(yLabelText)

    def title(self,label):

        xGraphMin = self.xGraphMin
        yGraphMin = self.yGraphMin
        xGraphMax = self.xGraphMax
        yGraphMax = self.yGraphMax
        graphNorth = self.graphArea.bbox().n

        titlePadding = 0.1
        # ## now put an title on it
        titleText = TeX(s=graphNorth + P(0.0,titlePadding),
                        text=label)
            
        return self.objects.append(titleText)

