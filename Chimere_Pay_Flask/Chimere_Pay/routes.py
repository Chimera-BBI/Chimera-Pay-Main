import os
from Chimere_Pay import app
from .Modules import LoginModule
from flask import render_template

# from web3 import Web3

from .Modules.Database import postgres_api as db
# from .Modules.session_check import SessionCheck


import requests




from flask_jwt_extended import (create_access_token,get_jwt_identity,jwt_required,
                                JWTManager,create_refresh_token,get_jwt_identity,set_access_cookies,
                                set_refresh_cookies,get_jwt,get_csrf_token,unset_jwt_cookies,unset_access_cookies)

from flask import render_template, request, flash, redirect, send_from_directory, url_for,session,request,make_response,jsonify



# login module starts
jwt = JWTManager(app)


def unset_jwt():

    resp = make_response(redirect(url_for('login'),302))
    unset_jwt_cookies(resp)
    return resp

@jwt.unauthorized_loader
def unauthorized_callback(*args,**kwargs):
    # No auth header
    print('unauth token')
    return redirect(url_for('login'),302)

@jwt.invalid_token_loader
def invalid_token_callback(*args,**kwargs):
    # Invalid Fresh/Non-Fresh Access token in auth header
    resp = make_response(redirect(url_for('login'),302))
    print('invalid token')
    unset_jwt_cookies(resp)
    return resp, 302

@jwt.expired_token_loader
def expired_token_callback(*args,**kwargs):
    resp = make_response(redirect(url_for('login'),302))
    print('expired token')
    unset_jwt_cookies(resp)
    return resp,302


@app.after_request
def add_header(r):

    """Adds default header to a page request

    Args:
        r (flask request): request recieved by flask

    Returns:
        flask request: modified request with header
    """
    r.headers["Cache-Control"] = "no-cache, no-store, must-revalidate",'public, max-age=0'
    r.headers["Pragma"] = "no-cache"    
    r.headers["Expires"] = "0"    
    return r



def user_details_update():
    columns     = ["Name","Email","Profile_Data_Complete","AML_Complete"]
    values      = db.execute_get_data(table_name="USER_DETAILS",column_names=columns,where_dict={"Phone_Number":session["Phone_Number"]})
    values      = values[0]
    for i in range(len(columns)):
        session[columns[i]] = values[i]
    
    columns     = ["BALANCE","CURRENCY"]
    values      = db.execute_get_data(table_name="USER_BALANCE",column_names=columns,where_dict={"Phone_Number":session["Phone_Number"]})
    if len(values)>0:
        values = values[0]
        for i in range(len(columns)):
            session[columns[i]] = values[i]
    else:
        session[columns[0]] = None



# @app.route("/get-started")
@app.route("/")
def get_started():
    return render_template("get-started.html")


@app.route("/login")
def login():
    return render_template("enter_phone_number.html")


@app.route("/GetOtp",methods=['GET','POST'])
def GetOtp():

    data = request.form.to_dict()

    status = "Failed"

    key = LoginModule.start_authentication(data["phoneNumber"])
    status = "Already Exists"
    
    session["Authentication Key"] = key

    return (status)
        

@app.route("/VerifyOTP",methods=['GET','POST'])
def VerifyOTP():

    data = request.form.to_dict()

    phone_number    = data["phoneNumber"]
    auth_key        = session["Authentication Key"] 
    otp             = data["OTP"]
    result          = LoginModule.verify_otp(phone_number,auth_key,otp)
    session["Authentication Key"] = ""

    # raise Exception("Test")

    if result==1:
        
        access_token        = create_access_token(identity=str(phone_number))
        resp                = make_response(redirect(url_for('user_profile'),302)) # change this to send
        set_access_cookies(resp,access_token)
        session["Phone_Number"] = phone_number
        user_details_update()

        return resp,302
    
    flash("OTP Not Valid",'alert')
    return redirect(url_for("login"))

@app.route("/FillUserProfile", methods=['GET','POST'])
def user_profile():

    columns = ["Name","Email","Address","DOB","Gender"]

    if request.method == "POST":
        data = request.form.to_dict()

        input_dict = {}
        for i in columns:
            input_dict[i] = data[i]

        test = db.execute_enter_data(table_name="USER_DETAILS",input_dict=input_dict,update_table=True,where_dict={"Phone_Number":session["Phone_Number"]})

        if test==1:
            print("update user profile")
    
        user_details_update()

        return redirect(url_for("connect_bank"))
    
    return render_template("user_profile.html") 

@app.route("/ConnectBank", methods = ["GET","POST"])
def connect_bank():

    if request.method == "POST":
        data = request.form.to_dict()
        input_dict = {"BALANCE":10000}
        input_dict["Currency"] = data["Currency"]

        test = db.execute_enter_data(table_name="USER_BALANCE",input_dict=input_dict,update_table=True,where_dict={"Phone_Number":session["Phone_Number"]})

        if test==1:
            print("update user balance")
            test2 = db.execute_enter_data(table_name="USER_DETAILS",input_dict={"AML_Complete":"TRUE"},update_table=True,where_dict={"Phone_Number":session["Phone_Number"]})


        user_details_update()

        return redirect(url_for("connect_bank"))
        
    return render_template("connect_bank.html")

@app.route("/AML", methods = ["GET","POST"])
def AML_Data():

    if request.method == "POST":

        test = db.execute_enter_data(table_name="USER_BALANCE",input_dict=input_dict,update_table=True,where_dict={"Phone_Number":session["Phone_Number"]})

        if test==1:
            print("update user balance")

        user_details_update()

        return redirect(url_for("send"))
        
    return render_template("complete_aml.html")


@app.route("/send")
def send():
    # balance = get_balance_eth(session["Recieving Address"])
    return render_template("send.html",balance=5000)


# @app.route("/Update-Recieving-Account", methods=['GET' , 'POST'])
# @SessionCheck(Name="Check Phone Session")
# def Update_Recieving_Account():

    
#     # return "Entered Page"

#     if request.method == "POST":
#         data = request.form.to_dict()
#         new_eth_address = data["Eth Account"]

#         accepted = chimera_postgres_api.execute_enter_data("chimera_user", ["phone","Address"], [session["phone_number"],new_eth_address])

#         if accepted == -1:
#             raise Exception("Error while database connection")

#         return redirect(url_for("send"))

#     return render_template("connect_meta_mask_wallet.html")


# @app.route("/Get-Eth-Address", methods=['GET' , 'POST'])
# @SessionCheck(Name="Check Phone Session")
# def GetAddress():
#     data = request.form.to_dict()
#     ph = data["to_address"]

#     print("phone number ",ph)

#     addresses =  chimera_postgres_api.execute_get_data("chimera_user", ["Address"], {"phone" : ph})

#     print("addresses ", addresses)


#     # raise Exception("testing")

#     if addresses==-1 or len(addresses)<1:
#         return "-1"
    
#     return addresses[0][0]



@app.route('/logout')
def logout():
    session.clear()
    # session["phone_number"] = None
    # session["Recieving Address"] = None
    resp = unset_jwt()
    return resp,302


