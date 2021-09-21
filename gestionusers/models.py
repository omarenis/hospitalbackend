from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import BooleanField, ForeignKey, Model, SET_NULL, TextField
from rest_framework.serializers import ModelSerializer
import string
import random
from common.models import create_model, create_model_serializer

app_label = 'gestionusers'
LOCALISATION_FIELDS = {
    'governorate': TextField(null=False),
    'delegation': TextField(null=False),
    'zipCode': TextField(null=False, db_column='zip_code')
}
Localisation = create_model(name='Localisation', type_model=Model, fields=LOCALISATION_FIELDS,
                            options={
                                'db_table': 'localisations',
                                'unique_together': ('governorate', 'delegation', 'zipCode')
                            },
                            app_label=app_label)


class UserManager(BaseUserManager):
    def create(self, name, familyName, cin, telephone, typeUser, is_active=False, localisation_id=None, email=None,
               password=None, speciality=None):
        data = {'name': name, 'familyName': familyName, 'cin': cin, 'telephone': telephone, 'accountId': None,
                'is_active': is_active, 'password': password, 'email': self.normalize_email(email) if email else email,
                'localisation_id': localisation_id, 'typeUser': typeUser}
        try:
            if typeUser == 'parent':
                user = Parent(**data)
            elif typeUser == 'doctor':
                if speciality is None:
                    return Exception('speciality is required')
                data['speciality'] = speciality
                user = Doctor(**data)
            elif typeUser == 'teacher':
                user = Teacher(**data)
            elif typeUser == 'superdoctor':
                data['is_active'] = True
                user = Person(**data)
            elif typeUser == 'admin':
                data['is_active'] = True
                data['is_superuser'] = True
                data['is_staff'] = True
                user = Person(**data)
            else:
                raise AttributeError('user must be parent or doctor')
            user.username = name + ' ' + familyName + cin
            if is_active:
                user.set_password(password)
            else:
                randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=1258))
                user.set_password(randomstr)
            user.save()
            return user
        except Exception as exception:
            return exception


PERSON_FIElDS = {
    'name': TextField(null=False),
    'familyName': TextField(null=False, db_column='family_name'),
    'cin': TextField(null=False, unique=True),
    'email': TextField(null=True),
    'telephone': TextField(null=False),
    'password': TextField(null=False),
    'accountId': TextField(null=True, db_column='account_id'),
    'is_active': BooleanField(null=False, default=False),
    'typeUser': TextField(null=False, db_column='type_user'),
    'localisation': ForeignKey(null=True, to='Localisation', on_delete=SET_NULL),
    'objects': UserManager()
}

Person = create_model(name='Person', type_model=AbstractUser, fields=PERSON_FIElDS, options={
    'db_table': 'persons'
}, app_label=app_label)


class LocalisationSerializer(ModelSerializer):
    class Meta:
        model = Localisation
        fields = '__all__'
        excludes = ['person_set']


class PersonSerializer(ModelSerializer):
    localisation = LocalisationSerializer(read_only=True, allow_null=True)

    class Meta:
        model = Person
        fields = '__all__'


class Parent(Person):
    class Meta:
        db_table = 'parents'


class Doctor(Person):
    speciality: TextField = TextField(null=False)

    class Meta:
        db_table = 'doctors'


class Teacher(Person):
    class Meta:
        db_table = 'teachers'


ParentSerializer = create_model_serializer(model=Parent, name='ParentSerializer', app_label=app_label)
TeacherSerializer = create_model_serializer(model=Teacher, name='TeacherSerializer', app_label=app_label)
DoctorSerializer = create_model_serializer(model=Doctor, name='DoctorSerializer', app_label=app_label)
