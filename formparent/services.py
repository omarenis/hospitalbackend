from common.services import FormService
from .repositories import AnxityTroubleParentRepository, BehaviorTroubleParentRepository, \
    ExtraTroubleParentRepository, HyperActivityTroubleParentRepository, ImpulsivityTroubleParentRepository, \
    LearningTroubleParentRepository, SomatisationTroubleParentRepository


class AnxityTroubleParentService(FormService):
    def __init__(self, repository=AnxityTroubleParentRepository()):
        super().__init__(repository)


class ImpulsivityTroubleParentService(FormService):
    def __init__(self, repository=ImpulsivityTroubleParentRepository()):
        super().__init__(repository)


class LearningTroubleParentService(FormService):
    def __init__(self, repository=LearningTroubleParentRepository()):
        super().__init__(repository)


class SomatisationTroubleParentService(FormService):
    def __init__(self, repository=SomatisationTroubleParentRepository()):
        super().__init__(repository)


class HyperActivityTroubleParentService(FormService):
    def __init__(self, repository=HyperActivityTroubleParentRepository()):
        super().__init__(repository)


class BehaviorTroubleParentService(FormService):
    def __init__(self, repository=BehaviorTroubleParentRepository()):
        super().__init__(repository)


class ExtraTroubleParentService(FormService):
    def __init__(self, repository=ExtraTroubleParentRepository()):
        super().__init__(repository)
