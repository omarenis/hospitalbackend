from django.urls import path
from rest_framework.response import Response
from rest_framework.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from common.models import text_field
from common.repositories import Repository
from common.services import Service
from common.views import ViewSet
from formparent.services import AnxityTroubleParentService, BehaviorTroubleParentService, ExtraTroubleParentService, \
    HyperActivityTroubleParentService, ImpulsivityTroubleParentService, LearningTroubleParentService, \
    SomatisationTroubleParentService
from formteacher.services import BehaviorTroubleTeacherService, ExtraTroubleTeacherService, \
    HyperActivityTroubleTeacherService, ImpulsivityTroubleTeacherService, InattentionTroubleTeacherService
from .models import Orientation, OrientationSerializer, Patient, PatientSerializer, Teacher


def add_other_data_to_patient(data: dict, service, patient_id, teacher_id=None):
    if data is not None:
        print(data)
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
    'parent_id': {'type': 'foerign_key', 'required': False},
    'doctor_id': {'type': 'foreign_key', 'required': False}
}

ORIENTATION_FIELDS = {
    'patient_id': {'type': 'foerign_key', 'required': True},
    'doctor_id': {'type': 'foreign_key', 'required': True},
    'diagnostic': text_field
}

TEACHER_FIELDS = {
    'name': {'type': 'text', 'required': True},
    'familyName': {'type': 'text', 'required': True},
    'cin': {'type': 'text', 'required': True},
    'telephone': {'type': 'text', 'required': True}
}


class TeacherRepository(Repository):
    def __init__(self, model=Teacher):
        super().__init__(model)


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
        data = {}
        created = False
        for i in list(self.fields.keys()):
            if request.data.get(i) is None and self.fields[i]['required']:
                return Response(data={'error': f'field {i} is required'}, status=HTTP_400_BAD_REQUEST)
            data[i] = request.data.get(i)
        data['parent_id'] = request.data.get('parent_id')
        patient_object = self.service.filter_by(data=data).first()
        if patient_object is None:
            patient_object = self.service.create(data)
            created = True
            if isinstance(patient_object, Exception):
                raise patient_object
        patient_id = patient_object.id
        try:
            add_other_data_to_patient(
                data=request.data.get('behaviorTroubleParent'), service=BehaviorTroubleParentService(),
                patient_id=patient_id, teacher_id=None
            )
            add_other_data_to_patient(
                data=request.data.get('impulsivityTroubleParent'), service=ImpulsivityTroubleParentService(),
                patient_id=patient_id, teacher_id=None
            )
            add_other_data_to_patient(data=request.data.get('learningTroubleParent'),
                                      service=LearningTroubleParentService(),
                                      patient_id=patient_id, teacher_id=None)
            add_other_data_to_patient(data=request.data.get('anxityTroubleParent'),
                                      service=AnxityTroubleParentService(),
                                      patient_id=patient_id, teacher_id=None)
            add_other_data_to_patient(
                data=request.data.get('somatisationTroubleParent'),
                service=SomatisationTroubleParentService(), patient_id=patient_id,
                teacher_id=None
            )
            add_other_data_to_patient(
                data=request.data.get('hyperActivityTroubleParent'),
                service=HyperActivityTroubleParentService(), patient_id=patient_id,
                teacher_id=None
            )
            add_other_data_to_patient(data=request.data.get('extraTroubleParent'),
                                      service=ExtraTroubleParentService(),
                                      patient_id=patient_id,
                                      teacher_id=None
                                      )
            if request.data.get('teacher_id'):
                add_other_data_to_patient(
                    data=request.data.get('behaviorTroubleTeacher_set')[0],
                    service=BehaviorTroubleTeacherService(),
                    patient_id=patient_id,
                    teacher_id=request.data.get('teacher_id')
                )
                add_other_data_to_patient(
                    data=request.data.get('extraTroubleTeacher_set')[0],
                    service=ExtraTroubleTeacherService(),
                    patient_id=patient_id, teacher_id=request.data.get('teacher_id')
                )
                add_other_data_to_patient(
                    data=request.data.get('hyperActivityTeacher_set')[0],
                    service=HyperActivityTroubleTeacherService(),
                    patient_id=patient_id, teacher_id=request.data.get('teacher_id')
                )
                add_other_data_to_patient(
                    data=request.data.get('impulsivityTroubleTeacher_set')[0],
                    service=ImpulsivityTroubleTeacherService(),
                    patient_id=patient_id, teacher_id=request.data.get('teacher_id')
                )
                add_other_data_to_patient(
                    data=request.data.get('inattentionTroubleTeacher_set')[0],
                    service=InattentionTroubleTeacherService(),
                    patient_id=patient_id, teacher_id=request.data.get('teacher_id')
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
