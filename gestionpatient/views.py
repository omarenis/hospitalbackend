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
from gestionpatient.models import Orientation, OrientationSerializer, Patient, PatientSerializer
from gestionusers.services import get_or_create_parent


def add_other_data_to_patient(data: dict, service, _id):
    if data is not None:
        data['patient_id'] = _id
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
        if request.data.get('parent_id') is None:
            parent_id = get_or_create_parent(request.data.get('parent'))
            if isinstance(parent_id, Exception):
                return Response(data={'error': str(parent_id)}, status=HTTP_400_BAD_REQUEST)
        else:
            parent_id = request.data.get('parent_id')
        data = {}
        created = False
        for i in list(self.fields.keys()):
            if request.data.get(i) is None and self.fields[i]['required']:
                return Response(data={'error': f'field {i} is required'}, status=HTTP_400_BAD_REQUEST)
            data[i] = request.data.get(i)
        data['parent_id'] = parent_id
        patient_object = self.service.filter_by(data=data).first()
        if patient_object is None:
            patient_object = self.service.create(data)
            print(patient_object)
            created = True
            if isinstance(patient_object, Exception):
                raise patient_object
        patient_id = patient_object.id
        try:
            add_other_data_to_patient(
                data=request.data.get('behaviorTroubleParent'), service=BehaviorTroubleParentService(),
                _id=patient_id
            )
            add_other_data_to_patient(
                data=request.data.get('impulsivityTroubleParent'),
                _id=patient_id, service=ImpulsivityTroubleParentService()
            )
            add_other_data_to_patient(data=request.data.get('learningTroubleParent'),
                                      service=LearningTroubleParentService(),
                                      _id=patient_id)
            add_other_data_to_patient(data=request.data.get('anxityTroubleParent'),
                                      service=AnxityTroubleParentService(),
                                      _id=patient_id)
            add_other_data_to_patient(
                data=request.data.get('somatisationTroubleParent'),
                service=SomatisationTroubleParentService(), _id=patient_id
            )
            add_other_data_to_patient(
                data=request.data.get('hyperActivityTroubleParent'),
                service=HyperActivityTroubleParentService(), _id=patient_id
            )
            add_other_data_to_patient(data=request.data.get('extraTroubleParent'),
                                      service=ExtraTroubleParentService(),
                                      _id=patient_id)
            if request.data.get('behaviorTroubleTeacher_set'):
                add_other_data_to_patient(
                    data=request.data.get('behaviorTroubleTeacher_set')[0],
                    service=BehaviorTroubleTeacherService(),
                    _id=patient_id
                )
            if request.data.get('extraTroubleTeacher_set'):
                add_other_data_to_patient(
                    data=request.data.get('extraTroubleTeacher_set')[0],
                    service=ExtraTroubleTeacherService(),
                    _id=patient_id
                )
            if request.data.get('hyperActivityTeacher_set'):
                add_other_data_to_patient(
                    data=request.data.get('hyperActivityTeacher_set')[0],
                    service=HyperActivityTroubleTeacherService(),
                    _id=patient_id
                )
            if request.data.get('impulsivityTroubleTeacher_set'):
                add_other_data_to_patient(
                    data=request.data.get('impulsivityTroubleTeacher_set')[0],
                    service=ImpulsivityTroubleTeacherService(),
                    _id=patient_id
                )
            if request.data.get('inattentionTroubleTeacher_set'):
                add_other_data_to_patient(
                    data=request.data.get('inattentionTroubleTeacher_set')[0],
                    service=InattentionTroubleTeacherService(),
                    _id=patient_id
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
