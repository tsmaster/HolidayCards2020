import math
import bdgmath as m
import drawutil
import drawSvg as draw

class Glyph:
    def __init__(self, c, strokes, advance):
        self.character = c
        self.strokes = strokes
        self.advance = advance


font3x5 = [
    Glyph('A',
          [(0, 0,
            0, 4,
            1, 5,
            2, 5,
            3, 4,
            3, 0),
           (0, 2,
            3, 2)],
          4),

    Glyph('B',
          [(0, 2,
            2, 2,
            3, 3,
            3, 4,
            2, 5,
            0, 5,
            0, 0,
            2, 0,
            3, 1,
            2, 2)],
          4),

    Glyph('C',
          [(3, 4,
            2, 5,
            1, 5,
            0, 4,
            0, 1,
            1, 0,
            2, 0,
            3, 1)],
          4),

    Glyph('D',
          [(0, 0,
            0, 5,
            2, 5,
            3, 4,
            3, 1,
            2, 0,
            0, 0)],
          4),

    Glyph('E',
          [(3, 5,
            0, 5,
            0, 0,
            3, 0),
           (2, 2,
            0, 2)],
          4),

    Glyph('F',
          [(3, 5,
            0, 5,
            0, 0),
           (2, 2,
            0, 2)],
          4),

    Glyph('G',
          [(3, 4,
            2, 5,
            1, 5,
            0, 4,
            0, 1,
            1, 0,
            2, 0,
            3, 1,
            3, 2,
            2, 2)],
          4),

    Glyph('H',
          [(0, 0,
            0, 5),
           (0, 2,
            3, 2),
           (3, 0,
            3, 5)],
          4),

    Glyph('I',
          [(0, 0,
            0, 5)],
          1),

    Glyph('J',
          [(3, 5,
            3, 1,
            2, 0,
            1, 0,
            0, 1)],
          4),

    Glyph('K',
          [(0, 5,
            0, 0),
           (3, 5,
            0, 2,
            1, 2,
            3, 0)],
          4),

    Glyph('L',
          [(0, 5,
            0, 0,
            3, 0)],
          4),

    Glyph('M',
          [(0, 0,
            0, 5,
            2, 3,
            4, 5,
            4, 0)],
          5),

    Glyph('N',
          [(0, 0,
            0, 5,
            3, 2),
           (3, 0,
            3, 5)],
          4),

    Glyph('O',
          [(1, 0,
            0, 1,
            0, 4,
            1, 5,
            2, 5,
            3, 4,
            3, 1,
            2, 0,
            1, 0),
          ],
          4),

    Glyph('P',
          [(0, 0,
            0, 5,
            2, 5,
            3, 4,
            3, 3,
            2, 2,
            0, 2)],
          4),

    Glyph('Q',
          [(1, 0,
            0, 1,
            0, 4,
            1, 5,
            2, 5,
            3, 4,
            3, 1,
            2, 0,
            1, 0),
           (2, 1,
            3, 0)],
          4),

    Glyph('R',
          [(0, 0,
            0, 5,
            2, 5,
            3, 4,
            3, 3,
            2, 2,
            0, 2),
           (2, 2,
            3, 1,
            3, 0)],
          4),

    Glyph('S',
          [(0, 1,
            1, 0,
            2, 0,
            3, 1,
            2, 2,
            1, 2,
            0, 3,
            0, 4,
            1, 5,
            2, 5,
            3, 4)],
          4),
    
    Glyph('T',
          [(0, 5,
            3, 5),
           (1.5, 5,
            1.5, 0)],
          4),

    Glyph('U',
          [(0, 5,
            0, 1,
            1, 0,
            2, 0,
            3, 1,
            3, 5)],
          4),

    Glyph('V',
          [(0, 5,
            0, 0,
            3, 3,
            3, 5)],
          4),

    Glyph('W',
          [(0, 5,
            0, 0,
            2, 2,
            4, 0,
            4, 5)],
          5),

    Glyph('X',
          [(0, 0,
            0, 1,
            3, 4,
            3, 5),
           (0, 5,
            0, 4,
            3, 1,
            3, 0)],
          4),

    Glyph('Y',
          [(0, 5,
            0, 3,
            1, 2,
            2, 2),
           (3, 5,
            3, 3,
            0, 0)],
          4),

    Glyph('Z',
          [(0, 5,
            3, 5,
            3, 4,
            0, 1,
            0, 0,
            3, 0)],
          4),

    Glyph(' ',
          [],
          2),

    Glyph(',',
          [(0, 0,
            -0.3, -0.3)],
          1),

    Glyph('.',
          [(-0.1, -0.1,
            -0.1, 0.1,
            0.1, 0.1,
            0.1, -0.1,
            -0.1, -0.1)],
          1),    

    Glyph('"',
          [(-0.1, 4.8,
            -0.1, 5.0),
           (0.1, 4.8),
           (0.1, 5.0)],
          1),
    
    Glyph("'",
          [(0, 4.8,
            0, 5.0)],
          1),

    Glyph('?',
          [(0, 3,
            0, 4,
            1, 5,
            2, 5,
            3, 4,
            3, 3,
            2, 2,
            1, 2,
            1, 1),
           (1, 0,
            2, 0)],
          4),

    Glyph('+',
          [(0, 2,
            2, 2),
           (1, 1,
            1, 3)],
          3),
    Glyph('-',
          [(0, 2,
            2, 2)],
          3),
    Glyph('*',
          [(0, 1,
            2, 3),
           (2, 1,
            0, 3),
           (1, 4,
            1, 0)],
          3),
    Glyph('=',
          [(0, 1,
            2, 1),
           (0, 3,
            2, 3)],
          3),
           

    Glyph('/',
          [(3, 5,
            0, 0)],
          4),

    

    Glyph('0',
          [(1, 0,
            0, 1,
            0, 4,
            1, 5,
            2, 5,
            3, 4,
            3, 1,
            2, 0,
            1, 0),
           (0, 1,
            3, 4)
          ],
          4),

    Glyph('1',
          [(0, 0,
            2, 0),
           (1, 0,
            1, 5,
            0, 4)],
          3),

    Glyph('2',
          [(0, 4,
            1, 5,
            2, 5,
            3, 4,
            3, 3,
            0, 0,
            3, 0)],
          4),

    Glyph('3',
          [(0, 5,
            3, 5,
            1, 3,
            2, 3,
            3, 2,
            3, 1,
            2, 0,
            1, 0,
            0, 1)],
          4),

    Glyph('4',
          [(3, 2,
            0, 2,
            3, 5,
            3, 0)],
          4),
    
    Glyph('5',
          [(3, 5,
            0, 5,
            0, 2,
            1, 3,
            2, 3,
            3, 2,
            3, 1,
            2, 0,
            1, 0,
            0, 1)],
          4),

    Glyph('6',
          [(3, 5,
            0, 2,
            0, 1,
            1, 0,
            2, 0,
            3, 1,
            3, 2,
            2, 3,
            1, 3)],
          4),

    Glyph('7',
          [(0, 5,
            3, 5,
            3, 4,
            1, 2,
            1, 0),
           (0, 2,
            2, 2)],
          4),

    Glyph('8',
          [(1, 5,
            2, 5,
            3, 4,
            3, 3,
            2, 2,
            1, 2,
            0, 3,
            0, 4,
            1, 5),
           (2, 2,
            3, 2,
            3, 1,
            2, 0,
            1, 0,
            0, 1,
            0, 2,
            1, 2)],
          4),

    Glyph('9',
          [(2, 2,
            1, 2,
            0, 3,
            0, 4,
            1, 5,
            2, 5,
            3, 4,
            3, 3,
            0, 0)],
          4),

    
    

    ]

