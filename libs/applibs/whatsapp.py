from jnius import autoclass
from time import sleep

Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

def send_messages(phone_numbers, message):
    activity = PythonActivity.mActivity
    # for phone in phone_numbers:
        # url = 
    uri = Uri.parse(f"https://wa.me/whatsappbusiness?phone={phone_numbers}&text={message}")
    intent = Intent(Intent.ACTION_VIEW, uri)
    activity.startActivity(intent)
    sleep(2)  # Wait for WhatsApp to open before sending the next message