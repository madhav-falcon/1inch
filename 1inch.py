#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 22 16:14:51 2021

@author: madhavrai
"""
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 14 14:27:05 2021

@author: madhavrai
"""
import requests

import cryptocompare
from web3 import Web3
import math



def get_price(symbol , token):
    symbol = symbol.upper()
    a = cryptocompare.get_price(symbol, currency=token)
    return float(a[symbol][token])

def buy_token2(amountToken1=0 , amountToken2=0, token1 = "USDC" , token2="ETH"):
  token1 = token1.upper()
  
  token2= token2.upper()
  
  token_map = {"USDC":["0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48", 6], "USDT" : ["0xdac17f958d2ee523a2206206994597c13d831ec7",6] , "WBTC":["0x2260fac5e5542a773aa44fbcfedf7c193bc2c599",8],"ETH":["0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee",18]}
  
  decimals_1 = token_map[token1][1]
  
  address_1 = token_map[token1][0]
  
  decimals_2 = token_map[token2][1]
  
  address_2 = token_map[token2][0]
  amount = amountToken1
  price = get_price(token2,token1)
  print(price)
  if amountToken2>0:
    amount = amount + amountToken2*price
  
  
  amount = str(int(amount*10**decimals_1))
  
  r= requests.get('https://api.1inch.exchange/v3.0/1/quote?fromTokenAddress=' + address_1 + "&toTokenAddress="  + address_2 +  "&amount=" + amount).json()
  
  if token2!="ETH":
    token2 = float(r["toTokenAmount"]) - float(r["estimatedGas"]*10**(decimals_2-9))*get_price("ETH",token2)
  else:
    token2 = float(r["toTokenAmount"]) - float(r["estimatedGas"]*10**9)
       
  token1 = float(r["fromTokenAmount"])
  
  executed_price = token1*10**(decimals_2-decimals_1)/token2
  print(address_1)
  
  slippage = (1-price/executed_price)*100
  implied_volatility_daily = 5
  
  implied_volatility_30s = implied_volatility_daily/math.sqrt(2880)
  estimated_slippage_percent = slippage + 0.5*implied_volatility_30s
  print(estimated_slippage_percent)
  safe_slippage_percent = slippage + 6*implied_volatility_30s
  
  tx = get_transaction(amount , safe_slippage_percent , "buy" ,address_1 , address_2 )
  
  return estimated_slippage_percent, tx

  
def get_transaction(amount,slippage, side,address_1, address_2):
    print(slippage)
    
    slippage = round(slippage,3)
    #public_adress = os.environ.get("public-key")
    print(amount)
    public_adress ='0x73bceb1cd57c711feac4224d062b0f6ff338501e'#largest eth wallet added for testing purposes(can comment out public_adress = os.environ.get("public-key"))
    link = 'https://api.1inch.exchange/v3.0/1/swap?fromTokenAddress=' + address_1 + "&toTokenAddress=" + address_2  + "&amount=" + str(amount) + "&fromAddress=" + public_adress + "&slippage=" + str(slippage)
    print(link)
    
    r = requests.get(link)
  
    return r.json()


def execute_transaction(tx):
  w3 = Web3(Web3.HTTPProvider('https://mainnet.infura.io/v3/699154aa8e20430a9e615fd70f98d5cd'))
  
  connected = w3.isConnected()
  
  print(connected)
  
  public_adress = os.environ.get("public-key")
  
  
  
  private_key = os.environ.get("private-key")
  
  
  
  adress1 = Web3.toChecksumAddress(public_adress)
  
  adress2 = Web3.toChecksumAddress(tx["to"])
  
  nonce = w3.eth.getTransactionCount(adress1)
  
  print(nonce)
  
  tx["nonce"] = nonce
  
  tx["value"] = int(tx["value"])
  
  tx["gasPrice"] = int(tx["gasPrice"])
  tx["to"] = adress2
  
  
  
  
  
  
  signed_tx = w3.eth.account.signTransaction(tx,private_key)
  
  
  print(signed_tx) 
  
  tx_hash = w3.eth.sendRawTransaction(signed_tx.rawTransaction)
  
  return "done"




slippage, tx = buy_token2(token1="eth" , token2 = "usdc" , amountToken2 = 100000)

#a = execute_transaction(tx)





#0.5 rights side of the bell curve







