# External Dependencies
import threading
from threading import Timer

# Internal file class dependencies
from . import View
from seedsigner.helpers import B, CameraPoll


class IOTestView(View):

    def __init__(self, controller) -> None:
        View.__init__(self, controller)
        self.camera_loop_timer = None
        self.redraw = False
        self.redraw_complete = False
        self.qr_text = "Scan ANY QR Code"

    def display_io_test_screen(self):
        
        # display loading screen
        self.draw_modal(["Initializing I/O Test"])
        print("Initializing I/O Test")
        self.qr_text = "Scan ANY QR Code"

        # initialize camera
        self.controller.to_camera_queue.put(["start"])

        # First get blocking, this way it's clear when the camera is ready for the end user
        self.controller.from_camera_queue.get()

        self.camera_loop_timer = CameraPoll(0.05, self.get_camera_data) # it auto-starts, no need of rt.start()

        while True:

            self.draw_io_screen()

            input = self.buttons.wait_for([B.KEY_UP, B.KEY_DOWN, B.KEY_PRESS, B.KEY_RIGHT, B.KEY_LEFT, B.KEY1, B.KEY2, B.KEY3], False)
            if input == B.KEY_UP:
                ret_val = self.up_button()
            elif input == B.KEY_DOWN:
                ret_val = self.down_button()
            elif input == B.KEY_RIGHT:
                ret_val = self.right_button()
            elif input == B.KEY_LEFT:
                ret_val = self.left_button()
            elif input == B.KEY_PRESS:
                ret_val = self.press_button()
            elif input == B.KEY1:
                ret_val = self.a_button()
            elif input == B.KEY2:
                ret_val = self.b_button()
            elif input == B.KEY3:
                ret_val = self.c_button()
                return True

    def get_camera_data(self):
        try:
            data = self.controller.from_camera_queue.get(False)
            if data[0] != "nodata":
                self.draw_scan_detected()
        except:
            data = ["nodata"]

        if self.redraw is True and self.redraw_complete is True:
            self.draw_io_screen()

    def draw_io_screen(self):
        self.redraw_complete = False
        self.redraw = False
        self.empty_screen()
        self.draw_text("Input/Output Check:", 5, 18, width=45)
        self.draw_polygon([(61, 89), (80, 46), (99, 89)], fill=0)
        self.draw_polygon([(51, 100), (8, 119), (51, 138)], fill=0)
        self.draw_polygon([(109, 100), (152, 119), (109, 138)], fill=0)
        self.draw_polygon([(61, 151), (80, 193), (99, 151)], fill=0)
        self.draw_ellipse([(61, 99), (99, 141)], fill=0)
        self.draw_ellipse([(198, 40), (238, 80)],  fill=0)
        self.draw_ellipse([(198, 95), (238, 135)],  fill=0)
        self.draw_text("EXIT", 160, 18, width=200)
        self.draw_rectangle((30, 205, 210, 235),  fill="BLACK")
        self.draw_text(self.qr_text, 205, 22)
        View.DispShowImage()
        self.redraw_complete = True

    def a_button(self):
        if self.redraw is False and self.redraw_complete is True:
            self.draw_ellipse([(198, 40), (238, 80)])
            View.DispShowImage()
            self.redraw = True

    def b_button(self):
        if self.redraw is False and self.redraw_complete is True:
            self.draw_ellipse([(198, 95), (238, 135)])
            View.DispShowImage()
            self.redraw = True

    def c_button(self):
        self.camera_loop_timer.stop()
        self.controller.to_camera_queue.put(["stop"])

    def up_button(self):
        if self.redraw is False and self.redraw_complete is True:
            self.draw_polygon([(61, 89), (80, 46), (99, 89)])
            View.DispShowImage()
            self.redraw = True
        
    def down_button(self):
        if self.redraw is False and self.redraw_complete is True:
            self.draw_polygon([(61, 151), (80, 193), (99, 151)])
            View.DispShowImage()
            self.redraw = True
        
    def left_button(self):
        if self.redraw is False and self.redraw_complete is True:
            self.draw_polygon([(51, 100), (8, 119), (51, 138)])
            View.DispShowImage()
            self.redraw = True
        
    def right_button(self):
        if self.redraw is False and self.redraw_complete is True:
            self.draw_polygon([(109, 100), (152, 119), (109, 138)])
            View.DispShowImage()
            self.redraw = True
        
    def press_button(self):
        if self.redraw is False and self.redraw_complete is True:
            self.draw_ellipse([(61, 99), (99, 141)])
            View.DispShowImage()
            self.redraw = True
    
    def draw_scan_detected(self):
        self.qr_text = "QR Scanned"
        if self.redraw is False and self.redraw_complete is True:
            self.draw_rectangle((30, 205, 210, 235))
            self.draw_text(self.qr_text, 205, 22, fill='BLACK')
            View.DispShowImage()
            self.redraw = True
        