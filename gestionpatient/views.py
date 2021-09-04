from django.urls import path
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from common.models import text_field
from common.views import ViewSet, extract_data_with_validation
from formparent.services import AnxityTroubleParentService, BehaviorTroubleParentService, ExtraTroubleParentService, \
    HyperActivityTroubleParentService, ImpulsivityTroubleParentService, LearningTroubleParentService, \
    SomatisationTroubleParentService
from formteacher.services import BehaviorTroubleTeacherService, ExtraTroubleTeacherService, \
    HyperActivityTroubleTeacherService, ImpulsivityTroubleTeacherService, InattentionTroubleTeacherService
from .models import ConsultationSerializer, PatientSerializer, SuperviseSerializer
from gestionusers.services import PersonService
from .service import ConsultationService, PatientService


def add_other_data_to_patient(data: dict, service, patient_id, teacher_id=None):
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
    else:
        return _object


PATIENT_FIELDS = {
    'name': text_field,
    'familyName': text_field,
    'school': text_field,
    'birthdate': {'type': 'date', 'required': True},
    'parent_id': {'type': 'foreign_key', 'required': False},
    'parent': {'type': 'foreign_key', 'required': False},
    'teacher': {'type': 'foreign_key', 'required': False},
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
    'validated': {'type': 'bool', 'required': True}
}

CONSULTATION_FIELDS = {
    'patient_id': {'type': 'int', 'required': True},
    'doctor_id': {'type': 'int', 'required': True},
    'parent_id': {'type': 'int', 'required': True},
    'date': {'type': 'int', 'required': True},
    'accepted': {'type': 'bool', 'required': True}
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

    def create(self, request, *args, **kwargs):
        data = extract_data_with_validation(request=request, fields=self.fields)
        created = False
        patient_id = None
        teacher_id = None
        if isinstance(data, Exception):
            return Response(data={'error': str(data)}, status=HTTP_400_BAD_REQUEST)
        try:
            parent_id = request.data.get('parent_id')
            if parent_id is None:
                parent = PersonService().filter_by({'cin': request.data.get('parent').get('cin')}).first()
                parent = PersonService().create(request.data.get('parent')) if parent is None else parent
                if isinstance(parent, Exception):
                    raise parent
                else:
                    parent_id = parent.id

            if request.data.get('teacher') is not None:
                teacher = PersonService().filter_by({'cin': request.data.get('teacher').get('cin')}).first()
                teacher = PersonService().create(request.data.get('teacher')) if teacher is None else teacher
                if isinstance(teacher, Exception):
                    raise teacher
                teacher_id = teacher.id
            data['parent_id'] = parent_id
            required_data = {
                'name': data.get('name'),
                'familyName': data.get('familyName'),
                'school': data.get('school'),
                'birthdate': data.get('birthdate'),
                'parent_id': data.get('parent_id')
            }
            patient_object = self.service.filter_by(data=required_data).first()
            if patient_object is None:
                patient_object = self.service.create(required_data)
                created = True
                if isinstance(patient_object, Exception):
                    raise patient_object
            patient_id = patient_object.id
            for i in self.fields:
                if not self.fields[i].get('required') and request.data.get(i) is not None \
                        and self.fields[i].get('type') != 'date' and self.fields[i].get('typr') != 'text' \
                        and self.fields[i].get('type') != 'foreign_key':
                    add_other_data_to_patient(
                        data=request.data.get(i)[0] if teacher_id is not None else request.data.get(i),
                        service=self.services[i],
                        patient_id=patient_id,
                        teacher_id=teacher_id if teacher_id is not None else None
                    )
            return Response(data=self.serializer_class(patient_object).data, status=HTTP_201_CREATED)
        except Exception as exception:
            if created:
                self.service.delete(_id=patient_id)
            return Response(data={'error': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class ConsultationViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=ConsultationSerializer, service=ConsultationService(), **kwargs):
        if fields is None:
            fields = CONSULTATION_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


class SuperviseViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=SuperviseSerializer, service, **kwargs):
        if fields is None:
            fields = SUPERVICE_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


patients, patient = PatientViewSet.get_urls()

urlpatterns = [
    path('', patients),
    path('<int:pk>', patient),
]
