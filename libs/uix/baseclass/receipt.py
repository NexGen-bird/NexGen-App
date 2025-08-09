from main_imports import MDScreen,MDCard,MDLabel,MDListItem,MDBoxLayout,NumericProperty,StringProperty,MDListItemLeadingAvatar,MDListItemHeadlineText,MDListItemSupportingText,MDListItemTertiaryText
from libs.applibs import utils
from libs.applibs.supabase_db import *
from libs.applibs.loader import Dialog_cls
from kivy.clock import Clock
import threading
import concurrent.futures
from functools import partial
import time
from libs.applibs.whatsapp import send_messages

utils.load_kv("receipt.kv")
class ReceiptSentItem(MDCard):
    id = StringProperty()
    created_at = StringProperty()
    transaction_id = StringProperty()
    receiptid = StringProperty()
    transaction_date = StringProperty()
    customer_name = StringProperty()
    customer_phone = StringProperty()
    shift = StringProperty()
    payment_mode = StringProperty()
    payment_amount = NumericProperty()
    joining_date = StringProperty()
    expiration_date = StringProperty()
    plantype = StringProperty()
    is_sent = NumericProperty()
    receipt_url = StringProperty()
    def whatsappmsg(self,receiptid,phone,url,name):
        final_message = f"""
Hi {name} 👋
Please find your receipt at the link below 👇🏻

Steps to download your receipt:
1. Click on the link
2. Enter your registered mobile number
3. View and download your receipt

📄 {url}

If you face any issues, feel free to reply to this message.
Thank you for choosing NexGen Self Study Center! 🙏
"""     
        whatsapp_number = "91"+str(phone)
        update_receipt_sent(receiptid)
        send_messages(whatsapp_number,final_message)
        Receipt().on_leave()
        Receipt().search_redirect = ""
        Receipt().ids.search_field.text = ""
        Receipt().active = False
        Receipt().fetch_data()

class ReceiptPendingItem(MDCard):
    id = StringProperty()
    created_at = StringProperty()
    transaction_id = StringProperty()
    receiptid = StringProperty()
    transaction_date = StringProperty()
    customer_name = StringProperty()
    customer_phone = StringProperty()
    shift = StringProperty()
    payment_mode = StringProperty()
    payment_amount = NumericProperty()
    joining_date = StringProperty()
    expiration_date = StringProperty()
    plantype = StringProperty()
    is_sent = NumericProperty()
    receipt_url = StringProperty()
    def whatsappmsg(self,receiptid,phone,url,name):
        final_message = f"""
Hi {name} 👋
Please find your receipt at the link below 👇🏻

Steps to download your receipt:
1. Click on the link
2. Enter your registered mobile number
3. View and download your receipt

📄 {url}

If you face any issues, feel free to reply to this message.
Thank you for choosing NexGen Self Study Center! 🙏
"""
        whatsapp_number = "91"+str(phone)
        update_receipt_sent(receiptid)
        send_messages(whatsapp_number,final_message)
        Receipt().on_leave()
        Receipt().search_redirect = ""
        Receipt().ids.search_field.text = ""
        Receipt().active = False
        Receipt().fetch_data()
      

class ListItems(MDListItem):
    custid = StringProperty()
    avatar_source = StringProperty()
    name = StringProperty()
    expiry_date = StringProperty()
    status = StringProperty()
    phone = StringProperty()

