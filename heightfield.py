import math
import random
import bdgmath as m
import drawutil
import drawSvg as draw
import text
import clipvols



class HeightField:
    def clipPolyLines(self, polyLines):
        newPolyLines = []
        for p in polyLines:
            newPolyLines += self.clipPolyLine(p)
        return newPolyLines

    def clipPolyLine(self, polyLine):
        # for each segment, generate a list of intersections, which yields a set of disconnected segments.
        # check to connect the last clipped segment to its neighbor into an output polyline.
        
        #print("in clipPolyLine")
        polyLines = []
        currentLine = []
        lastVert = polyLine[0]
        lastAccepted = self.clipPoint(lastVert)

        #print("first lastAccepted:", lastAccepted)
        
        if lastAccepted:
            currentLine.append(lastVert)
            
        #print("starting currentLine:", currentLine)

        for vi in range(0, len(polyLine)-1):
            vi1 = vi + 1

            viVect = polyLine[vi]
            vi1Vect = polyLine[vi1]

            sAcc, eAcc, lines = self.clipSegment(viVect, vi1Vect)

            if len(lines) == 1:
                # trivial cases
                
                if sAcc and eAcc:
                    # just append this segment to the current line

                    # TODO remove this hack, should not have to test currentLine
                    if (currentLine):
                        currentLine.append(vi1Vect)
                    continue
                if sAcc:
                    # start in, finish out

                    # TODO remove this hack, should not have to test currentline
                    if currentLine:
                        currentLine.append(lines[0][1])
                        polyLines.append(currentLine)
                    currentLine = []
                    lastAccepted = False
                    continue
                if eAcc:
                    # start out, finish in
                    currentLine = lines[0]
                    lastAccepted = True
                    continue
                # else, out out
                assert((not sAcc) and (not eAcc))
                polyLines.append(lines[0])
                continue

            #print("lines:", lines)
            midSegs = lines[:]
            endSeg = None
            
            if sAcc:
                startSeg = midSegs[0]
                midSegs = midSegs[1:]

                # process start segment
                currentLine.append(startSeg[1])
                polyLines.append(currentLine)
                currentLine = []

            if eAcc:
                # TODO fix this hack
                if midSegs:
                    endSeg = midSegs[-1]
                    midSegs = midSegs[:-1]

            # process any mid segments
            for ms in midSegs:
                polyLines.append(ms)

            if eAcc:
                # start the end segment line
                currentLine = endSeg
                lastAccepted = True

        if currentLine:
            polyLines.append(currentLine)

        #print("returning from clipPolyLines", polyLines)
        return polyLines

    def clipPoint(self, v):
        # return True if the point is UNCLIPPED by the heightfield
        h = self.getHeight(v.x())
        #print("h:", h)
        return v.y() >= h

    def clipSegment(self, v1, v2):
        # return list of polylines (segments?) that are accepted

        #print("clipping segment", v1, v2)
        
        x1 = v1.x()
        y1 = v1.y()

        x2 = v2.x()
        y2 = v2.y()

        sdx = x2-x1
        sdy = y2-y1

        v1in = self.clipPoint(v1)

        #print ("v1in?", v1in)

        lines = []
        currentLine = []
        if v1in:
            currentLine.append(v1)

        #print ("starting currentLine:", currentLine)
        
        for hvIndex in range(0, len(self.vertices) - 1):
            hvIndex1 = hvIndex + 1
            hvVert = self.vertices[hvIndex]
            hvVert1 = self.vertices[hvIndex1]

            intersect, colinear, t, u = m.intersectSegments(v1, v2, hvVert, hvVert1)

            if not (intersect is None):
                #print("found intersect", intersect)
                if currentLine:
                    currentLine.append(intersect)
                    lines.append(currentLine)
                    currentLine = []
                else:
                    currentLine = [intersect]
        
        # ok, now we just need to deal with the end
        v2in = self.clipPoint(v2)

        #print ("v2in?", v2in)

        # but we have to tidy it up, just like other segments
        if v2in:
            # TODO fix this assertion
            #assert(currentLine)            
            if currentLine:
                currentLine.append(v2)
                lines.append(currentLine)
        else:
            assert (not currentLine)
            
        #print ("returning", v1in, v2in, lines)
        return v1in, v2in, lines
        
    def getHeight(self, x):
        if x < self.minX:
            v0 = self.vertices[0]
            return v0.y()
        if x > self.maxX:
            v1 = self.vertices[-1]
            return v1.y()
        for i in range(0, len(self.vertices) -1):
            vi = self.vertices[i]
            vi1 = self.vertices[i+1]
            if vi.x() <= x and x <= vi1.x():
                vix = vi.x()
                vi1x = vi1.x()
                spanWidth = vi1x - vix
                distIntoSpan = x - vix
                
                f = distIntoSpan / spanWidth
                viy = vi.y()
                vi1y = vi1.y()
                dy = vi1y - viy
                return dy * f + viy

    


