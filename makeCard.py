import bdgmath as m
import math
import snowflake
import random
import drawSvg as draw
import drawutil

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


def drawCenteredString(dwg, s, glyphUnit, x, y):
    tbx, tby = text.getStringBounds(s, glyphUnit)
    left = x - tbx / 2
    right = left + tbx
    bottom = y - tby / 2
    top = bottom + tby
    
    text.drawString(dwg, s, glyphUnit, left, bottom)


def drawTextLayer(dwg, cardWidth, cardHeight):
    halfCardWidth = cardWidth / 2
    halfCardHeight = cardHeight / 2
    
    drawCenteredString(dwg, 'HAPPY HOLIDAYS', 10, halfCardWidth, halfCardHeight)
    drawCenteredString(dwg, '2020', 12, halfCardWidth, halfCardHeight - 70)

def drawFlakeLayer(dwg, cardWidth, cardHeight):
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
        drawutil.drawPolylines(dwg, tpl)
    
def drawTreeLayer(dwg):
    pass
    
def drawMountainLayer(dwg):
    pass
    
def drawMoonLayer(dwg):
    pass
    
def drawStarLayer(dwg):
    pass
    

def makeCard(seed = None):
    if not (seed is None):
        random.seed(seed)

    cardWidth = 1500
    cardHeight = 1000

    dwg = draw.Drawing(cardWidth, cardHeight)
    dwg.setRenderSize('150mm', '100mm')

    drawTextLayer(dwg, cardWidth, cardHeight)
    drawFlakeLayer(dwg, cardWidth, cardHeight)
    drawTreeLayer(dwg)
    drawMountainLayer(dwg)
    drawMoonLayer(dwg)
    drawStarLayer(dwg)
    

    dwg.saveSvg("card.svg")
    dwg.savePng("card.png")


if __name__ == "__main__":
    makeCard()
