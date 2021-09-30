import enum

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
from .models import DiagnosticSerializer, RendezVousSerializer, PatientSerializer, SuperviseSerializer
from gestionusers.services import PersonService
from .service import ConsultationService, DiagnosticService, PatientService, SuperviseService
from AI import FILE, classifier, train
from ethereum import PRIVATE_DATA
columns = list(FILE.columns[1:-1])
PRIVATE_DATA.recuperate_data()


class Quantify(enum.Enum):
    never = 0
    sometimes = 1
    usual = 2
    always = 3


def add_person(data: dict, type_user: str):
    if data is not None:
        person = PersonService().filter_by({'cin': data.get('cin'), 'typeUser': type_user}).first()
        if person is None:
            person = PersonService().create(data)
            if isinstance(person, Exception):
                raise person
        return person.id
    return None


PATIENT_FIELDS = {
    'name': {'type': 'text', 'required': True},
    'familyName': {'type': 'text', 'required': True},
    'school': {'type': 'text', 'required': True},
    'birthdate': {'type': 'date', 'required': True},
    'parent_id': {'type': 'foreign_key', 'required': False},
    'parent': {'type': 'foreign_key', 'required': False},
    'teacher': {'type': 'foreign_key', 'required': False},
    'sick': {'type': 'bool', 'required': False},
    'behaviortroubleparent': {'type': 'BehaviorTroubleParent', 'required': False},
    'impulsivitytroubleparent': {'type': 'ImpulsivityTroubleParent', 'required': False},
    'learningtroubleparent': {'type': 'LearningTroubleParent', 'required': False},
    'anxitytroubleparent': {'type': 'AnxityTroubleParent', 'required': False},
    'somatisationtroubleparent': {'type': 'SomatisationTroubleParent', 'required': False},
    'hyperactivitytroubleparent': {'type': 'HyperActivityTroubleParent', 'required': False},
    'extratroubleparent': {'type': 'ExtraTroubleParent', 'required': False},
    'behaviorTroubleTeacher_set': {'type': 'list', 'required': False},
    'hyperActivityTroubleTeacher_set': {'type': 'list', 'required': False},
    'impulsivityTroubleTeacher_set': {'type': 'list', 'required': False},
    'inattentionTroubleTeacher_set': {'type': 'list', 'required': False},
    'extraTroubleTeacher_set': {'type': 'list', 'required': False}
}
SUPERVICE_FIELDS = {
    'patient_id': {'type': 'int', 'required': True},
    'doctor_id': {'type': 'int', 'required': True},
    'accepted': {'type': 'bool', 'required': True}
}

CONSULTATION_FIELDS = {
    'doctor_id': {'type': 'int', 'required': True},
    'parent_id': {'type': 'int', 'required': True},
    'date': {'type': 'int', 'required': True},
    'accepted': {'type': 'bool', 'required': True}
}

DIAGNOSTIC_FIELDS = {
    'patient_id': {'type': 'int', 'required': True},
    'diagnostic': {'type': 'str', 'required': True},
    'consultation_id': {'type': 'int', 'required': True}
}


