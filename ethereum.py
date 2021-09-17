import time

from web3 import Web3

W3 = Web3(Web3.IPCProvider('/home/trikiomar/TP2/noeud2/geth.ipc'))
BYTECODE = open('contract.bin', 'r').read()
ABI = open('abi-contrat.json', 'r').read()


class PrivateData(object):
    def __init__(self):
        self.contract = None
        self.contract_address = None
        self.account = None
        self.private_key = None

    def login(self, private_key: str, password: str):
        try:
            self.account = W3.geth.personal.import_raw_key(private_key, password)
            unlocked = W3.geth.personal.unlock_account(W3.geth.personal.import_raw_key(private_key, password), password)
            if unlocked:
                self.deploy_contract()
                self.private_key = private_key
        except Exception as exception:
            return exception

    def signup(self, passphrase):
        account = W3.eth.account.create(passphrase)
        cointbase = W3.eth.coinbase
        W3.geth.miner.set_etherbase(account.address)
        W3.geth.miner.start(1)
        time.sleep(300)
        W3.geth.miner.stop()
        W3.geth.miner.set_etherbase(cointbase)
        self.private_key = account.privateKey.hex()
        return self.private_key

    def deploy_contract(self):
        nonce = W3.eth.get_transaction_count(self.account)
        contract_instance = W3.eth.contract(abi=ABI, bytecode=BYTECODE)
        gas_price = contract_instance.constructor().estimateGas()
        tx_hash = contract_instance.constructor().buildTransaction(
            {
                'gasPrice': gas_price,
                'chainId': W3.eth.chain_id,
                'from': self.account,
                'nonce': nonce
            }
        )
        signed_tx = W3.eth.account.sign_transaction(tx_hash, self.private_key)
        result = W3.eth.send_raw_transaction(signed_tx.rawTransaction)
        receipt = W3.eth.wait_for_transaction_receipt(result)
        self.contract_address = receipt['contractAddress']
        self.contract = W3.eth.contract(address=self.contract_address, abi=ABI)
