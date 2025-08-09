
from main_imports import MDScreen,MDApp,Window,MDRelativeLayout,MDButtonIcon,FitImage,MDDialog,MDDialogHeadlineText,MDDialogContentContainer,MDWidget,MDLabel,MDListItemHeadlineText,MDListItemSupportingText,NumericProperty, sp,dp,StringProperty,MDCard,MDIconButton,MDListItemLeadingAvatar,BoxLayout,MDButton,MDButton,BoxLayout,MDListItem
from libs.applibs import utils
from datetime import datetime
from libs.applibs.supabase_db import *
from libs.applibs.loader import Dialog_cls
from libs.applibs.whatsapp import send_messages
from kivy.clock import Clock
import threading
import concurrent.futures
from functools import partial
from datetime import datetime
from libs.applibs.dualbarchart import  AKDualBarChart


utils.load_kv("dashboard.kv")
class Item1(MDListItem):
    divider = None
    source = StringProperty()

class ExpItemcard(MDCard):
    id = StringProperty()
    name = StringProperty()
    expdate = StringProperty()
    phone = StringProperty()
    img = "assets/img/blank_profile.png" #StringProperty()
    expcolor = list()
    msg = StringProperty()
    def getcolor(self,date):
        val = utils.get_background_color(date)
        return val
    def whatsappmsg(self,phone,msg):
        send_messages(phone,msg)
