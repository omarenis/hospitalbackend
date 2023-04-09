from common.models import text_field
from common.services import FormService
from .repositories import BehaviorTroubleTeacherRepository, HyperActivityTroubleTeacherRepository, \
    InattentionTroubleTeacherRepository, FormAbrRepository

BEHAVIOR_TROUBLE_TEACHER_FIELDS = {
    'arrogant_impolite': text_field,
    'angry_unexpected_behavior': text_field,
    'sensitive_criticism': text_field,
    'pout_sulk_easily': text_field,
    'moody': text_field,
    'brawler': text_field,
    'deny_mistakes_blame_others': text_field,
    'less_ask_teacher_help': text_field,
}

HYPER_ACTIVITY_TROUBLE_Teacher = {
    'restless_squirms_chair': text_field,
    'inappropriate_noises': text_field,
    'immediately_satisfied_needs': text_field,
    'annoy_students': text_field,
    'goes_left_right': text_field,
    'easily_turn_on_impulsive': text_field,
    'excessive_attention_from_teacher': text_field
}

INATTENTION_Trouble_TEACHER = {
    'distracted': text_field,
    'dreamer': text_field,
    'led_by_others': text_field,
    'trouble_guiding_others': text_field,
    'trouble_finishing_things': text_field,
    'immature': text_field,
    'upset_easily_make_effort': text_field,
    'has_learning_difficulties': text_field,
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

FORM_ABR = {
    'restless_squirms_chair': text_field,
    'angry_unexpected_behavior': text_field,
    'distracted': text_field,
    'annoy_students': text_field,
    'pout_sulk_easily': text_field,
    'moody': text_field,
    'goes_left_right': text_field,
    'easily_turn_on_impulsive': text_field,
    'trouble_finishing_things': text_field,
    'upset_easily_make_effort': text_field
}


class BehaviorTroubleTeacherService(FormService):
    def __init__(self, repository=BehaviorTroubleTeacherRepository()):
        super().__init__(repository, fields=BEHAVIOR_TROUBLE_TEACHER_FIELDS)


class HyperActivityTroubleTeacherService(FormService):
    def __init__(self, repository=HyperActivityTroubleTeacherRepository()):
        super().__init__(repository, fields=hyperactivity_trouble_teacher)


class InattentionTroubleTeacherService(FormService):
    def __init__(self, repository=InattentionTroubleTeacherRepository()):
        super().__init__(repository, fields=INATTENTION_Trouble_TEACHER)


class FormAbrService(FormService):

    def __init__(self, repository=FormAbrRepository()):
        super().__init__(repository, fields=FORM_ABR)
