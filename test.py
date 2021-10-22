# from web3 import Web3
#
# ### sender_address, receiver_address and private keys are initialised here ###
#
# url = 'http://localhost:8545'
# web3 = Web3(Web3.IPCProvider('/home/trikiomar/.ethereum/geth.ipc'))
# print('Connected?', web3.isConnected()) # OUTPUT ==> True
#
# token_address = '0x6218df99C84B15E19e49Eae2d2369142D22BFE4e'
# BYTECODE = open('contract.bin', 'r').read()
# contract = web3.eth.contract(address=token_address, ABI=ABI)
# print(contract.caller.getPatientById(1))
#
from __future__ import print_function

from solc import compile_source
# from web3 import Web3
#
# w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
# encrypted_key = open('/home/trikiomar/TP2/noeud2/keystore/UTC--2021-09-09T10-29-29.732285980Z'
#                      '--7d4e323e3a056899bd18aa8d80208c202a6b9c5c', 'r').read()


# result = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
# receipt = W3.eth.wait_for_transaction_receipt(result)
# print(receipt)
# store_var_contract = W3.eth.contract(address=address, ABI=contract_interface["ABI"])
# gas_estimate = store_var_contract.functions.createPatient(1, 'omar', 'triki', '2018-01-05').estimateGas()
# print(gas_estimate)
# # print(f'Gas estimate to transact with setVar: {gas_estimate}')
# #
# if gas_estimate < 1000000:
#     print("Sending transaction to setVar(255)\n")
#     store_var_contract = W3.eth.contract(address=address, ABI=contract_interface["ABI"],
#                                          BYTECODE=contract_interface['bin'])
#     deployed = store_var_contract.constructor().transact({'from': address})
#     print(deployed)
#     receipt = W3.eth.wait_for_transaction_receipt(deployed)
#     tx_hash = store_var_contract.functions.createPatient(1, 'omar', 'triki', '2018-01-05').transact(
#         {'from': address}
#     )
#     receipt = W3.eth.wait_for_transaction_receipt(tx_hash)
#     print("Transaction receipt mined:")
#     pprint.pprint(dict(receipt))
#     print(store_var_contract.functions.getPatientById(1).call())
#     print("\nWas transaction successful?")
#     pprint.pprint(receipt["status"])
# else:
#     print("Gas cost exceeds 100000")
from telesign.messaging import MessagingClient
from telesign.util import random_with_n_digits
import sys

if sys.version[0] == "3":
    raw_input = input
customer_id = "55341A14-DF68-4FED-8A75-953CC85136E5"
api_key = "jbuZ01njFKDOFHLwmehzeTBsF1i+72O1NY/TeGLH8BwsZmrRblI4pIOJ3cV4zwBtXImIiHXptshJYqQT9Uw2oA=="

phone_number = "+21644320549"
verify_code = random_with_n_digits(5)

message = "Your code is {}".format(verify_code)
message_type = "OTP"

messaging = MessagingClient(customer_id, api_key)
response = messaging.message(phone_number, message, message_type)
print(verify_code)
user_entered_verify_code = input("Please enter the verification code you were sent: ")

if verify_code == user_entered_verify_code.strip():
    print("Your code is correct.")
else:
    print("Your code is incorrect.")
