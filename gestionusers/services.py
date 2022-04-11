from common.repositories import Repository
from common.services import Service
from .models import Doctor, Localisation, Person, SchoolTeacherIds, Teacher, User
from cryptography.fernet import Fernet
from base64 import b64encode
from hashlib import pbkdf2_hmac

URL = "http://localhost:5000/"

FERNET = Fernet(
    b64encode(pbkdf2_hmac("sha256", "hEq52fRbu1WGrU2TIsZ3vtFf7xJp2SMOEC4-olvJ3hA=".encode("ascii"),
                          "hEq52fRbu1WGrU2TIsZ3vtFf7xJp2SMOEC4".encode("ascii"),
                          1000))
)

LOCALISATION_FIELDS = {
    'governorate': {'type': 'text', 'required': True},
    'delegation': {'type': 'text', 'required': True},
    'zipCode': {'type': 'text', 'required': True}
}

USER_FIELDS = {
    'name': {'type': 'text', 'required': True},
    'loginNumber': {'type': 'text', 'required': True},
    'email': {'type': 'email', 'required': False},
    'telephone': {'type': 'email', 'required': True},
    'password': {'type': 'password', 'required': True},
    'typeUser': {'type': 'text', 'required': True}
}

PERSON_FIELDS = {
    **USER_FIELDS,
    'localisation_id': {'type': 'integer', 'required': False},
    'familyName': {'type': 'text', 'required': True}
}

DOCTOR_FIELDS = {
    **PERSON_FIELDS,
    'speciality': {'type': 'text', 'required': False},
    'is_super': {'type': 'bool', 'required': False}
}


class UserService(Service):
    def __init__(self, repository=Repository(model=User)):
        super().__init__(repository, fields=USER_FIELDS)

    def retrieve(self, _id: int):
        user = super().retrieve(_id)
        if user.typeUser == 'doctor':
            return DoctorService().retrieve(_id=_id)
        return user


class LoginSignUpService(object):
    def __init__(self):
        self.user_service = UserService()
        self.person_service = PersonService()

    def login(self, login_number: str, password: str):
        user = self.user_service.filter_by({'loginNumber': login_number}).first()
        if user is not None and user.is_active:
            print(user.localisation_id)
            if user.check_password(password) and (user.localisation_id is not None or user.typeUser == 'admin' or
                                                  user.typeUser == 'superdoctor'):
                return user
            elif not user.is_active:
                return Exception('الحساب غير مفعّل')
            else:
                return Exception('كلمة السر غير صحيحة')
        else:
            return Exception('الحساب غير موجود')

    def signup(self, data: dict):
        localisation_id = data.get('localisation_id')
        if data.get('localisation_id') is None:
            localisation_service = LocalisationService()
            localisation = localisation_service.filter_by(data.get('localisation')).first()
            if localisation is None:
                localisation = localisation_service.create(data=data.get('localisation'))
            if isinstance(localisation, Exception):
                return localisation
            localisation_id = localisation.id
        data['is_active'] = True
        data['localisation_id'] = localisation_id
        data['typeUser'] = 'parent'
        return self.person_service.create(data)


class PersonService(Service):
    def __init__(self, repository=Repository(model=Person)):
        super().__init__(repository, fields=PERSON_FIELDS)

    def reset_password(self, _id: int, password):
        user = self.repository.retrieve(_id)
        if user is None:
            return Exception("user not found")
        else:
            user.set_password(password)
        return user

    def create(self, data: dict):
        if data.get('school_id') is not None:
            school_id = data.pop('school_id')
            user = super().create(data)
            if isinstance(user, Exception):
                return user
            SchoolTeacherIds.objects.create(school_id=school_id, teacher_id=user.id)
            return user
        return super().create(data)

    def filter_by(self, data: dict):
        if data.get('typeUser') == 'teacher':
            self.repository = Repository(model=Teacher)
            print(self.repository.model)
        return self.repository.filter_by(data=data)


class LocalisationService(Service):
    def __init__(self, repository=Repository(model=Localisation)):
        super().__init__(repository, fields=LOCALISATION_FIELDS)


class DoctorService(Service):
    def __init__(self, repository=Repository(model=Doctor)):
        super().__init__(repository, fields=DOCTOR_FIELDS)
