




def send_balance(token_to_check):
    pass

def mint_token(token_name:str, token_amount:float, private_key_minter:str, public_key_reciever:str):
    pass

def burn_token(token_name:str, token_amount:float, private_key_burner:str):
    pass

def send_token(token_name:str, token_amount:float, private_key_sender:str, public_key_reciever:str):
    pass

def swap_token(token_swap_from:str,
               token_swap_to:str, 
               token_amount_to_swap:int,
               token_amount_to_recieve:int, 
               private_key_account:str, 
               public_key_account:str,
               private_key_LP:str, 
               public_key_LP:str
               ):
    
    swap1_address = send_token(token_swap_from,token_amount_to_swap,private_key_account,public_key_LP)

    if swap1_address!=-1:
        swap2_address = send_token(token_swap_to,token_amount_to_recieve,private_key_LP,public_key_account)

        if swap2_address!=-1:
            return (swap1_address,swap2_address)
        return(swap1_address,-1)
    
    return(-1,-1)