from common.services import FormService
from .repositories import BehaviorTroubleTeacherRepository, ExtraTroubleTeacherRepository, \
    HyperActivityTroubleTeacherRepository, ImpulsivityTroubleTeacherRepository, InattentionTroubleTeacherRepository


class BehaviorTroubleTeacherService(FormService):
    def __init__(self, repository=BehaviorTroubleTeacherRepository()):
        super().__init__(repository)


class HyperActivityTroubleTeacherService(FormService):
    def __init__(self, repository=HyperActivityTroubleTeacherRepository()):
        super().__init__(repository)


class ImpulsivityTroubleTeacherService(FormService):
    def __init__(self, repository=ImpulsivityTroubleTeacherRepository()):
        super().__init__(repository)


class ExtraTroubleTeacherService(FormService):
    def __init__(self, repository=ExtraTroubleTeacherRepository()):
        super().__init__(repository)


class InattentionTroubleTeacherService(FormService):
    def __init__(self, repository=InattentionTroubleTeacherRepository()):
        super().__init__(repository)
