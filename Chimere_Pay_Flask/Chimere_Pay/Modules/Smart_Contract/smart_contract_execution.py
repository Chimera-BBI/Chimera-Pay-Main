# # Set the URL of the Ethereum node you want to connect to
# infura_url = "https://goerli.ethereum.coinbasecloud.net"
# # Set the API key and username to use for authentication
# # These are test keys and will be deleted

# #Create a session with username and password
# sessionx = requests.Session()
# sessionx.auth = (username, api_key)



# @app.route("/GetEthBalance/<address>")
# def get_balance_eth(address):
#     #Connect to your Node
#     web3 = Web3(Web3.HTTPProvider(infura_url, session=sessionx))

#     # Checking if the connection to the node was successful
#     if web3.isConnected():
#         print("Successfully connected to the node at", infura_url)
#     else:
#         print("Connection to node failed. Please check the URL and try again.")
#     # Getting the balance of the wallet in Wei using the getBalance method
#     address = Web3.toChecksumAddress(address)
#     balance_in_wei = web3.eth.getBalance(address)

#     return str(balance_in_wei)


# @app.route("/send")
# @SessionCheck(Name="Check Phone Account Link")
# def send():
#     balance = get_balance_eth(session["Recieving Address"])
#     return render_template("send.html",balance=balance)

