import bdgmath as m
import math
import snowflake
import random
import drawSvg as draw
import drawutil
import clipvols

import text
import snowflake

"""
The steps, using painter's algorithm, from front to back:

1) HAPPY HOLIDAYS 2020

2) Snowflakes

3) Trees

4) hills/mountains (heightfield)

5) moon

6) stars
"""



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
    cy = random.uniform(hTotY, cardHeight - hTotY)

    titleTop = cy + hTotY
    titleBottom = titleTop - tby
    titleLeft = cx - htbx
    titleRight = titleLeft + tbx

    yearTop = titleBottom - yspc
    yearBottom = yearTop - yby
    yearLeft = cx - ybx / 2
    yearRight = yearLeft + ybx
    
    text.drawString(dwg, title, titleSize, titleLeft, titleBottom)
    text.drawString(dwg, year, yearSize, yearLeft, yearBottom)

    clipMargin = 20
    clips.append(clipvols.OutsideRect(titleLeft - clipMargin,
                                      titleTop + clipMargin,
                                      titleRight - clipMargin,
                                      yearBottom - clipMargin))

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

        flakeScale = random.uniform(2,6)

        mat = m.makeTranslationRotationScaleUniform(fpv.x(), fpv.y(), angle, flakeScale)
        tpl = drawutil.transformPolyLines(spaths, mat)

        clippedPolylines = tpl
        for c in clips:
            clippedPolylines = c.clipPolyLines(clippedPolylines)
            
        drawutil.drawPolylines(dwg, clippedPolylines)
    
def drawTreeLayer(dwg, clips):
    pass
    
def drawMountainLayer(dwg, clips):
    pass
    
def drawMoonLayer(dwg, clips):
    pass
    
def drawStarLayer(dwg, clips):
    pass
    

def makeCard(seed = None):
    if not (seed is None):
        random.seed(seed)

    cardWidth = 1500
    cardHeight = 1000

    dwg = draw.Drawing(cardWidth, cardHeight)
    dwg.setRenderSize('150mm', '100mm')

    clips = []    
    drawTextLayer(dwg, cardWidth, cardHeight, clips)
    drawFlakeLayer(dwg, cardWidth, cardHeight, clips)
    drawTreeLayer(dwg, clips)
    drawMountainLayer(dwg, clips)
    drawMoonLayer(dwg, clips)
    drawStarLayer(dwg, clips)
    

    dwg.saveSvg("Output/card.svg")
    dwg.savePng("Output/card.png")


if __name__ == "__main__":
    makeCard("UNIT TEST")
