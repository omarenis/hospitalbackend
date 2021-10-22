from django.contrib.auth.hashers import check_password

from backend.settings import API_KEY, CONSUMER_ID
from common.services import Service
from .repositories import DoctorRepository, LocalisationRepository, UserRepository
from telesign.messaging import MessagingClient
from telesign.util import random_with_n_digits


def generate_sms_auth_code(phone_number):
    verify_code = random_with_n_digits(5)
    print(type(verify_code))
    message = "Your code is {}".format(verify_code)
    message_type = "OTP"
    messaging = MessagingClient(CONSUMER_ID, API_KEY)
    messaging.message(phone_number, message, message_type)
    return verify_code


def get_or_create_parent(data):
    person_service = PersonService()
    if data is None:
        return Exception('parent data must be filled')
    parent = person_service.filter_by({'cin': data['cin']}).first()
    if parent is not None:
        if parent.name != data.get('name') or parent.familyName != data.get('familyName') or \
                parent.email != data.get('email') or parent.telephone != data.get('telephone'):
            return Exception('data of parent is incorrect')
        parent_id = parent.id
    else:
        data['is_active'] = False
        parent_id = person_service.create(data)
        if not isinstance(parent_id, Exception):
            parent_id = parent_id.id
    return parent_id


class LocalisationService(Service):
    def __init__(self, repository=LocalisationRepository()):
        super().__init__(repository)


class PersonService(Service):
    def __init__(self, repository=UserRepository()):
        super().__init__(repository)

    def login(self, cin, password):
        user = self.filter_by({'cin': cin}).first()
        if user is not None and user.is_active:
            if check_password(password=password, encoded=user.password):
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


class DoctorService(Service):
    def __init__(self, repository=DoctorRepository()):
        super().__init__(repository)
