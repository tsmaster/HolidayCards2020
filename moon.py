import math
import random
import bdgmath as m
import drawutil
import drawSvg as draw
import text
import clipvols


def genMoonPoints(phase = -1):
    if (phase < 0):
        numVerts = random.uniform(0, 8)

    steps = 10

    radius = 25

    leftUpPoints = []

    startAngle = 0
    endAngle = math.pi
    
    for s in range(steps):
        a = startAngle + (endAngle - startAngle) * (s / steps)
        leftUpPoints.append(m.Vector2(-radius * math.sin(a), radius * math.cos(a)))

    invertMat = m.makeScaleUniform(-1)
    
    rightDownPoints = drawutil.transformPolyLine(leftUpPoints, invertMat)

    if phase < 4:
        pn = (2 - phase) / 2

        rightDownPoints = drawutil.transformPolyLine(rightDownPoints, m.makeScaleNonUniform(pn, 1))
    else:
        pn = (phase - 6) / 2
        leftUpPoints = drawutil.transformPolyLine(leftUpPoints, m.makeScaleNonUniform(pn, 1))
    
    totalPoints = leftUpPoints + rightDownPoints
    totalPoints.append(totalPoints[0])

    return totalPoints
    

def testDrawMoon():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    xStep = 1500 / 6
    yStep = 1000 / 4
    xOffset = xStep / 2
    yOffset = yStep / 2
    
    for x in range(6):
        for y in range(4):
            phase = (y + x * 4) / 3
            print ("x y p", x, y, phase)
            pl = genMoonPoints(phase)

            # translate
            transMat = m.makeTranslationMat3(x* xStep + xOffset,
                                             y * yStep + yOffset)

            scaleMat = m.makeScaleUniform(3)

            mat = transMat.mulMat3(scaleMat)

            tPl = drawutil.transformPolyLine(pl, mat)
            
            drawutil.drawPolyline(dwg, tPl)

    dwg.savePng("moon.png")
    dwg.saveSvg("moon.svg")
    

    
if __name__ == "__main__":
    testDrawMoon()

