from kivy.properties import StringProperty
from main_imports import MDScreen,MDDropdownMenu,Window,MDFileManager,MDSnackbar,MDSnackbarText,Clock,MDModalDatePicker,MDModalInputDatePicker,MDSnackbarText,MDSnackbarSupportingText,dp
from libs.applibs import utils,supabase_db as db
from libs.applibs.loader import Dialog_cls
from datetime import datetime
# from libs.uix.baseclass.add_transactions import AddTransactions
import os

utils.load_kv("admission_form_screen.kv")
class AdmissionFormScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Window.bind(on_keyboard=self.events)
        self.manager_open = False
        self.file_manager = MDFileManager(
            exit_manager=self.exit_manager, select_path=self.select_path,preview=True,
        )
    full_name = StringProperty("")
    date_of_birth = StringProperty("")
    gender = StringProperty("")
    contact_number = StringProperty("")
    age = StringProperty("")
    email_id = StringProperty("")
    address = StringProperty("")
    education_qualification = StringProperty("")
    joining_for = StringProperty("")
    profile_image = "profile.png"
    all_customer_contacts = list()
    filtered_data = []
    
    def on_pre_enter(self):
        self.contacts = db.get_all_customers_contact()
        print("This is all customer contacts ----> ",self.contacts)
    def on_enter(self):
        loader = Dialog_cls()
        loader.open_dlg()
        
        if self.contacts:
            self.all_customer_contacts = self.contacts
            loader.close_dlg()
        else:
            loader.close_dlg()
            utils.snack("red","Sorry could not get contacts")
        self.menu = MDDropdownMenu(
            caller=self.ids.contact_field,
            items=[],
            position="bottom",
            width_mult=4,
        )
    # contact filter section ------------------------------
    def on_leave(self):
        self.full_name = ""
        self.date_of_birth = ""
        customer_age=0
        self.age = str(customer_age)+" years"
        self.gender = ""
        self.email_id = ""
        self.address = ""
        self.education_qualification = ""
        self.joining_for = ""
        self.profile_image = ""  
        self.contact_number = ""
    def set_item(self, text_item):
        self.contact_number = text_item
        loader = Dialog_cls()
        try:
            loader.open_dlg()
            response = db.get_customers_details(text_item)
            if response:
                self.fill_existing_customer_details(response[0])
                loader.close_dlg()
        except:
            loader.close_dlg()
            utils.snack("red","Something went wrong No Customer data fetched")
        self.menu.dismiss()
    def fill_existing_customer_details(self,details):
        loader = Dialog_cls()
        loader.open_dlg()
        self.full_name = details["name"]
        self.date_of_birth = details["dob"]
        customer_age=self.calculate_age(self.date_of_birth)
        self.age = str(customer_age)+" years"
        self.gender = details["gender"]
        self.email_id = details["email"]
        self.address = details["address"]
        self.education_qualification = details["education"]
        self.joining_for = details["joining_for"]
        self.profile_image = details["profile_image"]
        loader.close_dlg()
    def update_menu(self, query):
        self.contact_number = query
        # Filter data based on the query
        if query:
            if len(query)>3:
                self.filtered_data = [item for item in self.all_customer_contacts if query.lower() in item.lower()]
        else:
            self.filtered_data = []

        # Update menu items
        menu_items = [
            {
                "text": f"{i}",
                "on_release": lambda x=f"{i}": self.set_item(x),
            } for i in self.filtered_data
        ]
        self.menu.items = menu_items
        self.menu.position="bottom"

        # Open the menu if there are items to show
        if self.filtered_data:
            if not self.menu.parent:
                self.menu.open()
        else:
            self.menu.dismiss()

    # File manager----------------------------------
    def file_manager_open(self):
        self.file_manager.show(
            os.path.expanduser("~"))  # output manager to the screen
        self.manager_open = True

    def select_path(self, path: str):
        '''
        It will be called when you click on the file name
        or the catalog selection button.

        :param path: path to the selected directory or file;
        '''
        self.profile_image = path
        self.exit_manager()
        MDSnackbar(
            MDSnackbarText(
                text=path,
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        ).open()

    def exit_manager(self, *args):
        '''Called when the user reaches the root of the directory tree.'''

        self.manager_open = False
        self.file_manager.close()

    def events(self, instance, keyboard, keycode, text, modifiers):
        '''Called when buttons are pressed on the mobile device.'''

        if keyboard in (1001, 27):
            if self.manager_open:
                self.file_manager.back()
        return True

    # End file manager---------------------------------

#    Data picker start-------------------
    def show_modal_input_date_picker(self, *args):
        def on_edit(*args):
            date_dialog.dismiss()
            print("Inside on edit method")
            Clock.schedule_once(self.show_modal_date_picker, 0.2)

        date_dialog = MDModalInputDatePicker()
        date_dialog.date_format="dd/mm/yyyy"
        date_dialog.bind(on_edit=on_edit)
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.bind(on_cancel=self.on_cancel)
        date_dialog.open()

    def on_edit(self, instance_date_picker):
        instance_date_picker.dismiss()
        print("Inside On edit main method")
        Clock.schedule_once(self.show_modal_input_date_picker, 0.2)

    def show_modal_date_picker(self, *args):
        print("Inside date picker 1")
        date_dialog = MDModalDatePicker()
        date_dialog.bind(on_edit=self.on_edit)
        date_dialog.bind(on_ok=self.on_ok)
        date_dialog.bind(on_cancel=self.on_cancel)
        date_dialog.open()
    def on_cancel(self, instance_date_picker):
        instance_date_picker.dismiss()


    def on_ok(self, instance_date_picker):
        print("inside On OK method")
        instance_date_picker.dismiss()
        self.date_of_birth = str(instance_date_picker.get_date()[0])
        customer_age = self.calculate_age(self.date_of_birth)
        self.age = str(customer_age)+" years"

        

        # Date picker end -----------------
        # gender menu------------------
    def open_gender_menu(self, item):
        self.menu = MDDropdownMenu()
        menu_items = [
            {
                "text": "Male",
                "leading_icon": "human-male",
                "on_release": lambda x="Male": self.menu_callback(x),
            },
            {
                "text": "Female",
                "leading_icon": "human-female",
                "on_release": lambda x="Female": self.menu_callback(x),
            },
            {
                "text": "Trans Gender",
                "leading_icon": "gender-male-female",
                "on_release": lambda x="Trans Gender": self.menu_callback(x),
            },
        ]
        self.menu.caller=item
        self.menu.items=menu_items
        self.menu.position="bottom"
        self.menu.open()

    def menu_callback(self, text_item):
        self.ids.drop_text.text = text_item
        self.gender = text_item
        self.menu.dismiss()

    def calculate_age(self,date_str):
        # Parse the date string into a datetime object
        birth_date = datetime.strptime(date_str, "%Y-%m-%d")
        # Get today's date
        today = datetime.today()
        # Calculate age
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        return age

    def submit_form(self):
        add_txn = self.parent.get_screen("addTxn")
        # add_txn.addmission_form_data 
        # Logic for form submission (printing entered data as a placeholder)
        if self.full_name!="" and self.date_of_birth!="" and self.gender!="" and self.contact_number!="" and self.email_id!="" and self.education_qualification!="" and self.joining_for!="" and self.address!="":

            form_data = {
                "customer_name": self.full_name.strip(),
                "customer_dob": self.date_of_birth,
                "customer_gender": self.gender,
                "customer_phone_number": self.contact_number.strip(),
                "customer_email": self.email_id.strip(),
                "customer_education": self.education_qualification.strip(),
                "customer_joining_for": self.joining_for.strip(),
                "customer_address": self.address.strip(),
                "customer_profile_image": self.profile_image.strip(),
            }
            # create_customer = supabase_db.create_customer(name=self.full_name,dob=self.date_of_birth,gender=self.gender,phone_number=self.contact_number,email=self.email_id,education=self.education_qualification,joining_for=self.joining_for,address=self.address,profile_image=self.profile_image)
            # print(create_customer)
            utils.snack(color="green",text="Admission Form Submitted Successfully!")
            # print(form_data)  # Replace this with actual form submission logic
            add_txn.addmission_form_data = form_data
            self.parent.change_screen("addTxn")
        else:
            utils.snack(color="red",text="Please fill all the fields..")
            
