from common.repositories import Repository
from gestionpatient.models import Consultation, Patient, Supervise


class ConsultationRepository(Repository):
    def __init__(self, model=Consultation):
        super().__init__(model)


class SuperviseRepository(Repository):
    def __init__(self, model=Supervise):
        super().__init__(model)


class PatientRepository(Repository):
    def __init__(self, model=Patient):
        super().__init__(model)
