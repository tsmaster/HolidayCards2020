import math
import bdgmath as m
import drawutil
import drawSvg as draw

import font4x6

f4 = font4x6.fontDict4x6

def drawString(dwg, s, glyphUnit, sx, sy):
    x = sx
    
    for c in s:
        g = f4.get(c, None)
        if not g:
            g = f4.get('?', None)
        assert(not (g is None))

        isX = True
        for line in g.strokes:
            pts = []
            for coordIndex in range(0, len(line), 2):
                xCoord = line[coordIndex] * glyphUnit + x
                yCoord = line[coordIndex + 1] * glyphUnit + sy
                pts.append(m.Vector2(xCoord, yCoord))
            drawutil.drawPolyline(dwg, pts)

        x += glyphUnit * g.advance

def drawCenteredString(dwg, s, glyphUnit, x, y):
    tbx, tby = getStringBounds(s, glyphUnit)
    left = x - tbx / 2
    right = left + tbx
    bottom = y - tby / 2
    top = bottom + tby
    
    drawString(dwg, s, glyphUnit, left, bottom)

def getStringBounds(s, glyphUnit):
    h = f4.get('height') * glyphUnit
    w = 0
    for c in s:
        glyph = f4[c]
        w += glyph.advance * glyphUnit
    return (w,h)

def drawHappyHolidays():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, 'HAPPY HOLIDAYS', 20, 50, 500)

    dwg.savePng("Output/happyHolidays.png")
    dwg.saveSvg("Output/happyHolidays.svg")

def drawHelloWorld():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, 'HELLO, WORLD', 20, 50, 500)

    dwg.savePng("Output/helloWorld.png")
    dwg.saveSvg("Output/helloWorld.svg")

def drawWelcome2021():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, 'WELCOME, 2021', 20, 50, 500)

    dwg.savePng("Output/welcome2021.png")
    dwg.saveSvg("Output/welcome2021.svg")

def drawTrebek():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, 'WATCH "JEOPARDY", ALEX TREBEK\'S FUN TV QUIZ GAME.', 8, 50, 500)

    dwg.savePng("Output/trebek.png")
    dwg.saveSvg("Output/trebek.svg")

def drawNumbers():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, '1234567890', 10, 50, 500)
    drawString(dwg, '12 + 34 - 56 * 78 / 90 =', 10, 50, 400)
    drawString(dwg, '#NUMBERS', 10, 50, 300)

    dwg.savePng("Output/numbers.png")
    dwg.saveSvg("Output/numbers.svg")
    


def drawPangrams():
    pangrams = ['WATCH "JEOPARDY", ALEX TREBEK\'S FUN TV QUIZ GAME.',
                'A QUICK BROWN FOX JUMPS OVER THE LAZY DOG',
                'PACK MY BOX WITH FIVE DOZEN LIQUOR JUGS',
                'SPHINX OF BLACK QUARTZ, JUDGE MY VOW',
                'THE FIVE DOZEN BOXING WIZARDS JUMP QUICKLY',
                'SQUIDGY FEZ, BLANK JIMP CRWTH VOX',
                'LISA BONET ATE NO BASIL',
                'ABLE SIR DID IDRIS ELBA',
    ]
                
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    start = 800
    stepSize = 100
    for pi, pg in enumerate(pangrams):
        drawString(dwg, pg, 7, 25, start - stepSize * pi)

    dwg.savePng("Output/pangrams.png")
    dwg.saveSvg("Output/pangrams.svg")
    
    

if __name__ == '__main__':
    #drawHelloWorld()
    #drawHappyHolidays()
    #drawWelcome2021()
    #drawTrebek()
    drawPangrams()
    drawNumbers()
    
    
    
          

    
          
                

