import bdgmath as m
import math
import snowflake
import random
import drawSvg as draw
import drawutil
import clipvols

import text
import snowflake
import sprucetree
import heightfield
import moon
import stars

"""
The steps, using painter's algorithm, from front to back:

1) HAPPY HOLIDAYS 2020

2) Snowflakes

3) Trees

4) hills/mountains (heightfield)

5) moon

6) stars
"""


def drawFrameLayer(dwg, cardWidth, cardHeight):
    ll = m.Vector2(0, 1)
    ul = m.Vector2(0, cardHeight-1)
    ur = m.Vector2(cardWidth-1, cardHeight-1)
    lr = m.Vector2(cardWidth-1, 1)

    step = 50
    
    uStep = m.Vector2(0, step)
    dStep = m.Vector2(0, -step)
    rStep = m.Vector2(step, 0)
    lStep = m.Vector2(-step, 0)

    drawutil.drawPolyline(dwg, [ll.addVec2(rStep),
                                ll,
                                ll.addVec2(uStep)])

    drawutil.drawPolyline(dwg, [ul.addVec2(rStep),
                                ul,
                                ul.addVec2(dStep)])

    drawutil.drawPolyline(dwg, [lr.addVec2(lStep),
                                lr,
                                lr.addVec2(uStep)])
    
    drawutil.drawPolyline(dwg, [ur.addVec2(lStep),
                                ur,
                                ur.addVec2(dStep)])


    
def drawTextLayer(dwg, cardWidth, cardHeight, clips):
    
    halfCardWidth = cardWidth / 2
    halfCardHeight = cardHeight / 2

    title = 'HAPPY HOLIDAYS'
    titleSize = 10
    year = '2020'
    yearSize = 12

    tbx, tby = text.getStringBounds(title, titleSize)
    ybx, yby = text.getStringBounds(year, yearSize)
    yspc = 10

    htbx = tbx / 2
    totY = tby + yspc + yby
    hTotY = totY / 2

    cx = random.uniform(htbx, cardWidth - htbx)
    cy = random.uniform(hTotY, 2 * cardHeight / 3 - hTotY)

    titleTop = cy + hTotY
    titleBottom = titleTop - tby
    titleLeft = cx - htbx
    titleRight = titleLeft + tbx

    yearTop = titleBottom - yspc
    yearBottom = yearTop - yby
    yearLeft = cx - ybx / 2
    yearRight = yearLeft + ybx

    clipMargin = 20
    
    mLeft = titleLeft - clipMargin
    mTop = titleTop + clipMargin
    mRight = titleRight + clipMargin
    mBottom = yearBottom - clipMargin

    for i in range(2):
        drawutil.drawPolyline(dwg, [m.Vector2(mLeft, mBottom),
                                    m.Vector2(mLeft, mTop),
                                    m.Vector2(mRight, mTop),
                                    m.Vector2(mRight, mBottom),
                                    m.Vector2(mLeft, mBottom)])
    
    text.drawString(dwg, title, titleSize, titleLeft, titleBottom)
    text.drawString(dwg, year, yearSize, yearLeft, yearBottom)
    
    clips.append(clipvols.OutsideRect(mLeft,
                                      mTop,
                                      mRight,
                                      mBottom))

    

def drawFlakeLayer(dwg, cardWidth, cardHeight, clips):
    flakeMargin = 100
    flakePoints = drawutil.pickPointsInBox(flakeMargin, flakeMargin,
                                           cardWidth - flakeMargin, cardHeight - flakeMargin,
                                           12, 80)

    for fp in flakePoints:
        fpv = m.Vector2(*fp)
        sfg = snowflake.SnowflakeGenerator(random.randrange(9, 16))
        sfg.generate()
        spaths = sfg.generatePaths()

        #print("paths:",spaths)

        angle = random.uniform(0, 2*math.pi)

        flakeScale = random.uniform(4,8)

        mat = m.makeTranslationRotationScaleUniform(fpv.x(), fpv.y(), angle, flakeScale)
        tpl = drawutil.transformPolyLines(spaths, mat)

        clippedPolylines = tpl
        for c in clips:
            clippedPolylines = c.clipPolyLines(clippedPolylines)
            
        drawutil.drawPolylines(dwg, clippedPolylines)
    
def drawTreeLayer(dwg, cardWidth, cardHeight, clips):
    leftCount = random.randrange(2,5)
    rightCount = random.randrange(2,5)

    counts = [leftCount, rightCount]

    xRanges = [[0, cardWidth / 3],
               [2 * cardWidth / 3, cardWidth]]
    
    for areaIndex in range(len(counts)):
        count = counts[areaIndex]
        depths = m.genSampleList(100, 130, count)
        
        for treeIndex in range(count):
            left, right = xRanges[areaIndex]
            bottom = 0
            top = cardHeight / 4

            hPct = 100 / depths[treeIndex] 
            
            x = random.uniform(left, right)
            y = bottom + (top - bottom) * (1 - hPct)

    
            print ("treex, y", x,y)
    
            h = 800 * hPct
            w = 600 * hPct
            trunkHeight = 60
            trunkWidth = 50
            numChunks = random.randrange(20,50)
            mat = m.makeTranslationMat3(x,y)
            paths = drawutil.transformPolyLines(
                sprucetree.drawSpruce(h, w, trunkHeight, trunkWidth, numChunks),
                mat)

            paths = clipvols.clipPolyLinesAgainstClipList(paths, clips)
    
            drawutil.drawPolylines(dwg, paths, strokeColor = 'green')

            left = x - w/2
            top = y + h
            right = x + w/2
            bottom = y + trunkHeight
            
            v0 = m.Vector2(left, bottom)
            v1 = m.Vector2(x, top)
            v2 = m.Vector2(right, bottom)
            
            treeClipVol = clipvols.OutsideTri(v0, v1, v2)
            clips.append(treeClipVol)
                                            
    
