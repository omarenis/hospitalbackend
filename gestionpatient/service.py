from common.services import Service
from .repositories import PatientRepository, SuperviseRepository, ConsultationRepository


class PatientService(Service):
    def __init__(self, repository=PatientRepository()):
        super().__init__(repository)


class SuperviseService(Service):
    def __init__(self, repository=SuperviseRepository()):
        super().__init__(repository)


class ConsultationService(Service):
    def __init__(self, repository=ConsultationRepository()):
        super().__init__(repository)