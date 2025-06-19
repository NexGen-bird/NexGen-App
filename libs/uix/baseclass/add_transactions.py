from kivy.properties import StringProperty
from main_imports import MDScreen,MDBoxLayout,MDButtonText,MDDialogButtonContainer,MDButton,MDWidget,MDDropdownMenu,ListProperty,BooleanProperty,NumericProperty,Window,MDFileManager,MDSnackbar,MDSnackbarText,Clock,MDModalDatePicker,MDModalInputDatePicker,MDSnackbarText,MDSnackbarSupportingText,dp
from libs.applibs import utils
from datetime import date
from libs.applibs.supabase_db import *
from libs.applibs.paymentQR import QRDialog_cls
from libs.applibs.whatsapp import send_messages

utils.load_kv("add_transactions.kv")
class CheckBoxButton(MDBoxLayout):
    text = StringProperty()

class CheckItem(MDBoxLayout):
    text = StringProperty()
    group = "root"
    checkvalue = NumericProperty()
    active_val = BooleanProperty()
class AddTransactions(MDScreen):
    addmission_form_data = dict()
    planTypeSelected = StringProperty("")
    txn_of = StringProperty("")
    receipt_id = StringProperty("")
    transaction_date = StringProperty("")
    plan_type = NumericProperty()
    shift = StringProperty("")
    amount = StringProperty("")
    transaction_mode = StringProperty("")
    transaction_made_by = StringProperty("")
    transaction_startdate = StringProperty("")
    transaction_enddate = StringProperty("")
    transaction_made_to = StringProperty("")
    transaction_type = StringProperty("")
    transaction_made_for = StringProperty("")
    menu = None
    shifts_selected = ListProperty([])
    shifts_selected1 = []
    is_locker = BooleanProperty()
    plantypeid = NumericProperty()
    def on_pre_enter(self):
        pass

    def on_enter(self):
        self.transaction_date = str(date.today())
        print(self.addmission_form_data)
        AS = self.parent.get_screen("admission_form")
        print("Transactions >>>>>",AS.contact_number)
        if AS.contact_number:
            print("inside if ")
            self.txn_of="Admission"
            self.transaction_made_for= "admission"
            self.transaction_made_by = self.addmission_form_data['customer_name']
            self.transaction_made_to = "abhijit shinde"
            self.transaction_type = "IN"
            self.ids.txntype_text.text = self.transaction_type
        else:
            print("inside else ")
            self.txn_of="General"
            # self.transaction_made_by = "nexgen"
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text="Adding Investment or Salary?",
                halign="left",
            ),
            MDDialogSupportingText(
                text="""
Note:
incase of investment-
transaction type - 'IN'
description - 'investment'
transaction made to - nexgen

incase of Salary-
transaction type - 'OUT'
description - 'salary'
transaction made to - name of staff
""",
                halign="left",
            ),
            # MDDialogButtonContainer(
            #     MDWidget(),
            #     # MDButton(
            #     #     MDButtonText(text="Cancel"),
            #     #     style="text",
            #     #     on_release=lambda x:self.close_dialog()
            #     # ),
            #     # MDButton(
            #     #     MDButtonText(text="Discard"),
            #     #     style="text",
            #     #     on_release=lambda x:self.dialog.dismiss()
            #     # ),
            #     spacing="8dp",
            # ),
        ).open()
    
    def on_leave(self):
        self.txn_of = ""
        self.receipt_id = ""
        self.transaction_date = ""
        self.plan_type = 0
        self.shift = ""
        self.amount = ""
        self.transaction_mode = ""
        self.transaction_made_by = ""
        self.transaction_startdate = ""
        self.transaction_enddate = ""
        self.transaction_made_to = ""
        self.transaction_type = ""
        self.transaction_made_for = ""
        self.menu = None
        self.shifts_selected.clear()
        self.shifts_selected1.clear()
        self.is_locker = False
        self.plantypeid = 0
        self.ids.txn_mode.text = "Txn Mode"
        self.ids.txntype_text.text = "Txn Type"
        self.ids.shift.text = "Select Shift"
        self.ids.plan_type.text = "Select Plan Type"

        self.addmission_form_data.clear()
    
    def show_qr(self):
        qr = QRDialog_cls()
        qr.open_qr_dlg()
    
    def change_txn_in(self,change_to):
        print(change_to)
        # if change_to == "Addmission":
        #     self.ids.receipt_id.disabled == True
        #     self.ids.shift_menu_id.disabled == True
        #     self.ids.plan_type_id.disabled == True
        # else:
        #     self.ids.receipt_id.disabled == False
        #     self.ids.shift_menu_id.disabled == False
        #     self.ids.plan_type_id.disabled == False

    def menu_txn_open(self):
        menu_items = [
            {
                "text": "General",
                "leading_icon": "account",
                "on_release": lambda z="General": self.menu_txn_callback(z),
            },
            {
                "text": "Admission",
                "leading_icon": "account-plus",
                "on_release": lambda z="Admission": self.menu_txn_callback(z),
            },
        ]
        self.menu=MDDropdownMenu(
            caller=self.ids.txnbtn, items=menu_items
        )
        self.menu.position="bottom"
        self.menu.open()

    def menu_txn_callback(self, text_item):
        self.ids.txntext.text = text_item
        self.change_txn_in(text_item)
        print("Menu Selected --> ",text_item)
        self.txn_of = text_item
        
        self.transaction_made_for = text_item
        self.menu.dismiss()
    
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
        self.transaction_date = str(instance_date_picker.get_date()[0])
        
    # Date picker end -----------------
    # Plan Type menu -------------------------------------
    def open_plantype_menu(self,item):
        self.menu = MDDropdownMenu()
        menu_items = [
            {
                "text": "Monthly",
                # "leading_icon": "bank-transfer-in",
                "on_release": lambda y="Monthly": self.menu_plantypecallback(y),
            },
            {
                "text": "Quaterly",
                # "leading_icon": "bank-transfer-out",
                "on_release": lambda y="Quaterly": self.menu_plantypecallback(y),
            },
            {
                "text": "Half Yearly",
                # "leading_icon": "bank-transfer-out",
                "on_release": lambda y="Half Yearly": self.menu_plantypecallback(y),
            },
            {
                "text": "Yearly",
                # "leading_icon": "bank-transfer-out",
                "on_release": lambda y="Yearly": self.menu_plantypecallback(y),
            },
            {
                "text": "Day",
                # "leading_icon": "bank-transfer-out",
                "on_release": lambda y="Day": self.menu_plantypecallback(y),
            },
            {
                "text": "Week-End",
                # "leading_icon": "bank-transfer-out",
                "on_release": lambda y="Week-End": self.menu_plantypecallback(y),
            },
        ]
        
        self.menu.caller=item
        self.menu.items=menu_items
        self.menu.position="bottom"
        self.menu.open()

    def open_shift_menu(self,item):
        self.menu = MDDropdownMenu()
        checkbox = [
            {
                "viewclass": "CheckItem",
                "text": "6am - 12pm",
                "checkvalue": 1,
                "active_val": 1 in self.shifts_selected,
            },
            {
                "viewclass": "CheckItem",
                "text": "12pm - 6pm",
                "checkvalue": 2,
                "active_val": 2 in self.shifts_selected,
            },
            {
                "viewclass": "CheckItem",
                "text": "6pm - 12am",
                "checkvalue": 3,
                "active_val": 3 in self.shifts_selected,
            },
            {
                "viewclass": "CheckItem",
                "text": "12am - 6am",
                "checkvalue": 4,
                "active_val": 4 in self.shifts_selected,
            },
        ]
        self.menu.caller=item
        self.menu.items=checkbox
        self.menu.position="center"
        self.menu.bind(on_dismiss=self.close_shift_pop_up)
        self.menu.open()

    # txntype menu------------------

    def on_checkbox_active(self, checkbox, value, text, check_val):
        if value:  # Checkbox is active
            if check_val not in self.shifts_selected:
                self.shifts_selected.append(check_val)
        else:  # Checkbox is inactive
            if check_val in self.shifts_selected:
                self.shifts_selected.remove(check_val)
        print("Selected Shifts -->", self.shifts_selected)

    def open_txntype_menu(self,item):
        self.menu = MDDropdownMenu()
        menu_items = [
            {
                "text": "IN",
                "leading_icon": "bank-transfer-in",
                "on_release": lambda y="IN": self.menu_txntypecallback(y),
            },
            {
                "text": "OUT",
                "leading_icon": "bank-transfer-out",
                "on_release": lambda y="OUT": self.menu_txntypecallback(y),
            },
            
        ]
        self.menu.caller=item
        self.menu.items=menu_items
        self.menu.position="bottom"
        self.menu.open()
    def open_txnmode_menu(self, item):
        self.menu = MDDropdownMenu()
        menu_items = [
            {
                "text": "UPI",
                "leading_icon": "google-plus",
                "on_release": lambda x="UPI": self.menu_callback(x),
            },
            {
                "text": "Cash",
                "leading_icon": "cash-100",
                "on_release": lambda x="Cash": self.menu_callback(x),
            },
            {
                "text": "Partial",
                "leading_icon": "cash-plus",
                "on_release": lambda x="Partial": self.menu_callback(x),
            },
        ]
        self.menu.caller=item
        self.menu.items=menu_items
        self.menu.position="bottom"
        self.menu.open()

    def menu_callback(self, text_item):
        self.ids.txn_mode.text = text_item
        self.transaction_mode = text_item
        self.menu.dismiss()

    def menu_txntypecallback(self, text_item):
        self.ids.txntype_text.text = text_item
        self.transaction_type = text_item
        if text_item == "OUT":
            self.transaction_made_by = "nexgen"
        else:
            self.transaction_made_by = ""
        self.menu.dismiss()
        print("STate ---> ",self.menu.state)

    def menu_plantypecallback(self, text_item):
        self.ids.plan_type.text = text_item
        self.planTypeSelected = self.ids.plan_type.text
        if text_item=="Monthly":
            self.plan_type = 2
        elif text_item=="Quaterly":
            self.plan_type = 3
        elif text_item=="Half Yearly":
            self.plan_type = 4
        elif text_item=="Yearly":
            self.plan_type = 5
        elif text_item=="Week-End":
            self.plan_type = 6
        elif text_item=="Day":
            self.plan_type = 1
            self.plantypeid = 4
            self.shifts_selected = [1,2,3]


        self.update_start_end_date(self.plan_type)
        self.menu.dismiss()

    def close_shift_pop_up(self,*args):
        """
        when shift pop up close then this method will call 
        and show text based on shifts selected 
        """
        if len(self.shifts_selected) >3:
            self.menu_shiftcallback("Ultimate plan")
            self.plantypeid = 5
        elif len(self.shifts_selected) >2:
            self.menu_shiftcallback("3 Shifts")
            self.plantypeid = 3
        elif len(self.shifts_selected) ==2:
            self.menu_shiftcallback("2 Shifts")
            self.plantypeid = 2
        else:
            self.menu_shiftcallback("1 Shifts")
            self.plantypeid = 1
        

    def menu_shiftcallback(self, text_item):
        self.ids.shift.text = text_item
        self.shift = text_item
        self.menu.dismiss()
    
    def update_start_end_date(self,plantype):
        print(type(self.transaction_date))
        self.transaction_startdate,self.transaction_enddate = utils.calculate_end_dates(self.transaction_date,plantype)


    def update_batch(self,is_locker):
        self.is_locker = is_locker
        self.amount_by_shift(self.ids.shift.text)
        

    def amount_by_shift(self,shift):
        # print("IS WEEKEND Value --->",self.is_weekend)
        if self.plan_type == 3:
            if "1 Shifts" in shift:
                self.amount = "3560"
            elif "2 Shifts" in shift:
                self.amount = "6270"
            elif "3 Shifts" in shift:
                self.amount = "8100"
            elif "Ultimate plan" in shift:
                self.amount = "9975"
            
        elif self.plan_type == 4:
            if "1 Shifts" in shift:
                self.amount = "7125"
            elif "2 Shifts" in shift:
                self.amount = "12540"
            elif "3 Shifts" in shift:
                self.amount = "16245"
            elif "Ultimate plan" in shift:
                self.amount = "19950"
        elif self.plan_type == 5:
            if "1 Shifts" in shift:
                self.amount = "13500"
            elif "2 Shifts" in shift:
                self.amount = "23760"
            elif "3 Shifts" in shift:
                self.amount = "30780"
            elif "Ultimate plan" in shift:
                self.amount = "37800"
        elif self.plan_type == 1:
            if "3 Shifts" in shift:
                self.amount = "250"
        elif self.plan_type == 6:
            if "1 Shifts" in shift:
                self.amount = "550"
            elif "2 Shifts" in shift:
                self.amount = "850"
            elif "3 Shifts" in shift:
                self.amount = "1250"
            elif "Ultimate plan" in shift:
                self.amount = "1700"
        else:
            if "1 Shifts" in shift:
                self.amount = "1250"
            elif "2 Shifts" in shift:
                self.amount = "2200"
            elif "3 Shifts" in shift:
                self.amount = "2850"
            elif "Ultimate plan" in shift:
                self.amount = "3500"
        if self.is_locker == True:
            self.amount = str(int(self.amount)+250)
        # else:
        #     if self.plan_type == 3:
        #         if "1 Shifts" in shift:
        #             self.amount = "1560"
        #         elif "2 Shifts" in shift:
        #             self.amount = "2420"
        #         elif "3 Shifts" in shift:
        #             self.amount = "3560"
        #         elif "Ultimate plan" in shift:
        #             self.amount = "4840"
                
        #     elif self.plan_type == 4:
        #         if "1 Shifts" in shift:
        #             self.amount = "3135"
        #         elif "2 Shifts" in shift:
        #             self.amount = "4845"
        #         elif "3 Shifts" in shift:
        #             self.amount = "7125"
        #         elif "Ultimate plan" in shift:
        #             self.amount = "9690"
        #     elif self.plan_type == 5:
        #         if "1 Shifts" in shift:
        #             self.amount = "5940"
        #         elif "2 Shifts" in shift:
        #             self.amount = "9690"
        #         elif "3 Shifts" in shift:
        #             self.amount = "13500"
        #         elif "Ultimate plan" in shift:
        #             self.amount = "18360"
        #     elif self.plan_type == 1:
        #         if "3 Shifts" in shift:
        #             self.amount = "250"
        #     else:
        #         if "1 Shifts" in shift:
        #             self.amount = "550"
        #         elif "2 Shifts" in shift:
        #             self.amount = "850"
        #         elif "3 Shifts" in shift:
        #             self.amount = "1250"
        #         elif "Ultimate plan" in shift:
        #             self.amount = "1700"

    def submit_form(self):
        # Logic for form submission (printing entered data as a placeholder)
        # Get the current date and time with microseconds
        txn_date = utils.add_current_time_to_date(self.transaction_date)
        data = {
            "customer_transaction_date": txn_date,
            "customer_transaction_type": self.transaction_type,
            "customer_amount": self.amount.strip(),
            "customer_payment_method": self.transaction_mode,
            "customer_description": self.transaction_made_for.strip(),
            "customer_transaction_for": self.txn_of.strip(),
            "customer_transaction_made_to": self.transaction_made_to.strip(),
            "customer_plantypeid": self.plantypeid,
            "customer_planduerationid": self.plan_type,
            "customer_shiftid": self.shifts_selected,  # Pass multiple shift IDs as a list
            "customer_seatid": 1,
            "customer_planstartdate": self.transaction_startdate,
            "customer_planexpirydate": self.transaction_enddate,
            "customer_paymenttype": self.transaction_mode,
            "customer_isactive": 1
            # "is_locker": 1 if self.is_locker==True else 0
        }
        # print("Before --- > ",self.addmission_form_data)
        final = self.addmission_form_data.update(data)
        print("After --- > ",self.addmission_form_data)
        number = "918108236131"
        # try:
        if self.txn_of != "Admission":
            print("Inside only insert Full ")
            try:
                if self.transaction_type!="" and self.amount!="" and self.transaction_made_by!="" and self.transaction_mode!="" and self.txn_of!="" and self.transaction_made_for!="" and self.transaction_made_to!="":
                    res = create_transaction(txn_date=txn_date,
                                            transaction_type=self.transaction_type,
                                            amount=int(self.amount),
                                            txn_made_by=(self.transaction_made_by.lower()).strip(),
                                            payment_method=self.transaction_mode,
                                            transaction_for=self.txn_of.strip(),
                                            description=self.transaction_made_for.strip(),
                                            transaction_made_to= self.transaction_made_to.strip())
                    result = res.split(":")[0]
                    if result.strip()=="Pass":
                        utils.snack(color="green",text="Transaction Submitted Successfully!")
                        try:
                            msg = f"""
Transaction Type - OUT/Expense
Transaction Date - {txn_date}
Transaction Made By - {(self.transaction_made_by.lower()).strip()}
Transaction Made To - {self.transaction_made_to.strip()}
Amount - {self.amount}
Mode of Transaction - {self.transaction_mode}
Description - {self.transaction_made_for.strip()}

"""
                            send_messages(phone_numbers=number,message=msg)
                        except Exception as e:
                            utils.snack("red",f"{e}")

                        self.parent.change_screen("transactions")
                    else:
                        utils.snack(color="red",text= str(res.split(":")[1]))
                else:
                    utils.snack(color="red",text= "Please Fill all Fields..")
            except Exception as e:
                utils.snack("red",f"{e}")

        elif self.transaction_type!="" and self.amount!="" and self.transaction_made_by!="" and self.transaction_mode!="" and self.txn_of!="" and self.transaction_made_for!="" and self.transaction_made_to!="":
            print("Inside only insert Transaction ")
            if "customer_phone_number" in self.addmission_form_data:
                res = insert_addmission(self.addmission_form_data)
                print("Admission Result --> ",res)
                result = res.split(":")[0]
                if result.strip()=="Pass":
                    utils.snack(color="green",text="Admission Submitted Successfully!")
                    try:
                        # user_details = get_customers_details("phone_number",self.addmission_form_data['customer_phone_number'])
                        # user_id = user_details[0]['id']
                        # upload_image(self.addmission_form_data['customer_profile_image'],str(user_id))
                        # profile_url = get_profile_img(user_id)
                        # update_customer(self.addmission_form_data['customer_phone_number'],{"profile_image":f"{profile_url}"})
                        receipt_data = {
                            "customer_name": self.addmission_form_data['customer_name'],
                            "customer_phone_number": self.addmission_form_data['customer_phone_number'],

                            "customer_transaction_date": self.transaction_date,
                            "customer_transaction_id": int((res.split(":")[2]).strip()),
                            "customer_receiptid": str((res.split(":")[4]).strip()),
                            "customer_payment_method": self.transaction_mode,
                            "customer_amount": int(self.amount.strip()),

                            "customer_planstartdate": self.transaction_startdate,
                            "customer_planexpirydate": self.transaction_enddate,
                            "customer_shift": utils.get_shift_text(self.shifts_selected),
                            "customer_plantype": self.planTypeSelected
                        }
                        receipt_res = insert_receipt_data(receipt_data)
                        print("receipt Result --> ",receipt_res)
                        receipt_result = receipt_res.split(":")[0]
                        if receipt_result.strip()=="Pass":
                            utils.snack(color="green",text=receipt_res.split(":")[1])
                        else:
                            utils.snack(color="red",text=receipt_res.split(":")[1])

                        msg = f"""
ID - NG
Name - {self.addmission_form_data['customer_name']}
phone - {self.addmission_form_data['customer_phone_number']}
Shift - {utils.get_shift_text(self.shifts_selected)}
Payment mode - {self.transaction_mode}
Payment Amount- {self.amount.strip()}
Payment date - {utils.date_format(self.transaction_date)}
Joining Date - {utils.date_format(self.transaction_startdate)}
Subscription Expiry date - {utils.date_format(self.transaction_enddate)}
                """
                        send_messages(phone_numbers=number,message=msg)
                    except Exception as e:
                        utils.snack("red",f"{e}")

                    self.parent.change_screen("customers_list")
                else:
                    utils.snack(color="red",text=str(res.split(":")[1]))
            else:
                utils.snack(color="red",text="Admission form data not present.")
        else:
            utils.snack(color="red",text="Please fill app the details.")

        # print(data)
        # except:
        # print("Something went wrong please try after some time or contact admin.")
        
        # print(res)  # Replace this with actual form submission logic
