from main_imports import MDScreen,MDLabel,MDListItem,MDBoxLayout,MDCard,StringProperty,MDListItemLeadingAvatar,MDListItemHeadlineText,MDListItemSupportingText,MDListItemTertiaryText
from libs.applibs import utils
from libs.applibs.supabase_db import *
from libs.applibs.loader import Dialog_cls

utils.load_kv("expired_sub.kv")

class SubcriptionCard(MDCard):
    id = StringProperty()
    name = StringProperty()
    startdate = StringProperty()
    expirydate = StringProperty()
    avatar_source=StringProperty()
    plan = StringProperty()
    shift = StringProperty()
    status = StringProperty()
    Color = StringProperty()
    seatid = StringProperty()

class EListItems(MDListItem):
    custid = StringProperty()
    avatar_source = StringProperty()
    name = StringProperty()
    Expired_on = StringProperty()
    status = StringProperty()

class ExpiredCustomersList(MDScreen):
    temp_list = []
    customer_list = []
    plan = {1:"Day",2:"Monthly",3:"Querterly",4:"Half Yearly",5:"Yearly"}
    shift = {1:"6am to 12pm",2:"12pm to 6pm",3:"6pm to 12am",4:"12am to 6am"}
    profile_redirect1 = ""
    def on_enter(self):
        self.temp_list.clear()
    # Define the dialog
        # for x in range(38):
        #     self.ids.main_scroll.add_widget(self.create_list_item(email=str(x),avatar_source="assets/img/blank_profile.png"))
        loader = Dialog_cls()
        loader.open_dlg()
        
        customers=get_subcriptionpagedata()
        
        if customers:
            self.customer_list = customers
            loader.close_dlg()
            print("Customers data -->",customers)
            for x in customers:
        
                list_item = {
                    "id":str(x["id"]),
                    "avatar_source":"assets/img/blank_profile.png",
                    "name":x["name"],
                    "planstartdate":utils.date_format(x["planstartdate"]),
                    "planexpirydate":utils.date_format(x["planexpirydate"]),
                    "planduerationid":self.plan[x["planduerationid"]],
                    "shiftid":self.shift[x["shiftid"]],
                    "seatid":str(x["seatid"]),
                    "status":"Active" if x["isactive"] == 1 else "Expired",
                    "color":x["color"]
                }
                print("All Customers E----->",(list_item))
                self.temp_list.append(list_item)
        else:
            no_data = MDBoxLayout(
                MDLabel(
                    text= "No Data Found",
                    halign= "center"
                )
                
            )
            loader.close_dlg()
            self.ids.mainbox.add_widget(no_data)
            utils.snack("red","No Customer Data found...")
        if self.profile_redirect1 != "":
            self.set_list_items(self.profile_redirect1,True)
            print("inside Search on enter...",self.profile_redirect1)
            # self.ids.search_field.text = self.profile_redirect1
        else:
            self.set_list_items()
    def on_leave(self):
        self.profile_redirect1 = ""
        self.ids.search_field.text = ""
        self.ids.rv.data = []
        self.set_list_items()
    def set_list_items(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''
        if text != "":
            text=text.lower()

        def add_item(item):
            
            self.ids.rv.data.append(
                {
                    "viewclass": "SubcriptionCard",
                    "id": item["id"],
                    "name":item["name"],
                    "avatar_source":item["avatar_source"],
                    "startdate":item["planstartdate"],
                    "expirydate":item["planexpirydate"],
                    "plan":item["planduerationid"],
                    "shift":item["shiftid"],
                    "seatid":item["seatid"],
                    "status":item["status"],
                    "Color":item["color"],
                    "callback": lambda x: self.get_text(item["custid"]),
                }
            )

        self.ids.rv.data = []
        for Name in self.temp_list:
            if search:
                if text in Name["name"].lower():
                    add_item(Name)
                elif text in Name["planstartdate"].lower():
                    add_item(Name)
                elif text in Name["planexpirydate"].lower():
                    add_item(Name)
                elif text in Name["shiftid"].lower():
                    add_item(Name)
                elif text in Name["status"].lower():
                    add_item(Name)
            else:
                add_item(Name)
    
    
    
    def get_text(self, id):
        # Print the email text when the list item is clicked
        print(f"Clicked item text: {id}")
        customer_profile = self.parent.get_screen("customer_profile")
        # customer_profile.customer_id = id
        
        query = f"""
                SELECT s.planstartdate, s.planexpirydate, c.*
                FROM "Customers" c
                LEFT JOIN subscription s
                ON c.id = s.customerid::uuid
                WHERE c.id = '{id}'
                ORDER BY s.planexpirydate DESC
                LIMIT 1
                """
        if id:
            print(query)
            isinternet=utils.is_internet_available()
            if isinternet:
                data =  run_sql(query)
            else:
                utils.snack("red","No Internet Connection..")
            print("Customer data --- >",data)
            if data:
                customer_profile.username = data[0]["name"]
                customer_profile.join_date = data[0]["planstartdate"]
                customer_profile.expiry_date = data[0]["planexpirydate"]
                customer_profile.dob = data[0]["dob"]
                customer_profile.email = data[0]["email"]
                customer_profile.phone = data[0]["phone_number"]
                customer_profile.address = data[0]["address"]
                self.parent.change_screen("customer_profile")
            else:
                print("No data found.....")
        else:
            print("No Customer ID found...")
