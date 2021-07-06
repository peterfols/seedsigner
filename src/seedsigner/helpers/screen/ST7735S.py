from ST7789 import ST7789
from _ST7735S import ST7735 as RefClass


class ST7735S(ST7789, RefClass):
    def __init__(self, spi, rst=27, dc=25, bl=24):
        RefClass.__init__(self, )
        ST7789.__init__(self, )

    def command(self):
        pass

    def Init(self):
        pass

    def data(self):
        pass

    def reset(self):
        RefClass.reset()

    def SetWindows(self):
        pass

    def ShowImage(self, Image, Xstart, Ystart):
        pass

    def clear(self):
        pass
