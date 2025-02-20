from supabase_lib.supabase_config import supabase
from supabase_lib.supabase_auth import *
from libs.applibs import utils
# Create a new customer
from postgrest.exceptions import APIError
from gotrue.helpers import get_error_code
def create_customer(name, email, phone_number, dob, address, profile_image):
    data = {
        "name": name,
        "email": email,
        "phone_number": phone_number,
        "dob": dob,
        "address": address,
        "profile_image": profile_image,
    }
    response = supabase.table("Staff").insert(data).execute()
    supabase.auth.sign_out()
    return response.data

# Get all customers
def get_all_customers():
    response = supabase.table("Customers").select("*").execute()
    supabase.auth.sign_out()
    # print(response)
    return response.data
def get_all_customers_contact():
    response = supabase.rpc("get_phone_numbers").execute()

    # Extract the array fro m the response
    phone_numbers = response.data  # ['1234567891', '1234567890']
    print(phone_numbers)
    # response = supabase.table("Customers").select("phone_number").execute()
    supabase.auth.sign_out()
    # print(response)
    return phone_numbers
# Update a customer
def update_customer(customer_id, updates):
    response = supabase.table("Customers").update(updates).eq("id", customer_id).execute()
    supabase.auth.sign_out()
    return response.data

# Delete a customer
def delete_customer(customer_id):
    response = supabase.table("Customers").delete().eq("id", customer_id).execute()
    supabase.auth.sign_out()
    return response.data

def create_transaction(transaction_type, reference_id,amount,receipt_id, payment_method, description, transaction_for):
    data = {
        "transaction_type": transaction_type,
        "receipt_id":receipt_id,
        "amount": amount,
        "reference_id": reference_id,
        "payment_method": payment_method,
        "description": description,
        "transaction_for": transaction_for,
    }
    response = supabase.table("Transactions").insert(data).execute()
    # supabase.auth.sign_out()

    return response.data

def get_all_transactions():
    # response = supabase.table("Transactions").select("*").execute()
    # response = supabase.rpc("get_user_orders", {"user_name": user_name}).execute()
    response = supabase.rpc("fetch_transaction_details").execute()
    supabase.auth.sign_out()
    print("This is ---------->",response)
    return response.data

def delete_transaction(transaction_id):
    response = supabase.table("Transactions").delete().eq("id", transaction_id).execute()
    supabase.auth.sign_out()
   
    return print(response.data)
def insert_addmission(data):
    response = supabase.rpc("insert_addmissionnew", data).execute()
    supabase.auth.sign_out()
    return response.data
login_with_email_password("abhijit.shinde@test.com","india@123")
# new_customer = create_customer(
#     name="Rupesh Kamble",
#     email="rupeshkamble@gmail.com",
#     phone_number="9930253216",
#     dob="1996-01-01",
#     address="123 Main Street, Cityville",
#     profile_image="https://example.com/profile.jpg"
# )

    
# updated_customer = update_customer(
#     customer_id=str(customers[0]["id"]),
#     updates={
#         "phone_number": "+9876543210",
#         "address": "Kalyan"
#     }
# )
# print("Updated ----->",updated_customer)

# deleted_customer = delete_customer(customer_id=customers[0]["id"])
# print(deleted_customer)

# new_transaction = create_transaction(transaction_type="IN",
#                                      reference_id="ecb68e61-c29d-474a-baf4-8175c2c377f3",
#                                      amount=1700,
#                                      receipt_id="NG000002",payment_method="UPI",transaction_for="Addmission",description="Test")
# print(new_transaction)



# A = get_all_customers_contact()
# final = []
# for x in A:
#     final.append(x["phone_number"])
# print(A)


params1 = {
    "customer_name": "John Doe",
    "customer_dob": "1990-01-01",
    "customer_gender": "Male",
    "customer_phone_number": "1234567890",
    "customer_email": "john@example.com",
    "customer_education": "Bachelor",
    "customer_joining_for": "Gym",
    "customer_address": "123 Main St",
    "customer_profile_image": "profile.jpg",
    "customer_transaction_type": "Credit",
    "customer_planduerationid": 1,
    "customer_shiftids": [1, 2, 3],  # Pass multiple shift IDs as a list
    "customer_plantypeid": 1,
    "customer_seatid": 1,
    "customer_planstartdate": "2025-01-01",
    "customer_planexpirydate": "2025-12-31",
    "customer_paymenttype": "Full Payment",
    "customer_isactive": 1,
    "customer_amount": 100.00,
    "customer_payment_method": "Cash",
    "customer_description": "Payment for admission",
    "customer_transaction_for": "Addmission",
    "customer_transaction_made_to": "Gym Admin",
}

params ={
    'customer_name': 'Abhijit Shinde', 
    'customer_dob': '1998-09-03', 
    'customer_gender': 'Male', 
    'customer_phone_number': '9594897959', 
    'customer_email': 'abhijitshinde@gmail.com', 
    'customer_education': 'BE ', 
    'customer_joining_for': 'Test', 
    'customer_address': 'Dawadi Dombavali East', 
    'customer_profile_image': '/Users/abhijit.shinde/Desktop/nexgen/logo.png', 
    'customer_transaction_type': 'In', 
    'customer_planduerationid': 3, 
    'customer_shiftid': [4, 3], 
    'customer_plantypeid': 2, 
    'customer_seatid': 1, 
    'customer_planstartdate': '2025-01-12', 
    'customer_planexpirydate': '2025-04-11', 
    'customer_paymenttype': 'UPI', 
    'customer_isactive': 1, 
    'customer_amount': '2200', 
    'customer_payment_method': 'UPI', 
    'customer_description': 'Test ', 
    'customer_transaction_for': 'Addmission', 
    'customer_transaction_made_to': 'Thakre'
}




