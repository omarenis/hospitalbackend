from django.urls import path
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from common.models import text_field
from common.repositories import Repository
from common.services import Service
from common.views import ViewSet, extract_data_with_validation
from formparent.services import AnxityTroubleParentService, BehaviorTroubleParentService, ExtraTroubleParentService, \
    HyperActivityTroubleParentService, ImpulsivityTroubleParentService, LearningTroubleParentService, \
    SomatisationTroubleParentService
from formteacher.services import BehaviorTroubleTeacherService, ExtraTroubleTeacherService, \
    HyperActivityTroubleTeacherService, ImpulsivityTroubleTeacherService, InattentionTroubleTeacherService, \
    TeacherService
from .models import Orientation, OrientationSerializer, Patient, PatientSerializer
from gestionusers.services import PersonService


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
    'doctor_id': {'type': 'foreign_key', 'required': False},
    'parent': {'type': 'foreign_key', 'required': False},
    'behaviorTroubleParent': {'type': 'BehaviorTroubleParent', 'required': False},
    'impulsivityTroubleParent': {'type': 'ImpulsivityTroubleParent', 'required': False},
    'learningTroubleParent': {'type': 'LearningTroubleParent', 'required': False},
    'anxityTroubleParent': {'type': 'AnxityTroubleParent', 'required': False},
    'somatisationTroubleParent': {'type': 'SomatisationTroubleParent', 'required': False},
    'hyperactivityTroubleParent': {'type': 'HyperActivityTroubleParent', 'required': False},
    'extraTroubleParent': {'type': 'ExtraTroubleParent', 'required': False},
    'behaviorTroubleTeacher_set': {'type': 'list', 'required': False},
    'hyperActivityTroubleTeacher_set': {'type': 'list', 'required': False},
    'impulsivityTroubleTeacher_set': {'type': 'list', 'required': False},
    'inattentionTroubleTeacher_set': {'type': 'list', 'required': False},
    'extraTroubleTeacher_set': {'type': 'list', 'required': False}
}

ORIENTATION_FIELDS = {
    'patient_id': {'type': 'foerign_key', 'required': True},
    'doctor_id': {'type': 'foreign_key', 'required': True},
    'diagnostic': text_field
}


class PatientRepository(Repository):
    def __init__(self, model=Patient):
        super().__init__(model)


class OrientationRepository(Repository):
    def __init__(self, model=Orientation):
        super().__init__(model)


class PatientService(Service):
    def __init__(self, repository=PatientRepository()):
        super().__init__(repository)


class OrientationService(Service):
    def __init__(self, repository=OrientationRepository()):
        super().__init__(repository)


class PatientViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=PatientSerializer, service=PatientService(), **kwargs):
        if fields is None:
            fields = PATIENT_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)

    def create(self, request, *args, **kwargs):
        services = {
            'behaviorTroubleParent': BehaviorTroubleParentService(),
            'impulsivityTroubleParent': ImpulsivityTroubleParentService(),
            'learningTroubleParent': LearningTroubleParentService(),
            'anxityTroubleParent': AnxityTroubleParentService(),
            'somatisationTroubleParent': SomatisationTroubleParentService(),
            'hyperactivityTroubleParent': HyperActivityTroubleParentService(),
            'extraTroubleParent': ExtraTroubleParentService(),
            'behaviorTroubleTeacher_set': BehaviorTroubleTeacherService(),
            'hyperActivityTroubleTeacher_set': HyperActivityTroubleTeacherService(),
            'impulsivityTroubleTeacher_set': ImpulsivityTroubleTeacherService(),
            'inattentionTroubleTeacher_set': InattentionTroubleTeacherService(),
            'extraTroubleTeacher_set': ExtraTroubleTeacherService()
        }
        data = extract_data_with_validation(request=request, fields=self.fields)
        created = False
        patient_id = None
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
            data['parent_id'] = parent_id
            print("parent _id ", parent_id)
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
            print("patient_id = ", patient_object.id)
            teacher = TeacherService().filter_by({'cin': request.data.get('teacher').get('cin')}).first() \
                if request.data.get('teacher') else None
            teacher = TeacherService().create(request.data.get('teacher')) if teacher is None and request.data.get('teacher') else teacher
            if isinstance(teacher, Exception):
                raise teacher
            if request.data.get('teacher') and isinstance(teacher, Exception):
                raise teacher
            for i in self.fields:
                if not self.fields[i].get('required') \
                        and self.fields[i].get('type') not in ['date', 'foreign_key', 'text']:
                    print(request.data.get(i))
                    if request.data.get(i) is not None:
                        add_other_data_to_patient(
                            data=request.data.get(i)[0] if teacher is not None else request.data.get(i),
                            service=services[i],
                            patient_id=patient_id,
                            teacher_id=teacher.id if teacher is not None else None
                        )
            return Response(data=self.serializer_class(patient_object).data, status=HTTP_201_CREATED)
        except Exception as exception:
            if created:
                self.service.delete(_id=patient_id)
            return Response(data={'error': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class OrientationViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=OrientationSerializer, service=OrientationService(), **kwargs):
        if fields is None:
            fields = ORIENTATION_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


patients, patient = PatientViewSet.get_urls()
orientations, orientation = OrientationViewSet.get_urls()

urlpatterns = [
    path('', patients),
    path('<int:id>', patient),
    path('orientations', orientations),
    path('orentations/<int:id>', orientation)
]