fontDict3x5 = {}
for g in font3x5:
    fontDict3x5[g.character] = g

def drawString(dwg, s, glyphUnit, sx, sy):
    x = sx
    
    for c in s:
        g = fontDict3x5.get(c, None)
        if not g:
            g = fontDict3x5.get('?', None)
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
        

def drawHappyHolidays():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, 'HAPPY HOLIDAYS', 20, 50, 500)

    dwg.savePng("happyHolidays.png")
    dwg.saveSvg("happyHolidays.svg")

def drawHelloWorld():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, 'HELLO, WORLD', 20, 50, 500)

    dwg.savePng("helloWorld.png")
    dwg.saveSvg("helloWorld.svg")

def drawWelcome2021():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, 'WELCOME, 2021', 20, 50, 500)

    dwg.savePng("welcome2021.png")
    dwg.saveSvg("welcome2021.svg")

def drawTrebek():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, 'WATCH "JEOPARDY", ALEX TREBEK\'S FUN TV QUIZ GAME.', 8, 50, 500)

    dwg.savePng("trebek.png")
    dwg.saveSvg("trebek.svg")

def drawNumbers():
    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    drawString(dwg, '1234567890', 10, 50, 500)
    drawString(dwg, '12 + 34 - 56 * 78 / 90 =', 10, 50, 400)

    dwg.savePng("numbers.png")
    dwg.saveSvg("numbers.svg")
    


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
        drawString(dwg, pg, 8, 25, start - 100 * pi)

    dwg.savePng("pangrams.png")
    dwg.saveSvg("pangrams.svg")
    
    

if __name__ == '__main__':
    #drawHelloWorld()
    #drawHappyHolidays()
    #drawWelcome2021()
    #drawTrebek()
    #drawPangrams()
    drawNumbers()
    
    
    
          

    
          
                

