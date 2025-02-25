from main_imports import MDScreen,MDLabel,MDListItem,MDBoxLayout,StringProperty,MDListItemLeadingAvatar,MDListItemHeadlineText,MDListItemSupportingText,MDListItemTertiaryText
from libs.applibs import utils
from libs.applibs.supabase_db import *
from libs.applibs.loader import Dialog_cls

utils.load_kv("cutomers_list.kv")

class ListItems(MDListItem):
    custid = StringProperty()
    avatar_source = StringProperty()
    name = StringProperty()
    expiry_date = StringProperty()
    status = StringProperty()

class CustomersList(MDScreen):
    temp_list = []
    customer_list = []
    search_redirect = ""
    def on_enter(self):
        self.temp_list.clear()
    # Define the dialog
        # for x in range(38):
        #     self.ids.main_scroll.add_widget(self.create_list_item(email=str(x),avatar_source="assets/img/blank_profile.png"))
        loader = Dialog_cls()
        loader.open_dlg()
        query_customer_list = """
                            SELECT DISTINCT ON (c.id) 
                                c.id, 
                                c.name, 
                                c.email, 
                                c.created_at,
                                p.isactive, 
                                p.planstartdate, 
                                p.planexpirydate
                            FROM "Customers" c
                            JOIN "subscription"  p ON c.id = p.customerid::uuid
                            ORDER BY c.id, p.planstartdate DESC
                            """
        isinternet=utils.is_internet_available()
        if isinternet:
            customers=run_sql(query_customer_list)
        else:
            utils.snack("red","No Internet Connection..")
        if customers:
            self.customer_list = customers
            loader.close_dlg()
            print("Customers data -->",customers)
            for x in customers:
        
                list_item = {
                    "custid":x["id"],
                    "avatar_source":"assets/img/blank_profile.png",
                    "name":x["name"],
                    "expiry_date":utils.date_format(x["planexpirydate"]),
                    "status":"Active" if x["isactive"] == 1 else "Expired"
                }
                print("All Customers----->",(list_item))
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
        if self.search_redirect!="":
            self.set_list_items(self.search_redirect,True)
        else:
            self.set_list_items()
    def on_leave(self):
        self.search_redirect = ""
        self.ids.search_field.text = ""

        self.ids.rv.data = []
        self.set_list_items()
    def set_list_items(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_item(item):
            self.ids.rv.data.append(
                {
                    "viewclass": "ListItems",
                    "custid": item["custid"],
                    "avatar_source":item["avatar_source"],
                    "name":item["name"],
                    "expiry_date":item["expiry_date"],
                    "status":item["status"],
                    "callback": lambda x: self.get_text(item["custid"]),
                }
            )

        self.ids.rv.data = []
        for Name in self.temp_list:
            if search:
                if text in Name["name"].lower():
                    add_item(Name)
                elif text in Name["status"].lower():
                    add_item(Name)
            else:
                add_item(Name)
    
    
    def create_list_item(self, email, avatar_source):
        # Helper function to create a list item with a supporting text and avatar
        list_item = MDListItem(
            MDListItemLeadingAvatar(
                source=avatar_source,
            ),
            MDListItemHeadlineText(
                text= "Abhijit Shinde"
            ),
            MDListItemSupportingText(
                text="Joined On : "+str(email)+" Nov 2024",
            ),
            MDListItemTertiaryText(
                text="Active",
                theme_text_color="Custom",
                text_color="#3cb043"
            ),
            theme_bg_color="Custom",
            md_bg_color=self.theme_cls.transparentColor,
            on_release=lambda x: self.get_text(email)  # Pass email directly to the callback
        )
        return list_item

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
                customer_profile.join_date = str(utils.date_format(data[0]["planstartdate"]))
                customer_profile.expiry_date = str(utils.date_format(data[0]["planexpirydate"]))
                customer_profile.dob = str(utils.date_format(data[0]["dob"]))
                customer_profile.email = data[0]["email"]
                customer_profile.phone = data[0]["phone_number"]
                customer_profile.address = data[0]["address"]
                self.parent.change_screen("customer_profile")
            else:
                print("No data found.....")
        else:
            print("No Customer ID found...")
