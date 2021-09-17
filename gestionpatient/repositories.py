from common.repositories import Repository
from gestionpatient.models import Diagnostic, RenderVous, Patient, Supervise


class ConsultationRepository(Repository):
    def __init__(self, model=RenderVous):
        super().__init__(model)


class SuperviseRepository(Repository):
    def __init__(self, model=Supervise):
        super().__init__(model)


class PatientRepository(Repository):
    def __init__(self, model=Patient):
        super().__init__(model)


class DiagnosticRepository(Repository):
    def __init__(self, model=Diagnostic):
        super().__init__(model)
