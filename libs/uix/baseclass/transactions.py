
from main_imports import MDScreen,MDCard,StringProperty,NumericProperty,MDIconButton,MDTextFieldTrailingIcon,MDTextFieldLeadingIcon,MDTextFieldHintText,MDFabButton,MDTextField
from libs.applibs import utils
from libs.applibs import utils,supabase_db as db
from libs.applibs.loader import Dialog_cls

utils.load_kv("transactions.kv")
class OverviewCards(MDCard):
    '''Implements a material card.'''

    cardlabel = StringProperty()
    amount = NumericProperty()
    color= StringProperty()
class CustomOneLineIconListItem(MDCard):
    Name = StringProperty()
    Date = StringProperty()
    txn_type = StringProperty()
    Amount = NumericProperty()
    Color = StringProperty()
class Transactions(MDScreen):
    usertype="Member"
    transaction_list = []
    profile_redirect = ""
    def on_pre_enter(self):
        print("start enter")
        loader = Dialog_cls()
        loader.open_dlg()
        print("L1 enter")
        response = db.get_transactionspagedata()
        if response:
            self.transaction_list = response
            loader.close_dlg()
            print("L2 enter")
        else:
            loader.close_dlg()
            print("L3 enter")
            utils.snack("red","Sorry could not get transactions")

    def on_enter(self):
        profit, expenses = db.get_expense_profit()
        box_layoput = self.ids.box
        if box_layoput.children:
            box_layoput.clear_widgets()
        self.ids.box.add_widget(
            OverviewCards(cardlabel="Expenses",amount=int(expenses),color="red")
        )
        self.ids.box.add_widget(
            OverviewCards(cardlabel="Profit",amount=int(profit),color="green")
        )
        self.ids.box.add_widget(
            MDFabButton(icon="plus",style= "standard", on_release=lambda x : self.parent.change_screen("addTxn"))
        )
        if self.profile_redirect != "":
            self.set_txns(self.profile_redirect,True)
        else:
            self.set_txns()

    def on_leave(self):
        self.profile_redirect = ""
        self.ids.rv.data = []
        self.set_txns()
    def change_lay(self):
        print("Inside Change lay")
        specific_widget = self.ids.get("search_btn")
        specific_widget.parent.remove_widget(specific_widget)
        # START Text field---------------------------------------------
        search_field = MDTextField(
            mode= "outlined",
            
        )

        # Adding a leading icon to the text field
        txt = MDTextFieldHintText(text="Search Transaction")
        leading_icon = MDTextFieldLeadingIcon(icon="magnify")
        trailing_icon = MDIconButton(icon= "alpha-x-circle",on_release=lambda x: self.remove_search())
        search_field.add_widget(txt)
        search_field.add_widget(leading_icon)

        # Bind the `text` property to the `set_txns` function
        search_field.bind(text=self.get_fieldtxt)
        # END Search field--------------------------------------------
        main_widget = self.ids.get("filters")
        self.ids.filters.ids['searchfield']=search_field
        main_widget.add_widget(search_field)
        self.ids.filters.ids['crossbtn']=trailing_icon
        main_widget.add_widget(trailing_icon)

        print("Inside Change lay 1")

    
    def get_fieldtxt(self, instance, value):
        # This function is triggered whenever the text changes
        print(f"Search Text: {value}")
        self.set_txns(text=value,search=True)     
        
    def set_txns(self, text="", search=False,txnfilter=False,sdate="",edate="",member="",txn_type=""):
        '''Builds a list of icons for the screen MDIcons.'''
        if text != "":
            text=text.lower()
        # print(len([sdate,edate,member,txn_type]))
        def add_txn(txn):
            self.ids.rv.data.append(
                {
                    "viewclass": "CustomOneLineIconListItem",
                    "Name": "No Name" if txn["name"]==None else txn["name"],                    
                    "Date":str(utils.date_format(txn["transaction_date"])),
                    "txn_type": txn["transaction_type"],
                    "Amount": int(txn["amount"]),
                    "Color": txn["color"] if txn["color"]!=None else "black",
                    "callback": lambda x: x,
                }
            )

        self.ids.rv.data = []
        if search:
            for txn in self.transaction_list:
                if text in ("No Name" if txn["name"]==None else txn["name"]).lower():
                    add_txn(txn)
                elif text in str(int(txn["amount"])):
                    add_txn(txn)
                elif text in txn["transaction_type"].lower():
                    add_txn(txn)
        elif txnfilter:
            ll =[]
            print(member,edate,sdate,txn_type)
            if member != "All" or edate != 32 or sdate != 32 or txn_type != "All":
                print("In if of txnfilter")
                for i in range(len(self.transaction_list)):
                    if(member == "All"):
                        if(sdate == 32):
                            if(txn_type == "All"):
                                ll.append(self.transaction_list[i])
                            elif(self.transaction_list[i]["txn_type"]==txn_type):
                                ll.append(self.transaction_list[i])
                        elif(self.transaction_list[i]["Date"]>=sdate and self.transaction_list[i]["Date"]<=edate):
                            if(txn_type == "All"):
                                ll.append(self.transaction_list[i])
                            elif(self.transaction_list[i]["txn_type"]==txn_type):
                                ll.append(self.transaction_list[i])
                    elif(member == self.transaction_list[i]["name"]):
                        if(sdate == 32):
                            if(txn_type == "All"):
                                ll.append(self.transaction_list[i])
                            elif(self.transaction_list[i]["txn_type"]==txn_type):
                                ll.append(self.transaction_list[i])
                        elif(self.transaction_list[i]["Date"]>=sdate and self.transaction_list[i]["Date"]<=edate):
                            if(txn_type == "All"):
                                ll.append(self.transaction_list[i])
                            elif(self.transaction_list[i]["txn_type"]==txn_type):
                                ll.append(self.transaction_list[i])
                print("List from filter -->",ll)
                for txn in ll:
                    add_txn(txn)
            else:
               print("In Else filter")
               for txn in self.transaction_list:
                add_txn(txn) 
        else:
            for txn in self.transaction_list:
                add_txn(txn)