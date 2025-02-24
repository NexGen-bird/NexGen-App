from main_imports import MDScreen,MDDialog,dp,MDDialogHeadlineText,MDDialogSupportingText
from libs.applibs import utils
from supabase_lib.supabase_auth import login_with_email_password,send_password_reset_email
from kivy.core.window import Window

utils.load_kv("login.kv")

class Login_Screen(MDScreen):
    is_remember = True
    def on_enter(self):
        """
        This method used in development to avoid login 
        """
        data = utils.read_json_file(r"libs/applibs/remember_login.json")
        self.is_remember = False if data["is_remember"]!= "True" else True
        if data["username"]!="" and data["password"]!="":
            self.ids.Email.text = data["username"]
            self.ids.Password.text = data["password"]
    def on_checkbox_active(self, checkbox, value):
        if checkbox.state == "down":
            self.is_remember = True
            print("Checked...")
        else:
            self.is_remember = False
            utils.write_json_file(r"libs/applibs/remember_login.json","","",False)
            print('The checkbox', checkbox, 'is inactive', 'and', checkbox.state, 'state')
    def on_leave(self):
        self.ids.Email.text = ""
        self.ids.Password.text = ""
    def login(self, email: str, password: str):
        # Validate input fields
        if self.is_remember:
            utils.write_json_file(r"libs/applibs/remember_login.json",email,password,True)
        if not email.strip():
            utils.snack(color="red", text="Please enter your email.")
            return
        
        if not password.strip():
            utils.snack(color="red", text="Please enter your password.")
            return

        try:
            user = login_with_email_password(email, password)
            
            if user:
                self.auth_token = user.session.access_token
                self.parent.change_screen("land")
            else:
                utils.snack(color="red", text="Invalid email or password.")

        except Exception as e:
            utils.snack(color="red", text=f"Login failed: {str(e)}")


    def on_login_success(self, user_id):
        # Navigate to the next screen or perform other post-login actions
        utils.snack(color="green",text=f"Welcome, User {user_id}!")
        # Add logic here to navigate to the main screen or dashboard
    
    def forgot_password(self, email):
        if not email:
            utils.snack(color="red",text="Please enter your email address.")
        else:
            success = send_password_reset_email(email)
            if success:
                utils.snack(color="green",text="Password reset email sent! Check your inbox.")
            else:
                utils.snack(color="red",text="Failed to send password reset email.")