class SinNoiseGenerator (HeightField):
    def __init__(self, name, minX, maxX, xSampleDist, yCenter, amplWaveLenPairList):
        self.minX = minX
        self.maxX = maxX
        self.xSampleDist = xSampleDist
        self.yCenter = yCenter
        self.amplWaveLenPairList = amplWaveLenPairList
        self.offsets = []
        self.vertices = []
        self.name = name

    def __repr__(self):
        return self.name
        
    def __str__(self):
        return self.name        

    def generate(self):
        for i in range(len(self.amplWaveLenPairList)):
            self.offsets.append(random.uniform(0, 2*math.pi))

        x = self.minX
        while x < self.maxX:
            y = self.getContinuousHeight(x)
            v = m.Vector2(x,y)
            self.vertices.append(v)
            x += self.xSampleDist
        y = self.getContinuousHeight(self.maxX)
        v = m.Vector2(self.maxX, y)
        self.vertices.append(v)

    def getContinuousHeight(self, x):
        h = self.yCenter
        for wi in range(len(self.amplWaveLenPairList)):
            amp, wl = self.amplWaveLenPairList[wi]
            offset = self.offsets[wi]
            s = amp * math.sin(2 * x * math.pi / wl + offset)
            h += s
        return h

    def getSegments(self):
        pass

    


class CircularCloudGenerator:
    pass

class MountainRange (HeightField):
    def __init__(self, name, minX, minY, maxX, maxY):
        self.minX = minX
        self.minY = minY
        self.maxX = maxX
        self.maxY = maxY
        self.vertices = []
        self.name = name

    def __repr__(self):
        return name

    def __str__(self):
        return name

    def generate(self):
        h = random.uniform(self.minY, self.maxY)
        x = self.minX
        goingUp = True
        v = m.Vector2(x, h)
        self.vertices.append(v)

        while True:
            if goingUp:
                newHeight = random.uniform(h, self.maxY)
            else:
                newHeight = random.uniform(self.minY, h)
            advance = abs(newHeight - h)

            newX = x + advance
            if newX >= self.maxX:
                actualAdvance = self.maxX - x
                frac = actualAdvance / advance
                finalHeight = (newHeight - h) * frac + h
                v = m.Vector2(self.maxX, finalHeight)
                self.vertices.append(v)
                break
            else:
                v = m.Vector2(newX, newHeight)
                self.vertices.append(v)
                x = x + advance
                h = newHeight
                goingUp = not goingUp

    def getSegments(self):
        pass

            
            
        
    


def drawHeightField(dwg, hf, strokeColor, clips):
    print ("drawing heightfield ", strokeColor)
    
    coords = []
    for v in hf.vertices:
        coords.append(v)

    polyLines = [coords]

    #print ("unclipped polylines:", polyLines)

    for c in clips:
        polyLines = c.clipPolyLines(polyLines)
        #print("after clipping", c, polyLines)

    for p in polyLines:
        drawutil.drawPolyline(dwg, p, strokeColor = strokeColor)


def mrtest_01():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []
    mr1 = MountainRange(0, 400, 1500, 600)
    mr1.vertices=[
        m.Vector2(0, 350),
        m.Vector2(750, 450),
        m.Vector2(1500, 350)]

    drawHeightField(dwg, mr1, 'green', clips)

    clips.append(mr1)
   
    mr2 = MountainRange(0, 450, 1500, 650)
    mr2.vertices = [
        m.Vector2(0, 400),
        m.Vector2(1500, 400)]

    drawHeightField(dwg, mr2, 'blue', clips)
    
    clips.append(mr2)

    dwg.savePng("m_test_01.png")

def mrtest_02():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []
    mr1 = MountainRange(0, 400, 1500, 600)
    mr1.vertices=[
        m.Vector2(0, 450),
        m.Vector2(750, 350),
        m.Vector2(1500, 450)]

    drawHeightField(dwg, mr1, 'green', clips)

    clips.append(mr1)
   
    mr2 = MountainRange(0, 450, 1500, 650)
    mr2.vertices = [
        m.Vector2(0, 400),
        m.Vector2(1500, 400)]

    drawHeightField(dwg, mr2, 'blue', clips)
    
    clips.append(mr2)

    dwg.savePng("m_test_02.png")