class PatientViewSet(ViewSet):
    services = {
        'behaviortroubleparent': BehaviorTroubleParentService(),
        'impulsivitytroubleparent': ImpulsivityTroubleParentService(),
        'learningtroubleparent': LearningTroubleParentService(),
        'anxitytroubleparent': AnxityTroubleParentService(),
        'somatisationtroubleparent': SomatisationTroubleParentService(),
        'hyperactivitytroubleparent': HyperActivityTroubleParentService(),
        'extratroubleparent': ExtraTroubleParentService(),
        'behaviorTroubleTeacher_set': BehaviorTroubleTeacherService(),
        'hyperActivityTroubleTeacher_set': HyperActivityTroubleTeacherService(),
        'impulsivityTroubleTeacher_set': ImpulsivityTroubleTeacherService(),
        'inattentionTroubleTeacher_set': InattentionTroubleTeacherService(),
        'extraTroubleTeacher_set': ExtraTroubleTeacherService()
    }

    def __init__(self, fields=None, serializer_class=PatientSerializer, service=PatientService(), **kwargs):
        if fields is None:
            fields = PATIENT_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)
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
            output = []
            print(list(request.GET.keys()) == [])
            pts = self.service.list() if list(request.GET.keys()) == [] else self.service.filter_by(request.GET)
            print(pts)
            if isinstance(pts, QuerySet):
                for i in pts:
                    patient_private_data = PRIVATE_DATA.get_patient_by_id(i.id)
                    print(patient_private_data)
                    if isinstance(patient_private_data, Exception):
                        return Response(data={'error': str(patient_private_data)},
                                        status=HTTP_500_INTERNAL_SERVER_ERROR)
                    output.append({**patient_private_data, **self.serializer_class(i).data})
            else:
                for i in pts:
                    patient_private_data, patient_object = i
                    output.append({**patient_private_data, **self.serializer_class(patient_object).data})
            return Response(data=output, status=HTTP_200_OK)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def retrieve(self, request, pk=None, *args, **kwargs):
        patient_data = self.service.retreive(_id=pk)
        if isinstance(patient_data, Exception):
            return Response(data={'error': str(patient_data)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        if isinstance(patient_data, tuple):
            patient_object, patient_private_data = patient_data
            return Response(data={**patient_private_data, **self.serializer_class(patient_object).data},
                            status=HTTP_200_OK)

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
        try:
            if parent_id is None:
                parent_id = add_person(data=request.data.get('parent'), type_user='parent')
            teacher_id = add_person(request.data.get('teacher'), type_user='teacher')
            required_data['parent_id'] = parent_id
            patient_object, patient_private_data = self.service.filter_by(data=required_data)[0]
            if patient_object is None:
                patient_data = self.service.create(required_data)
                if isinstance(patient_data, Exception):
                    raise patient_data
                patient_object, patient_private_data = patient_data
            patient_id = patient_object.id
            created = True
            for i in self.fields:
                if request.data.get(i) is not None and not self.fields[i].get('required') \
                        and self.fields[i].get('type') != 'bool' and self.fields[i].get('type') != 'foreign_key':
                    self.add_other_data_to_patient(
                        data=request.data.get(i)[0] if teacher_id is not None else request.data.get(i),
                        service=self.services[i],
                        patient_id=patient_id,
                        teacher_id=teacher_id
                    )
            self.data_to_predict.append(0)
            patient_object.sick = classifier.predict([self.data_to_predict])[0] == 1
            patient_object.save()
            self.save_data_to_csv_file()
            return Response(data={**self.serializer_class(patient_object).data, **patient_private_data},
                            status=HTTP_201_CREATED)
        except Exception as exception:
            if created:
                self.service.delete(_id=patient_id)
            return Response(data={'error': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, pk=None, *args, **kwargs):
        deleted = self.service.delete(pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(data={}, status=HTTP_204_NO_CONTENT)


class RenderVousViewSet(ViewSet):
    def get_permissions(self):
        return [IsAuthenticated()]

    def __init__(self, fields=None, serializer_class=RendezVousSerializer, service=ConsultationService(), **kwargs):
        if fields is None:
            fields = CONSULTATION_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


class SuperviseViewSet(ViewSet):
    def get_permissions(self):
        return [AllowAny()]

    def __init__(self, fields=None, serializer_class=SuperviseSerializer, service=SuperviseService(), **kwargs):
        if fields is None:
            fields = SUPERVICE_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


class DiagnosticViewSet(ViewSet):
    def get_permissions(self):
        return [IsAuthenticated()]

    def __init__(self, fields=None, serializer_class=DiagnosticSerializer, service=DiagnosticService(), **kwargs):
        if fields is None:
            fields = DIAGNOSTIC_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


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
