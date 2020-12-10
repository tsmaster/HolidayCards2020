import math
import random
import bdgmath as m
import drawutil

# TODO be smarter about seeding?

class SnowflakeGenerator:
    def __init__(self, numSegments):
        self.numSegments = numSegments
        self.segments = []
        self.occCells = [(0, 0)]

    def generate(self):
        while len(self.segments) < self.numSegments:
            self.deposit()

    def deposit(self):
        while True:
            x = random.randrange(1, self.numSegments)
            y = random.randrange(0, x + 1)
            if (x, y) in self.occCells:
                continue
            break

        while True:
            d = random.randrange(0, 3)
            if d == 0:
                nx = x - 1
                ny = y
            elif d == 1:
                nx = x
                ny = y - 1
            else:
                nx = x - 1
                ny = y + 1

            if ny > nx:
                continue
            if ny < 0:
                continue

            npr = (nx, ny)
            if npr in self.occCells:
                self.occCells.append((x, y))
                self.segments.append((x, y, nx, ny))
                return
            else:
                x = nx
                y = ny

    def tryAddSegmentToPath(self, seg, p):
        sx0, sy0, sx1, sy1 = seg
        s0 = (sx0, sy0)
        s1 = (sx1, sy1)
        
        p0 = p[0]
        p1 = p[-1]

        if (s1 == p0):
            newPath = [s0] + p
            return True, newPath
        
        if (s0 == p1):
            newPath = p + [s1]
            return True, newPath

        # now flip segment
        if (s0 == p0):
            newPath = [s1] + p
            return True, newPath

        if (s1 == p1):
            newPath = p + [s0]
            return True, newPath

        # could not match
        return False, None
        

    def mergeUnitPaths(self):
        paths = []
        
        for s in self.segments:
            x0, y0, x1, y1 = s
            
            foundPath = False
            for pi, p in enumerate(paths):
                success, newPath = self.tryAddSegmentToPath(s, p)
                if success:
                    paths[pi] = newPath
                    foundPath = True
                    break
            if not foundPath:
                paths.append([(x0, y0), (x1, y1)])                
        return paths


    def generatePaths(self):
        paths = []
        vecX = m.Vector2(1,0)
        vecY = m.Vector2(0.5, math.cos(math.radians(60)))

        for path in self.mergeUnitPaths():
            verts = []
            flippedVerts = []
            for pt in path:
                xi, yi = pt
                v = vecX.mulScalar(xi).addVec2(vecY.mulScalar(yi))
                verts.append(v)
            paths.append(verts)
        oneArm = paths + drawutil.transformPolyLines(paths, m.makeScaleNonUniform(1, -1))

        allArms = []
        for i in range(6):
            rotMat = m.makeRotationMat3Radians(math.radians(60 * i))
            allArms += drawutil.transformPolyLines(oneArm, rotMat)
        return allArms

if __name__ == "__main__":
    sg = SnowflakeGenerator(10)
    sg.generate()
    for seg in sg.segments:
        print(seg)

    paths = sg.generatePaths()
    for p in paths:
        print(p)
