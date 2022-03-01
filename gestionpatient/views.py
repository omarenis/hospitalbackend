import enum

from django.contrib.auth.models import AnonymousUser
from django.db.models import QuerySet

from backend.settings import PROJECT_ROOT
from django.urls import path
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_400_BAD_REQUEST, HTTP_200_OK,\
    HTTP_204_NO_CONTENT
from common.views import ViewSet, extract_data_with_validation
from formparent.services import AnxityTroubleParentService, BehaviorTroubleParentService, ExtraTroubleParentService, \
    HyperActivityTroubleParentService, ImpulsivityTroubleParentService, LearningTroubleParentService, \
    SomatisationTroubleParentService
from formteacher.services import BehaviorTroubleTeacherService, ExtraTroubleTeacherService, \
    HyperActivityTroubleTeacherService, ImpulsivityTroubleTeacherService, InattentionTroubleTeacherService
from .models import DiagnosticSerializer, ConsultationSerilaizer, PatientSerializer, SuperviseSerializer
from gestionusers.services import PersonService
from .service import ConsultationService, DiagnosticService, PatientService, SuperviseService
from AI import FILE, classifier, train
columns = list(FILE.columns[1:-1])


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


class PatientViewSet(ViewSet):
    services = {
        'behaviortroubleparent': BehaviorTroubleParentService(),
        'impulsivitytroubleparent': ImpulsivityTroubleParentService(),
        'learningtroubleparent': LearningTroubleParentService(),
        'anxitytroubleparent': AnxityTroubleParentService(),
        'somatisationtroubleparent': SomatisationTroubleParentService(),
        'hyperactivitytroubleparent': HyperActivityTroubleParentService(),
        'extratroubleparent': ExtraTroubleParentService(),
        'behaviorTroubleTeacher': BehaviorTroubleTeacherService(),
        'hyperActivityTroubleTeacher': HyperActivityTroubleTeacherService(),
        'impulsivityTroubleTeacher': ImpulsivityTroubleTeacherService(),
        'inattentionTroubleTeacher': InattentionTroubleTeacherService(),
        'extraTroubleTeacher': ExtraTroubleTeacherService()
    }

    def __init__(self, serializer_class=PatientSerializer, service=PatientService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)
        self.data_to_predict = [0] * len(list(FILE.columns[1:-1]))

    def save_data_to_csv_file(self):
        with open(f'{PROJECT_ROOT}/dataset1.csv') as f:
            string = f"\n{len(f.readlines()) - 1},"
        for i in range(len(self.data_to_predict)-1):
            string += f"{self.data_to_predict[i]},"
        string += f"{self.data_to_predict[-1]}"
        with open(f"{PROJECT_ROOT}/dataset1.csv", "a") as f:
            f.write(string)
        train()

    def add_other_data_to_patient(self, data: dict, service, patient_id, teacher_id=None):
        for i in range(len(columns)):
            if data.get(columns[i]) is not None and self.data_to_predict[i] != Quantify[data.get(columns[i])].value:
                self.data_to_predict[i] = Quantify[data.get(columns[i])].value
        _object = service.filter_by({'teacher_id': teacher_id, 'patient_id': patient_id}).first() \
            if teacher_id is not None else service.filter_by({'patient_id': patient_id}).first()
        if _object:
            _object = service.put(data=data, _id=_object.id)
        else:
            data['patient_id'] = patient_id
            if teacher_id is not None:
                data['teacher_id'] = teacher_id
            _object = service.create(data=data)
        if isinstance(_object, Exception):
            raise _object
        return _object

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
                filter_dictionary['doctor_id'] = request.user.id
            for i in request.query_params:
                filter_dictionary[i] = request.query_params.get(i)
            output = []
            pts = self.service.list().distinct() if list(request.GET.keys()) == [] and filter_dictionary == {} \
                else self.service.filter_by(filter_dictionary)
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
        return Response(self.serializer_class(patient_data).data, status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        train()
        data = extract_data_with_validation(request=request, fields=self.fields)
        if isinstance(data, Exception):
            return Response(data={'error': str(data)}, status=HTTP_400_BAD_REQUEST)
        required_data = {
            'name': data.get('name'),
            'familyName': data.get('familyName'),
            'school': data.get('school'),
            'birthdate': data.get('birthdate'),
            'parent_id': data.get('parent_id')
        }
        created = False
        patient_id = None
        parent_id = request.data.get('parent_id')
        teacher_id = request.data.get('teacher_id')
        try:
            if parent_id is None:
                parent_id = add_person(data=request.data.get('parent'), type_user='parent')
            if teacher_id is None:
                teacher_id = add_person(request.data.get('teacher'), type_user='teacher')
            required_data['parent_id'] = parent_id
            patient_object = self.service.filter_by(required_data).first()
            if patient_object is None:
                patient_object = self.service.create(required_data)
            if isinstance(patient_object, Exception):
                raise patient_object
            else:
                created = True
            patient_id = patient_object.id
            for i in self.fields:
                if request.data.get(i) is not None and not self.fields[i].get('required') \
                        and self.fields[i].get('type') != 'bool' and self.fields[i].get('type') != 'foreign_key':
                    self.add_other_data_to_patient(
                        data=request.data.get(i),
                        service=self.services[i],
                        patient_id=patient_id,
                        teacher_id=teacher_id
                    )
            self.data_to_predict.append(0)
            patient_object.sick = classifier.predict([self.data_to_predict])[0] == 1
            patient_object.save()
            self.save_data_to_csv_file()
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

    def __init__(self, serializer_class=ConsultationSerilaizer, service=ConsultationService(), **kwargs):
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
    path('', patients),
    path('<int:pk>', patient),
    path('supervises', supervises),
    path('supervises/<int:pk>', supervise),
    path('consultations', consultations),
    path('consultations/<int:pk>', consultation),
    path('diagnostics', diagnostics),
    path('diagnostics/<int:pk>', diagnostic)
]
