from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import (
    MDDialog,MDDialogContentContainer)
KV = '''
<QR>:
    # radius: "36dp"
    # pos_hint: {'center_x': .5, 'center_y': .5}
    # size_hint: .7, .5
    theme_bg_color: "Custom"
    md_bg_color: "#192134"
    MDSmartTile:
        pos_hint: {"center_x": .5, "center_y": .5}
        size_hint: None, None
        size: "300dp", "320dp"
        overlap: False

        MDSmartTileImage:
            # pos_hint: {"center_x": .5, "center_y": .5}
            source: "assets/img/payment_QR.jpeg"
            radius: [dp(24), dp(24), dp(24), dp(24)]

'''
class QR(MDBoxLayout):
    # print("Inside QR Class>>>>>>>>>>>>>>>>>>>>")
    Builder.load_string(KV)
class QRDialog_cls(MDBoxLayout):
    def open_qr_dlg(self):
        dg = None
        # print("Inside open QR Function >>>>>>>>>>")
        self.dg = MDDialog(
        MDDialogContentContainer(QR())

        )
        self.dg.adaptive_size = True
        self.dg.auto_dismiss = True
        self.dg.pos_hint = {'center_x': .05,'center_y': .5}
        self.dg.open()
    def close_qr_dlg(self):
        self.dg.dismiss()

