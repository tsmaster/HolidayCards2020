import math
import random
import bdgmath as m
import drawutil
import drawSvg as draw
import text
import clipvols


def genStarPoints(numVerts = -1):
    if (numVerts < 4):
        numVerts = random.randrange(4, 9)

    outerRadius = 10
    innerRadius = outerRadius / 3

    points = []
    fullAngle = 2 * math.pi / numVerts
    halfAngle = fullAngle / 2
    
    for i in range(numVerts):
        points.append(m.Vector2(outerRadius * math.cos(fullAngle * i),
                                outerRadius * math.sin(fullAngle * i)))
        points.append(m.Vector2(innerRadius * math.cos(fullAngle * i + halfAngle),
                                innerRadius * math.sin(fullAngle * i + halfAngle)))

    points.append(points[0])

    return points

def testDrawStars():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    xStep = 1500 / 6
    yStep = 1000 / 4
    xOffset = xStep / 2
    yOffset = yStep / 2
    
    for x in range(6):
        for y in range(4):
            c = (y + 4 * x) % 9 + 4
            pl = genStarPoints(c)

            # rotate
            rotMat = m.makeRotationMat3Radians(random.uniform(0, 2*math.pi))

            # translate
            transMat = m.makeTranslationMat3(x* xStep + xOffset,
                                             y * yStep + yOffset)

            scaleMat = m.makeScaleUniform(5)

            mat = transMat.mulMat3(rotMat.mulMat3(scaleMat))

            tPl = drawutil.transformPolyLine(pl, mat)
            
            drawutil.drawPolyline(dwg, tPl)

    dwg.savePng("stars.png")
    dwg.saveSvg("stars.svg")
    

    
if __name__ == "__main__":
    testDrawStars()

