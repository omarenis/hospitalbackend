from requests import get, post, put, delete
from unittest import TestCase, main

URL = "http://localhost:5000/"
application_type = "application/json"


def sign_in(address, passphrase) -> dict:
    response = post(URL + 'sign_in', json={"address": address, "passphrase": passphrase})
    return response.json()


def create_account(passphrase) -> dict:
    response = post(URL + 'signup', json={'passphrase': passphrase})
    return response.json()


def get_patient_by_id(_id: int, contract_address: str):
    response = get(URL + f'patients/${_id}', params={
        'contractAddress': contract_address
    })
    if response.status_code != 200:
        return Exception('patient not found')
    else:
        return response.json()


def create_patient(patient: dict, account: dict, access: str) -> dict:
    response = post(URL + 'patients',
                    json=
                    {
                        "patient": patient,
                        "account": account,
                    },
                    headers=
                    {
                        "Content-Type": application_type,
                        "Accept": application_type,
                        "Authorization": f"Bearer {access}"
                    })
    return response.json()


def update_patient(_id: int, patient: dict, account: dict, access: str) -> dict:
    contract_address = patient.pop("contractAddress")
    response = put(URL + f'patients/{_id}',
                   headers=
                   {
                       "Content-Type": application_type,
                       "Accept": application_type,
                       "Authorization": f"Bearer {access}"
                   },
                   json={
                       "patient": patient,
                       "account": account
                   },
                   params={"contractAddress": contract_address})
    return response.json()


def delete_patient(patient: dict, access: str, account: dict):
    response = delete(URL + f"patients/{patient.get('id')}",
                      headers=
                      {
                          "Content-Type": application_type,
                          "Accept": application_type,
                          "Authorization": f"Bearer {access}"
                      },
                      json={
                          "address": account.get("address"),
                          "passphrase": account.get("passphrase")
                      },
                      params={
                          "contractAddress": patient.get("contractAddress")
                      }
                      )
    return response.json()


class TestFlaskFunctions(TestCase):

    def setUp(self) -> None:
        self.account = create_account('11608168')
        print(self.account.get('address'))
        self.account = sign_in(address=self.account.get('address'), passphrase='11608168')

    # def test_create_account(self):
    #     self.account = create_account('11608168')
    #     print(self.account)
    #     self.assertIsNotNone(self.account.get('address'))

    def test_sign_in(self):
        address = "0x1AAE24b1367fd015E45bBa03AF6Eb427b73E4da4"
        cin = "11608168"
        self.account = {
            "address": address,
            "passphrase": cin
        }
        self.account = sign_in(address=self.account.get("address"), passphrase=self.account.get("passphrase"))
        self.assertIsNotNone(self.account.get('access'))

    # def test_create_patient(self):
    #     patient = {
    #         'id': 1,
    #         'name': 'omar',
    #         'familyName': 'triki',
    #         'birthdate': '2017-02-01',
    #         'school': 'saida',
    #         'parentId': 2
    #     }
    #     account = {
    #         "address": self.account.get('address'),
    #         "passphrase": "11608168"
    #     }
    #     response = create_patient(patient=patient, account=account, access=self.account.get("access"))
    #     print(response)
    #     self.assertIsNotNone(response.get('id'))
    #
    # def test_update_patient(self):
    #     patient = {
    #         'id': 1,
    #         'name': 'ahmed',
    #         'familyName': 'triki',
    #         'birthdate': '2017-02-01',
    #         'school': 'saida',
    #         'parentId': 2,
    #         "contractAddress": "0xE7deC18DfcDbaF0Df5aa32a1f1B64C69781A95A3"
    #     }
    #     account = {
    #         "address": self.account.get('address'),
    #         "passphrase": "11608168"
    #     }
    #     patient = update_patient(1, patient=patient, account=account, access=self.account.get('access'))
    #     self.assertIsNotNone(patient.get('id'))
    #
    # def test_get_patient_by_id(self):
    #     _id = 1
    #     contract_address = "0xE7deC18DfcDbaF0Df5aa32a1f1B64C69781A95A3"
    #     response = get_patient_by_id(_id=_id, access=self.account.get('access'), contract_address=contract_address)
    #     self.assertIsNotNone(response.get('id'))
    #
    # def test_delete_patient(self):
    #     patient = {
    #         "id": 1,
    #         "contractAddress": "0xE7deC18DfcDbaF0Df5aa32a1f1B64C69781A95A3"
    #     }


if __name__ == '__main__':
    main()
