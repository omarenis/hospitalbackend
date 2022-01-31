from common.services import Service
from .repositories import DiagnosticRepository, PatientRepository, SuperviseRepository, ConsultationRepository

URL = "http://localhost:5000/"
application_type = "application/json"


class PatientService(Service):
    def __init__(self, repository=PatientRepository()):
        super().__init__(repository)


class SuperviseService(Service):
    def __init__(self, repository=SuperviseRepository()):
        super().__init__(repository)


class ConsultationService(Service):
    def __init__(self, repository=ConsultationRepository()):
        super().__init__(repository)


class DiagnosticService(Service):
    def __init__(self, repository=DiagnosticRepository()):
        super().__init__(repository)
