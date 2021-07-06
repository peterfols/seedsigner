# External Dependencies
from PIL import Image, ImageDraw, ImageFont
import spidev as SPI
from multiprocessing import Queue
from functools import partial
from seedsigner.helpers.screen import Screen, get_screen_dimensions, scale_dimension


### Generic View Class to Instatiate Display
### Static Class variables are used for display
### Designed to be inherited for other view classes, but not required
DEFAULT_COLOR = "ORANGE"

class View:
    WIDTH, HEIGHT = get_screen_dimensions()
    scale_dimension = partial(scale_dimension, HEIGHT)

    RST = 27
    DC = 25
    BL = 24

    controller = None
    buttons = None
    canvas_width = 0
    canvas_height = 0
    canvas = None
    draw = None
    bus = 0
    device = 0
    disp = None

    def __init__(self, controller) -> None:

        # Global Singleton
        View.controller = controller
        View.buttons = View.controller.buttons

        View.canvas_width = View.WIDTH
        View.canvas_height = View.HEIGHT
        View.canvas = Image.new('RGB', (View.canvas_width, View.canvas_height))
        View.draw = ImageDraw.Draw(View.canvas)

        # cls.WIDTHxcls.WIDTH display with hardware SPI:
        View.bus = 0
        View.device = 0
        View.disp = Screen(SPI.SpiDev(View.bus, View.device), View.RST, View.DC, View.BL)
        View.disp.Init()

        View.queue = Queue()

    @classmethod
    def DispShowImage(cls, image=None):
        if image == None:
            image = View.canvas
        View.disp.ShowImage(image, 0, 0)

    @classmethod
    def DispShowImageWithText(cls, image, text):
        image_copy = image.copy()
        draw = ImageDraw.Draw(image_copy)
        tw, th = draw.textsize(text, font=cls.get_font('couriernew', cls.scale_dimension(14)))
        draw.text(((cls.WIDTH - tw) / 2, cls.scale_dimension(228)), text, fill="GREY", font=cls.get_font('couriernew', cls.scale_dimension(14)))
        View.disp.ShowImage(image_copy, 0, 0)

    @classmethod
    def get_font(cls, name, size):
        if name == 'impact':
            return ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/Impact.ttf', size)
        elif name == 'couriernew':
            return ImageFont.truetype('/usr/share/fonts/truetype/msttcorefonts/courbd.ttf', size)

    @classmethod
    def draw_text(cls, text, height, font, font_size, align='center', fill=DEFAULT_COLOR, width=None):
        font_size = cls.scale_dimension(font_size)
        height = cls.scale_dimension(height)
        width = cls.scale_dimension(width) if width else None
        if not width and align == 'center':
            tw, th = View.draw.textsize(text, font=cls.get_font(font, font_size))
            width = (cls.WIDTH - tw) / 2
        elif not width and align == 'right':
            tw, th = cls.WIDTH - cls.get_font(font, font_size).getsize(text)[0]
            width = tw
        View.draw.text(width, height, text, fill=fill, font=cls.get_font(font, font_size))

    @classmethod
    def draw_polygon(cls, dimensions, outline=DEFAULT_COLOR, fill=DEFAULT_COLOR):
        View.draw.polygon([cls.scale_dimension(dim) for dim in dimensions], outline=outline, fill=fill)

    @classmethod
    def draw_rectangle(cls, dimensions, outline=DEFAULT_COLOR, fill=DEFAULT_COLOR, resize=True):
        if resize:
            dimensions = [cls.scale_dimension(dim) for dim in dimensions]
        return cls.draw.rectangle(dimensions, outline=outline, fill=fill)

    @classmethod
    def empty_screen(cls):
        return cls.empty_screen()

    @classmethod
    def draw_ellipse(cls, dimensions, outline=DEFAULT_COLOR, fill=DEFAULT_COLOR):
        dimensions = [cls.scale_dimension(dim) for dim in dimensions]
        return cls.draw.ellipse(dimensions, outline=outline, fill=fill)

    @classmethod
    def draw_modal(cls, lines=[], title="", bottom="") -> None:

        View.empty_screen()

        if len(title) > 0:
            cls.draw_text(title, 2, 'impact', 22)
        if len(lines) == 1:
            cls.draw_text(lines[0], 90, 'impact', 26)
        elif len(lines) == 2:
            cls.draw_text(lines[0], 90, 'impact', 22)
            cls.draw_text(lines[1], 125, 'impact', 22)
        elif len(lines) == 3:
            cls.draw_text(lines[0], 55, 'impact', 26)
            cls.draw_text(lines[1], 90, 'impact', 22)
            cls.draw_text(lines[2], 125, 'impact', 22)
        elif len(lines) == 4:
            cls.draw_text(lines[0], 55, 'impact', 22)
            cls.draw_text(lines[1], 90, 'impact', 22)
            cls.draw_text(lines[2], 125, 'impact', 22)
            cls.draw_text(lines[3], 160, 'impact', 22)

        if len(bottom) > 0:
            cls.draw_text(lines[3], 210, 'impact', 18)

        View.DispShowImage()

        return

    @classmethod
    def draw_prompt_yes_no(cls, lines=[], title="", bottom="") -> None:

        cls.draw_prompt_custom("", "Yes ", "No ", lines, title, bottom)
        return

    @classmethod
    def draw_prompt_custom(cls, a_txt, b_txt, c_txt, lines=[], title="", bottom="") -> None:

        View.empty_screen()

        if len(title) > 0:
            cls.draw_text(title, 2, 'impact', 22)

        if len(bottom) > 0:
            cls.draw_text(title, 210, 'impact', 18)

        if len(lines) == 1:
            cls.draw_text(lines[0], 90, 'impact', 26)
        elif len(lines) == 2:
            cls.draw_text(lines[0], 90, 'impact', 22)
            cls.draw_text(lines[1], 125, 'impact', 22)
        elif len(lines) == 3:
            cls.draw_text(lines[0], 20, 'impact', 26)
            cls.draw_text(lines[1], 90, 'impact', 22)
            cls.draw_text(lines[2], 125, 'impact', 22)
        elif len(lines) == 4:
            cls.draw_text(lines[0], 20, 'impact', 22)
            cls.draw_text(lines[1], 90, 'impact', 22)
            cls.draw_text(lines[2], 125, 'impact', 22)
            cls.draw_text(lines[3], 160, 'impact', 22)

        cls.draw_text(a_txt, 39, 'impact', 25)
        cls.draw_text(a_txt, 39+60, 'impact', 25)
        cls.draw_text(a_txt, 39+120, 'impact', 25)

        View.DispShowImage()

        return

    ###
    ### Power Off Screen
    ###

    @classmethod
    def display_power_off_screen(cls):

        View.empty_screen()

        cls.draw_text("Powering Down...", 45, 'impact', 22)
        cls.draw_text("Please wait about", 100, 'impact', 20)
        cls.draw_text("30 seconds before", 130, 'impact', 20)
        cls.draw_text("disconnecting power.", 160, 'impact', 20)
        View.DispShowImage()

    @classmethod
    def display_blank_screen(cls):
        View.empty_screen()
        View.DispShowImage()
