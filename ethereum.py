import pandas as pd
from solcx import compile_source, install_solc
from web3 import Web3
from backend.settings import BASE_DIR

W3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
compiled_sol = compile_source(open(BASE_DIR / 'contract.sol').read())
FIRST_ADDRESS = W3.eth.account.privateKeyToAccount(
    '0x70f1384b24df3d2cdaca7974552ec28f055812ca5e4da7a0ccd0ac0f8a4a9b00').address
contract_id, contract_interface = compiled_sol.popitem()
BYTECODE, ABI = contract_interface['bin'], contract_interface['abi']
PRIVATE_KEY = "0x70f1384b24df3d2cdaca7974552ec28f055812ca5e4da7a0ccd0ac0f8a4a9b00"
filename = "patients.csv"
DATA = pd.read_csv('./'+filename)

account = W3.eth.account.create('11608168')


class PrivateData(object):
    def __init__(self):
        self.contract = None
        self.contract_address = None
        self.account = None
        self.private_key = None

    def login(self, private_key: str, password: str):
        try:
            self.account = W3.eth.account.privateKeyToAccount(private_key).address
            unlocked = W3.geth.personal.unlock_account(self.account, password, 1000)
            if unlocked:
                self.deploy_contract()
                self.private_key = private_key
        except Exception as exception:
            return exception

    def signup(self, passphrase):
        account = W3.eth.account.create(passphrase)
        W3.eth.sendTransaction({'to': account.address, 'from': FIRST_ADDRESS, 'value': W3.toWei("200", "ether"),
                                'gasPrice': 2000})
        W3.eth.accounts.append(account.address)
        self.account = account.address
        self.private_key = account.privateKey.hex()
        return self.private_key

    def deploy_contract(self):
        contract_instance = W3.eth.contract(abi=ABI, bytecode=BYTECODE)
        nonce = W3.eth.get_transaction_count(FIRST_ADDRESS)
        tx_hash = contract_instance.constructor().buildTransaction({'from': FIRST_ADDRESS, 'nonce': nonce})
        receipt = W3.eth.get_transaction_receipt(
            W3.eth.send_raw_transaction(W3.eth.account.sign_transaction(tx_hash, PRIVATE_KEY).rawTransaction)
        )
        self.contract_address = receipt['contractAddress']
        self.contract = W3.eth.contract(address=self.contract_address, abi=ABI)

    def get_patient_by_id(self, _id: int):
        data = self.contract.functions.getPatientById(_id).call()
        if data[0] != 0:
            return {
                'id': data[0],
                'name': data[1],
                'familyName': data[2],
                'birthdate': data[3],
                'school': data[4],
                'parent_id': data[5]
            }
        return None

    def create_patient(self, data: dict):
        try:
            dataframe = DATA.append(data, ignore_index=True)
            nonce = W3.eth.get_transaction_count(FIRST_ADDRESS)
            transaction = self.contract.functions.createPatient(data['id'], data['name'], data['familyName'],
                                                                data['birthdate'], data['school'], data['parent_id']
                                                                ).buildTransaction(
                {'nonce': nonce, 'from': FIRST_ADDRESS})
            W3.eth.get_transaction_receipt(
                W3.eth.send_raw_transaction(
                    W3.eth.account.sign_transaction(transaction, PRIVATE_KEY).rawTransaction)
            )
            dataframe.to_csv(filename, index=False)
            return data
        except Exception as exception:
            return exception

    def delete_patient(self, _id: int):
        try:
            for i in DATA.index:
                if int(DATA['id'][i]) == _id:
                    DATA.drop(index=[i], inplace=True)
                    nonce = W3.eth.get_transaction_count(FIRST_ADDRESS)
                    transaction = self.contract.functions.deletePatient(_id).buildTransaction(
                        {'nonce': nonce, 'from': FIRST_ADDRESS}
                    )
                    W3.eth.get_transaction_receipt(
                        W3.eth.send_raw_transaction(
                            W3.eth.account.sign_transaction(transaction, PRIVATE_KEY).rawTransaction)
                    )
                    DATA.to_csv(filename, index=False)
                    return True
            return False
        except Exception as exception:
            return exception

    def update_patient(self, data: dict):
        try:
            for i in DATA.index:
                if int(DATA['id'][i]) == data['id']:
                    DATA.at[i, 'name'] = data['name']
                    DATA.at[i, 'familyName'] = data['familyName']
                    DATA.at[i, 'birthdate'] = data['birthdate']
                    DATA.at[i, 'school'] = data['school']
                    nonce = W3.eth.get_transaction_count(FIRST_ADDRESS)
                    transaction = self.contract.functions.updatePatient(data['id'], data['name'], data['familyName'],
                                                                        data['birthdate'], data['school']
                                                                        ).buildTransaction({'nonce': nonce,
                                                                                            'from': FIRST_ADDRESS})
                    W3.eth.get_transaction_receipt(
                        W3.eth.send_raw_transaction(
                            W3.eth.account.sign_transaction(transaction, PRIVATE_KEY).rawTransaction)
                    )
                    DATA.to_csv(filename, index=False)
                    return data
            return False
        except Exception as exception:
            return exception

    def filter_by(self, data: dict):
        try:
            patient_private_data = self.contract.functions.filterPatient(data['name'],
                                                                         data['familyName'],
                                                                         data['school'],
                                                                         data['birthdate'],
                                                                         data['parent_id']).call()
            if int(patient_private_data[0]) == 0:
                return None
            return {
                'id': patient_private_data[0],
                'name': patient_private_data[1],
                'familyName': patient_private_data[2],
                'birthdate': patient_private_data[3],
                'school': patient_private_data[4],
                'parent_id': patient_private_data[5]
            }
        except Exception as exception:
            return exception

    def recuperate_data(self):
        if self.contract_address is None:
            self.deploy_contract()
            data = pd.read_csv(filename)
            for i in data.index:
                try:
                    nonce = W3.eth.get_transaction_count(FIRST_ADDRESS)
                    transaction = self.contract.functions.createPatient(int(data['id'][i]), data['name'][i],
                                                                        data['familyName'][i],
                                                                        data['birthdate'][i], data['school'][i],
                                                                        int(data['parent_id'][i])
                                                                        ).buildTransaction(
                        {'nonce': nonce, 'from': FIRST_ADDRESS})
                    W3.eth.get_transaction_receipt(
                        W3.eth.send_raw_transaction(
                            W3.eth.account.sign_transaction(transaction, PRIVATE_KEY).rawTransaction)
                    )
                except Exception as exception:
                    self.contract_address = None
                    return exception
            return True


PRIVATE_DATA = PrivateData()
# PRIVATE_DATA.recuperate_data()
