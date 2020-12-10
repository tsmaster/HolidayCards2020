import drawSvg as draw


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


def transformPolyLine(vecList, mat):
    return [mat.mulVec2(v) for v in vecList]

def transformPolyLines(polyLineList, mat):
    return [transformPolyLine(p) for p in polyLineList]

    
