from common.repositories import Repository
from common.services import Service
from .models import Consultation, Diagnostic, Patient, Supervise

URL = "http://localhost:5000/"
APPLICATION_TYPE = "application/json"


PATIENT_FIELDS = {
    'name': {'type': 'text', 'required': True},
    'familyName': {'type': 'text', 'required': True},
    'birthdate': {'type': 'date', 'required': True},
    'parent_id': {'type': 'foreign_key', 'required': False},
    'sick': {'type': 'bool', 'required': False},
    'behaviortroubleparent': {'type': 'BehaviorTroubleParent', 'required': False},
    'impulsivitytroubleparent': {'type': 'ImpulsivityTroubleParent', 'required': False},
    'learningtroubleparent': {'type': 'LearningTroubleParent', 'required': False},
    'anxitytroubleparent': {'type': 'AnxityTroubleParent', 'required': False},
    'somatisationtroubleparent': {'type': 'SomatisationTroubleParent', 'required': False},
    'hyperactivitytroubleparent': {'type': 'HyperActivityTroubleParent', 'required': False},
    'extratroubleparent': {'type': 'ExtraTroubleParent', 'required': False},
    'behaviorTroubleTeacher': {'type': 'list', 'required': False},
    'hyperActivityTroubleTeacher': {'type': 'list', 'required': False},
    'impulsivityTroubleTeacher': {'type': 'list', 'required': False},
    'inattentionTroubleTeacher': {'type': 'list', 'required': False},
    'extraTroubleTeacher': {'type': 'list', 'required': False}
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


class PatientService(Service):
    def __init__(self, repository=Repository(model=Patient)):
        super().__init__(repository, fields=PATIENT_FIELDS)


class SuperviseService(Service):
    def __init__(self, repository=Repository(model=Supervise)):
        super().__init__(repository, fields=SUPERVICE_FIELDS)

    def create(self, data: dict):
        supervise = super().create(data)
        if isinstance(supervise, Exception):
            return supervise
        try:
            patient = Patient.objects.get(id=data['patient_id'])
            patient.isSupervised = True
            patient.save()
        except Exception as exception:
            return exception
        return supervise


class ConsultationService(Service):
    def __init__(self, repository=Repository(model=Consultation)):
        super().__init__(repository, fields=CONSULTATION_FIELDS)


class DiagnosticService(Service):
    def __init__(self, repository=Repository(model=Diagnostic)):
        super().__init__(repository, fields=DIAGNOSTIC_FIELDS)
