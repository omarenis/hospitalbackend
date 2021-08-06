from django.contrib.auth.hashers import check_password
from common.services import Service
from gestionusers.repositories import LocalisationRepository, UserRepository


def get_or_create_parent(data):
    person_service = PersonService()
    if data is None:
        return Exception('parent data must be filled')
    parent = person_service.filter_by({'cin': data['cin']}).first()
    print(parent)
    if parent is not None:
        if parent.name != data.get('name') or parent.familyName != data.get('familyName') or \
                parent.email != data.get('email') or parent.telephone != data.get('telephone'):
            return Exception('data of parent is incorrect')
        parent_id = parent.id
    else:
        data['is_active'] = False
        parent_id = person_service.create(data)
        print(parent_id)
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
