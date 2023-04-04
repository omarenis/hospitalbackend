import enum

from django.db.models import QuerySet
from django.urls import path
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK, \
    HTTP_204_NO_CONTENT

from common.views import ViewSet, extract_data_with_validation
from formparent.services import AnxityTroubleParentService, BehaviorTroubleParentService, ExtraTroubleParentService, \
    HyperActivityTroubleParentService, ImpulsivityTroubleParentService, LearningTroubleParentService, \
    SomatisationTroubleParentService
from formteacher.services import BehaviorTroubleTeacherService, ExtraTroubleTeacherService, \
    HyperActivityTroubleTeacherService, ImpulsivityTroubleTeacherService, InattentionTroubleTeacherService
from gestionusers.services import PersonService, UserService
from .models import DiagnosticSerializer, ConsultationSerializer, PatientSerializer, SuperviseSerializer
from .service import ConsultationService, DiagnosticService, PatientService, SuperviseService


class Quantify(enum.Enum):
    never = 0
    sometimes = 1
    usual = 2
    always = 3


def add_person(data: dict, type_user: str):
    if data is not None:
        person = PersonService().filter_by({'loginNumber': data.get('cin'), 'typeUser': type_user}).first()
        if person is None:
            person = PersonService().create(data)
            if isinstance(person, Exception):
                raise person
        return person.id
    return None


def add_other_data_to_patient(data: dict, service, patient_id, teacher_id=None):
    if teacher_id is not None:
        _object = service.filter_by({'teacher_id': teacher_id, 'patient_id': patient_id}).first()
    else:
        _object = service.filter_by({'patient_id': patient_id}).first()
    if _object is not None:
        _object = service.put(data=data, _id=_object.id)
    else:
        data['patient_id'] = patient_id
        if teacher_id is not None:
            data['teacher_id'] = teacher_id
    _object = service.create(data=data)
    if isinstance(_object, Exception):
        print(_object)
        raise _object
    return _object


