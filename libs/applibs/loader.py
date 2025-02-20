from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.dialog import (
    MDDialog,MDDialogContentContainer)
KV = '''
<Details>:
    pos_hint: {'center_x': .5, 'center_y': .5}
    theme_bg_color: "Custom"
    md_bg_color: "#192134"
    MDCircularProgressIndicator:
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {'center_x': .5, 'center_y': .5}
'''
class Details(MDBoxLayout):
    Builder.load_string(KV)
class Dialog_cls(MDBoxLayout):
    def open_dlg(self):
        dg = None
        self.dg = MDDialog(
        MDDialogContentContainer(Details())

        )
        self.dg.adaptive_size = True
        self.dg.auto_dismiss = False
        self.dg.pos_hint = {'center_y': .5,'center_x':.4}
        self.dg.open()
    def close_dlg(self):
        self.dg.dismiss()

