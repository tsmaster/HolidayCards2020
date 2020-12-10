# maybe not what a real spruce tree looks like.

import bdgmath as m
import math
import random

def drawSpruce(totalHeight, width, trunkHeight, trunkWidth, chunks = 3):
    """ returns a list of segments to draw"""

    segments = []
    
    # draw trunk

    trunkLeft = -trunkWidth / 2
    trunkRight = trunkWidth / 2
    trunkLines = max(6, int(trunkWidth / 10))

    trunkLinePosns = m.genSampleList(trunkLeft, trunkRight, trunkLines)
    
    for x in trunkLinePosns:
        base = m.Vector2(x, 0)
        top = m.Vector2(x, trunkHeight)
        # oops, this will be upside down.

        seg = (base, top) #m.LineSegment(base, top)
        segments.append(seg)

    # draw chunks
    needleMax = max(16, int(width / 20))
    
    chunkBases = m.genSampleList(trunkHeight, totalHeight, chunks + 1)
    chunkWidths = m.genSampleList(0, width, chunks + 1)
    chunkWidths.reverse()

    chunkLineCounts = m.genSampleList(needleMax / 2 , needleMax, chunks + 1)
    chunkLineCounts.reverse()
    chunkLineCounts = [int(x) for x in chunkLineCounts]
    
    for chunkIndex in range(0, chunks):
        thisChunkBase = chunkBases[chunkIndex]
        thisChunkTop = chunkBases[chunkIndex + 1]

        chunkLines = chunkLineCounts[chunkIndex]

        taper = 0.8
        chunkBaseWidth = chunkWidths[chunkIndex]
        chunkTopWidth = chunkWidths[chunkIndex + 1] * taper

        chunkLineFracs = m.genSampleList(0, 1, chunkLines)

        for f in chunkLineFracs:
            baseX = -chunkBaseWidth / 2 + f * chunkBaseWidth
            topX = -chunkTopWidth / 2 + f * chunkTopWidth
            base = m.Vector2(baseX, thisChunkBase)
            top = m.Vector2(topX, thisChunkTop)
            #seg = m.LineSegment(base, top)
            seg = (base, top)
            segments.append(seg)

    return segments


if __name__ == "__main__":
    import drawSvg as draw

    dwg = draw.Drawing(1500, 1000)
    dwg.setRenderSize('150mm', '100mm')

    for x in range(75, 1500, 150):
        for y in range(20, 1000, 150):
            print("xy",x,y)
            h = random.uniform(90, 100)
            w = random.uniform(70, 80)
            th = random.uniform(10, 15)
            numChunks = random.randrange(2, 5)
            
            spruceSegs = drawSpruce(h, w, th, 10, numChunks)

            mat = m.makeTranslationMat3(x, y)
    
            for seg in spruceSegs:
                verts = [mat.mulVec2(p) for p in seg.endpoints]
                dwg.append(draw.Lines(verts[0].x(), verts[0].y(),
                                      verts[1].x(), verts[1].y(),
                                      close = False,
                                      stroke = 'green'))

    dwg.saveSvg("spruce.svg")
    dwg.savePng("spruce.png")

    #print(m.genSampleList(0, 100, 10))


        
