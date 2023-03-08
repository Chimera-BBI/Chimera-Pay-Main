"""
All Session Variable Name and Use


Authentication Key : temporary key generated for authentication

phone_number : Phone number of the user

Recieving Address : Linked Eth Address of the User

"""

from Chimere_Pay import app
from functools import wraps
from flask import session, redirect, url_for
from .Database.chimera_postgres_api import execute_get_data

def SessionCheck(Name="Check Phone Session"):
    """_summary_

    Args:
        Name (str, optional): _description_. Defaults to "".

    Options for Name: 
        - Check Phone Account Link
        - Check Phone Session
    """

    def Check_Phone_No(fn):
        
        @wraps(fn)
        def decorator(*args, **kwargs):
            if "phone_number" in session:
                if session["phone_number"]!=None or session["phone_number"]!="":
                    return fn(*args, **kwargs)
            
            return redirect(url_for("login"))
            
        return decorator


    
    def Check_Account_Link(fn):
        
        @Check_Phone_No
        @wraps(fn)
        def decorator(*args, **kwargs):
            if "Recieving Address" in session:
                if session["Recieving Address"]!=None or session["Recieving Address"]!="":
                    return fn(*args, **kwargs)

            phone = session["phone_number"]
            with app.app_context():
                data = execute_get_data("chimera_user", ["phone","Address"], {"phone" : f"{phone}"})
            if data == -1:
                print("DataBase Exception")
                raise Exception("Error in database connection")
            elif len(data)>0:
                print("Session Validated ", data)
                session["Recieving Address"] = data[0][1]
                return fn(*args, **kwargs)
            
            return redirect(url_for("Update_Recieving_Account"))
            
        return decorator
        



    if Name=="Check Phone Account Link":
        return Check_Account_Link
    if Name=="Check Phone Session":
        return Check_Phone_No
            
