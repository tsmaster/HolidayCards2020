import bdgmath as m
import math
import random
import drawSvg as draw
import drawutil
import clipvols

import text

leftmessage = "may 2020 close with peace and comfort, and may 2021 be a time of health and joy.".upper()

ipsumMessage = "Santa candle give hug chimney cedar gingerbread wreath. Celebrate boots wintertime, sugarplum December Vixen poinsettia merry carols snow eggnog Jack Frost. Gold bells Dasher spirit party holiday Cupid.".upper()

cardWidth = 1530
cardHeight = 980
    


def drawAddress(dwg, lines):
    for li, line in enumerate(lines):
        unit = 5

        targetHeight = 70
        targetWidth = 530
        
        sb = text.getStringBounds(line, unit)

        xScale = sb[0] / targetWidth
        yScale = sb[1] / targetHeight

        bigScale = max(xScale, yScale)

        unit /= bigScale
        
        print (line, sb, bigScale, unit)
        text.drawString(dwg, line, unit, 920, cardHeight - 460 - 80 * li)

def drawReturn(dwg):
    lines = ["Dave LeCompte",
             "12029 218th PL SE",
             "Snohomish WA 98296"]
    lines = [x.upper() for x in lines]

    top = 920
    left = 20
    stepDown = 60
    
    for li, line in enumerate(lines):
        text.drawString(dwg, line, 4, left, top - stepDown * li)

    drawutil.drawPolyline(dwg, [m.Vector2(0, 780),
                                m.Vector2(360, 780)])


def drawMessage(dwg, seed):
    top = 700
    left = 20
    right = 900
    bottom = 0

    unit = 8
    stepDown = 80

    msg = leftmessage
    
    lines = text.wordWrap(msg, unit, right-left)
    for li, line in enumerate(lines):
        print (li, line)
        text.drawString(dwg, line, unit, left, top - li * stepDown)

    if len(seed) > 8:
        seed = seed[:6]+"..."
    seedLine = "SEED: " + seed.upper()
    text.drawString(dwg, seedLine, 6, left, 20)

def makeCard(lines, fn, seed):
    outputDir = "Output/"

    dwg = draw.Drawing(cardWidth, cardHeight)
    dwg.setRenderSize("153mm", "98mm")

    drawAddress(dwg, lines)
    drawReturn(dwg)
    drawMessage(dwg, seed)
    
    dwg.saveSvg(outputDir + fn + ".svg")

    

                


if __name__ == "__main__":
    lines = ["Loopy user".upper(),
             "123 Fake Street".upper(),
             "Apt #1".upper(),
             "springfield, QA 01234".upper()]

    makeCard(lines, "test_back", "seed")
    
    
