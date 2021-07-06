# SeedSigner file class dependencies
from . import View
from seedsigner.helpers import B, QR


class SettingsToolsView(View):

    def __init__(self, controller) -> None:
        View.__init__(self, controller)

        self.qr = QR()
        self.donate_image = None

    ### Donate Menu Item

    def display_donate_info_screen(self):
        self.draw_modal(["You can support", "SeedSigner by donating", "any amount of BTC", "Thank You!!!"], "", "(Press right for a QR code)")
        return True

    def display_donate_qr(self):
        self.draw_modal(["Loading..."])
        self.donate_image = self.qr.qrimage("bc1q8u3dyltlg6pu56fe7m58aqz9cwrfld0s03zlrjl0wvm9x4nfa60q2l0g97")
        View.DispShowImage(self.donate_image)
        return True

    ### Display Network Selection

    def display_current_network(self) -> str:
        r = self.controller.menu_view.display_generic_selection_menu(["... [ Return to Settings ]", "Mainnet", "Testnet"], "Which Network?")
        if r == 2:
            return "main"
        elif r == 3:
            return "test"
        else:
            return "cancel"

    ### Display Wallet Selection

    def display_wallet_selection(self) ->str:
        r = self.controller.menu_view.display_generic_selection_menu(["... [ Return to Settings ]", "Specter Desktop", "Blue Wallet Vault", "Sparrow Multisig", "UR 2.0 Multisig"], "Which Wallet?")
        if r == 2:
            return "Specter Desktop"
        elif r == 3:
            return "Blue Wallet Vault"
        elif r == 4:
            return "Sparrow Multisig"
        elif r == 5:
            return "UR 2.0 Multisig"
        # elif r == 3:
        #     return "Specter Desktop Single Sig"
        else:
            return "cancel"

    ###
    ### Version Info
    ###

    def display_version_info(self):
        View.draw_rectangle((0, 0, View.canvas_width, View.canvas_height), outline=0, fill=0, resize=False)
        self.draw_text("SeedSigner", 20, 'impact', 22)
        self.draw_text("Version v" + self.controller.VERSION, 55, 'impact', 22)
        self.draw_text("built for use with", 90, 'impact', 22)
        self.draw_text("Specter-desktop", 125, 'impact', 22)
        self.draw_text("v1.1.0 or higher", 160, 'impact', 22)
        self.draw_text("(Joystick RIGHT to EXIT)", 210, 'impact', 18)
        View.DispShowImage()