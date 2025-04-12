from kivy.lang import Builder
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.dialog import (
    MDDialog,MDDialogContentContainer)

KV = '''
<Details>:
    # pos_hint: {'center_x': .5, 'center_y': .5}
    theme_bg_color: "Custom"
    md_bg_color: "#192134"
    MDCircularProgressIndicator:
        size_hint: None, None
        size: "48dp", "48dp"
        pos_hint: {'center_x': .5, 'center_y': .5}
    # Image:
    #     id: gif
    #     source: 'assets/loader.gif'
    #     size_hint: None, None
    #     size: 200, 200
    #     allow_stretch: True
    #     anim_delay: 0.02  # lower = faster
    #     anim_loop: 0  # 0 means loop forever
    #     pos_hint: {"center_x": 0.5, "center_y": 0.5}
    
'''
class Details(MDBoxLayout):
    Builder.load_string(KV)
class Dialog_cls(MDBoxLayout):
    def open_dlg(self,islogin=False):
        dg = None
        self.dg = MDDialog(
        MDDialogContentContainer(Details())
        # MDDialogContentContainer(MDLabel(
        #             text="Logging In.." if islogin==True else "Data Loading..",
        #             halign="center",
        #         ))

        )
        self.dg.adaptive_size = True
        # self.dg.size_hint = .2,.15
        self.dg.auto_dismiss = False
        self.dg.pos_hint = {'center_y': .5,'x':.35}
        self.dg.open()
    def close_dlg(self):
        self.dg.dismiss()

