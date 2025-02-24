from main_imports import MDScreen,MDButton,MDWidget,StringProperty, MDButtonText,MDDropdownMenu,MDDialog, MDDialogHeadlineText, MDDialogButtonContainer,MDDialogSupportingText,MDBoxLayout,MDLabel, dp,MDCard,MDIconButton,BoxLayout,BoxLayout
from libs.applibs import utils
from libs.applibs.supabase_db import *
from libs.applibs.loader import Dialog_cls
#  Expansion 
# import asynckivy
# from kivy.animation import Animation
# from kivy.metrics import dp
# from kivy.uix.behaviors import ButtonBehavior
# from kivymd.uix.behaviors import RotateBehavior
# from kivymd.uix.expansionpanel import MDExpansionPanel
# from kivymd.uix.list import MDListItemTrailingIcon

utils.load_kv("cutomer_profile.kv")
# class ExpansionPanelItem(MDExpansionPanel):
#     ...


# class TrailingPressedIconButton(
#     ButtonBehavior, RotateBehavior, MDListItemTrailingIcon
# ):
#     ...


class CustomerProfile(MDScreen):
    customer_id = StringProperty()
    dialog = None
    username = StringProperty()
    join_date = StringProperty()
    expiry_date = StringProperty()
    profile_image = "assets/img/blank_profile.png" # Path to user's profile image
    dob = StringProperty()
    email= StringProperty()
    phone = StringProperty()
    address = StringProperty()

    def on_enter(self):
        # async def set_panel_list():
        #     for i in range(2):
        #         await asynckivy.sleep(0)
        #         self.ids.container.add_widget(ExpansionPanelItem())

        # asynckivy.start(set_panel_list())
        
        print("Inside page -- >",self.username,self.join_date,self.expiry_date,self.dob,self.email,self.phone,self.address)
        # else:
        #     print("No Customer ID found...")
    # def tap_expansion_chevron(
    #         self, panel: MDExpansionPanel, chevron: TrailingPressedIconButton
    #     ):
    #         Animation(
    #             padding=[0, dp(12), 0, dp(12)]
    #             if not panel.is_open
    #             else [0, 0, 0, 0],
    #             d=0.2,
    #         ).start(panel)
    #         panel.open() if not panel.is_open else panel.close()
    #         panel.set_chevron_down(
    #             chevron
    #         ) if not panel.is_open else panel.set_chevron_up(chevron)
    def go_back(self, instance):
        # Function to go back to the previous screen
        print("Back to previous screen")
        self.parent.previous_screen()

    def go_to_transaction_history(self):
        # Implement the navigation to the Transactional History page
        print("Navigating to Transactional History")

    def go_to_user_details(self):
        # Implement the navigation to the User Details page
        print("Navigating to User Details")
        self.open_user_details()
    
    def open_user_details(self):
        self.user_data = f"""
                        [b]Name :[/b] {self.username}
                        [b]Phone :[/b] {self.phone}
                        [b]Email :[/b] {self.email}
                        [b]DOB :[/b] {self.dob}
                        [b]Address :[/b] {self.address}

                        """
        print("User Data ---> ",self.user_data)
        # self.user_data_text = MDDialogSupportingText(
        #             text=self.user_data,
        #             halign="left",
        #         )
        if self.dialog == None:
            self.dialog = MDDialog(
                MDDialogHeadlineText(
                    text="User Details",
                    halign="center",
                ),
                MDDialogSupportingText(
                    text=self.user_data,
                    halign="left",
                ),
                MDDialogButtonContainer(
                    MDWidget(),
                    MDButton(
                        MDButtonText(text="Close"),
                        style="text",
                        on_release=self.close_popup
                    ),
                    MDWidget(),
                    spacing="8dp",
                ),
            )
        else:
            print(self.dialog.ids.supporting_text_container.children[0].text)
        self.dialog.ids.supporting_text_container.children[0].text = self.user_data
        self.dialog.open()
    def close_popup(self, *args):
        if self.dialog:
            print(self.dialog.ids.supporting_text_container.children[0].text)
            # self.dialog.remove_widget(self.dialog.ids.supporting_text_container)
            self.dialog.dismiss()

    def navigate_transactions(self):
        self.parent.get_screen("transactions").profile_redirect = self.username
        self.parent.change_screen("transactions")
    def navigate_subcriptions(self):
        print(self.username)
        self.parent.get_screen("expired_list").profile_redirect1 = self.username
        self.parent.change_screen("expired_list")