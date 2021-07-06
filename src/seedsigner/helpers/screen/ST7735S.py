from ST7789 import ST7789
from _ST7735S import ST7735 as RefClass
from _ST7735S import BG_SPI_CS_FRONT


class ST7735S(ST7789, RefClass):
    def __init__(self, spi, rst=27, dc=25, bl=24):
        RefClass.__init__(self, port=spi, cs=BG_SPI_CS_FRONT, dc=dc, backlight=bl, rst=rst, rotation=0)
        #ST7789.__init__(self, spi, rst, dc, bl)

    def command(self, cmd):
        RefClass.command(self, cmd)

    def Init(self):
        RefClass._init(self)

    def data(self, val):
        RefClass.data(self, val)

    def reset(self):
        RefClass.reset(self)

    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        RefClass.set_window(self, Xstart, Ystart, Xend, Yend)

    def ShowImage(self, Image, Xstart, Ystart):
        pass

    def clear(self):
        pass
