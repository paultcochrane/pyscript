# pyscript plotting functions

from pyscript import *
from Numeric import *

class Plot(Area):

    """
    Plot object
    """

    def __init__(self,**dict):

        self.natives(
            {"bg":None,
             "fg":Color(0),
             "linewidth":defaults.linewidth,
             "dash":defaults.dash,
             "width":10,
             "height":10,
             "border":0.5,
             "offset":0.0,
             "xlabel":None,
             "ylabel":None,
             "title":None,
             }, dict)

        apply(Area.__init__,(self,),dict)

    def plot(self,x,y,xlabel="",ylabel="",title=""):
        """
        plot the thing
        """

        plotWidth = self['width']
        plotHeight = self['height']
        plotBorder = self['border']

        # check that x and y have the same lengths
        if len(x) != len(y):
            raise "Input vectors must be the same length"
            return
        
        # find range of data
        xMin = min(x)
        xMax = max(x)
        yMin = min(y)
        yMax = max(y)
        xRange = xMax - xMin
        yRange = yMax - yMin
        
        # do it dodgily to get it going
        # will need to add a bit so that the ranges are nice
        
        # shift all data so that minimum data point is at zero
        xPlotData = x-xMin
        yPlotData = y-yMin

        # scale xMax and xMin to fit between 0+border and width-border
        xScale = (plotWidth-2.0*plotBorder)/max(xPlotData)
        # scale yMax and yMin to fit between 0+border and height-border
        yScale = (plotHeight-2.0*plotBorder)/max(yPlotData)

        # now scale the plotData
        xPlotData = xPlotData*xScale
        yPlotData = yPlotData*yScale

        # the max and min of the axes needs to be just
        # a bit longer than these limits
        # also need to test to see if min and max limits are too
        # close to one another to plot, and so use a default range
        
        graph = Group()

        axes = self.defineAxes(xMin,xMax,yMin,yMax)
        data = self.dataPlot(xPlotData,yPlotData)

        graph.append(axes)
        graph.append(data)

        if xlabel is not "":
            xlabelText = self.xlabelMake(xlabel)
            graph.append(xlabelText)
        
        if ylabel is not "":
            ylabelText = self.ylabelMake(ylabel)
            graph.append(ylabelText)
        
        if title is not "":
            titleText = self.titleMake(title)
            graph.append(titleText)
        
        return graph

    def dataPlot(self,xPlotData,yPlotData):
        """
        plot the data
        """
        offset = self['offset']
        border = self['border']

        # dumb question:  how do we plot this stuff?
        # to get it going, I'm just going to do the whole thing as a path
        # and later add in different plot styles
        plottedData = Group()  # I really want this to be a path, and just add to it!!
        for i in range(len(xPlotData)-1):
            plottedData.append(Path(
                P(offset+border+xPlotData[i],offset+border+yPlotData[i]),
                P(offset+border+xPlotData[i+1],offset+border+yPlotData[i+1])))

        return plottedData

    def xlabelMake(self,xlabel):
        """
        adds a label to the x-axis
        """
        plotWidth = self['width']
        plotHeight = self['height']
        border = self['border']
        offset = self['offset']
        textHeight = 0.8
        horizCentre = (plotWidth - 2.0*border)/2.0  # want centred on x-axis

        # doing this stuff would be a lot easier with a 'packing' mechanism
        xlabelText = TeX(c=P(offset+border+horizCentre,offset-textHeight),text=xlabel)
        
        return xlabelText

    def ylabelMake(self,ylabel):
        """
        adds a label to the y-axis
        """
        plotWidth = self['width']
        plotHeight = self['height']
        border = self['border']
        offset = self['offset']
        textHeight = 0.2
        vertCentre = (plotHeight - 2.0*border)/2.0  # want centred on y-axis

        # doing this stuff would be a lot easier with a 'packing' mechanism
        ylabelText = TeX(c=P(offset-textHeight,offset+vertCentre),text=ylabel)
        ylabelText.rotate(-90)

        return ylabelText

    def titleMake(self,title):
        """
        adds a title to the graph
        """
        plotWidth = self['width']
        plotHeight = self['height']
        border = self['border']
        offset = self['offset']
        textHeight = 0.8
        horizCentre = plotWidth/2.0  # want centred on graph
        vertCentre = plotHeight

        # doing this stuff would be a lot easier with a 'packing' mechanism
        titleText = TeX(c=P(offset+horizCentre,offset+vertCentre),text=title)


        return titleText

    def defineAxes(self,xMin,xMax,yMin,yMax):
        """
        define the axes for the plot
        """

        width = self['width']
        height = self['height']
        border = self['border']
        offset = self['offset']

        majorTickLen = 0.2
        textHeight = 0.5
        textWidth = 0.8

        xNumMajorTicks = 10.0
        yNumMajorTicks = 10.0

        xAxisBare = Path(P(offset+border,offset+border),
                         P(width-border,offset+border))
        yAxisBare = Path(P(offset+border,offset+border),
                         P(offset+border,height-border))
        
        xMajorTickSep = (width-2.0*border)/(xNumMajorTicks-1)
        yMajorTickSep = (height-2.0*border)/(yNumMajorTicks-1)

        xTickValueSep = (xMax - xMin)/xNumMajorTicks
        yTickValueSep = (yMax - yMin)/yNumMajorTicks
        xTickValueSep = round(xTickValueSep*xNumMajorTicks)/xNumMajorTicks
        yTickValueSep = round(yTickValueSep*yNumMajorTicks)/yNumMajorTicks

        xTickValues = arrayrange(xMin,xMax+xTickValueSep,xTickValueSep)
        yTickValues = arrayrange(yMin,yMax+yTickValueSep,yTickValueSep)

        # put the ticks and values on the axis
        xMajorTicks = Group()
        yMajorTicks = Group()
        xTickText = Group()
        yTickText = Group()
        for i in range(0,xNumMajorTicks):
            xMajorTicks.append(
                Path(P(offset+border+i*xMajorTickSep,offset+border),
                     P(offset+border+i*xMajorTickSep,offset+border+majorTickLen)))
            xTickText.append(
                Text(c=P(offset+border+i*xMajorTickSep,offset+border-textHeight),
                     text="%.4g" % xTickValues[i]))
            yMajorTicks.append(
                Path(P(offset+border,offset+border+i*yMajorTickSep),
                     P(offset+border+majorTickLen,offset+border+i*yMajorTickSep)))
            yTickText.append(
                Text(c=P(offset+border-textWidth,offset+border+i*yMajorTickSep),
                     text="%.4g" % yTickValues[i]))


        return Group(xAxisBare,xMajorTicks,xTickText,yAxisBare,yMajorTicks,yTickText)
        
