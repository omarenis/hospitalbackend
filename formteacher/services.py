from common.models import text_field
from common.services import FormService
from .repositories import BehaviorTroubleTeacherRepository, ExtraTroubleTeacherRepository, \
    HyperActivityTroubleTeacherRepository, ImpulsivityTroubleTeacherRepository, InattentionTroubleTeacherRepository

behavior_trouble_teacher_fields = {
    'immediatelySatisfiedNeeds': text_field,
    'angryUnexpectedBehavior': text_field,
    'sensitiveCriticism': text_field,
    'poutSulkEasily': text_field,
    'moody': text_field,
    'brawler': text_field,
    'denyMistakesBlameOthers': text_field,
    'lessAskTeacherHelp': text_field
}

impulsivity_trouble_teacher_fields = {
    'restlessSquirmsChair': text_field,
    'inappropriateNoises': text_field,
    'arrogantImpolite': text_field,
    'annoyStudents': text_field,
    'goesLeftRight': text_field,
    'easilyTurnOnImpulsive': text_field,
    'excessiveAttentionFromTeacher': text_field
}

inattention_trouble_teacher = {
    'distracted': text_field,
    'dreamer': text_field,
    'beLedByOthers': text_field,
    'troubleGuidingOthers': text_field,
    'troubleFinishingThings': text_field,
    'immature': text_field,
    'upsetEasilyMakeEffort': text_field,
    'hasLearningDifficulties': text_field
}

hyperactivity_trouble_teacher = {
    'restlessSquirmsChair': text_field,
    'angryUnexpectedBehavior': text_field,
    'distracted': text_field,
    'annoyStudents': text_field,
    'poutSulkEasily': text_field,
    'moody': text_field,
    'goesLeftRight': text_field,
    'easilyTurnOnImpulsive': text_field,
    'troubleFinishingThings': text_field,
    'upsetEasilyMakeEffort': text_field
}

extra_trouble_teacher = {
    'submissiveAttitudeTowardsAuthority': text_field,
    'lessAcceptedByGroup': text_field,
    'unacceptDefeat': text_field,
    'troubleIntegratingWithOtherStudents': text_field,
    'lessCooperateWithOthers': text_field
}


class BehaviorTroubleTeacherService(FormService):
    def __init__(self, repository=BehaviorTroubleTeacherRepository()):
        super().__init__(repository, fields=behavior_trouble_teacher_fields)


class HyperActivityTroubleTeacherService(FormService):
    def __init__(self, repository=HyperActivityTroubleTeacherRepository()):
        super().__init__(repository, fields=hyperactivity_trouble_teacher)


class ImpulsivityTroubleTeacherService(FormService):
    def __init__(self, repository=ImpulsivityTroubleTeacherRepository()):
        super().__init__(repository, fields=impulsivity_trouble_teacher_fields)


class ExtraTroubleTeacherService(FormService):
    def __init__(self, repository=ExtraTroubleTeacherRepository()):
        super().__init__(repository, fields=extra_trouble_teacher)


class InattentionTroubleTeacherService(FormService):
    def __init__(self, repository=InattentionTroubleTeacherRepository()):
        super().__init__(repository, fields=inattention_trouble_teacher)
