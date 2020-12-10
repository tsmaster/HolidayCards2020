import bdgmath as m
import math
import snowflake
import random
import drawSvg as draw
import drawutil
import clipvols

cardWidth = 1500
cardHeight = 1000

dwg = draw.Drawing(cardWidth, cardHeight)
dwg.setRenderSize('150mm', '100mm')

clips = []

def drawTri(dwg, v0, v1, v2, clips):
    polyLines = [[v0, v1, v2, v0]]
    for c in clips:
        polyLines = c.clipPolyLines(polyLines)

    drawutil.drawPolylines(dwg, polyLines)

    clips.append(clipvols.OutsideTri(v0, v1, v2))

drawTri(dwg,
        m.Vector2(600, 600),
        m.Vector2(800, 600),
        m.Vector2(700, 400),
        clips)

drawTri(dwg,
        m.Vector2(600, 500),
        m.Vector2(800, 500),
        m.Vector2(700, 300),
        clips)
        
drawTri(dwg,
        m.Vector2(500, 550),
        m.Vector2(700, 550),
        m.Vector2(600, 350),
        clips)
        
    

dwg.saveSvg("Output/tri_test.svg")
dwg.savePng("Output/tri_test.png")