class LandingScreen1(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = True
        self.api_thread = None
    app = MDApp.get_running_app()
    total_members = StringProperty()
    expired_count = StringProperty()
    active_members = StringProperty()
    collection_amount = StringProperty()
    collection_amount_absolute = StringProperty()
    expense_amount = StringProperty()
    expense_amount_absolute = StringProperty()
    net_pnl = StringProperty()
    net_pnl_absolute = StringProperty()
    pnl_amount = StringProperty()
    pnl_amount_absolute = StringProperty()
    morning= StringProperty()
    afternoon= StringProperty()
    evening= StringProperty()
    night= StringProperty()
    weekend= StringProperty()
    shifts = {"morning": "45", "afternoon": "45", "evening": "45","night":"45","weekend":"20"}
    dialog = None
    api_results = []
    val1 = ""
    val2 = ""
    chart_month = []
    chart_values = []
    admission_chart_month = []
    admission_chart_values = []
    def load_data_from_apis(self):
        # don't run if screen is inactive
        if not self.active:
            return
        self.api_results = {}
        weekend_ppl_count = """
                            SELECT 20-COUNT(DISTINCT customerid) as count
                            FROM subscription
                            WHERE isactive = 1 and planstartdate <= current_date and planduerationid = 6
                            """
        shiftwiseactivecount = """
                                SELECT CONCAT('Shift',shiftid, ':', 45-COUNT(DISTINCT seatid)) as count
                                FROM subscription
                                WHERE isactive = 1 and planstartdate <= current_date and planduerationid != 6-- Filter for active subscriptions
                                GROUP BY shiftid
                                """
        collection_query = """SELECT 
    SUM(CASE WHEN transaction_type = 'IN' THEN amount ELSE 0 END) AS total_revenue,
    SUM(CASE WHEN transaction_type = 'OUT' THEN amount ELSE 0 END) AS total_expenses
        FROM "Transactions"
        """
        active_members_query = """select count(distinct customerid)
                                from subscription
                                where isactive=1
                                """
        exp_members_query = """SELECT DISTINCT ON (c.id) 
                                    c.id, 
                                    c.name,
                                    c.phone_number, 
                                    p.planstartdate,
                                    p.planexpirydate,
                                    c.profile_image
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
        month_start,month_end = utils.get_current_period_range()
        print("This is dates ---> ",month_start,month_end)
        api_tasks = {
            "shiftcount": partial(run_sql,shiftwiseactivecount),
            "weekendcount": partial(run_sql,weekend_ppl_count),
            "collection": partial(run_sql,collection_query),
            "active_members": partial(run_sql,active_members_query),
            "pnl_amount": partial(get_net_profit,month_start,month_end),
            "expired_count": partial(run_sql,expired_count),
            "expiring_members": partial(run_sql,exp_members_query),
        }

        results = {}
        login_with_email_password("abhijit.shinde@test.com","india@123")
        # with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        #     future_to_key = {
        #         executor.submit(func): key for key, func in api_tasks.items()
        #     }

        #     for future in concurrent.futures.as_completed(future_to_key):
        #         key = future_to_key[future]
        #         try:
        #             results[key] = future.result()
        #         except Exception as e:
        #             results[key] = f"Error: {str(e)}"

        # New Logic ------
        for key, func in api_tasks.items():
            try:
                results[key] = func()
            except Exception as e:
                results[key] = f"Error: {str(e)}"
        self.api_results = results
        # Schedule UI update only if still active
        if self.active:
            Clock.schedule_once(self.update_ui)

    def update_ui(self,dt):
        shiftcount = self.api_results['shiftcount']
        weekendcount = self.api_results['weekendcount']
        collection = self.api_results['collection']
        active_members = self.api_results['active_members']
        pnl_amount = self.api_results['pnl_amount']
        expired_count = self.api_results['expired_count']
        expiring_members = self.api_results['expiring_members']
        print(self.api_results)
        try:
            if weekendcount:# weekend batch available seats
                    print("Weekend batch --> ",weekendcount[0]['count'])
                    self.shifts["weekend"] = str(weekendcount[0]['count'])
                    
            if shiftcount:# 1st, 2nd, 3rd, 4th shift availble seats
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
            self.ids.morningshift.text = self.shifts['morning']
            self.ids.afternoonshift.text = self.shifts['afternoon']
            self.ids.eveningshift.text = self.shifts['evening']
            self.ids.nightshift.text = self.shifts['night']
            self.ids.weekend.text = self.shifts['weekend']
            if collection:
                self.collection_amount = str("0" if collection[0]['total_revenue']==None else "{}{}".format("₹", utils.format_number(float(collection[0]["total_revenue"]))))
                self.collection_amount_absolute = str("0" if collection[0]['total_revenue']==None else "{}{}".format("₹", collection[0]["total_revenue"]))
                self.expense_amount = str("0" if collection[0]['total_expenses']==None else "{}{}".format("₹",utils.format_number(float(collection[0]["total_expenses"]))))
                self.expense_amount_absolute = str("0" if collection[0]['total_expenses']==None else "{}{}".format("₹",collection[0]["total_expenses"]))
                self.net_pnl ="{}{}".format("₹", utils.format_number(float(int(0 if collection[0]['total_revenue']==None else collection[0]['total_revenue']) - int(0 if collection[0]['total_expenses']==None else collection[0]['total_expenses']))))        
                self.net_pnl_absolute ="{}{}".format("₹", int(0 if collection[0]['total_revenue']==None else collection[0]['total_revenue']) - int(0 if collection[0]['total_expenses']==None else collection[0]['total_expenses']))      
            
            if active_members:
                self.active_members = str("0" if active_members[0]['count']==None else active_members[0]['count'])
            
            self.pnl_amount = str(0 if pnl_amount==None else utils.format_number(float(pnl_amount)))
            self.pnl_amount_absolute = str("{}{}".format("₹",0 if pnl_amount==None else pnl_amount))
            

            self.expired_count = str("0" if expired_count[0]['count']==None else expired_count[0]['count'])
            if expiring_members:
                sorted_data = sorted(expiring_members, key=lambda x: datetime.strptime(x['planexpirydate'], "%Y-%m-%d"), reverse=False)
                for x in sorted_data:
                    self.expCard(id=x['id'],name=x['name'],expdate=x['planexpirydate'],phone=x['phone_number'],img=x['profile_image'])
            else:
                self.ids.mainboxx.add_widget(MDLabel(
                        adaptive_size=True,
                        pos_hint={"center_x": 0.5, "center_y": 0.5},
                        text="No Expiring Subcriptions.",
                        allow_selection=True,
                        padding=("4dp", "4dp"),
                    ))
        except:
            print("Issue in API or while UI loading..")
        end_time = datetime.now()
        print("Start time --->",self.start_time)
        print("End time --->",end_time)
        print("time to complete api  --->",end_time-self.start_time)

        # collection vs Expenses Chart Details
        chart_data = get_chart_data()
        if chart_data: 
            for i in chart_data:
                self.chart_month.append(i['month'])
                self.chart_values.append([i['collection'],i['expense']])
            chart = self.ids.chart
            print(f"Chart ANimation {chart.anim}")
            # self.chart_month.clear()
            # self.chart_values.clear()
            if self.chart_values and self.chart_month:
                chart.height = "280dp"
                chart.x_values= self.chart_month  # Numeric values
                chart.y_values= self.chart_values
                chart.current_bar_color=[0.2, 0.6, 1, 1]
                chart.previous_bar_color=[1, 0.5, 0.2, 1]
            else:
                self.ids.collection_summary.clear_widgets()
                chart.height = "0dp"

        else:
            chart = self.ids.chart
            self.ids.collection_summary.clear_widgets()
            chart.height = "0dp"
            print("Collection chart is Null")

        # Admission and reAdmissions chart
        chart_readmission_data = get_admission_chart_data() 
        if chart_readmission_data:
            for i in chart_readmission_data:
                self.admission_chart_month.append(i['month_label'])
                self.admission_chart_values.append([i['new_admissions'],i['readmissions']])
            print(f"Admission chart data MONTH --> {self.admission_chart_month}")
            print(f"Admission chart data Value --> {self.admission_chart_values}")
            chart_readmission = self.ids.chart_readmission
            if self.admission_chart_month and self.admission_chart_values:
                chart_readmission.height = "280dp"
                chart_readmission.x_values= self.admission_chart_month  # Numeric values
                chart_readmission.y_values= self.admission_chart_values
                chart_readmission.current_bar_color=[0.2, 0.6, 1, 1]
                chart_readmission.previous_bar_color=[1, 0.5, 0.2, 1]
            else:
                chart_readmission = self.ids.chart_readmission
                self.ids.admission_summary.clear_widgets()
                chart_readmission.height = "0dp"
        else:
            chart_readmission = self.ids.chart_readmission
            self.ids.admission_summary.clear_widgets()
            chart_readmission.height = "0dp"

        
        self.loader.close_dlg()
        
    def on_pre_enter(self):
        pass
       
        
    def on_enter(self):
        self.active = True
        self.loader = Dialog_cls()
        self.loader.open_dlg()
        self.start_time=datetime.now()
        isinternet=utils.is_internet_available()

        if self.api_thread and self.api_thread.is_alive():
            print("Thread still running. Skipping new call.")
            return
        if isinternet:
            self.api_thread = threading.Thread(target=self.load_data_from_apis)
            self.api_thread.start()
        else:
            utils.snack("red","No Internet Connection..")
        
        
        # pass
        # customer_count_query = """
        #                         select count(*)
        #                         from "Customers"
        #                         """
        # isinternet=utils.is_internet_available()
        # if isinternet:
            # customer_count = run_sql(customer_count_query)
        # else:
        #     utils.snack("red","No Internet Connection..")
        # print("customer count ---->" ,customer_count[0])
        # if customer_count:
        #     self.total_members = str("0" if customer_count[0]['count']==None else customer_count[0]['count'])
    #     collection_query = """SELECT 
    # SUM(CASE WHEN transaction_type = 'IN' THEN amount ELSE 0 END) AS total_revenue,
    # SUM(CASE WHEN transaction_type = 'OUT' THEN amount ELSE 0 END) AS total_expenses
    #     FROM "Transactions"
    #     """
    #     isinternet=utils.is_internet_available()
    #     if isinternet:
    #         collection = run_sql(collection_query)
    #     else:
    #         utils.snack("red","No Internet Connection..")
            
    #     if collection:
    #         self.collection_amount = str("0" if collection[0]['total_revenue']==None else "{}{}".format("₹", utils.format_number(float(collection[0]["total_revenue"]))))
    #         self.expense_amount = str("0" if collection[0]['total_expenses']==None else "{}{}".format("₹",utils.format_number(float(collection[0]["total_expenses"]))))
    #         self.net_pnl ="{}{}".format("₹", utils.format_number(float(int(0 if collection[0]['total_revenue']==None else collection[0]['total_revenue']) - int(0 if collection[0]['total_expenses']==None else collection[0]['total_expenses']))))        
        
    #     active_members_query = """select count(distinct customerid)
    #                             from subscription
    #                             where isactive=1
    #                             """
    #     isinternet=utils.is_internet_available()
    #     if isinternet:
    #         active_members = run_sql(active_members_query)
    #     else:
    #         utils.snack("red","No Internet Connection..")
    #     if active_members:
    #         self.active_members = str("0" if active_members[0]['count']==None else active_members[0]['count'])
    #     month_start,month_end = utils.get_current_period_range()
    #     self.pnl_amount = str(0 if get_net_profit(month_start,month_end)==None else utils.format_number(float(get_net_profit(month_start,month_end))))
        
    #     self.ids.morningshift.text = self.shifts['morning']
    #     self.ids.afternoonshift.text = self.shifts['afternoon']
    #     self.ids.eveningshift.text = self.shifts['evening']
    #     self.ids.nightshift.text = self.shifts['night']
    #     self.ids.weekend.text = self.shifts['weekend']
        
    #     exp_members_query = """SELECT DISTINCT ON (c.id) 
    #                                 c.id, 
    #                                 c.name,
    #                                 c.phone_number, 
    #                                 p.planstartdate,
    #                                 p.planexpirydate,
    #                                 c.profile_image
    #                             FROM "Customers" c
    #                             INNER JOIN "subscription"  p ON c.id = p.customerid
    #                             where p.planexpirydate >= current_date
    #                             """
    #     expired_count = """
    #                     select count(distinct customerid)
    #                     from subscription
    #                     where isactive=0 and customerid not in (select distinct customerid
    #                     from subscription
    #                     where isactive=1)
    #                     """
    #     isinternet=utils.is_internet_available()
    #     if isinternet:
    #         expired_count = run_sql(expired_count)
    #         self.expired_count = str("0" if expired_count[0]['count']==None else expired_count[0]['count'])
    #     else:
    #         utils.snack("red","No Internet Connection..")
       
    #     isinternet=utils.is_internet_available()
    #     if isinternet:
    #         expiring_members = run_sql(exp_members_query)
    #     else:
    #         utils.snack("red","No Internet Connection..")
    #     if expiring_members:
    #         sorted_data = sorted(expiring_members, key=lambda x: datetime.strptime(x['planexpirydate'], "%Y-%m-%d"), reverse=False)
    #         for x in sorted_data:
    #             self.expCard(id=x['id'],name=x['name'],expdate=x['planexpirydate'],phone=x['phone_number'],img=x['profile_image'])
    #     else:
    #         self.ids.mainboxx.add_widget(MDLabel(
    #                 adaptive_size=True,
    #                 pos_hint={"center_x": 0.5, "center_y": 0.5},
    #                 text="No Expiring Subcriptions.",
    #                 allow_selection=True,
    #                 padding=("4dp", "4dp"),
    #             ))
        # end_time = datetime.now()
        # print("Start time --->",self.start_time)
        # print("End time --->",end_time)
        # print("time to complete api  --->",end_time-self.start_time)
        
        # self.loader.close_dlg()
    
    def expCard(self,id,name,expdate,phone,img=""):
        # if img == "":
        img = "assets/img/blank_profile.png"
        # img = search_profile_img(str(id))
        phone_no = "91"+str(phone)
        msg = f"""
Hi {name},

This is a reminder that your NexGen Study Center subscription is expiring on *{utils.date_format(expdate)}*.

To avoid any interruption in your study schedule, please renew your subscription at the earliest.

You can reply to this message or contact us directly for assistance.

Thank you for choosing NexGen Study Center!

Best regards,
NexGen Study Center Team"""
        
        self.ids.rv.data.append(
                {
                    "viewclass": "ExpItemcard",
                    "id": id,
                    "name": name[:25]+".." if len(name)>25 else name,
                    "expdate": utils.date_format(expdate),
                    "phone": phone_no,
                    "img": img,
                    # "expcolor": utils.get_background_color(expdate),
                    "msg": msg,
                    "callback": lambda x: x,
                }
            )
        

    def on_leave(self):
       self.ids.rv.data =[]
       self.active = False
       self.chart_values.clear()
       self.chart_month.clear()
       self.admission_chart_month.clear()
       self.admission_chart_values.clear()
    #    self.ids.mainboxx.clear_widgets()
    
    def rediret_expired_customer(self):
        self.parent.get_screen("customers_list").search_redirect = "expired"
        self.parent.change_screen("customers_list")
    # Tooltip methods ----------
    def show_tooltip(self, widget, amount,y_data):
        if hasattr(self, 'tooltip_label') and self.tooltip_label:
            self.remove_widget(self.tooltip_label)
        
        tooltip_text = (str(amount))
        # Create a temporary label to measure size
        temp_label = MDLabel(
            text=tooltip_text,
            font_size=sp(14),
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            halign="left",
            valign="top",
            size_hint=(None, None),
            shorten=False,
        )

        # Force wrap even for long words (e.g., number strings)
        temp_label.texture_update()
        print(f"Temp -->{temp_label.width},{temp_label.texture_size[1]}")
        # Tooltip width and height based on text size
        max_width = Window.width * 0.9  # 90% of screen width
        min_width = dp(60)

        tooltip_width = min(max(temp_label.texture_size[0] + dp(20), min_width), max_width)
        tooltip_height = temp_label.texture_size[1] + dp(20)

        # Calculate tooltip position and prevent overflow
        x = widget.center_x - (tooltip_width / 2)
        y = widget.top + dp(10)

        # Prevent tooltip from going out of screen
        x = max(dp(10), min(x, Window.width - tooltip_width - dp(10)))
        y = min(y, Window.height - tooltip_height - dp(10))
        print(f"Final size cal --> {x-(len(tooltip_text)*20)-15}, {y-(20/len(tooltip_text))-15}")
        print(f"Final size --> {x}, {y}")
        # Create a label positioned above the widget
        self.tooltip_label = MDLabel(
            text=tooltip_text,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            md_bg_color="#5ABFAD",
            padding=(10),
            # pos=(x, y),
            pos=(x-(len(tooltip_text)*20)-5, y_data),# Upper 775 Lower 460
            # pos_hint= {"center_x": 0.5, "center_y":0.5},
            size_hint=(None, None),
            # width=dp(250),
            halign="center",
            radius=[dp(10)]
        )
        print(x-(len(tooltip_text)*20)-5, (y-len(tooltip_text))/20-50)
        self.tooltip_label.height = dp(len(tooltip_text)/10+40)
        self.tooltip_label.width = dp(len(tooltip_text)*10+10)
        # print(self.tooltip_label.texture_size[1])

        self.add_widget(self.tooltip_label)

        # Auto-hide after 2 seconds
        Clock.schedule_once(self.hide_tooltip, 5)

    def hide_tooltip(self, *args):
        if hasattr(self, 'tooltip_label') and self.tooltip_label:
            self.remove_widget(self.tooltip_label)
            self.tooltip_label = None
            