from main_imports import MDScreen,StringProperty,MDDropdownMenu,MDDialogHeadlineText,MDDialogContentContainer,MDListItemHeadlineText,MDDialog,MDButton,MDButtonText,MDBoxLayout,MDLabel,MDListItem, dp,MDCard,MDIconButton,BoxLayout,BoxLayout
from libs.applibs import utils
from kivy.clock import Clock
from datetime import datetime

utils.load_kv("seatregister.kv")
class SItem(MDListItem):
    divider = None
    source = StringProperty()
class SeatButton(MDButton):
    color = []

class SeatRegisterScreen(MDScreen):
    selected_shift = "Select Shift"
    # Initialize the dropdown menu with shift options
    dialog=None
    
    def on_enter(self):
        shift_options = ["Single Shift", "Double Shift", "Ultimate Plan", "Week-end Plan", "Day Plan", "Flexi Shift"]
        self.menu = MDDropdownMenu(
            caller=self.ids.shift_selector,
            items=[{"text": option, "viewclass": "MDListItem", "on_release": lambda x=option: self.set_shift(x)} for option in shift_options],
            width_mult=4
        )

        # Set up seats
        self.seat_status = {i: "green" for i in range(1, 38)}  # Assume all seats are green initially
        self.update_seat_display(self.ids.seats_grid)

    def set_shift(self, shift):
        self.selected_shift = shift
        self.menu.dismiss()
        self.update_seat_availability(shift)

    def update_seat_availability(self, shift):
        # Set the color of seats based on the selected shift
        if shift == "Single Shift":
            self.seat_status = {i: "green" for i in range(1, 5)}
        elif shift == "Double Shift":
            self.seat_status = {i: "yellow" if i % 3 == 1 else "green" for i in range(1, 38)}
        elif shift == "Ultimate Plan":
            self.seat_status = {i: "red" for i in range(1, 38)}
        # Add other shift conditions as needed
        
        # Update seat display after setting seat availability
        self.update_seat_display(self.ids.seats_grid)

    def update_seat_display(self, seats_grid):
        # Clear current seat buttons
        seats_grid.clear_widgets()

        # Add buttons for seats with appropriate colors
        for i in range(1, 38):
            color = {
                "green": (0, 1, 0, 1),
                "yellow": (1, 1, 0, 1),
                "red": (1, 0, 0, 1)
            }[self.seat_status[i]]
            seat_button = self.add_btn_details(seatnumber=i,color=color)
            seats_grid.add_widget(seat_button)
    def add_btn_details(self,seatnumber,color):
        btn = SeatButton(
            MDButtonText(
                text=str(seatnumber), ), 
                theme_bg_color= "Custom",
                md_bg_color=color,
                on_release=lambda x: self.show_shift_details(str(seatnumber))
                )
        return btn
    def show_shift_details(self, seat_number):
        # Define shift availability details
        shift_details = [
            {"shift": "Single shift (7am - 3pm)", "status": "Abhijit Shinde"},
            {"shift": "Double shift", "status": "Available"},
            {"shift": "Ultimate Plan", "status": "Unavailable"},
            {"shift": "Flexi Shift", "status": "Available"}
        ]

        # Generate content for the dialog based on shift details
        self.content = MDDialogContentContainer(orientation="vertical",)
        for detail in shift_details:
            # self.content.append(SItem(text=f"{detail['shift']} - {detail['status']}", source="assets/img/table_5490782.png"))
            self.content.add_widget(self.create_list_item(txt=f"{detail['shift']} - {detail['status']}", avatar_source="assets/img/table_5490782.png"))

        # Show the dialog with shift details
        if self.dialog == None: 
            self.dialog = MDDialog(
                # title=f"Seat {seat_number} Shift Details",
                MDDialogHeadlineText(text=f"Seat {seat_number} Shift Details"),
                self.content,
                
            )
            self.dialog.theme_bg_color="Custom"
            self.dialog.md_bg_color="#fcfbff"
            self.dialog.open()
        else:
            self.dialog.dismiss()
            self.dialog = MDDialog(
                # title=f"Seat {seat_number} Shift Details",
                MDDialogHeadlineText(text=f"Seat {seat_number} Shift Details"),
                self.content,
                
            )
            self.dialog.theme_bg_color="Custom"
            self.dialog.md_bg_color="#fcfbff"
            self.dialog.open()
    def create_list_item(self, txt, avatar_source):
        # Helper function to create a list item with a supporting text and avatar
        list_item = SItem(
            
            MDListItemHeadlineText(
                text=txt,
            ),
            source = avatar_source,
            theme_bg_color="Custom",
            md_bg_color=self.theme_cls.transparentColor,
            on_release=lambda x: self.get_text(txt)  # Pass email directly to the callback
        )
        return list_item 
    def get_text(self, item_text):
        print("This is Good :: ",item_text)
        self.dialog.dismiss()
        self.parent.change_screen("admission_form")