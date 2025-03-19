from supabase_lib.supabase_config import supabase
from supabase_lib.supabase_auth import *
from main_imports import MDApp

# Create a new customer
def create_customer(name, dob, gender, phone_number, email, education, joining_for, address, profile_image):
    data = {
        "name": name,
        "dob": dob,
        "gender":gender,
        "phone_number": phone_number,
        "email": email,
        "education":education,
        "joining_for": joining_for,
        "address": address,
        "profile_image": profile_image,
    }
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
            utils.snack("red","No active session. please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.table("Customers").insert(data).execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    
    # supabase.auth.sign_out()

# Get all customers
def get_all_customers():
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.table("Customers").select("*").execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    
# Get customer details
def get_customers_details(column_name,contact_number):
    isinternet=utils.is_internet_available()
    if isinternet:
        response = supabase.table("Customers").select("*").eq(column_name, contact_number).execute()
        # supabase.auth.sign_out()
        print(response.data)
        return response.data
    else:
        utils.snack("red","No Internet Connection..")
# Update a customer
def update_customer(contact_number, updates):
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.table("Customers").update(updates).eq("phone_number", contact_number).execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")

# Delete a customer
def delete_customer(customer_name):
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.table("Customers").delete().eq("id", customer_name).execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")

def get_all_customers_contact():
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("get_phone_numbers").execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")

def get_all_customers_names():
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("get_names").execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
#  Add Transaction
def create_transaction(txn_date,transaction_type,amount,txn_made_by, payment_method, description, transaction_for,transaction_made_to):
    data = {
        "txn_date": txn_date,
        "txn_made_by": txn_made_by,
        "customer_transaction_type": transaction_type,
        "customer_amount": amount,
        "customer_payment_method": payment_method,
        "customer_description": description,
        "customer_transaction_for": transaction_for,
        "customer_transaction_made_to":transaction_made_to
    }
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("insert_general_transactions", data).execute()
            # supabase.auth.sign_out()
            utils.snack(color="green",text="Transaction Submitted Successfully!")
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    

#  Get All Transactions
def get_all_transactions():
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.table("Transactions").select("*").execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    
def get_transactionspagedata():
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("fetch_transaction_details").execute()
            #  
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")

def get_investmenttransactionspagedata():
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("fetch_investment_transaction_details").execute()
            #  
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    
def get_subcriptionpagedata():
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("fetch_subcription_details").execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    
    
def get_net_profit(start_date,end_date):
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("get_net_profit", {"start_date": start_date, "end_date": end_date}).execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")

    
def get_investment_details(name):
    print("This is name -->",name)
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("get_investment_details", {"staffname": str(name)}).execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
        
def get_expense_profit():
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response_in = supabase.rpc("calculate_total_amount", {"filter_value": "IN"}).execute()
            response_out = supabase.rpc("calculate_total_amount", {"filter_value": "OUT"}).execute()
            # supabase.auth.sign_out()
            return response_in.data,response_out.data
            
    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    
#  Delete transaction by id 
def delete_transaction(transaction_id):
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.table("Transactions").delete().eq("id", transaction_id).execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    

def insert_addmission(data):
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
             
             utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("insert_addmissions", data).execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    

def run_sql(query):
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
                
                utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = supabase.rpc("execute_sql", {"query": query}).execute()
            return response.data

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
def upload_image(imagepath,imagename):
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
                
                utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            with open(imagepath, "rb") as f:
                response = (
                    supabase.storage
                    .from_("customer_images")
                    .upload(
                        file=f,
                        path=f"{imagename}.png",
                        file_options={"content-type":"image/png"}
                    )
                )
            return response

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")
    
def get_profile_img(imagename):
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
                
                utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = (
            supabase.storage
            .from_("customer_images")
            .get_public_url(f"{imagename}.png")
            )
            return response

    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")

def search_profile_img(imagename):
    isinternet = utils.is_internet_available()

    try:
        user = supabase.auth.get_user()

        if not user:
                
                utils.snack("red","No active session. Please Re-login.")
        elif not isinternet:
            utils.snack("red", "No Internet Connection.")
        else:
            response = (
                supabase.storage
                .from_("customer_images")
                .list(
                    options = {
                        "limit": 100,
                        "offset": 0,
                        "sortBy": {"column": "name", "order": "desc"},
                        "search": imagename,
                    }
                )
            )
            if response:
                return get_profile_img(imagename)
            else:
                return "assets/img/blank_profile.png"


    except Exception as e:
       utils.snack("red",f"Error fetching user: {e}, Re-Login")