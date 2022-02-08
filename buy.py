import time
import config as config
from web3 import Web3

# Opens 'abi.txt' and reads it. This is simply housekeeping.
PancakeABI = open('abi.txt', 'r').read()

# Connects to the BSC node to interact with the BSC 
bsc="https://bsc-dataseed.binance.org/"
web3 = Web3(Web3.HTTPProvider(bsc))
print(web3.isConnected())
 
# User must set their own BSC address to this variable
sender_address = config.address

# User must set their wallet private key to this variable
private=config.private

# This is the PancakeSwap V2 Router address
router_address = "0x10ED43C718714eb63d5aA57B78B54704E256024E"
 
# WBNB token address
spend = web3.toChecksumAddress("0xbb4cdb9cbd36b01bd1cbaebf2de08d9173bc095c")
 
# Prints out the balance of the given address
balance = web3.eth.get_balance(sender_address)
humanReadable = web3.fromWei(balance,'ether')
print(humanReadable)
 
# Prompts the user to input the amount of BNB they want to spend
amount = input("Input how much BNB to spend: ")
# Prompts the user to input the address of the token they are buying
contract_id = web3.toChecksumAddress(input("Enter the contract address of token you want to buy: "))

contract = web3.eth.contract(address=router_address, abi=PancakeABI)
nonce = web3.eth.get_transaction_count(sender_address)
start = time.time()
 
pancakeswap2_txn = contract.functions.swapExactETHForTokensSupportingFeeOnTransferTokens(
  0, # This represents slippage. 0 is a market buy, so BE WARY
  [spend,contract_id],
  sender_address,
  (int(time.time()) + 1000000)
).buildTransaction({
  'from': sender_address,
  'value': web3.toWei(amount,'ether'),
  'gas': 1000000,
  'gasPrice': web3.toWei('10','gwei'),
  'nonce': nonce,
})
 
signed_txn = web3.eth.account.sign_transaction(pancakeswap2_txn, private)
tx_token = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
print(web3.toHex(tx_token))