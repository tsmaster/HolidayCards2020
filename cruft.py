### stuff I don't need to make the cards


def drawSquareGrid(dwg, widthInMillimeters):
    hLineGroup = dwg.add(dwg.g(id='hlines', stroke='green'))
    y = 0
    while y < 100:
        hLineGroup.add(dwg.add(dwg.line(
            start = (0*mm, y*mm),
            end = (150*mm, y*mm))))
        y += widthInMillimeters

    vLineGroup = dwg.add(dwg.g(id='vlines', stroke='blue'))
    x = 0
    while x < 150:
        vLineGroup.add(dwg.add(dwg.line(
            start = (x*mm, 0*mm),
            end = (x*mm, 100*mm))))
        x += widthInMillimeters

def drawCenteredSquare(dwg, widthInMillimeters):
    sqgrp = dwg.add(dwg.g(id='sqgrp', stroke='red'))

    hw = widthInMillimeters / 2
    sqgrp.add(dwg.add(dwg.line(
        start = (-hw * mm, -hw * mm),
        end = (hw * mm, -hw * mm))))
    sqgrp.add(dwg.add(dwg.line(
        start = (-hw * mm, hw * mm),
        end = (hw * mm, hw * mm))))
    sqgrp.add(dwg.add(dwg.line(
        start = (-hw * mm, -hw * mm),
        end = (-hw * mm, hw * mm))))
    sqgrp.add(dwg.add(dwg.line(
        start = (hw * mm, -hw * mm),
        end = (hw * mm, hw * mm))))

def drawSegment(dwg, seg, strokeColor = 'black'):
    e0 = seg.endpoints[0]
    e1 = seg.endpoints[1]
    e0x = e0.x()
    e0y = e0.y()
    e1x = e1.x()
    e1y = e1.y()

    print ("drawing segment from (%f %f) to (%f %f)" % (e0x, e0y, e1x, e1y))
    
    #dwg.add(dwg.line(
    #    start = (e0x * mm, e0y * mm),
    #    end = (e1x * mm, e1y * mm),
    #    stroke = strokeColor
    #))
    dwg.append(draw.Lines(e0x, e0y,
                          e1x, e1y,
                          close = False,
                          stroke = strokeColor))


def drawPolyline(dwg, vecList, strokeColor = 'black'):
    p = draw.Path(stroke = strokeColor, fill='none')
    p.M(vecList[0][0], vecList[0][1])
    for v in vecList[1:]:
        p.L(v[0], v[1])
    dwg.append(p)

    
def testCenteredTri(dwg, w, mat):
    v0 = m.Vector2(w, 0)
    v1 = m.Vector2(w * math.cos(2*math.pi / 3.0), w * math.sin(2*math.pi / 3.0))
    v2 = m.Vector2(w * math.cos(2*math.pi / 3.0), -w * math.sin(2*math.pi / 3.0))

    tv0 = mat.mulVec2(v0)
    tv1 = mat.mulVec2(v1)
    tv2 = mat.mulVec2(v2)

    s0 = m.LineSegment(tv0, tv1)
    s1 = m.LineSegment(tv1, tv2)
    s2 = m.LineSegment(tv2, tv0)

    drawSegment(dwg, s0)
    drawSegment(dwg, s1)
    drawSegment(dwg, s2)


#dwg = svgwrite.Drawing('test.svg', size=(u'150mm', u'100mm'), profile='tiny')
dwg = draw.Drawing(1500, 1000)
dwg.setRenderSize('150mm', '100mm')

#link = dwg.add(dwg.a("http://link.to/internet"))
#square = dwg.add(dwg.rect((0, 0), (1, 1)))

#dwg.add(dwg.line((0, 0), (10, 0), stroke=svgwrite.rgb(10, 10, 16, '%')))
#dwg.add(dwg.text('Test', insert=(75, 100)))

print("drawing grid of width", 10)

#drawSquareGrid(dwg, 10)

#drawCenteredSquare(dwg, 25)
#testCenteredTri(dwg, 20, m.Matrix3())

xlate = m.makeTranslationMat3(60, 60)
print("trans mat", xlate)
#testCenteredTri(dwg, 20, xlate)

rot = m.makeRotationMat3Radians(math.radians(10))
xlateAndRot = xlate.mulMat3(rot)
#testCenteredTri(dwg, 20, xlateAndRot)

def drawFlake(dwg, sf, mat):
    paths = sf.generatePaths()
    
    for i in range(6):
        moreRotMat = m.makeRotationMat3Radians(math.radians(60) * i)

        rm = mat.mulMat3(moreRotMat)

        vecX = m.Vector2(1, 0)
        vecY = m.Vector2(0.5, math.cos(math.radians(60)))
        fVecY = m.Vector2(0.5, -math.cos(math.radians(60)))
        
        for path in paths:
            verts = []
            fverts = []
            for pt in path:
                xi, yi = pt
                p = vecX.mulScalar(xi).addVec2(vecY.mulScalar(yi))
                pTrans = rm.mulVec2(p)
                verts.append((pTrans.x(), pTrans.y()))

                p = vecX.mulScalar(xi).addVec2(fVecY.mulScalar(yi))
                pTrans = rm.mulVec2(p)
                fverts.append((pTrans.x(), pTrans.y()))

            drawPolyline(dwg, verts)
            drawPolyline(dwg, fverts)




points = pickPointsInBox(200, 200, 1300, 800, 10, 200)

for p in points:
    rx, ry = p
    ra = random.randrange(0, 60)
    
    xlate = m.makeTranslationMat3(rx, ry)

    rot = m.makeRotationMat3Radians(math.radians(ra))
    xlateAndRot = xlate.mulMat3(rot)

    scale = m.makeScaleUniform(10.0)
    xrs = xlateAndRot.mulMat3(scale)
    
    sf = snowflake.SnowflakeGenerator(random.randrange(10, 15))
    sf.generate()

    drawFlake(dwg, sf, xrs)

            
