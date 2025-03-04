
from main_imports import MDScreen,MDApp,MDRelativeLayout,MDButtonIcon,FitImage,MDDialog,MDDialogHeadlineText,MDDialogContentContainer,MDWidget,MDLabel,MDListItemHeadlineText,MDListItemSupportingText,NumericProperty, dp,StringProperty,MDCard,MDIconButton,MDListItemLeadingAvatar,BoxLayout,MDButton,MDButton,BoxLayout,MDListItem
from libs.applibs import utils
from kivy.clock import Clock
from datetime import datetime
from libs.applibs.supabase_db import *
from libs.applibs.loader import Dialog_cls
from libs.applibs.whatsapp import send_messages






utils.load_kv("dash.kv")
class Item(MDListItem):
    divider = None
    source = StringProperty()

class LandingScreen(MDScreen):
    app = MDApp.get_running_app()
    total_members = StringProperty()
    expired_count = StringProperty()
    active_members = StringProperty()
    collection_amount = StringProperty()
    expense_amount = StringProperty()
    pnl_amount = StringProperty()
    morning= StringProperty()
    afternoon= StringProperty()
    evening= StringProperty()
    night= StringProperty()
    shifts = {"morning": "45", "afternoon": "45", "evening": "45","night":"45"}
    dialog = None
    
    
    def on_pre_enter(self):
        self.loader = Dialog_cls()
        self.loader.open_dlg()
        shiftwiseactivecount = """
                                SELECT CONCAT('Shift',shiftid, ':', 45-COUNT(DISTINCT seatid)) as count
                                FROM subscription
                                WHERE isactive = 1  -- Filter for active subscriptions
                                GROUP BY shiftid
                                """
        isinternet=utils.is_internet_available()
        if isinternet:
            shiftcount = run_sql(shiftwiseactivecount)
            if shiftcount:
                # Mapping shift names to dictionary keys
                shift_mapping = {
                    "Shift1": "morning",
                    "Shift2": "afternoon",
                    "Shift3": "evening",
                    "Shift4": "night"
                }

                # Update shifts from shiftcount
                for x in shiftcount:
                    shift, count = x['count'].split(":")
                    if shift in shift_mapping:
                        self.shifts[shift_mapping[shift]] = count
                print(self.shifts)
        else:
            utils.snack("red","No Internet Connection..")
       
        
    def on_enter(self):
        # pass
        # Schedule the carousel to move automatically every 3 seconds
        # Clock.schedule_interval(self.switch_slide, 5)
        # self.populate_subscription_list()
        # self.refresh_data()
        # self.add_txn_list()

        customer_count_query = """
                                select count(*)
                                from "Customers"
                                """
        isinternet=utils.is_internet_available()
        if isinternet:
            customer_count = run_sql(customer_count_query)
        else:
            utils.snack("red","No Internet Connection..")
        # print("customer count ---->" ,customer_count[0])
        if customer_count:
            self.total_members = str("0" if customer_count[0]['count']==None else customer_count[0]['count'])
        collection_query = """SELECT 
    SUM(CASE WHEN transaction_type = 'IN' THEN amount ELSE 0 END) AS total_revenue,
    SUM(CASE WHEN transaction_type = 'OUT' THEN amount ELSE 0 END) AS total_expenses
        FROM "Transactions"
        """
        isinternet=utils.is_internet_available()
        if isinternet:
            collection = run_sql(collection_query)
        else:
            utils.snack("red","No Internet Connection..")
            
        if collection:
            self.collection_amount = str("0" if collection[0]['total_revenue']==None else "{}{}".format("₹", utils.format_number(float(collection[0]["total_revenue"]))))
            self.expense_amount = str("0" if collection[0]['total_expenses']==None else "{}{}".format("₹",utils.format_number(float(collection[0]["total_expenses"]))))
        active_members_query = """select count(distinct customerid)
                                from subscription
                                where isactive=1
                                """
        isinternet=utils.is_internet_available()
        if isinternet:
            active_members = run_sql(active_members_query)
        else:
            utils.snack("red","No Internet Connection..")
        if active_members:
            self.active_members = str("0" if active_members[0]['count']==None else active_members[0]['count'])
        month_start,month_end = utils.get_previous_month_range()
        self.pnl_amount = str(0 if get_net_profit(month_start,month_end)==None else utils.format_number(float(get_net_profit(month_start,month_end))))
        
        self.ids.morningshift.text = self.shifts['morning']
        self.ids.afternoonshift.text = self.shifts['afternoon']
        self.ids.eveningshift.text = self.shifts['evening']
        self.ids.nightshift.text = self.shifts['night']
        
        exp_members_query = """SELECT DISTINCT ON (c.id) 
                                    c.id, 
                                    c.name,
                                    c.phone_number, 
                                    p.planstartdate,
                                    p.planexpirydate
                                FROM "Customers" c
                                INNER JOIN "subscription"  p ON c.id = p.customerid
                                where p.planexpirydate >= current_date
                                """
        expired_count = """
                        select count(distinct customerid)
                        from subscription
                        where isactive=0 and customerid not in (select distinct customerid
                        from subscription
                        where isactive=1)
                        """
        isinternet=utils.is_internet_available()
        if isinternet:
            expired_count = run_sql(expired_count)
            self.expired_count = str("0" if expired_count[0]['count']==None else expired_count[0]['count'])
        else:
            utils.snack("red","No Internet Connection..")
       
        isinternet=utils.is_internet_available()
        if isinternet:
            expiring_members = run_sql(exp_members_query)
        else:
            utils.snack("red","No Internet Connection..")
        if expiring_members:
            sorted_data = sorted(expiring_members, key=lambda x: datetime.strptime(x['planexpirydate'], "%Y-%m-%d"), reverse=False)
            for x in sorted_data:
                self.expCard(name=x['name'],expdate=x['planexpirydate'],phone=x['phone_number'])
        else:
            self.ids.mainboxx.add_widget(MDLabel(
                    adaptive_size=True,
                    pos_hint={"center_x": 0.5, "center_y": 0.5},
                    text="No Expiring Subcriptions.",
                    allow_selection=True,
                    padding=("4dp", "4dp"),
                ))
        
        self.loader.close_dlg()
    def availble_seats_popup(self):
        # Create and open the dialog with clickable items
        try:
            shift_info = {
                        "Double Shift": 35,
                        "Flexi Shift": 7,
                        "Single Shift": 10,
                        "Ultimate Shift": 5
                    }
            total_seats = "37"
        except:
            print("Facing issue while accessing Firebase")
        self.GV = MDDialogContentContainer(orientation="vertical",)
        for shift, seats in shift_info.items():
            # MDButton(text=f"{shift}: {seats} seats available", halign="center")
            self.GV.add_widget(Item(MDListItemHeadlineText(text=f"{shift}: {int(total_seats)-int(seats)} seats available"), source="assets/img/clock_11513341.png"))

        
        if self.dialog == None: 
            self.dialog = MDDialog(
                
                MDDialogHeadlineText(text="Available Seats"),
                self.GV,
                
            )
            self.dialog.theme_bg_color="Custom"
            self.dialog.md_bg_color="#fcfbff"
            self.dialog.open()
        else:
            self.dialog.dismiss()
            self.dialog = MDDialog(
                
                MDDialogHeadlineText(text="Available Seats"),
                self.GV,
                
            )
            self.dialog.theme_bg_color="Custom"
            self.dialog.md_bg_color="#fcfbff"
            self.dialog.open()

    def item_clicked(self):
        # print("This is Good :: ",item_text)
        self.dialog.dismiss()
        self.parent.change_screen("seat")
    def expCard(self,name,expdate,phone,img="assets/img/blank_profile.png"):
        phone_no = "91"+str(phone)
        msg = f"""
Hi {name},

This is a reminder that your NexGen Study Center subscription is expiring on *{utils.date_format(expdate)}*.

To avoid any interruption in your study schedule, please renew your subscription at the earliest.

You can reply to this message or contact us directly for assistance.

Thank you for choosing NexGen Study Center!

Best regards,
NexGen Study Center Team"""
        card = MDCard(
                orientation="horizontal",
                elevation= .8,
                size_hint= (None, None),
                size= (dp(350), dp(100)),
                padding= "10dp",
                spacing = "5dp",
                pos_hint= {"center_x": 0.5},
                radius= [20, 20, 20, 20],
                theme_bg_color= "Custom",
                md_bg_color= "#FFFFFF",
                style= "elevated",
                # md_bg_color= utils.get_background_color(expdate)
            )

        # Profile image
        profile_image = FitImage(
            source=img,  # Image URL from data
            # size_hint_y=None,
            # height="80dp",

            size_hint= (None, None),
            size= (dp(60), dp(60)),
            radius= [self.width/2,],
            pos_hint= {"center_y": 0.5},
        )
        main = MDRelativeLayout()
        # Name and Date labels
        name=name
        name_label = MDLabel(
            text=name[:25]+".." if len(name)>25 else name,
            theme_text_color="Primary",
            halign="left",
            adaptive_size= True,
            height="24dp",
            font_style="Title",
            role="medium",
            pos_hint= {"center_y": 0.6,"x": 0.3}
        )
        date_label = MDLabel(
            text=utils.date_format(expdate),
            theme_text_color="Custom",
            text_color= utils.get_background_color(expdate),
            halign="center",
            adaptive_size= True,
            height="20dp",
            font_style="Title",
            role="medium",
            pos_hint= {"center_y": 0.2,"right": 1}
        )
        whatsapp = MDIconButton(
                    icon="whatsapp",
                    style= "standard",
                    pos_hint={"top": 1, "right": 1},
                    on_release=lambda x: send_messages(phone_numbers=phone_no, message=msg))
        # Add widgets to the card
        main.add_widget(profile_image)
        main.add_widget(whatsapp)
        main.add_widget(name_label)
        main.add_widget(date_label)
        card.add_widget(main)
        self.ids.mainboxx.add_widget(card)
        self.ids.mainboxx.add_widget(MDWidget(
            size_hint_y= None,
            height= "5dp",
        ))
    



    def on_leave(self):
       self.ids.mainboxx.clear_widgets()
        

    def switch_slide(self, dt):
        # Move to the next slide
        carousel = self.ids.performance_carousel
        carousel.load_next(mode='next')

    def populate_subscription_list(self):
        # Example data for users whose subscriptions are expiring
        subscriptions = [
            {"name": "John Doe", "profile": "assets/img/blank_profile.png", "expiry_date": "31 Oct 2024", "expired": False},
            {"name": "Jane Smith", "profile": "assets/img/blank_profile.png", "expiry_date": "18 Oct 2024", "expired": True},
            {"name": "Alex Johnson", "profile": "assets/img/blank_profile.png", "expiry_date": "01 Nov 2024", "expired": False}
        ]
        
        for subscription in subscriptions:
            self.add_subscription_item(subscription)

    def add_subscription_item(self, subscription):
        # Format date for comparison
        expiry_date = datetime.strptime(subscription['expiry_date'], "%d %b %Y")
        current_date = datetime.now()

        # Create a new list item
        list_item = MDListItem(MDListItemHeadlineText(text=subscription['name']),
                               MDListItemSupportingText(text =f"Expiry Date: {subscription['expiry_date']}")
            )

        # Change color to red if the expiry date is in the past
        if expiry_date < current_date:
            list_item.secondary_theme_text_color = "Custom"
            list_item.secondary_text_color = (1, 0, 0, 1)  # Red color for expired dates

        # Add the profile picture as circular
        profile_image = MDListItemLeadingAvatar(source=subscription['profile'])
        profile_image.radius = [profile_image.height / 2]  # Circular image
        list_item.add_widget(profile_image)

        # # If the subscription is expired, add a cross button to remove the item
        # if subscription['expired']:
        #     delete_button = IconRightWidget(icon="close", on_release=lambda x: self.remove_subscription_item(list_item))
        #     list_item.add_widget(delete_button)

        # Add the item to the subscription list
        self.ids.subscription_list.add_widget(list_item)
    def remove_subscription_item(self, list_item):
        # Remove the selected list item
        self.ids.subscription_list.remove_widget(list_item)
        utils.snack(color="green",text="Subscription removed.").open()

    # def show_seat_popup(self):
        # Seat information for each shift
        # shift_info = db.child("shift_seats").get().val()

        # # Layout for the popup content
        # content = BoxLayout(orientation="vertical")
        # for shift, seats in shift_info.items():
        #     content.add_widget(
        #         MDButton(text=f"{shift}: {seats} seats available", halign="center")
        #     )

    #     # Popup Dialog
    #     dialog = MDDialog(
    #         title="Shift-wise Available Seats",
    #         type="custom",
    #         content_cls=content,
    #         buttons=[
    #             MDButton(text="Close", on_release=lambda x: dialog.dismiss())
    #         ],
    #     )
    #     dialog.open()

    def update_seat_count(self):
        # Fetch the total number of available seats from Firebase
        total_seats = "37"
        self.ids.available_seats.text = str(total_seats)

    def update_expiring_subscriptions(self):
        # Fetch expiring subscriptions from Firebase
        subscriptions_list = {
                "Abhijit Shinde": "2024-11-05",
                "Jane Smith": "2024-11-03",
                "John Doe": "2024-11-01"
            }

        # Clear any existing subscription list
        self.ids.subscription_list.clear_widgets()

        # Add subscriptions to the list
        for name, expiry_date in subscriptions_list.items():
            self.ids.subscription_list.add_widget(
                MDListItem(MDListItemHeadlineText(text=f"{name} - Expires on {expiry_date}"))
            )
    
    def show_shift_popup(self):
        # Example data for available sits per shift from Firebase
        shift_info = {
            "Single Shift": "4" or 37,
            "Double Shift": "30" or 37,
            "Ultimate Shift": "4" or 37,
            "Flexi Shift": "11" or 37
        }

        # Layout for the shift cards inside the popup
        shift_cards_layout = BoxLayout(orientation="vertical", spacing="10dp")
        
        for shift, sits in shift_info.items():
            # Create a small card for each shift
            card = MDCard(
                orientation="horizontal",
                size_hint=(None, None),
                height="50dp",
                width=self.width * 0.85,
                padding="10dp",
                md_bg_color="#ed991f"  # Update with your theme color
            )
            

            # Right arrow button for navigation
            right_arrow = MDIconButton(
                icon="arrow-right",
                size_hint=(0.2, None),
                height="40dp",
                on_release=lambda x: self.redirect_to_future_page()  # Currently redirects to landing page
            )
            card.add_widget(right_arrow)

            shift_cards_layout.add_widget(card)

        # Create and show the dialog
        self.dialog = MDDialog(
            title="Shift-wise Available Seats",
            type="custom",
            content_cls=shift_cards_layout,
            buttons=[
                MDButton(
                    text="Close",
                    on_release=self.close_shift_popup
                )
            ],
            size_hint=(None, None),
            width=self.width * 0.85,
            height= self.content_cls * 0.85
            # height=min(self.height, 450)
        )
        self.dialog.open()

    def close_shift_popup(self, *args):
        if self.dialog:
            self.dialog.dismiss()

    def redirect_to_future_page(self):
        # Currently redirects to the landing page but can be updated for future page
        self.manager.current = "landing"

    def refresh_data(self):
        # This method is called when user pulls down from top to refresh data
        self.refresh_shift_data()
        # self.populate_subscription_list()  # Refresh subscription list if needed
        Clock.schedule_once(self.refresh_complete, 2)  # Simulate refresh delay

    def rediret_expired_customer(self):
        self.parent.get_screen("customers_list").search_redirect = "expired"
        self.parent.change_screen("customers_list")
    def refresh_complete(self, dt):
        # Notify the RefreshLayout that the refresh is done
        self.ids.refresh_layout.refresh_done()  # This will stop the loading indicator
    def add_txn(self,txn):
            self.ids.rv.data.append(
                {
                    "viewclass": "RecentTxn",
                    "Name": txn["name"],                    
                    "Date":txn["Date"],
                    "txn_type": txn["txn_type"],
                    "Amount": txn["Amount"],
                    "callback": lambda x: x,
                }
            )
            