class PatientViewSet(ViewSet):
    serviceParent = {'behaviortroubleparent': BehaviorTroubleParentService(),
                     'impulsivitytroubleparent': ImpulsivityTroubleParentService(),
                     'learningtroubleparent': LearningTroubleParentService(),
                     'anxitytroubleparent': AnxityTroubleParentService(),
                     'somatisationtroubleparent': SomatisationTroubleParentService(),
                     'hyperactivitytroubleparent': HyperActivityTroubleParentService(),
                     'extratroubleparent': ExtraTroubleParentService()}
    servicesTeacher = {'behaviorTroubleTeacher': BehaviorTroubleTeacherService(),
                       'hyperActivityTroubleTeacher': HyperActivityTroubleTeacherService(),
                       'impulsivityTroubleTeacher': ImpulsivityTroubleTeacherService(),
                       'inattentionTroubleTeacher': InattentionTroubleTeacherService(),
                       'extraTroubleTeacher': ExtraTroubleTeacherService()}

    def __init__(self, serializer_class=PatientSerializer, service=PatientService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)

    def get_permissions(self):
        return [IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        try:
            filter_dictionary = {}
            if request.user.typeUser == 'teacher':
                filter_dictionary['form__teacher_id'] = request.user.id
            elif request.user.typeUser == 'school':
                filter_dictionary['form__teacher__schoolteacherids__school_id'] = request.user.id
            elif request.user.typeUser == 'parent':
                filter_dictionary['parent_id'] = request.user.id
            elif request.user.typeUser == 'doctor':
                filter_dictionary['supervise__doctor_id'] = request.user.id
                filter_dictionary['supervise__accepted'] = True
            for i in request.query_params:
                filter_dictionary[i] = request.query_params.get(i)

            output = []
            pts = self.service.list().distinct() if list(
                request.GET.keys()) == [] and filter_dictionary == {} else self.service.filter_by(filter_dictionary)
            if isinstance(pts, QuerySet):
                for i in pts.distinct():
                    output.append(self.serializer_class(i).data)
            else:
                for i in pts:
                    patient_private_data, patient_object = i
                    output.append(self.serializer_class(patient_object).data)
            return Response(data=output, status=HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None, *args, **kwargs):
        patient_data = self.service.retrieve(_id=pk)
        if isinstance(patient_data, Exception):
            return Response(data={'error': str(patient_data)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        medical_teacher_data = None
        return Response({**self.serializer_class(patient_data).data,
                         'school': patient_data.form_set.first().teacher.schoolteacherids.school.name},
                        status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        required_data = {'name': request.data.get('name'), 'familyName': request.data.get('familyName'),
                         'birthdate': request.data.get('birthdate'), }
        if request.user.typeUser == 'parent':
            required_data['parent_id'] = request.user.id
        else:
            parent_cin = request.data.pop('parentCin')
            parent = UserService().filter_by({'loginNumber': parent_cin}).first()
            if parent is None:
                parent = UserService().create(
                    {'loginNumber': parent_cin, 'name': '', 'familyName': '', 'typeUser': 'parent', 'telephone': '',
                     'password': ''})
            required_data['parent_id'] = parent.id
        data = extract_data_with_validation(request=request, fields=self.fields)
        data['parent_id'] = required_data['parent_id']
        if isinstance(data, Exception):
            return Response(data={'error': str(data)}, status=HTTP_400_BAD_REQUEST)
        created = False
        patient_id = None
        try:
            patient_object = self.service.filter_by(required_data).first()
            if patient_object is None:
                patient_object = self.service.create(required_data)
            if isinstance(patient_object, Exception):
                raise patient_object
            else:
                created = True
            patient_id = patient_object.id
            if request.user.typeUser == 'teacher':
                for i in self.servicesTeacher:
                    patient_object.scoreTeacher += add_other_data_to_patient(data=data.get(i),
                                                                             service=self.servicesTeacher[i],
                                                                             patient_id=patient_id,
                                                                             teacher_id=request.user.id).score
                patient_object.scoreTeacher /= 10
            else:
                for i in self.serviceParent:
                    patient_object.scoreParent = add_other_data_to_patient(data=data.get(i),
                                                                           service=self.serviceParent[i],
                                                                           patient_id=patient_id, teacher_id=None).score
                patient_object.scoreParent /= 10
            if patient_object.scoreTeacher > 0 and patient_object.scoreParent > 0:
                patient_object.sick = patient_object.scoreParent > 1.5 and patient_object.scoreTeacher > 1.5
            else:
                patient_object.sick = None
            patient_object.save()
            return Response(data=self.serializer_class(patient_object).data, status=HTTP_201_CREATED)
        except Exception as exception:
            if created:
                self.service.delete(_id=patient_id)
            return Response(data={'error': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None, *args, **kwargs):
        deleted = self.service.delete(pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(status=HTTP_204_NO_CONTENT)


class RenderVousViewSet(ViewSet):
    def get_permissions(self):
        if self.request.user.typeUser == 'doctor':
            return [IsAuthenticated()]

    def __init__(self, serializer_class=ConsultationSerializer, service=ConsultationService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class SuperviseViewSet(ViewSet):
    def get_permissions(self):
        if self.request.user.typeUser == 'doctor' or self.request.user.typeUser == 'superdoctor':
            return [IsAuthenticated()]

    def __init__(self, serializer_class=SuperviseSerializer, service=SuperviseService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class DiagnosticViewSet(ViewSet):
    def get_permissions(self):
        return [IsAuthenticated()]

    def __init__(self, serializer_class=DiagnosticSerializer, service=DiagnosticService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


patients, patient = PatientViewSet.get_urls()
supervises, supervise = SuperviseViewSet.get_urls()
consultations, consultation = RenderVousViewSet.get_urls()
diagnostics, diagnostic = DiagnosticViewSet.get_urls()

urlpatterns = [
    path('', patients), path('/<int:pk>', patient),
    path('/supervises', supervises),
    path('/supervises/<int:pk>', supervise),
    path('/consultations', consultations),
    path('/consultations/<int:pk>', consultation),
    path('/diagnostics', diagnostics),
    path('/diagnostics/<int:pk>', diagnostic)
]
