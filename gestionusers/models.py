from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.db.models import CASCADE, CharField, EmailField, ForeignKey, Model, OneToOneField, SET_NULL, TextField, \
    BooleanField, BigIntegerField
import string
import random
from common.models import create_model, create_model_serializer

app_label = 'gestionusers'


# create the user manager and the person manager
class UserManager(BaseUserManager):
    def create(self, name: str, loginNumber: str, telephone: str, password: str, typeUser: str, localisation_id=None,
               email=None):
        data = {
            'name': name,
            'loginNumber': loginNumber,
            'telephone': telephone,
            'typeUser': typeUser,
            'localisation_id': localisation_id,
            'email': self.normalize_email(email) if email is not None else None,
            'username': loginNumber
        }
        if typeUser == 'school':
            user = School(**data)
        else:
            data['is_active'] = True
            data['is_superuser'] = True
            data['is_staff'] = True
            user = User(**data)
        user.set_password(password)
        user.save()
        return user


class PersonManager(UserManager):
    def create(self, name: str, loginNumber: str, telephone: str, typeUser: str, familyName: str = None,
               address=None, is_active=False, localisation_id=None, email=None, password=None, speciality=None,
               super_doctor_id=None, is_super=False):
        try:
            data = {
                'name': name,
                'familyName': familyName,
                'loginNumber': loginNumber,
                'telephone': telephone,
                'typeUser': typeUser,
                'address': address,
                'is_active': is_active,
                'localisation_id': localisation_id,
                'username': loginNumber
            }
            if typeUser == 'admin' or typeUser == 'school':
                return super().create(name=name, loginNumber=loginNumber, telephone=telephone, password=password,
                                      typeUser=typeUser, email=email, localisation_id=localisation_id)
            if familyName is None:
                return Exception('familyName is required')
            if typeUser == 'parent':
                user = Parent(**data)
            elif typeUser == 'superdoctor':
                data['is_super'] = True
                data['speciality'] = ''
                user = Doctor(**data)
            elif typeUser == 'doctor':
                if speciality is None:
                    return Exception('speciality is required')
                if super_doctor_id is None:
                    return Exception('doctor must be associated to super doctor')
                data['speciality'] = speciality
                data['is_super'] = False
                data['super_doctor_id'] = super_doctor_id
                data['typeUser'] = 'superdoctor'
                user = Doctor(**data)
            elif typeUser == 'teacher':
                user = Teacher(**data)
            else:
                raise AttributeError('user must be parent, teacher or doctor')
            random_str = ''.join(random.choices(string.ascii_letters + string.digits, k=1258)) if not is_active else \
                password
            print(user)
            user.set_password(random_str)
            user.save()
            return user
        except Exception as exception:
            print(exception)
            return exception


LOCALISATION_FIELDS = {
    'governorate': TextField(null=False),
    'delegation': TextField(null=False),
    'zipCode': TextField(null=False, db_column='zip_code')
}
USER_FIELD = {
    'name': TextField(null=False),
    'email': EmailField(null=True),
    'loginNumber': CharField(null=False, unique=True, max_length=9, db_column='login_number'),
    'telephone': TextField(null=False),
    'password': TextField(null=False),
    'address': TextField(null=True, default=None),
    'typeUser': TextField(null=False, db_column='type_user'),
    'localisation': ForeignKey(null=True, to='Localisation', on_delete=SET_NULL),
    'objects': PersonManager()
}
PERSON_FIElDS = {
    'familyName': TextField(null=False, db_column='family_name')
}

PARENT_FIELDS = {}
DOCTOR_FIELDS = {
    'is_super': BooleanField(null=False, default=False),
    'speciality': TextField(null=False),
    'super_doctor_id': BigIntegerField(null=True)
}
TEACHER_FIELDS = {}

# create models
Localisation = create_model(name='Localisation', type_model=Model, fields=LOCALISATION_FIELDS,
                            options={
                                'db_table': 'localisations',
                                'unique_together': ('governorate', 'delegation', 'zipCode')
                            },
                            app_label=app_label)

User = create_model(name='User', type_model=AbstractUser, fields=USER_FIELD, options={'db_table': 'users'},
                    app_label=app_label)

School = create_model(name='School', type_model=User, fields={}, options={'db_table': 'schools'}, app_label=app_label)

Person = create_model(name='Person', type_model=User, fields=PERSON_FIElDS, options={'db_table': 'persons'},
                      app_label=app_label)

Parent = create_model(name='Parent', type_model=Person, fields=PARENT_FIELDS, options={'db_table': 'parents'},
                      app_label=app_label)
Doctor = create_model(name='Doctor', type_model=Person, fields=DOCTOR_FIELDS, app_label=app_label,
                      options={'db_table': 'doctors'})
Teacher = create_model(name='Teacher', type_model=Person, fields=TEACHER_FIELDS,
                       options={'db_table': 'teachers'}, app_label=app_label)
SchoolTeacherIds = create_model(name='SchoolTeacherIds', type_model=Model, fields={
    'teacher': OneToOneField(to='Teacher', on_delete=CASCADE, null=False),
    'school': ForeignKey(to='School', on_delete=CASCADE, null=False)
}, app_label=app_label, options={'db_table': 'school_teacher_ids', 'unique_together': ('school_id', 'teacher_id')})
LocalisationSerializer = create_model_serializer(name='LocalisationSerializer', model=Localisation, app_label=app_label,
                                                 options={'fields': '__all__', 'excludes': ['person_set']})

UserSerializer = create_model_serializer(model=User, name='UserSerializer', app_label=app_label,
                                         options={
                                             'fields': ['id', 'name', 'email', 'telephone', 'email',
                                                        'localisation', 'typeUser', 'loginNumber', 'password'],
                                             'depth': 1},
                                         fields={'localisation': LocalisationSerializer(read_only=True)})
PersonSerializer = create_model_serializer(name='PersonSerializer', model=Person, app_label=app_label, fields={
    'localisation': LocalisationSerializer(read_only=True, allow_null=True),
}, options={'fields': ['id', 'name', 'loginNumber', 'localisation', 'telephone', 'typeUser', 'familyName', 'email',
                       'password'],
            'depth': 1})
ParentSerializer = create_model_serializer(model=Parent, name='ParentSerializer', app_label=app_label)
TeacherSerializer = create_model_serializer(model=Teacher, name='TeacherSerializer', app_label=app_label)
DoctorSerializer = create_model_serializer(model=Doctor, name='DoctorSerializer', app_label=app_label,
                                           options={'fields': ['id', 'name', 'loginNumber', 'localisation', 'telephone',
                                                               'typeUser', 'email', 'password', 'speciality'],
                                                    'depth': 1})
