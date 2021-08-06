from common.repositories import Repository
from .models import BehaviorTroubleTeacher, ExtraTroubleTeacher, HyperActivityTroubleTeacher, ImpulsivityTroubleTeacher, \
    InattentionTroubleTeacher


class BehaviorTroubleTeacherRepository(Repository):
    def __init__(self, model=BehaviorTroubleTeacher):
        super().__init__(model)


class HyperActivityTroubleTeacherRepository(Repository):
    def __init__(self, model=HyperActivityTroubleTeacher):
        super().__init__(model)


class ImpulsivityTroubleTeacherRepository(Repository):
    def __init__(self, model=ImpulsivityTroubleTeacher):
        super().__init__(model)


class ExtraTroubleTeacherRepository(Repository):
    def __init__(self, model=ExtraTroubleTeacher):
        super().__init__(model)


class InattentionTroubleTeacherRepository(Repository):
    def __init__(self, model=InattentionTroubleTeacher):
        super().__init__(model)
