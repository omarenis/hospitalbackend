from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import BooleanField, CharField, EmailField, Model, TextField
from rest_framework.serializers import ModelSerializer
import string
import random
from common.models import create_model

LOCALISATION_FIELDS = {
    'governorate': TextField(null=False),
    'delegation': TextField(null=False),
    'zipCode': TextField(null=False, db_column='zip_code')
}
Localisation = create_model(name='Localisation', type_model=Model, fields=LOCALISATION_FIELDS, options={
    'db_table': 'localisations',
    'unique_together': ('governorate', 'delegation', 'zipCode')
}, app_label='gestionusers')


class UserManager(BaseUserManager):
    def create(self, name, familyName, cin, telephone, email, typeUser, is_active, password=None):
        data = {'name': name, 'familyName': familyName, 'cin': cin, 'telephone': telephone,
                'email': self.normalize_email(email), 'accountId': None, 'is_active': is_active,
                'password': password}
        try:
            if typeUser == 'parent':
                user = Parent(**data)
            elif typeUser == 'doctor':
                user = Doctor(**data)
            else:
                raise AttributeError('user must be parent or doctor')
            user.username = name + ' ' + familyName
            if is_active:
                user.set_password(password)
            else:
                randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=1258))
                user.set_password(randomstr)
            user.save()
            return user
        except Exception as exception:
            return exception


class Person(AbstractUser):
    objects = UserManager()
    name: TextField = TextField(null=False)
    familyName: TextField = TextField(null=False, db_column='family_name')
    cin: CharField = CharField(max_length=255, null=False, unique=True)
    email: EmailField = EmailField(null=False, unique=True)
    telephone: CharField = CharField(max_length=255, null=False, unique=True)
    password: TextField = TextField(null=True)
    accountId: TextField = TextField(null=True, db_column='account_id')
    is_active = BooleanField(null=False, default=False)
    typeUser: TextField = TextField(null=False)

    class Meta:
        db_table = 'persons'


class PersonSerializer(ModelSerializer):
    class Meta:
        model = Person
        fields = '__all__'
        excludes = ['password', 'accountId']


class Parent(Person):

    class Meta:
        db_table = 'parents'


class Doctor(Person):

    class Meta:
        db_table = 'doctors'


class LocalisationSerializer(ModelSerializer):
    class Meta:
        model = Localisation
        fields = '__all__'
        excludes = ['person_set']
