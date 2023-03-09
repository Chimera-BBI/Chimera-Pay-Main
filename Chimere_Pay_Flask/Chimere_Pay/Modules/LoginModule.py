from .Database import postgres_api as db



def sign_up_user(phone_number):
   
   data = db.execute_enter_data(table_name="USER_DETAILS",input_dict={"Phone_Number":phone_number})
   data = db.execute_enter_data(table_name="USER_BALANCE",input_dict={"Phone_Number":phone_number})
   return 1

def start_authentication(phone_number):

   data = db.execute_get_data(table_name="USER_DETAILS",column_names=["*"],where_dict={"Phone_Number":phone_number})
   if len(data)<1:
      sign_up_user(phone_number)

   # authentication_key = generate_otp(phone_number)

   authentication_key = "sample_auth_mech"

   return authentication_key

def verify_otp(phone_number,auth_key,otp):
   
   # correct_otp = fetch_otp(auth_key)
   correct_otp = "123456"

   if correct_otp == otp:
      return 1
   
   return -1
