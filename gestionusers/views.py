from django.urls import path
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_401_UNAUTHORIZED
from rest_framework_simplejwt.tokens import RefreshToken
from common.views import ViewSet
from gestionusers.models import LocalisationSerializer, PersonSerializer
from gestionusers.services import LocalisationService, PersonService


class LocalisationViewSet(ViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes.append(AllowAny)
        else:
            permission_classes.append(IsAdminUser)
        return [permission() for permission in permission_classes]

    def __init__(self, fields=None,
                 serializer_class=LocalisationSerializer,
                 service=LocalisationService(),
                 **kwargs):
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
                'is_active': {'type': 'boolean', 'required': True}
            }
        super().__init__(fields=fields, serializer_class=serializer_class, service=service, **kwargs)
        self.localisation_service = LocalisationService()

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes.append(IsAdminUser)
        elif self.action == 'retrieve' or self.action == 'logout':
            permission_classes.append(IsAuthenticated)
        elif self.action == 'signup' or self.action == 'login':
            permission_classes.append(AllowAny)
        return [permission() for permission in permission_classes if permission is not None]

    def retrieve(self, request, pk=None, *args, **kwargs):
        user = self.service.retreive(pk)
        if user is None:
            return Response(data={"error": "لم يتم العثور على المستخدم"}, status=404)
        else:
            return Response(data=self.serializer_class(data=user).data, status=200)

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
            "user": user.name + ' ' + user.familyName
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
                "username": user.name + ' ' + user.familyName,
                "name": user.name,
                "familyName": user.familyName,
                "cin": user.cin,
                "telephone": user.telephone,
                "email": user.email,
            })

    @staticmethod
    def logout(request, *args, **kwargs):
        token = RefreshToken(request.data.get('token').encode('utf-8'))
        token.blacklist()
        return None


users_list, user_retrieve_update_delete = PersonViewSet.get_urls()

login = PersonViewSet.as_view({
    'post': 'login'
})
signup = PersonViewSet.as_view({
    'post': 'signup'
})
logout = PersonViewSet.as_view({
    'post': 'logout'
})

urlpatterns = [
    path('', users_list),
    path('<int:user_id>', user_retrieve_update_delete),
    path('login', login),
    path('signup', signup),
    path('logout', logout)
]