def mrtest_03():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []
    mr1 = MountainRange(0, 400, 1500, 600)
    mr1.vertices=[
        m.Vector2(0, 300),
        m.Vector2(500, 500),
        m.Vector2(1000, 300),
        m.Vector2(1500, 500)]

    drawHeightField(dwg, mr1, 'green', clips)

    clips.append(mr1)
   
    mr2 = MountainRange(0, 450, 1500, 650)
    mr2.vertices = [
        m.Vector2(0, 400),
        m.Vector2(1500, 400)]

    drawHeightField(dwg, mr2, 'blue', clips)
    
    clips.append(mr2)

    dwg.savePng("m_test_03.png")

def mrtest_04():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []
    mr1 = MountainRange(0, 400, 1500, 600)
    mr1.vertices=[
        m.Vector2(0, 500),
        m.Vector2(500, 300),
        m.Vector2(1000, 500),
        m.Vector2(1500, 300)]

    drawHeightField(dwg, mr1, 'green', clips)

    clips.append(mr1)
   
    mr2 = MountainRange(0, 450, 1500, 650)
    mr2.vertices = [
        m.Vector2(0, 400),
        m.Vector2(1500, 400)]

    drawHeightField(dwg, mr2, 'blue', clips)
    
    clips.append(mr2)

    dwg.savePng("m_test_04.png")

def mrtest_05():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []
    mr1 = MountainRange(0, 400, 1500, 600)
    mr1.vertices=[
        m.Vector2(0, 300),
        m.Vector2(300, 500),
        m.Vector2(700, 300),
        m.Vector2(1000, 500),
        m.Vector2(1500, 300)]

    drawHeightField(dwg, mr1, 'green', clips)

    clips.append(mr1)
   
    mr2 = MountainRange(0, 450, 1500, 650)
    mr2.vertices = [
        m.Vector2(0, 400),
        m.Vector2(1500, 400)]

    drawHeightField(dwg, mr2, 'blue', clips)
    
    clips.append(mr2)

    dwg.savePng("m_test_05.png")
    
def mrtest_06():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []
    mr1 = MountainRange(0, 400, 1500, 600)
    mr1.vertices=[
        m.Vector2(0, 300),
        m.Vector2(300, 500),
        m.Vector2(700, 300),
        m.Vector2(1000, 500),
        m.Vector2(1500, 300)]

    drawHeightField(dwg, mr1, 'green', clips)

    clips.append(mr1)
   
    mr2 = MountainRange(0, 450, 1500, 650)
    mr2.vertices = [
        m.Vector2(0, 400),
        m.Vector2(1500, 450)]

    drawHeightField(dwg, mr2, 'blue', clips)
    
    clips.append(mr2)

    dwg.savePng("m_test_06.png")

def mrtest_07():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []
    mr1 = MountainRange(0, 400, 1500, 410)
    mr1.vertices=[
        m.Vector2(0, 300),
        m.Vector2(1500, 300)]

    drawHeightField(dwg, mr1, 'green', clips)

    clips.append(mr1)
   
    mr2 = MountainRange(0, 450, 1500, 650)
    mr2.vertices = [
        m.Vector2(0, 400),
        m.Vector2(1500, 400)]

    drawHeightField(dwg, mr2, 'blue', clips)
    
    clips.append(mr2)

    dwg.savePng("m_test_07.png")

    

    
    
def mrtest_stress():
    random.seed("STRESS TEST")
    
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []

    step = 20
    span = 75
    start = 100
    
    for i in range(25):
        mr1 = MountainRange(0, step*i+start, 1500, step*i+start+span)
        mr1.generate()
        drawHeightField(dwg, mr1, 'black', clips)
        clips.append(mr1)
   
    dwg.savePng("m_test_s.png")


def sn_test_01():
    random.seed("STRESS TEST")
    
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []

    sn1 = SinNoiseGenerator(0, 1500, 20, 400,
                            [[150, 300]])
    sn1.generate()
    drawHeightField(dwg, sn1, 'blue', clips)
    clips.append(sn1)

    sn2 = SinNoiseGenerator(0, 1500, 20, 500,
                            [[150, 300]])
    sn2.generate()
    drawHeightField(dwg, sn2, 'blue', clips)
    clips.append(sn2)
    
    dwg.savePng("sn_test_01.png")



    

        
