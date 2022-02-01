from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import BooleanField, CASCADE, EmailField, ForeignKey, Model, SET_NULL, TextField
from rest_framework.serializers import ModelSerializer
import string
import random
from common.models import create_model, create_model_serializer


# create the user manager and the person manager
class UserManager(BaseUserManager):
    def create(self, name, loginNumber, telephone, password, typeUser, localisation_id=None,
               email=None):
        data = {
            'name': name,
            'loginNumber': loginNumber,
            'telephone': telephone,
            'typeUser': typeUser,
            'localisation_id': localisation_id,
            'email': self.normalize_email(email) if email is not None else None
        }
        user = None
        if typeUser == 'school':
            user = School(**data)
        elif typeUser == 'admin' or typeUser == 'superdoctor':
            data['is_active'] = True
            data['is_superuser'] = True
            data['is_staff'] = True
            user = Person(**data)

        user.save()
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
                is_active = True
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
                print(password)
                user.set_password(password)
            else:
                randomstr = ''.join(random.choices(string.ascii_letters + string.digits, k=1258))
                user.set_password(randomstr)
            user.save()
            return user
        except Exception as exception:
            return exception


class PersonManager(UserManager):
    def create(self, name, familyName, cin, telephone, typeUser, address=None, is_active=False, localisation_id=None,
               email=None, password=None, speciality=None):

app_label = 'gestionusers'
LOCALISATION_FIELDS = {
    'governorate': TextField(null=False),
    'delegation': TextField(null=False),
    'zipCode': TextField(null=False, db_column='zip_code')
}
USER_FIELD = {
    'name': TextField(null=False),
    'email': EmailField(null=True),
    'loginNumber': TextField(null=False, unique=True),
    'telephone': TextField(null=False),
    'password': TextField(null=False),
    'typeUser': TextField(null=False),
    'localisation': ForeignKey(null=False, to='Localisation', on_delete=SET_NULL),
    'objcts': UserManager()
}

PERSON_FIElDS = {
    'familyName': TextField(null=False, db_column='family_name'),
    'address': TextField(null=True, db_column='address'),
    'is_active': BooleanField(null=False, default=False),
}

PARENT_FIELDS = {}
DOCTOR_FIELDS = {'speciality': TextField(null=False)}
TEACHER_FIELDS = {'school': ForeignKey(null=False, to='School', on_delete=CASCADE)}

# create models
Localisation = create_model(name='Localisation', type_model=Model, fields=LOCALISATION_FIELDS,
                            options={
                                'db_table': 'localisations',
                                'unique_together': ('governorate', 'delegation', 'zipCode')
                            },
                            app_label=app_label)


User = create_model(name='User', type_model=AbstractUser, fields=USER_FIELD, options={'db_table': 'persons'},
                    app_label=app_label)

School = create_model(name='School', type_model=User, fields={}, options={'db_tables': 'schools'}, app_label=app_label)

Person = create_model(name='Person', type_model=User, fields=PERSON_FIElDS, options={'db_table': 'persons'},
                      app_label=app_label)

Parent = create_model(name='Parent', type_model=Person, fields={}, options={'db_table': 'parents'})
Doctor = create_model(name='Doctor', type_model=Person, fields={})
Teacher = create_model(name='Teacher', type_model=Person, fields=TEACHER_FIELDS, options={'db-table': 'teachers'})


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


ParentSerializer = create_model_serializer(model=Parent, name='ParentSerializer', app_label=app_label)
TeacherSerializer = create_model_serializer(model=Teacher, name='TeacherSerializer', app_label=app_label)
DoctorSerializer = create_model_serializer(model=Doctor, name='DoctorSerializer', app_label=app_label)
