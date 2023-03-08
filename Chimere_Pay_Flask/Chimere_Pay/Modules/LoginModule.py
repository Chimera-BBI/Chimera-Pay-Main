def sign_up_user(phone_number):

   """
    Registers a new user with the specified phone number in the Cognito user pool.
    
    Parameters:
        - phone_number (str): the phone number of the user to be registered
    
    Returns:
        None
    """
   sign_up_dict = {

      "ClientId": client_ID,
      "Password": "null_password",
      "Username": phone_number,
      "ValidationData": [ 
         { 
            "Name": "phone_number",
            "Value": phone_number
         }
      ]
   }

   # Use the client to initiate the OTP request
   response = client.sign_up(**sign_up_dict)


def start_authentication(phone_number):

   initiate_auth_dict = {

      "AuthFlow": "CUSTOM_AUTH",
      "AuthParameters": { 
         "USERNAME" : phone_number,
         "PASSWORD":"null_password" 
      },
      "ClientId": client_ID,
   }

   response = client.initiate_auth(**initiate_auth_dict)

   return response["Session"]


def verify_otp(phone_number,session_var,answer="opensesame"):
   response_to_auth = {
      "ChallengeName": "CUSTOM_CHALLENGE",
      "ChallengeResponses": { 
         "USERNAME" : phone_number,
         "ANSWER"      : answer 
      },
      "ClientId": client_ID,
      "Session": session_var
   }

   response = client.respond_to_auth_challenge(**response_to_auth)

   return response
