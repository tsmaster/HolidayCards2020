import math
import random

class Matrix3:
    def __init__(self,
                 c00 = 1.0, c10 = 0.0, c20 = 0.0,
                 c01 = 0.0, c11 = 1.0, c21 = 0.0):
        self.components = ((c00, c10, c20),
                           (c01, c11, c21))

    def getComponent(self, col, row):
        return self.components[row][col]
                 
    def mulVec2(self, vec2):
        v0 = (vec2.x() * self.getComponent(0, 0) +
              vec2.y() * self.getComponent(1, 0) +
              self.getComponent(2,0))
        v1 = (vec2.x() * self.getComponent(0, 1) +
              vec2.y() * self.getComponent(1, 1) +
              self.getComponent(2,1))
        return Vector2(v0, v1)

    def mulMat3(self, mat3):
        lc = self.components
        rc = mat3.components

        c00 = lc[0][0] * rc[0][0] + lc[0][1] * rc[1][0]
        c10 = lc[0][0] * rc[0][1] + lc[0][1] * rc[1][1]
        c20 = lc[0][0] * rc[0][2] + lc[0][1] * rc[1][2] + lc[0][2]
        c01 = lc[1][0] * rc[0][0] + lc[1][1] * rc[1][0]
        c11 = lc[1][0] * rc[0][1] + lc[1][1] * rc[1][1]
        c21 = lc[1][0] * rc[0][2] + lc[1][1] * rc[1][2] + lc[1][2]
        
        return Matrix3(c00, c10, c20,
                       c01, c11, c21)

    def __str__(self):
        c = self.components
        s = """[%0.2f %0.2f %0.2f]
[%0.2f %0.2f %0.2f]""" % (c[0][0], c[0][1], c[0][2],
                          c[1][0], c[1][1], c[1][2])
        return s

def makeRotationMat3Radians(r):
    c = math.cos(r)
    s = math.sin(r)

    return Matrix3(c, s, 0,
                   -s, c, 0)

def makeTranslationMat3(x, y):
    return Matrix3(1, 0, x,
                   0, 1, y)

def makeScaleUniform(s):
    return Matrix3(s, 0, 0,
                   0, s, 0)

def makeScaleNonUniform(sx, sy):
    return Matrix3(sx, 0, 0,
                   0, sy, 0)

def makeTranslationRotationScaleUniform(x, y, r, s):
    translate = makeTranslationMat3(x,y)
    rot = makeRotationMat3Radians(r)
    scale = makeScaleUniform(s)
    return translate.mulMat3(rot.mulMat3(scale))

    
class Vector2:
    def __init__(self, x=0.0, y=0.0):
        self.components = (x,y)

    def mag(self):
        xc = self.x()
        yc = self.y()
        
        return math.sqrt(xc*xc+yc*yc)

    def magsqr(self):
        xc = self.x()
        yc = self.y()
        
        return xc*xc+yc*yc

    def x(self):
        return self.components[0]

    def y(self):
        return self.components[1]

    def mulScalar(self, s):
        return Vector2(self.components[0] * s,
                       self.components[1] * s)

    def addVec2(self, other):
        return Vector2(self.components[0] + other.components[0],
                       self.components[1] + other.components[1])

    def subVec2(self, other):
        return Vector2(self.components[0] - other.components[0],
                       self.components[1] - other.components[1])

    def cross2dVector2(self, other):
        return self.x()*other.y() - self.y()*other.x()
    

    def __str__(self):
        return "<%0.2f %0.2f>" % self.components

    def __repr__(self):
        return str(self)
        

class LineSegment:
    def __init__(self, v0, v1):
        self.endpoints = (v0, v1)

    def transform(self, mat3):
        tv0 = mat3.mulVec2(self.endpoints[0])
        tv1 = mat3.mulVec2(self.endpoints[1])

        return LineSegment(tv0, tv1)

    
def genSampleList(startVal, endVal, endCount, genCount = -1):
    if genCount < endCount:
        genCount = endCount * 10

    samples = [startVal, endVal]
    while len(samples) < genCount:
        samples.append(random.uniform(startVal, endVal))

    samples.sort()
    outSamples = []
    for i in range(endCount - 1):
        gI = int(i * genCount / endCount)
        outSamples.append(samples[gI])
    outSamples.append(samples[-1])

    return outSamples
    

def intersectSegments(s1v1, s1v2,
                      s2v1, s2v2):

    s1v1x = s1v1.x()
    s1v1y = s1v1.y()

    s1v2x = s1v2.x()
    s1v2y = s1v2.y()

    s2v1x = s2v1.x()
    s2v1y = s2v1.y()

    s2v2x = s2v2.x()
    s2v2y = s2v2.y()

    
    dx1 = s1v2x - s1v1x
    dy1 = s1v2y - s1v1y

    dx2 = s2v2x - s2v1x
    dy2 = s2v2y - s2v2y

    # from https://stackoverflow.com/questions/563198/how-do-you-detect-where-two-line-segments-intersect

    # we're looking for p + tr = q + us
    # where
    # p = s1v1
    # t in [0, 1]
    # r = s1v2 - s1v1
    # q = s2v1
    # u in [0,1]
    # s = s2v2 - s2v1

    p = s1v1
    r = s1v2.subVec2(p)
    q = s2v1
    s = s2v2.subVec2(q)

    qMinusP = q.subVec2(p)
    
    rCrossS = r.cross2dVector2(s)

    if rCrossS == 0:
        # case 1
        if qMinusP.cross2dVector2(r) == 0:
            # two lines are colinear
            return s1v1, True, 0, 0
        # case 2
        else:
            # parallel and non-intersecting
            return None, False, 0, 0
    else:
        rScaled = r.mulScalar(1.0 / rCrossS)
        u = qMinusP.cross2dVector2(rScaled)

        sScaled = s.mulScalar(1.0 / rCrossS)
        t = qMinusP.cross2dVector2(sScaled)

        if ((0.0 <= u) and (u < 1.0) and
            (0.0 <= t) and (t < 1.0)):
            return q.addVec2(s.mulScalar(u)), False, t, u
        else:
            return None, False, t, u
        