def testMountainRange():
    random.seed("TEST MOUNTAIN RANGE")
    
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    clips = []

    sn1 = SinNoiseGenerator(0, 1500, 20, 350, [(40, 400),
                                               (10, 117)])
    sn1.generate()

    drawHeightField(dwg, sn1, 'red', clips)

    clips.append(sn1)

    sn2 = SinNoiseGenerator(0, 1500, 20, 375, [(35, 300),
                                               (10, 93)])
    sn2.generate()

    drawHeightField(dwg, sn2, 'orange', clips)

    clips.append(sn2)

    sn3 = SinNoiseGenerator(0, 1500, 20, 400, [(30, 200),
                                               (10, 37)])
    sn3.generate()

    drawHeightField(dwg, sn3, 'yellow', clips)

    clips.append(sn3)

    mr1 = MountainRange(0, 400, 1500, 600)
    mr1.generate()
    """
    mr1.vertices=[
        m.Vector2(0, 350),
        m.Vector2(750, 450),
        m.Vector2(1500, 350)]
    """
    drawHeightField(dwg, mr1, 'green', clips)

    clips.append(mr1)
   
    mr2 = MountainRange(0, 450, 1500, 650)
    mr2.generate()
    """
    mr2.vertices = [
        m.Vector2(0, 400),
        m.Vector2(1500, 400)]
    """
    drawHeightField(dwg, mr2, 'blue', clips)
    
    clips.append(mr2)

    mr3 = MountainRange(0, 500, 1500, 700)
    mr3.generate()
 
    drawHeightField(dwg, mr3, 'purple', clips)


    dwg.saveSvg("mountains.svg")
    dwg.savePng("mountains.png")


def testMountainRangeAndText():
    random.seed("TEST MOUNTAIN RANGE AND TEXT")
    
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    cx = 750
    cy = 500

    clips = []

    #clips.append(clipvols.InsideRect(0, 1000, 1500, 0))

    title = "DEPECHE MODE"
    titleHeight = 575
    
    fontUnit = 8
    tbx, tby = text.getStringBounds(title, fontUnit)
    left = cx - tbx/2
    right = left + tbx
    bottom = titleHeight
    top = bottom + tby
    
    text.drawString(dwg, title, fontUnit, cx - tbx/2, bottom)

    clips.append(clipvols.OutsideRect(left - fontUnit, top + fontUnit,
                                      right + fontUnit, bottom - fontUnit))


    title = "BOYS DON'T CRY"
    titleHeight = 350
    
    fontUnit = 6
    tbx, tby = text.getStringBounds(title, fontUnit)
    left = cx - tbx/2
    right = left + tbx
    bottom = titleHeight
    top = bottom + tby
    
    text.drawString(dwg, title, fontUnit, cx - tbx/2, bottom)

    clips.append(clipvols.OutsideRect(left - fontUnit, top + fontUnit,
                                      right + fontUnit, bottom - fontUnit))

    
    

    sn1 = SinNoiseGenerator("sn1", 0, 1500, 20, 350, [(40, 400),
                                                      (10, 117)])
    sn1.generate()

    drawHeightField(dwg, sn1, 'red', clips)

    clips.append(sn1)

    
    sn2 = SinNoiseGenerator("sn2", 0, 1500, 20, 375, [(35, 300),
                                                      (10, 93)])
    sn2.generate()

    drawHeightField(dwg, sn2, 'orange', clips)

    clips.append(sn2)
    
    sn3 = SinNoiseGenerator("sn3 yellow", 0, 1500, 20, 400, [(30, 200),
                                                             (10, 37)])
    sn3.generate()

    drawHeightField(dwg, sn3, 'yellow', clips)

    clips.append(sn3)

    mr1 = MountainRange("mr1 green", 0, 400, 1500, 600)
    mr1.generate()
    drawHeightField(dwg, mr1, 'green', clips)
    clips.append(mr1)

    mr2 = MountainRange("mr2 blue", 0, 450, 1500, 650)
    mr2.generate()
    drawHeightField(dwg, mr2, 'blue', clips)
    clips.append(mr2)

    mr3 = MountainRange("mr3 purp", 0, 500, 1500, 700)
    mr3.generate()
    drawHeightField(dwg, mr3, 'purple', clips)

    dwg.saveSvg("text_mountains.svg")
    dwg.savePng("text_mountains.png")
    

if __name__ == "__main__":
    #testMountainRange()
    #mrtest_01()
    #mrtest_02()
    #mrtest_03()
    #mrtest_04()
    #mrtest_05()
    #mrtest_06()
    #mrtest_07()

    #mrtest_stress()

    #sn_test_01()
    testMountainRangeAndText()
