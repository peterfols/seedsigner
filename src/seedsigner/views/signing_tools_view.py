# Internal file class dependencies
from . import View
from seedsigner.helpers import Buttons, B

# External Dependencies
import time


class SigningToolsView(View):

    def __init__(self, controller, seed_storage) -> None:
        View.__init__(self, controller)
        self.seed_storage = seed_storage

    ###
    ### XPub
    ###

    def display_xpub_qr(self, wallet):
        xpubstring = wallet.import_qr()
        
        print(xpubstring)

        xpub_images = wallet.make_xpub_qr_codes(xpubstring)

        cnt = 0
        step = False
        if len(xpub_images) == 1:
            View.DispShowImage(xpub_images[0])
        while True:
            if len(xpub_images) != 1:
                if step is False:
                    View.DispShowImage(xpub_images[cnt])
                else:
                    frame_text = (str(cnt+1) + " of " + str(len(xpub_images)))
                    View.DispShowImageWithText(xpub_images[cnt], frame_text)
                    time.sleep(0.3)
                    # View.DispShowImage(xpub_images[cnt])
            if step is False:
                cnt += 1
                if cnt >= len(xpub_images):
                    cnt = 0
                wallet.qr_sleep()
                if self.buttons.check_for_low(B.KEY_RIGHT):
                    return
                if self.buttons.check_for_low(B.KEY1):
                    step = True
            else:
                input = self.buttons.wait_for([B.KEY1, B.KEY_RIGHT, B.KEY_UP, B.KEY_DOWN])
                if input == B.KEY_RIGHT:
                    return
                elif input == B.KEY1 or input == B.KEY_DOWN:
                    cnt += 1
                    if cnt >= len(xpub_images):
                        cnt = 0
                elif input == B.KEY_UP:
                    cnt -= 1
                    if cnt < 0:
                        cnt = len(xpub_images) - 1

    ###
    ### Sign Transaction
    ###

    def display_signed_psbt_animated_qr(self, wallet, psbt) -> None:
        self.draw_modal(["Generating QR ..."])

        print(psbt)
        images = wallet.make_signing_qr_codes(psbt, SigningToolsView.qr_gen_status)

        cnt = 0
        step = False
        while True:
            if step is False:
                View.DispShowImage(images[cnt])
            else:
                frame_text = (str(cnt+1) + " of " + str(len(images)))
                View.DispShowImageWithText(images[cnt], frame_text)
                time.sleep(0.3)
            if step is False:
                cnt += 1
                if cnt >= len(images):
                    cnt = 0
                wallet.qr_sleep()
                if self.buttons.check_for_low(B.KEY_RIGHT):
                    return
                if self.buttons.check_for_low(B.KEY1):
                    step = True
            else:
                input = self.buttons.wait_for([B.KEY1, B.KEY_RIGHT, B.KEY_UP, B.KEY_DOWN])
                if input == B.KEY_RIGHT:
                    return
                elif input == B.KEY1 or input == B.KEY_DOWN:
                    cnt += 1
                    if cnt >= len(images):
                        cnt = 0
                elif input == B.KEY_UP:
                    cnt -= 1
                    if cnt < 0:
                        cnt = len(images) - 1


    def display_transaction_information(self, wallet) -> None:
        self.empty_screen()
        View.draw_text("Confirm last 13 chars", 5, 'impact', 22)
        View.draw_text("of the receiving address:", 30, 'impact', 22)
        View.draw_text(wallet.destinationaddress[-13:], 55, 'impact', 22)
        View.draw_text("Amount Sending:", 90, 'impact', 22)
        if wallet.spend == 0:
            View.draw_text("Self-Transfer (not parsed)", 115, 'impact', 22)
        else:
            View.draw_text(str(wallet.spend) + " satoshis", 115, 'impact', 22)
        View.draw_text("Plus a fee of:", 150, 'impact', 22)
        View.draw_text(str(int(wallet.fee)) + " satoshis", 175, 'impact', 22)
        View.draw_text("Left to Exit, Right to Continue", 175, 'impact', 18)
        View.DispShowImage()

    @classmethod
    def qr_gen_status(cls, percentage):
        View.empty_screen()
        View.draw_text("QR Generation", 90, 'impact', 25)
        View.draw_text(str(round(percentage)) + "% Complete", 125, 'impact', 25)
        View.DispShowImage()

