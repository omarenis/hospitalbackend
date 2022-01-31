from common.services import Service
from .repositories import DoctorRepository, LocalisationRepository, UserRepository

URL = "http://localhost:5000/"
application_type = "application/json"


# def sign_in(address, passphrase) -> dict:
#     response = post(URL + 'sign_in', json={"address": address, "passphrase": passphrase})
#     return response.json()


# def create_account(passphrase) -> dict:
#     response = post(URL + 'signup', json={'passphrase': passphrase})
#     return response.json()


# def generate_sms_auth_code(phone_number):
#     verify_code = random_with_n_digits(5)
#     print(type(verify_code))
#     message = "Your code is {}".format(verify_code)
#     message_type = "OTP"
#     messaging = MessagingClient(CONSUMER_ID, API_KEY)
#     messaging.message(phone_number, message, message_type)
#     return verify_code

class PersonService(Service):
    def __init__(self, repository=UserRepository()):
        super().__init__(repository)

    def login(self, cin, password):
        user = self.filter_by({'cin': cin}).first()
        if user is not None and user.is_active:
            if user.check_password(password) and (user.address is not None or user.typeUser == 'admin' or
                                                  user.typeUser == 'superdoctor'):
                return user
            else:
                return Exception('كلمة السر غير صحيحة')
        else:
            return Exception('الحساب غير موجود')

    def reset_password(self, _id: int, password):
        user = self.repository.retreive(_id)
        if user is None:
            return Exception("user not found")
        else:
            user.set_password(password)

    def signup(self, data: dict):
        data['is_active'] = True
        # response = post(URL + 'signup', json={'passphrase': data.get('cin')})
        # if response.status_code != 201:
        #     return Exception(response.json().get('error'))
        # data['address'] = response.json().get('address')
        return super().create(data)


class LocalisationService(Service):
    def __init__(self, repository=LocalisationRepository()):
        super().__init__(repository)


class DoctorService(Service):
    def __init__(self, repository=DoctorRepository()):
        super().__init__(repository)


def get_or_create_parent(data):
    person_service = PersonService()
    if data is None:
        return Exception('parent data must be filled')
    parent_id = person_service.filter_by({'cin': data['cin']}).first()
    if parent_id is not None:
        if parent_id.name != data.get('name') or parent_id.familyName != data.get('familyName') or \
                parent_id.email != data.get('email') or parent_id.telephone != data.get('telephone'):
            return Exception('data of parent is incorrect')
        parent_id = parent_id.id
    else:
        data['is_active'] = False
        parent_id = person_service.create(data)
        if not isinstance(parent_id, Exception):
            parent_id = parent_id.id
    return parent_id
