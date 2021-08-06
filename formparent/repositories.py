from common.repositories import Repository
from formparent.models import AnxityTroubleParent, BehaviorTroubleParent, ExtraTroubleParent,\
    ImpulsivityTroubleParent, HyperActivityTroubleParent, LearningTroubleParent, SomatisationTroubleParent


class AnxityTroubleParentRepository(Repository):
    def __init__(self, model=AnxityTroubleParent):
        super().__init__(model)


class ImpulsivityTroubleParentRepository(Repository):
    def __init__(self, model=ImpulsivityTroubleParent):
        super().__init__(model)


class LearningTroubleParentRepository(Repository):
    def __init__(self, model=LearningTroubleParent):
        super().__init__(model)


class SomatisationTroubleParentRepository(Repository):
    def __init__(self, model=SomatisationTroubleParent):
        super().__init__(model)


class HyperActivityTroubleParentRepository(Repository):
    def __init__(self, model=HyperActivityTroubleParent):
        super().__init__(model)


class BehaviorTroubleParentRepository(Repository):
    def __init__(self, model=BehaviorTroubleParent):
        super().__init__(model)


class ExtraTroubleParentRepository(Repository):
    def __init__(self, model=ExtraTroubleParent):
        super().__init__(model)