def drawMountainLayer(dwg, cardWidth, cardHeight, clips):
    sn1 = heightfield.SinNoiseGenerator('r', 0, cardWidth, 20, 350, [(40, 400),
                                                                     (10, 117)])
    sn1.generate()
    heightfield.drawHeightField(dwg, sn1, 'red', clips)
    clips.append(sn1)

    sn2 = heightfield.SinNoiseGenerator('o', 0, cardWidth, 20, 375, [(35, 300),
                                                                     (10, 93)])
    sn2.generate()
    heightfield.drawHeightField(dwg, sn2, 'orange', clips)
    clips.append(sn2)

    sn3 = heightfield.SinNoiseGenerator('y', 0, cardWidth, 20, 400, [(30, 200),
                                                                     (10, 37)])
    sn3.generate()
    heightfield.drawHeightField(dwg, sn3, 'yellow', clips)
    clips.append(sn3)

    mr1 = heightfield.MountainRange('g', 0, 400, cardWidth, 600)
    mr1.generate()
    heightfield.drawHeightField(dwg, mr1, 'green', clips)
    clips.append(mr1)
   
    mr2 = heightfield.MountainRange('b', 0, 450, cardWidth, 650)
    mr2.generate()
    heightfield.drawHeightField(dwg, mr2, 'blue', clips)
    clips.append(mr2)

    mr3 = heightfield.MountainRange('p', 0, 500, cardWidth, 700)
    mr3.generate()
    heightfield.drawHeightField(dwg, mr3, 'purple', clips)
    clips.append(mr3)
    
    
def drawMoonLayer(dwg, cardWidth, cardHeight, clips):
    moonOrbitRadius = cardHeight - 200
    moonAngleMin = math.radians(60)
    moonAngleMax = math.radians(120)
    moonAngle = random.uniform(moonAngleMin, moonAngleMax)
    moonPhase = random.uniform(0, 8)
    moonPolyLines = [moon.genMoonPoints(moonPhase)]
    moonX = cardWidth / 2 + math.cos(moonAngle) * moonOrbitRadius
    moonY = math.sin(moonAngle) * moonOrbitRadius
    moonRadius = 3.5 * 25
    mat = m.makeTranslationRotationScaleUniform(moonX, moonY, 0, 3.5)
    moonPolyLines = drawutil.transformPolyLines(moonPolyLines, mat)

    moonPolyLines = clipvols.clipPolyLinesAgainstClipList(moonPolyLines, clips)

    drawutil.drawPolylines(dwg, moonPolyLines)

    clips.append(clipvols.OutsideCircle(m.Vector2(moonX, moonY), moonRadius))
    
def drawStarLayer(dwg, cardWidth, cardHeight, clips):
    numStars = random.randrange(40, 50)

    starLeft = 0
    starRight = cardWidth
    starBottom = cardHeight / 2
    starTop = cardHeight

    for n in range(numStars):
        x = random.uniform(starLeft, starRight)
        y = random.uniform(starBottom, starTop)

        angle = random.uniform(0, 2*math.pi)

        scale = 1

        mat = m.makeTranslationRotationScaleUniform(x, y, angle, scale)

        polylines = drawutil.transformPolyLines([stars.genStarPoints()], mat)

        polylines = clipvols.clipPolyLinesAgainstClipList(polylines, clips)

        drawutil.drawPolylines(dwg, polylines)
    

def makeCard(seed = None, name = None):
    if not (seed is None):
        random.seed(seed)

    if name is None:
        name = "card"

    outputDir = "Output/"

    cardWidth = 1330
    cardHeight = 980

    dwg = draw.Drawing(cardWidth, cardHeight)
    dwg.setRenderSize('133mm', '98mm')

    clips = []
    
    #drawFrameLayer(dwg, cardWidth, cardHeight)
    drawTextLayer(dwg, cardWidth, cardHeight, clips)
    drawFlakeLayer(dwg, cardWidth, cardHeight, clips)
    #drawTreeLayer(dwg, cardWidth, cardHeight, clips)
    drawMountainLayer(dwg, cardWidth, cardHeight, clips)
    drawMoonLayer(dwg, cardWidth, cardHeight, clips)
    drawStarLayer(dwg, cardWidth, cardHeight, clips)

    dwg.saveSvg(outputDir + name + ".svg")
    dwg.savePng(outputDir + name + ".png")

def makeFrame():
    outputDir = "Output/"

    cardWidth = 1330
    cardHeight = 980

    dwg = draw.Drawing(cardWidth, cardHeight)
    dwg.setRenderSize('133mm', '98mm')

    drawFrameLayer(dwg, cardWidth, cardHeight)
    dwg.saveSvg(outputDir + "frame" + ".svg")
    

def makeManyCards():    
    for i in range(20):
        name = "card_%04d" % i
        makeCard(name, name)
    

if __name__ == "__main__":
    #makeCard("UNIT TEST")
    makeFrame()
    #makeCard("DAVE'S OWN")
    makeCard("LAST DEC 10")