# SELECT insert_addmissionnew(
#     'John Doe', '1990-01-01', 'Male', '1234567890', 'john@example.com', 'Bachelor',
#     'Gym', '123 Main St', 'profile.jpg',
#     'Credit', 1200, 'Cash', 'Payment for admission', 'Addmission', 'Gym Admin',
#     2, 1, ARRAY[4], 1, '2025-01-01', '2025-12-31', 'Full Payment', 1
# );
# {'customer_name': 'Abhijit Shinde', 'customer_dob': '1998-09-03', 'customer_gender': 'Male', 'customer_phone_number': '9594897959', 'customer_email': 'abhijitshinde@gmail.com', 'customer_education': 'BE ', 'customer_joining_for': 'Test', 'customer_address': 'Dawadi Dombavali East', 'customer_profile_image': '/Users/abhijit.shinde/Desktop/nexgen/logo.png', 'customer_transaction_type': 'In', 'customer_amount': '1250', 'customer_payment_method': 'UPI', 'customer_description': 'SPP', 'customer_transaction_for': 'Addmission', 'customer_transaction_made_to': 'Test', 'customer_plantypeid': 1, 'customer_planduerationid': 2, 'customer_shiftid': [4], 'customer_seatid': 1, 'customer_planstartdate': '2025-01-25', 'customer_planexpirydate': '2025-02-24', 'customer_paymenttype': 'UPI', 'customer_isactive': 1}x
app = {'customer_name': 'Abhijit Shinde', 'customer_dob': '1998-09-03', 'customer_gender': 'Male', 'customer_phone_number': '9594897959', 'customer_email': 'abhijitshinde@gmail.com', 'customer_education': 'BE ', 'customer_joining_for': 'Test', 'customer_address': 'Dawadi Dombavali East', 'customer_profile_image': '/Users/abhijit.shinde/Desktop/nexgen/logo.png', 'customer_transaction_type': 'In', 'customer_planduerationid': 2, 'customer_shiftid': [4], 'customer_plantypeid': 1, 'customer_seatid': 1, 'customer_planstartdate': '2025-01-25', 'customer_planexpirydate': '2025-02-24', 'customer_paymenttype': 'UPI', 'customer_isactive': 1, 'customer_amount': '1250', 'customer_payment_method': 'UPI', 'customer_description': 'Add', 'customer_transaction_for': 'Addmission', 'customer_transaction_made_to': 'Test'}
sql = {'customer_name': 'John Doe', 
       'customer_dob': '1990-01-01', 
       'customer_gender': 'Male', 
       'customer_phone_number': '1234567890', 
       'customer_email': 'john@example.com', 
       'customer_education': 'Bachelor', 
       'customer_joining_for': 'Gym', 
       'customer_address': '123 Main St', 
       'customer_profile_image': '/Users/abhijit.shinde/Desktop/nexgen/logo.png', 

       'customer_transaction_type': 'Credit', 
       'customer_planduerationid': 1, 
       'customer_shiftid': [4], 
       'customer_plantypeid': 2, 
       'customer_seatid': 1, 
       'customer_planstartdate': '2025-01-25', 
       'customer_planexpirydate': '2025-02-24', 
       'customer_paymenttype': 'UPI', 
       'customer_isactive': 1, 
       'customer_amount': '1200', 
       'customer_payment_method': 'Cash', 
       'customer_description': 'Payment for admission', 
       'customer_transaction_for': 'Addmission', 
       'customer_transaction_made_to': 'Gym Admin'}

function_name = "insert_addmissions"
params = {'customer_name': 'Rocky Kamble', 'customer_dob': '1999-01-21', 'customer_gender': 'Male', 'customer_phone_number': '1234567890', 'customer_email': 'rockykamble@gmail.com', 'customer_education': 'MTech', 'customer_joining_for': 'Study', 'customer_address': 'Test Test', 'customer_profile_image': 'profile.png', 'customer_transaction_type': 'IN', 'customer_amount': '1250', 'customer_payment_method': 'UPI', 'customer_description': 'Addmission', 'customer_transaction_for': 'Addmission', 'customer_transaction_made_to': 'Abhijit', 'customer_plantypeid': 1, 'customer_planduerationid': 2, 'customer_shiftid': [2], 'customer_seatid': 1, 'customer_planstartdate': '2025-02-01', 'customer_planexpirydate': '2025-02-28', 'customer_paymenttype': 'UPI', 'customer_isactive': 1}

# Call the function using Supabase RPC

response = supabase.rpc(function_name, params).execute()

customer_id = "ecb68e61-c29d-474a-baf4-8175c2c377f3"  # Replace this with your dynamic value

query = f"""
                select count(*)
                                from "Customers"
                """
collection_query = """select sum(amount) from "Transactions" where transaction_type = 'IN'"""

# response = supabase.table("Customers").select("*").execute()
# data, error = response.get("data"), response.get("error")
print(response.data)
print(response.data.split(":")[0])
supabase.auth.sign_out()
# if error:
#     print("Error:", error)
# else:
#     print("Inserted successfully:", data)
