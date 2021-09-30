from common.services import Service
from .repositories import DiagnosticRepository, PatientRepository, SuperviseRepository, ConsultationRepository
from ethereum import PRIVATE_DATA


class PatientService(Service):
    def __init__(self, repository=PatientRepository()):
        super().__init__(repository)

    def create(self, data: dict):
        patient_object = self.repository.create(data={'parent_id': data.get('parent_id')})
        data['id'] = patient_object.id
        if isinstance(patient_object, Exception):
            return patient_object
        patient_private_data = PRIVATE_DATA.create_patient(data)
        if isinstance(patient_private_data, Exception):
            patient_object.delete()
            return patient_private_data
        return patient_object, patient_private_data

    def retreive(self, _id: int):
        patient_object = self.repository.retreive(_id)
        if patient_object is None:
            return patient_object
        patient_private_data = PRIVATE_DATA.get_patient_by_id(_id)
        if isinstance(patient_private_data, Exception):
            return patient_private_data
        return patient_object, patient_private_data

    def filter_by(self, data: dict):
        if data.get('name') is None and data.get('parent_id') is not None:
            output = []
            patients = self.repository.filter_by({'parent_id': data.get('parent_id')})
            if patients:
                for i in patients:
                    patient = PRIVATE_DATA.get_patient_by_id(i.id)
                    if isinstance(patient, Exception):
                        return patient
                    output.append((patient, i))
            return output
        patient_private_data = PRIVATE_DATA.filter_by(data=data)
        if isinstance(patient_private_data, Exception):
            return patient_private_data
        if patient_private_data is None:
            return [(None, None)]
        patient_object = super().retreive(_id=patient_private_data.get('id'))
        return [(patient_object, patient_private_data)]

    def delete(self, _id: int):
        deleted = PRIVATE_DATA.delete_patient(_id)
        if isinstance(deleted, Exception):
            return deleted
        if deleted:
            deleted = self.repository.delete(_id)
            if isinstance(deleted, Exception):
                return deleted
            return True
        return False


class SuperviseService(Service):
    def __init__(self, repository=SuperviseRepository()):
        super().__init__(repository)


class ConsultationService(Service):
    def __init__(self, repository=ConsultationRepository()):
        super().__init__(repository)


class DiagnosticService(Service):
    def __init__(self, repository=DiagnosticRepository()):
        super().__init__(repository)
