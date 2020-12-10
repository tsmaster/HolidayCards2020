import drawSvg as draw
import random

def drawPolyline(dwg, vecList, strokeColor = 'black', strokeWidth = 2):
    p = draw.Path(stroke = strokeColor, fill='none', stroke_width = strokeWidth)
    if type(vecList[0]) == type((0, 1)):
        p.M(vecList[0][0], vecList[0][1])
    else:
        p.M(vecList[0].x(), vecList[0].y())

        
    for v in vecList[1:]:
        if v is None:
            continue
        if type(v) == type((0, 1)):
            p.L(v[0], v[1])
        else:
            p.L(v.x(), v.y())
            
    dwg.append(p)

def drawPolylines(dwg, polylineList, strokeColor = 'black', strokeWidth = 2):
    for pl in polylineList:
        drawPolyline(dwg, pl, strokeColor, strokeWidth)


def transformPolyLine(vecList, mat):
    return [mat.mulVec2(v) for v in vecList]

def transformPolyLines(polyLineList, mat):
    return [transformPolyLine(p, mat) for p in polyLineList]

def pickPointsInBox(x0, y0, x1, y1, n, r):
    points = []

    rSqr = r*r

    for i in range(n * 3):
        rx = random.randrange(x0, x1)
        ry = random.randrange(y0, y1)

        tooClose = False
        for p in points:
            px, py = p
            dx = px - rx
            dy = py - ry
            distSqr = dx * dx + dy * dy
            if distSqr < rSqr:
                tooClose = True
                break
        if tooClose:
            continue
        points.append((rx, ry))
        if len(points) == n:
            break
    return points

    
