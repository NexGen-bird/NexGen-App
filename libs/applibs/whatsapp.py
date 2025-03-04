from jnius import autoclass
from time import sleep
from urllib.parse import quote
Intent = autoclass('android.content.Intent')
Uri = autoclass('android.net.Uri')
PythonActivity = autoclass('org.kivy.android.PythonActivity')

def send_messages(phone_numbers, message):
    # print(phone_numbers, message)
    # pass
    print(phone_numbers)
    print(message)
    encoded_message =quote(message) 
    activity = PythonActivity.mActivity
    # for phone in phone_numbers:
        # url = 
    uri = Uri.parse(f"https://wa.me/{phone_numbers}?text={encoded_message}")
    intent = Intent(Intent.ACTION_VIEW, uri)
    activity.startActivity(intent)
    sleep(2)  # Wait for WhatsApp to open before sending the next message