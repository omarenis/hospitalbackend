from django.urls import path
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from common.views import ViewSet, extract_get_data
from gestionusers.models import DoctorSerializer, LocalisationSerializer, Parent, PersonSerializer
from gestionusers.services import DoctorService, LocalisationService, PersonService, generate_sms_auth_code

PERSON_FIELDS = {
    'name': {'type': 'text', 'required': True},
    'familyName': {'type': 'text', 'required': True},
    'cin': {'type': 'text', 'required': True},
    'email': {'type': 'email', 'required': True},
    'telephone': {'type': 'email', 'required': True},
    'password': {'type': 'password', 'required': True},
    'localisation_id': {'type': 'integer', 'required': False},
    'typeUser': {'type': 'integer', 'required': True},
    'is_active': {'type': 'boolean', 'required': True},
}

DOCTOR_FIELDS = {
    **PERSON_FIELDS,
    'speciality': {'type': 'text', 'required': True}
}


class LocalisationViewSet(ViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes.append(AllowAny)
        else:
            permission_classes.append(IsAdminUser)
        return (permission() for permission in permission_classes)

    def __init__(self, fields=None, serializer_class=LocalisationSerializer, service=LocalisationService(), **kwargs):
        if fields is None:
            fields = {
                'governorate': {'type': 'text', 'required': True},
                'delegation': {'type': 'text', 'required': True},
                'zipCode': {'type': 'text', 'required': True}
            }
        super().__init__(fields, serializer_class, service, **kwargs)


class PersonViewSet(ViewSet):
    def __init__(self, serializer_class=PersonSerializer, service=PersonService(), fields=None, **kwargs):
        if fields is None:
            fields = {
                'name': {'type': 'text', 'required': True},
                'familyName': {'type': 'text', 'required': True},
                'cin': {'type': 'text', 'required': True},
                'email': {'type': 'email', 'required': True},
                'telephone': {'type': 'email', 'required': True},
                'password': {'type': 'password', 'required': True},
                'localisation_id': {'type': 'integer', 'required': False},
                'typeUser': {'type': 'integer', 'required': True},
                'is_active': {'type': 'boolean', 'required': True},
                'speciality': {'type': 'text', 'required': False}
            }
        super().__init__(fields=fields, serializer_class=serializer_class, service=service, **kwargs)
        self.localisation_service = LocalisationService()
        self.code = None
        self.user = None

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list' or self.action == 'retreive':
            permission_classes.append(IsAdminUser)
        elif self.action == 'logout' or self.action == 'delete' or self.action == 'get_parents' \
                or self.action == 'update':
            permission_classes.append(IsAuthenticated)
        elif self.action == 'signup' or self.action == 'login':
            permission_classes.append(AllowAny)
        return [permission() for permission in permission_classes if permission is not None]

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = self.service.retreive(pk)
        if user is None:
            return Response(data={"error": "لم يتم العثور على المستخدم"}, status=404)
        else:
            return Response(data=self.serializer_class(user).data, status=200)

    def get_parents(self, request, *args, **kwargs):
        data = Parent.objects.filter(**extract_get_data(request=request)).distinct()
        if data:
            return Response(data=[self.serializer_class(i).data for i in data], status=200)
        else:
            return Response(data=[], status=200)

    def login(self, request, *args, **kwargs):
        cin = request.data.get('cin')
        if cin is None:
            return Response(data={"error": "الحساب غير موجود"}, status=400)
        password = request.data.get('password')
        if password is None:
            return Response(data={"error": "كلمة المرور غير موجودة"}, status=400)
        user = self.service.login(cin, password)
        if isinstance(user, Exception):
            return Response(data={"error": str(user)}, status=500)
        token = RefreshToken.for_user(user=user)
        return Response(data={
            "access": str(token.access_token),
            "refresh": str(token),
            "userId": user.id,
            "typeUser": user.typeUser,
            "name": user.name,
            "familyName": user.familyName,
            "telephone": user.telephone,
            "email": user.email if user.email is not None else '',
            'cin': user.cin
        })

    def signup(self, request, *args, **kwargs):
        data = {}
        localisation = self.localisation_service.filter_by(request.data.get('localisation')).first()
        if localisation is None:
            localisation = self.localisation_service.create(data=request.data.get('localisation'))
        for i in self.fields:
            data[i] = request.data.get(i)
        data['localisation_id'] = localisation.id
        user = self.service.filter_by({'cin': request.data.get('cin')}).first()
        data['is_active'] = True
        if user is not None:
            if user.is_active:
                return Response(data={'error': 'لقد تم بالفعل إنشاء حساب بهذا الرقم'}, status=HTTP_401_UNAUTHORIZED)
            self.service.put(_id=user.id, data=data)
        else:
            user = self.service.create(data)
        if isinstance(user, Exception):
            return Response(data={"error": str(user)}, status=500)
        else:
            token = RefreshToken.for_user(user=user)
            return Response(data={
                "access": str(token.access_token),
                "refresh": str(token),
                "userId": user.id,
                "typeUser": user.typeUser,
                "name": user.name,
                "familyName": user.familyName,
                "email": user.email
            }, status=HTTP_201_CREATED)

    @staticmethod
    def logout(request, *args, **kwargs):
        token = RefreshToken(request.data.get('refresh'))
        token.blacklist()
        return Response(status=HTTP_204_NO_CONTENT)

    def generate_code(self, request, *args, **kwargs):
        if request.data.get('cin') is None:
            return Response(data={'error': 'يجب عليك إدخال بطاقة التعريف الوطنية الخاصة بك'},
                            status=HTTP_400_BAD_REQUEST)
        else:
            users = self.service.filter_by({'cin': request.data.get('cin')})
            if users:
                self.user = users[0]
                telephone = self.user.telephone
                try:
                    self.code = generate_sms_auth_code(telephone)
                except Exception as exception:
                    return Response(data={'error': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
                return Response(data={'response': 'code sent as sms to your phone'})
            else:
                return Response({'error': 'بطاقة التعريف الوطنية الخاصة بك غير مسجّل في الموقع\nالرجاء التسجيل في '
                                          'الموقع بإستعمال بطاقة التعريف'})

    def verify_code(self, request, *args, **kwargs):
        if request.data.get('code') != self.code:
            return Response(data={
                'error': 'الرمز المكتوب غير صحيح',
                'correct_code': self.code,
                'inserted_code': request.data.get('code')
            }, status=HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            self.user.set_password(request.data.get('password'))
            return Response(data={'response': 'تم تغيير كلمة السر بنجاح'}, status=HTTP_201_CREATED)


class DoctorViewSet(ViewSet):
    def get_permissions(self):
        permission_class = []
        if self.action == 'list':
            permission_class.append(AllowAny)
        elif self.action == 'retreive':
            permission_class.append(IsAuthenticated)
        return [permission() for permission in permission_class]

    def __init__(self, fields=None, serializer_class=DoctorSerializer, service=DoctorService(), **kwargs):
        if fields is None:
            fields = DOCTOR_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


users_list, user_retrieve_update_delete = PersonViewSet.get_urls()
doctor_list, doctor = DoctorViewSet.get_urls()
parent_list = PersonViewSet.as_view({
    'get': 'get_parents'
})
login = PersonViewSet.as_view({
    'post': 'login'
})
signup = PersonViewSet.as_view({
    'post': 'signup'
})
logout = PersonViewSet.as_view({
    'post': 'logout'
})
generate_sms_code = PersonViewSet.as_view({
    'post': 'generate_code'
})
verify_code = PersonViewSet.as_view({
    'post': 'verify_code'
})
urlpatterns = [
    path('', users_list),
    path('<int:pk>', user_retrieve_update_delete),
    path('login', login),
    path('signup', signup),
    path('logout', logout),
    path('doctors', doctor_list),
    path('doctors/<int:pk>', doctor),
    path('parents', parent_list),
    path('generate_code', generate_sms_code),
    path('verify_code', verify_code)
]
