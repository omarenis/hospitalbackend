from django.urls import path

from common.models import text_field
from common.views import FormViewSet, ViewSet
from formteacher.models import BehaviorTroubleTeacherSerializer, ExtraTroubleTeacherSerializer, \
    HyperActivityTroubleTeacherSerializer, \
    ImpulsivityTroubleTeacherSerializer, InattentionTroubleTeacherSerializer, TeacherSerializer
from formteacher.services import BehaviorTroubleTeacherService, ExtraTroubleTeacherService, \
    HyperActivityTroubleTeacherService, ImpulsivityTroubleTeacherService, InattentionTroubleTeacherService, \
    TeacherService

TEACHER_FIELDS = {
    'name': {'type': 'text', 'required': True},
    'familyName': {'type': 'text', 'required': True},
    'cin': {'type': 'text', 'required': True},
    'telephone': {'type': 'text', 'required': True}
}

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


class BehaviorTroubleTeacherViewSet(FormViewSet):
    def __init__(self, fields=None, serializer_class=BehaviorTroubleTeacherSerializer,
                 service=BehaviorTroubleTeacherService(), **kwargs):
        if fields is None:
            fields = behavior_trouble_teacher_fields
        super().__init__(fields, serializer_class, service, **kwargs)


class HyperActivityTroubleTeacherViewSet(FormViewSet):
    def __init__(self, fields=None, serializer_class=HyperActivityTroubleTeacherSerializer,
                 service=HyperActivityTroubleTeacherService(), **kwargs):
        if fields is None:
            fields = hyperactivity_trouble_teacher
        super().__init__(fields, serializer_class, service, **kwargs)


class ImpulsivityTroubleTeacherViewSet(FormViewSet):
    def __init__(self, fields=None, serializer_class=ImpulsivityTroubleTeacherSerializer,
                 service=ImpulsivityTroubleTeacherService(), **kwargs):
        if fields is None:
            fields = impulsivity_trouble_teacher_fields
        super().__init__(fields, serializer_class, service, **kwargs)


class ExtraTroubleTeacherViewSet(FormViewSet):
    def __init__(self, fields=None, serializer_class=ExtraTroubleTeacherSerializer,
                 service=ExtraTroubleTeacherService(), **kwargs):
        if fields is None:
            fields = extra_trouble_teacher
        super().__init__(fields, serializer_class, service, **kwargs)


class InattentionTroubleTeacherViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=InattentionTroubleTeacherSerializer,
                 service=InattentionTroubleTeacherService(), **kwargs):
        if fields is None:
            fields = inattention_trouble_teacher
        super().__init__(fields, serializer_class, service, **kwargs)


class TeacherViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=TeacherSerializer, service=TeacherService(), **kwargs):
        if fields is None:
            fields = TEACHER_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


teachers, teacher = TeacherViewSet.get_urls()

behavior_trouble_teacher_list, behavior_trouble_teacher_object = BehaviorTroubleTeacherViewSet.get_urls()


impulsivity_trouble_teacher_list, impulsivity_trouble_teacher_object = ImpulsivityTroubleTeacherViewSet.get_urls()


hyperactivity_trouble_teacher_list, hyperactivity_trouble_teacher_object = HyperActivityTroubleTeacherViewSet.get_urls()

extra_trouble_teacher_list, extra_trouble_teacher_object = ExtraTroubleTeacherViewSet.get_urls()

inattention_trouble_teacher_list, inattention_trouble_teacher_object = InattentionTroubleTeacherViewSet.get_urls()

urlpatterns = [
    path('behavior_trouble_teacher_list', behavior_trouble_teacher_list),
    path('behavior_trouble_teacher_list/<int:id>', behavior_trouble_teacher_object),
    path('impulsivity_trouble_teacher_list', impulsivity_trouble_teacher_list),
    path('impulsivity_trouble_teacher_list/<int:id>', impulsivity_trouble_teacher_list),
    path('hyperactivity_trouble_teacher_list', hyperactivity_trouble_teacher_list),
    path('hyperactivity_trouble_teacher_list/<int:id>', hyperactivity_trouble_teacher_object),
    path('extra_trouble_teacher_list', extra_trouble_teacher_list),
    path('extra_trouble_teacher_list/<int:id>', extra_trouble_teacher_object),
    path('inattention_trouble_teacher_list', inattention_trouble_teacher_list),
    path('inattention_trouble_teacher_list/<int:id>', inattention_trouble_teacher_object),
    path('teachers', teachers),
    path('teachers/:id', teacher)
]