class Receipt(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = True
        self.api_thread = None
    temp_list = []
    temp_list1 = []
    customer_list = []
    sent_receipt_list = []
    search_redirect = ""
    base_url = ""
    def on_navbar_switch(self, bar, item, icon, text):
        self.ids.tab_content.current = text
    def load_data_from_apis(self):
        # don't run if screen is inactive
        if not self.active:
            print("active is ",self.active)
            return
        self.api_results = {}
        query_receipt_list = """
                            SELECT *
                            FROM receipts
                            WHERE is_sent = 0
                            ORDER BY transaction_date DESC
                            """
        query_receipt_sent_list = """
                            SELECT *
                            FROM receipts
                            WHERE is_sent = 1
                            ORDER BY transaction_date DESC
                            """
        api_tasks = {
            "receipts": partial(run_sql,query_receipt_list),
            "receipts_sent": partial(run_sql,query_receipt_sent_list),
        }

        results = {}
        login_with_email_password("abhijit.shinde@test.com","india@123")
        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            future_to_key = {
                executor.submit(func): key for key, func in api_tasks.items()
            }

            for future in concurrent.futures.as_completed(future_to_key):
                key = future_to_key[future]
                try:
                    results[key] = future.result()
                except Exception as e:
                    results[key] = f"Error: {str(e)}"

        self.api_results = results
        # Schedule UI update only if still active
        if self.active:
            Clock.schedule_once(self.update_ui)
    def update_ui(self,dt):
        customers = self.api_results['receipts']
        sent_receipt = self.api_results['receipts_sent']
        print(self.api_results)
        if customers:
            self.customer_list = customers
            self.loader.close_dlg()
            print("Customers data -->",customers)
            for x in customers:
        
                list_item = {
                    "id":str(x["id"]),
                    "created_at":x["created_at"],
                    "transaction_id":str(x["transaction_id"]),
                    "receiptid":x["receiptid"],
                    "transaction_date":utils.date_format(x["transaction_date"]),
                    "customer_name":x["customer_name"],
                    "customer_phone":x["customer_phone"],
                    "shift":x["shift"],
                    "payment_mode":x["payment_mode"],
                    "payment_amount":x["payment_amount"], 
                    "joining_date":utils.date_format(x["joining_date"]),
                    "expiration_date":utils.date_format(x["expiration_date"]),
                    "plantype":x["plantype"],
                    "is_sent":x["is_sent"],
                    "receipt_url": str(self.base_url)+"/receipt/"+str(x["receiptid"])    
                }
                # print("All Customers----->",(list_item))
                self.temp_list.append(list_item)
        else:
            no_data = MDBoxLayout(
                MDLabel(
                    text= "No Data Found",
                    halign= "center"
                )
                
            )
            self.ids.mainboxx.add_widget(no_data)
            utils.snack("red","No Pending Receipts found...")
        if sent_receipt:
            self.sent_receipt_list = sent_receipt
            self.loader.close_dlg()
            print("receipt sent data -->",sent_receipt)
            for x in sent_receipt:
        
                list_item1 = {
                    "id":str(x["id"]),
                    "created_at":x["created_at"],
                    "transaction_id":str(x["transaction_id"]),
                    "receiptid":x["receiptid"],
                    "transaction_date":utils.date_format(x["transaction_date"]),
                    "customer_name":x["customer_name"],
                    "customer_phone":x["customer_phone"],
                    "shift":x["shift"],
                    "payment_mode":x["payment_mode"],
                    "payment_amount":x["payment_amount"], 
                    "joining_date":utils.date_format(x["joining_date"]),
                    "expiration_date":utils.date_format(x["expiration_date"]),
                    "plantype":x["plantype"],
                    "is_sent":x["is_sent"],
                    "receipt_url": str(self.base_url)+"/receipt/"+str(x["receiptid"])     
                }
                self.temp_list1.append(list_item1)
        else:
            no_data = MDBoxLayout(
                MDLabel(
                    text= "No Data Found",
                    halign= "center"
                )
                
            )
            self.loader.close_dlg()
            self.ids.mainboxsv.add_widget(no_data)
            utils.snack("red","No Sent Receipts...")
        if self.search_redirect!="":
            self.set_list_items(self.search_redirect,True)
        else:
            self.set_list_items()
    def on_enter(self):
        receiptquery = """
SELECT receipt_baseurl
FROM app_settings
LIMIT 1
"""
        response = run_sql(receiptquery)
        self.base_url = str(response[0]["receipt_baseurl"])
        self.fetch_data()
        print("This is app settings base url --> ",self.base_url)
        
    def fetch_data(self):
        self.active = True
        self.temp_list.clear()
        self.temp_list1.clear()
        self.loader = Dialog_cls()
        self.loader.open_dlg()
        print("inside on enter")
        isinternet=utils.is_internet_available()
        if self.api_thread and self.api_thread.is_alive():
            print("Thread still running. Skipping new call.")
            return
        if isinternet:
            self.api_thread = threading.Thread(target=self.load_data_from_apis)
            self.api_thread.start()
        else:
            utils.snack("red","No Internet Connection..")
    
    def on_leave(self):
        self.search_redirect = ""
        self.ids.search_field.text = ""
        self.active = False
        self.ids.rv.data = []
        self.ids.sv.data = []
        self.set_list_items()
    def set_list_items(self, text="", search=False):
        '''Builds a list of icons for the screen MDIcons.'''

        def add_item(item,is_sent = True):
            
            (self.ids.rv.data if is_sent==False else self.ids.sv.data).append(
                {
                    "viewclass": "ReceiptPendingItem" if is_sent==False else "ReceiptSentItem",
                    
                    "id":str(item["id"]),
                    "created_at":item["created_at"],
                    "transaction_id":item["transaction_id"],
                    "receiptid":item["receiptid"],
                    "transaction_date":str(item["transaction_date"]),
                    "customer_name":item["customer_name"],
                    "customer_phone":item["customer_phone"],
                    "shift":item["shift"],
                    "payment_mode":item["payment_mode"],
                    "payment_amount":item["payment_amount"], 
                    "joining_date":str(item["joining_date"]),
                    "expiration_date":str(item["expiration_date"]),
                    "plantype":item["plantype"],
                    "is_sent":item["is_sent"],
                    "receipt_url":item["receipt_url"],
                    "callback": lambda x: print(item["receiptid"]),
                }
            )
            print({
                    "viewclass": "ReceiptPendingItem" if is_sent==False else "ReceiptSentItem",
                    
                    "id":str(item["id"]),
                    "created_at":item["created_at"],
                    "transaction_id":item["transaction_id"],
                    "receiptid":item["receiptid"],
                    "transaction_date":str(item["transaction_date"]),
                    "customer_name":item["customer_name"],
                    "customer_phone":item["customer_phone"],
                    "shift":item["shift"],
                    "payment_mode":item["payment_mode"],
                    "payment_amount":item["payment_amount"], 
                    "joining_date":str(item["joining_date"]),
                    "expiration_date":str(item["expiration_date"]),
                    "plantype":item["plantype"],
                    "is_sent":item["is_sent"],
                    "receipt_url":item["receipt_url"],
                    "callback": lambda x: print(item["receiptid"]),
                })
        self.ids.rv.data = []
        self.ids.sv.data = []
        for Name in self.temp_list1:
            add_item(Name)
        for Name in self.temp_list:
            if search:
                if text in Name["customer_name"].lower():
                    add_item(Name,False)
                # elif text in Name["status"].lower():
                #     add_item(Name)
            else:
                add_item(Name,False)

    