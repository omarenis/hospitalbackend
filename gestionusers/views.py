from django.contrib.auth.models import AnonymousUser
from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet as RestViewSet
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_401_UNAUTHORIZED, HTTP_404_NOT_FOUND, \
    HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework_simplejwt.tokens import RefreshToken
from common.views import ViewSet, extract_serialized_objects_response, return_serialized_data_or_error_response
from gestionusers.models import DoctorSerializer, LocalisationSerializer, PersonSerializer, UserSerializer
from gestionusers.services import DoctorService, LocalisationService, LoginSignUpService, PersonService, UserService


class TokenViewSet(RestViewSet):
    service = PersonService()
    localisation_service = LocalisationService()
    login_sign_up_service = LoginSignUpService()

    def get_permissions(self):
        if self.action == 'logout':
            return [IsAuthenticated()]
        return [AllowAny()]

    def login(self, request, *args, **kwargs):
        login_number = request.data.get('loginNumber')
        if login_number is None:
            return Response(data={"exists": False}, status=400)
        password = request.data.get('password')
        if password is None:
            return Response(data={
                "exists": "كلمة المرور غير موجودة",
                "passwordMatches": False}, status=400)
        user = self.login_sign_up_service.login(login_number=login_number, password=password)
        if isinstance(user, Exception):
            return Response(data={"error": str(user)}, status=500)
        token = RefreshToken.for_user(user=user)
        return Response(data={
            "access": str(token.access_token),
            "refresh": str(token),
            "userId": user.id,
            "typeUser": user.typeUser,
            "name": user.name,
            "familyName": user.familyName if hasattr(user, "familyName") else None
        })

    def signup(self, request, *args, **kwargs):
        data = {}
        localisation = self.localisation_service.filter_by(request.data.get('localisation')).first()
        if localisation is None:
            localisation = self.localisation_service.create(data=request.data.get('localisation'))
        for i in self.service.fields:
            data[i] = request.data.get(i)
        data['localisation_id'] = localisation.id
        user = self.service.filter_by({'loginNumber': request.data.get('loginNumber')}).first()
        data['is_active'] = True
        if user is not None:
            if user.is_active:
                return Response(data={'created': True}, status=HTTP_401_UNAUTHORIZED)
            self.service.put(_id=user.id, data=data)
        else:
            user = self.login_sign_up_service.signup(data)
        if isinstance(user, Exception):
            return Response(data={"error": str(user)}, status=500)
        else:
            return Response(data={
                "created": True,
            }, status=HTTP_201_CREATED)


class LocalisationViewSet(ViewSet):

    def get_permissions(self):
        permission_classes = []
        if self.action == 'list':
            permission_classes.append(AllowAny)
        else:
            permission_classes.append(IsAdminUser)
        return (permission() for permission in permission_classes)

    def __init__(self, fields=None, serializer_class=LocalisationSerializer, service=LocalisationService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


@csrf_exempt
@api_view(http_method_names=['POST'])
def logout(request, *args, **kwargs):
    token = RefreshToken(request.data.get('refresh'))
    token.blacklist()
    return Response(status=HTTP_204_NO_CONTENT)


class UserViewSet(ViewSet):
    def __init__(self, serializer_class=UserSerializer, service=UserService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)
        self.localisation_service = LocalisationService()

    def create(self, request, *args, **kwargs):
        data = {}
        if request.user.typeUser == 'school':
            self.service = PersonService()
            self.serializer_class = PersonSerializer
            if request.data.get('school_id') is None:
                return Response(data={'error', 'school is required for teacher'}, status=HTTP_400_BAD_REQUEST)
            data['school_id'] = request.user.id
        elif request.user.typeUser == 'superdoctor':
            self.service = DoctorService()
            self.serializer_class = DoctorSerializer
        self.fields = self.service.fields
        for i in self.fields:
            data[i] = request.data.get(i)
        if request.data.get('typeUser') != 'superdoctor':
            localisation = self.localisation_service.filter_by(request.data.get('localisation')).first()
            if localisation is None:
                localisation = self.localisation_service.create(data=request.data.get('localisation'))
            data['localisation_id'] = localisation.id
        user = self.service.filter_by({'loginNumber': request.data.get('loginNumber')}).first()
        data['is_active'] = True
        if user is not None:
            if user.is_active:
                return Response(data={'created': True}, status=HTTP_401_UNAUTHORIZED)
            self.service.put(_id=user.id, data=data)
        else:
            user = self.service.create(data)
        if isinstance(user, Exception):
            return Response(data={"error": str(user)}, status=500)
        return Response(data=self.serializer_class(user).data, status=HTTP_201_CREATED)

    def get_permissions(self):
        permission_classes = []
        if isinstance(self.request.user, AnonymousUser) and self.request.method == 'GET' \
                and self.request.query_params.get('typeUser') == 'doctor':
            permission_classes.append(AllowAny())
        else:
            permission_classes.append(IsAuthenticated())
        return permission_classes

    def retrieve(self, request, pk=None, *args, **kwargs):
        if request.user.typeUser != 'admin' and request.user.typeUser != 'superdoctor':
            self.service = PersonService()
        user = self.service.retrieve(pk)
        if user is None:
            return Response(data={"error": "لم يتم العثور على المستخدم"}, status=HTTP_404_NOT_FOUND)
        else:
            if hasattr(user, 'familyName') is True:
                if hasattr(user, 'speciality') is True:
                    return return_serialized_data_or_error_response(_object=user, response_code=HTTP_200_OK,
                                                                    serializer_class=DoctorSerializer)
                return return_serialized_data_or_error_response(_object=user, response_code=HTTP_200_OK,
                                                                serializer_class=PersonSerializer)
            return return_serialized_data_or_error_response(_object=user, serializer_class=UserSerializer,
                                                            response_code=HTTP_200_OK)

    def list(self, request, *args, **kwargs):
        filter_data = {}
        if request.user.typeUser == 'school':
            self.serializer_class = PersonSerializer
            self.service = PersonService()
            filter_data['typeUser'] = 'teacher'
            filter_data['schoolteacherids__school_id'] = request.user.id
        elif request.user.typeUser == 'superdoctor':
            self.serializer_class = DoctorSerializer
            self.service = DoctorService()
            filter_data['is_super'] = False
            filter_data['doctor_']
        for i in request.query_params:
            if self.service.fields.get(i) is None:
                return Response(data={'error': f'{i} is not an attribute for the user model'})
            filter_data[i] = request.query_params.get(i)
        _objects = self.service.filter_by(data=filter_data) if filter_data != {} else self.service.list()
        return extract_serialized_objects_response(_objects=_objects, serializer_class=self.serializer_class)


users_list, user_retrieve_update_delete = UserViewSet.get_urls()
login = TokenViewSet.as_view({
    'post': 'login'
})
signup = TokenViewSet.as_view({
    'post': 'signup'
})
urlpatterns = [
    path('', users_list),
    path('/<int:pk>', user_retrieve_update_delete),
    path('/login', login),
    path('/signup', signup),
    path('/logout', logout)
]
