import os
import configparser
from kivy.core.window import Window
from kivy.metrics import dp
import socket
import json
from main_imports import Builder,MDButton,MDDialog,MDSnackbarText,Image, MDSnackbarActionButtonText,MDDropdownMenu,MDSnackbar,MDSnackbarActionButton,MDLabel
selected_group = ""

def load_kv(file_name, file_path=os.path.join("libs", "uix", "kv")):
    """
    `load_kv` func is used to load a .kv file.
    args that you can pass:
        * `file_name`: Name of the kv file.
        * `file_path`: Path to the kv file, it defaults
                       to `project_name/libs/kv`.

    Q: Why a custom `load_kv`?
    A: To avoid some encoding errors.
    """
    # print(file_path)
    with open(os.path.join(file_path, file_name), encoding="utf-8") as kv:
        Builder.load_string(kv.read())

def calldialog(self,title,text):
        MDDialog(
            title="Discard draft?",
            text="This will reset your device to its default factory settings.",
            buttons=[
                MDButton(
                    text="CANCEL",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                ),
                MDButton(
                    text="DISCARD",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                ),
            ],
        ).open()
def is_internet_available():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=2)
        return True
    except OSError:
        return False
def snack(color,text):
        if color == "red":
            clr= (1, 82/255, 82/255,1)
        elif color=="green":
            clr= (1, 1, 244/255, 1)
        else:
            clr= (11/255, 38/255, 83/255, 1)
        MDSnackbar(
             MDSnackbarText(
                text=text,
                text_color="black"
            ),
            MDSnackbarActionButton(
                MDSnackbarActionButtonText(
                    text="Done",
                    theme_text_color="Custom",
                    text_color="#8E353C",
                )
                
                
            ),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            orientation="horizontal",
            size_hint_x=(
                Window.width - (dp(10) * 2)
            ) / Window.width,
            md_bg_color=clr,
        ).open()
        # Snackbar(
        #     text=text,
        #     elevation=0.5,
        #     bg_color=clr,
        #     snackbar_x="10dp",
        #     snackbar_y="9dp",
        #     size_hint_x=(
        #         Window.width - (dp(10) * 2)
        #     ) / Window.width
        # ).open()

def show_alert_dialog():
    print("inside alert box")
    dialog = MDDialog(
        text="Do You Want to Exit?",
        buttons=[
            MDButton(
                text= "Cancel",
                # md_bg_color= (248/255, 178/255, 45/255,1),
                on_release= lambda x:dialog.dismiss() 
            ),
            MDButton(
                text= "Exit",
                md_bg_color= (242/255, 129/255, 42/255,1),
                on_release= lambda x: exit()
            )
        ],
    )
    dialog.open()

def baseurl():
    config = configparser.ConfigParser()
    config.read('project_config.conf')

    url = config["Base_URL"]["base_url"]
    return url
from datetime import datetime

def get_background_color(planexpirydate):
    today = datetime.today().date()
    expiry_date = datetime.strptime(planexpirydate, "%Y-%m-%d").date()
    days_left = (expiry_date - today).days

    if days_left == 0:
        return "#cc3300"  # Red (Expiring today)
    elif days_left == 1:
        return "#cc3300"  # Light Red
    elif days_left == 2:
        return "#ff9966"  # Orange
    elif days_left == 3:
        return "#FFBF69"  # Light Orange
    elif 4 <= days_left <= 7:
        return "#ffcc00"  # Yellow
    else:
        return "#339900"  # Light Green (More than a week left)

def date_format(input_date):

    # Input date string
    # input_date = '2024-11-28T16:30:12.257328+00:00'

    # Convert to datetime object
    date_obj = datetime.fromisoformat(input_date)

    # Format the date to desired format
    formatted_date = date_obj.strftime('%d %b %Y')

    return formatted_date

from datetime import datetime, timedelta,date
from dateutil.relativedelta import relativedelta

def calculate_end_dates1(input_date,plantype):
    """
    This function calculates the end dates for a given input date based on 
    Month, Quarter, Half Year, and Year durations.

    Parameters:
        input_date (str): Date in the format 'YYYY-MM-DD'

    Returns:
        dict: A dictionary containing the end dates for Month, Quarter, Half Year, and Year
    """
    # Parse the input date string to a datetime object
    start_date = datetime.strptime(str(input_date), '%Y-%m-%d').date()

    # Calculate the end dates
    if plantype =="Monthly": 
        end_date = start_date + relativedelta(months=1) - relativedelta(days=1)  # Add 1 month
    elif plantype=="Quaterly":
        end_date = start_date + relativedelta(months=3) - relativedelta(days=1) # Add 3 months
    elif plantype=="Half Yearly": 
        end_date =start_date + relativedelta(months=6) - relativedelta(days=1),  # Add 6 months
    elif plantype=="Yearly": 
        end_date =start_date + relativedelta(years=1)   # Add 1 year
    
    print("End Date --> ",str(end_date))
    return str(start_date),str(end_date)

def calculate_end_dates(input_date, plantype):
    """
    Calculates the end date based on the input date and plan type,
    reducing one day from the final calculated end date.

    Parameters:
        input_date (str): Date in the format 'YYYY-MM-DD'
        plantype (str): Type of plan duration ('Month', 'Quarter', 'Half Year', 'Year')

    Returns:
        tuple: A tuple containing start date and end date as datetime.date objects
    """
    try:
        # Parse the input date string to a date object
        start_date = datetime.strptime(str(input_date), '%Y-%m-%d').date()
    except ValueError:
        raise ValueError("Invalid input date format. Use 'YYYY-MM-DD'.")

    # Map plan types to duration
    durations = {
        2: relativedelta(months=1),
        3: relativedelta(months=3),
        4: relativedelta(months=6),
        5: relativedelta(years=1),
        1: relativedelta(days=1)
        
    }

    if plantype not in durations:
        raise ValueError("Invalid plan type. Choose from 'Month', 'Quarter', 'Half Year', or 'Year'.")

    # Calculate the end date and reduce one day
    end_date = start_date + durations[plantype] - relativedelta(days=1)  # Subtract 2 days

    return str(start_date), str(end_date)
def get_previous_month_range(input_date=None):
    """
    Returns the start and end date of the previous month's period.
    - Start date: Always 15th of the previous month.
    - End date: Always 14th of the current month.
    
    If input_date is not provided, it defaults to today's date.
    """
    if input_date is None:
        input_date = date.today()
    print(input_date)
    if input_date.day >= 15:
        # Current month is fine
        start_date = date(input_date.year, input_date.month - 1, 15) if input_date.month > 1 else date(input_date.year - 1, 12, 15)
        end_date = date(input_date.year, input_date.month, 14)
    else:
        # Go one more month back
        start_date = date(input_date.year, input_date.month - 2, 15) if input_date.month > 2 else date(input_date.year - 1, 12 + (input_date.month - 2), 15)
        end_date = date(input_date.year, input_date.month - 1, 14) if input_date.month > 1 else date(input_date.year - 1, 12, 14)

    return start_date.strftime("%Y-%m-%d"), end_date.strftime("%Y-%m-%d")


def write_json_file(filename, username, password,is_remember):
    """Writes a JSON file with the given username and password."""
    data = [{"username": username, "password": password,"is_remember":str(is_remember)}]
    
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def read_json_file(filename):
    """Reads and returns the data from the JSON file."""
    try:
        with open(filename, "r") as file:
            data = json.load(file)
        return data[0]
    except FileNotFoundError:
        print("File not found.")
        return None