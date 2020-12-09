

class ClipVolume:
    pass


class InsideRect(ClipVolume):
    """ accepts strokes INSIDE a rectangle """
    def __init__(self, left, top, right, bottom):
        pass



class OutsideRect(ClipVolume):
    """ accepts strokes OUTSIDE a rectangle """
    def __init__(self, left, top, right, bottom):
        pass

class OutsideTri(ClipVolume):
    def __init(self, v0, v1, v2):
        pass
    
