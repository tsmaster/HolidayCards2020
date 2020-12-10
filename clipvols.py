import bdgmath as m

class ClipVolume:
    def clipPolyLines(self, polyLines):
        newPolyLines = []
        for p in polyLines:
            newPolyLines += self.clipPolyLine(p)
        return newPolyLines
    
    def clipPolyLine(self, polyLine):
        # for each segment, generate a list of intersections, which yields a set of disconnected segments.
        # check to connect the last clipped segment to its neighbor into an output polyline.
        
        #print("in clipPolyLine")
        polyLines = []
        currentLine = []
        lastVert = polyLine[0]
        lastAccepted = self.clipPoint(lastVert)

        #print("first lastAccepted:", lastAccepted)
        
        if lastAccepted:
            currentLine.append(lastVert)
            
        #print("starting currentLine:", currentLine)

        for vi in range(0, len(polyLine)-1):
            vi1 = vi + 1

            viVect = polyLine[vi]
            vi1Vect = polyLine[vi1]

            sAcc, eAcc, lines = self.clipSegment(viVect, vi1Vect)

            if len(lines) == 1:
                # trivial cases
                
                if sAcc and eAcc:
                    # just append this segment to the current line
                    currentLine.append(vi1Vect)
                    continue
                if sAcc:
                    # start in, finish out
                    currentLine.append(lines[0][1])
                    polyLines.append(currentLine)
                    currentLine = []
                    lastAccepted = False
                    continue
                if eAcc:
                    # start out, finish in
                    currentLine = lines[0]
                    lastAccepted = True
                    continue
                # else, out out
                assert((not sAcc) and (not eAcc))
                polyLines.append(lines[0])
                continue

            #print("lines:", lines)
            midSegs = lines[:]
            endSeg = None
            
            if sAcc:
                startSeg = midSegs[0]
                midSegs = midSegs[1:]

                # process start segment
                currentLine.append(startSeg[1])
                polyLines.append(currentLine)
                currentLine = []

            if eAcc:
                endSeg = midSegs[-1]
                midSegs = midSegs[:-1]

            # process any mid segments
            for ms in midSegs:
                polyLines.append(ms)

            if eAcc:
                # start the end segment line
                currentLine = endSeg
                lastAccepted = True

        if currentLine:
            polyLines.append(currentLine)

        #print("returning from clipPolyLines", polyLines)
        return polyLines




class InsideRect(ClipVolume):
    """ accepts strokes INSIDE a rectangle """
    def __init__(self, left, top, right, bottom):
        pass



class OutsideRect(ClipVolume):
    """ accepts strokes OUTSIDE a rectangle """
    def __init__(self, left, top, right, bottom):
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def clipPoint(self, v):
        if (v.x() >= self.left and
            v.x() <= self.right and
            v.y() >= self.bottom and
            v.y() <= self.top):
            return False
        return True

    def clipSegment(self, v1, v2):
        # return list of polylines that are accepted

        sAcc = self.clipPoint(v1)
        eAcc = self.clipPoint(v2)
        if ((not sAcc) and (not eAcc)):
            return False, False, []
        
        intersections = []

        swCorner = m.Vector2(self.left, self.bottom)
        nwCorner = m.Vector2(self.left, self.top)
        neCorner = m.Vector2(self.right, self.top)
        seCorner = m.Vector2(self.right, self.bottom)

        sides = [(swCorner, nwCorner),
                 (nwCorner, neCorner),
                 (neCorner, seCorner),
                 (seCorner, swCorner)]

        for s in sides:
            c1, c2 = s
            i, isGood, t, u = m.intersectSegments(v1, v2, c1, c2)
            if not (i is None):
                #print("found intersection", t, i)
                intersections.append((t, i))

        if len(intersections) == 0:
            # trivial accept
            return sAcc, eAcc, [[v1, v2]]

        intersections.sort()

        if sAcc:
            preamble = [v1]
        else:
            preamble = []

        if eAcc:
            postamble = [v2]
        else:
            postamble = []
            

        points = preamble + [i[1] for i in intersections] + postamble

        assert((len(points) % 2) == 0)

        segs = []
        for ptIndex in range(0, len(points), 2):
            pt0 = points[ptIndex]
            pt1 = points[ptIndex+1]
            segs.append([pt0, pt1])
        return sAcc, eAcc, segs


class OutsideTri(ClipVolume):
    def __init__(self, v0, v1, v2):
        self.verts = [v0, v1, v2]

        self.sides = [(self.verts[0], self.verts[1]),
                      (self.verts[1], self.verts[2]),
                      (self.verts[2], self.verts[0])]

    def clipPoint(self, v):
        # check cross product to see if V is in front of any segment

        for s in self.sides:
            c0, c1 = s
            #print("testing against", c0, c1)
            sideVector = c1.subVec2(c0)
            #print("side vector", sideVector)
            q = v.subVec2(c0)
            #print("q vector", q)

            crossProduct = sideVector.cross2dVector2(q)
            #print("crossProduct", crossProduct)

            inFront = crossProduct > 0
            #print("in front?", inFront)
            if inFront:
                return True
        return False

    def clipSegment(self, v1, v2):
        # return list of polylines that are accepted

        sAcc = self.clipPoint(v1)
        eAcc = self.clipPoint(v2)
        if ((not sAcc) and (not eAcc)):
            return False, False, []
        
        intersections = []

        for s in self.sides:
            c1, c2 = s
            i, isGood, t, u = m.intersectSegments(v1, v2, c1, c2)
            if not (i is None):
                #print("found intersection", t, i)
                intersections.append((t, i))

        if len(intersections) == 0:
            # trivial accept
            return sAcc, eAcc, [[v1, v2]]

        intersections.sort()

        if sAcc:
            preamble = [v1]
        else:
            preamble = []

        if eAcc:
            postamble = [v2]
        else:
            postamble = []
            

        points = preamble + [i[1] for i in intersections] + postamble

        if ((len(points) % 2) != 0):
            print("ERROR")
            print(v1, v2)
            for s in self.sides:
                print (s)
            print ("intersections found:", intersections)
            print ("sAcc, eAcc", sAcc, eAcc)
        assert((len(points) % 2) == 0)

        segs = []
        for ptIndex in range(0, len(points), 2):
            pt0 = points[ptIndex]
            pt1 = points[ptIndex+1]
            segs.append([pt0, pt1])
        return sAcc, eAcc, segs
        
    


def clipPolyLinesAgainstClipList(polyLineList, clipVolumeList):
    outPolyLines = polyLineList

    for c in clipVolumeList:
        outPolyLines = c.clipPolyLines(outPolyLines)
        if not outPolyLines:
            return []
    return outPolyLines
            
