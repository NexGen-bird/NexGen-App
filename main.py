from kivy.config import Config
Config.set("graphics","width",390 )
Config.set("graphics","height",640)
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.screen import MDScreen
from kivy.lang import Builder
from kivymd.uix.snackbar.snackbar import MDSnackbar,MDSnackbarActionButton
from kivymd.uix.label.label import MDLabel
from kivy.metrics import dp
from supabase_lib.supabase_auth import *

#--[Start platform specific code]
"""This code to detect it's Android or not 
if it's not android than app window size change in android phone size"""
# from kivy.utils import platform
 
# if platform != 'android':
#     from kivy.config import Config
#     Config.set("graphics","width",360 )
#     Config.set("graphics","height",640)
#--[End platform specific code]

#--[Start Soft_Keyboard code ]
"""code for android keyboard. when in android keyboard show textbox 
automatic go to top of keyboard so user can see when he type msg"""
from kivy.core.window import Window

Window.keyboard_anim_args = {"d":.2,"t":"linear"}
Window.softinput_mode = "below_target"
#--[End Soft_Keyboard code ]

#--[Import All Baseclasses from lib.baseclass ]

from libs.uix.baseclass.root import Root
from libs.uix.baseclass.login import Login_Screen
from libs.uix.baseclass.dashboard import LandingScreen
from libs.uix.baseclass.seatregister import SeatRegisterScreen
from libs.uix.baseclass.customer_profile import CustomerProfile
from libs.uix.baseclass.customers_list import CustomersList
from libs.uix.baseclass.admission_form_screen import AdmissionFormScreen
from libs.uix.baseclass.transactions import Transactions
from libs.uix.baseclass.add_transactions import AddTransactions
from libs.uix.baseclass.expired_sub import ExpiredCustomersList


#--[End Import All Baseclasses from lib.baseclass ]

from main_imports import MDApp,MDNavigationLayout,MDNavigationDrawer,MDNavigationDrawerItemText,MDNavigationDrawerMenu,MDNavigationDrawerLabel,MDNavigationDrawerItem,MDNavigationDrawerDivider,MDNavigationDrawerHeader

#--[ Register custom classes ]
# from kivy.factory import Factory
# r = Factory.register
# _class = 'ChatListItem'
# module = 'libs.applibs.list'
# r(_class, module=module)
#--[ End Register custom classes ]

class NexGenApp(MDApp):
    def __init__(self, **kwargs):
        super(NexGenApp, self).__init__(**kwargs)
    
    def on_start(self):
        pass
        # login_with_email_password("abhijit.shinde@test.com","india@123")
    
    def build(self):
        """
        This method call before on_start() method so anything
        that need before start application all other method and code 
        write here.
        """
        self.theme_cls.primary_palette = "Lavender"
        # Create the root layout as an MDNavigationLayout to include the navigation drawer
        nav_layout = MDNavigationLayout()

        # Create the navigation drawer and add custom header and items
        nav_drawer = MDNavigationDrawer(
            radius=(0, dp(16), dp(16), 0),
        )
        # nav_drawer.theme_bg_color="Custom"
        # nav_drawer.md_bg_color="#192134"
        # Create the navigation drawer menu with items
        drawer_menu = MDNavigationDrawerMenu()
        drawer_header = MDNavigationDrawerLabel(text="NexGen Self Study Center",)
        drawer_item1 = MDNavigationDrawerItem(
            MDNavigationDrawerItemText(
                                text="Dashboard",
                                focus_color="#192134",
                                text_color="#ed991f",
                                
                            ),
                            on_release=lambda x: self.switch_screen("land")
                            )
        
        drawer_item2 = MDNavigationDrawerItem(
            MDNavigationDrawerItemText(text="Customer List",
            focus_color="#192134",
            text_color="#ed991f",
        ),
            on_release=lambda x: self.switch_screen("customers_list"))
        
        drawer_item3 = MDNavigationDrawerItem(
            MDNavigationDrawerItemText(text="Seats",
            focus_color="#192134",
            text_color="#ed991f",
            ),
            on_release=lambda x : self.switch_screen("seat")
        )
        drawer_item4 = MDNavigationDrawerItem(
            MDNavigationDrawerItemText(text="Admission Form",
            focus_color="#192134",
            text_color="#ed991f",
            ),
            on_release=lambda x : self.switch_screen("admission_form")
        )
        drawer_item5 = MDNavigationDrawerItem(
            MDNavigationDrawerItemText(text="Transactions",
            focus_color="#192134",
            text_color="#ed991f",
            ),
            on_release=lambda x : self.switch_screen("transactions")
        )
        drawer_item6 = MDNavigationDrawerItem(
            MDNavigationDrawerItemText(text="Add Transaction",
            focus_color="#192134",
            text_color="#ed991f",
            ),
            on_release=lambda x : self.switch_screen("addTxn")
        )
        drawer_item7 = MDNavigationDrawerItem(
            MDNavigationDrawerItemText(text="Subcriptions",
            focus_color="#192134",
            text_color="#ed991f",
            ),
            on_release=lambda x : self.switch_screen("expired_list")
        )
        # Add items to the drawer menu
        drawer_menu.add_widget(drawer_header)
        drawer_menu.add_widget(MDNavigationDrawerDivider())
        drawer_menu.add_widget(drawer_item1)
        drawer_menu.add_widget(MDNavigationDrawerDivider())
        drawer_menu.add_widget(drawer_item2)
        drawer_menu.add_widget(MDNavigationDrawerDivider())
        # drawer_menu.add_widget(drawer_item3)
        # drawer_menu.add_widget(MDNavigationDrawerDivider())
        drawer_menu.add_widget(drawer_item4)
        drawer_menu.add_widget(MDNavigationDrawerDivider())
        drawer_menu.add_widget(drawer_item5)
        drawer_menu.add_widget(MDNavigationDrawerDivider())
        drawer_menu.add_widget(drawer_item6)
        drawer_menu.add_widget(MDNavigationDrawerDivider())
        drawer_menu.add_widget(drawer_item7)

        # Add menu to the drawer
        nav_drawer.add_widget(drawer_menu)

        # Initialize the screen manager and add screens
        self.screen_manager = Root()
        self.screen_manager.add_widget(Login_Screen())
        self.screen_manager.add_widget(Transactions())
        self.screen_manager.add_widget(AddTransactions())
        self.screen_manager.add_widget(LandingScreen())
        self.screen_manager.add_widget(AdmissionFormScreen())
        self.screen_manager.add_widget(SeatRegisterScreen())
        self.screen_manager.add_widget(CustomerProfile())
        self.screen_manager.add_widget(CustomersList())
        self.screen_manager.add_widget(ExpiredCustomersList())
        
        # Add the screen manager and navigation drawer to the layout
        nav_layout.add_widget(self.screen_manager)
        nav_layout.add_widget(nav_drawer)
        
        return nav_layout
    def on_stop(self):
        self.logout()
    def switch_screen(self,screename):
        self.screen_manager.change_screen(screename)
        self.root.children[0].set_state("close")
    

    def logout(self):
        print("Inside Logout....")
        logout()
        self.screen_manager.change_screen("login")

if __name__ == '__main__':
    NexGenApp().run()
