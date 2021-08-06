from django.urls import path

from common.models import text_field
from common.views import FormViewSet, ViewSet
from formteacher.models import BehaviorTroubleTeacherSerializer, ExtraTroubleTeacherSerializer, \
    HyperActivityTroubleTeacherSerializer, \
    ImpulsivityTroubleTeacherSerializer, InattentionTroubleTeacherSerializer
from formteacher.services import BehaviorTroubleTeacherService, ExtraTroubleTeacherService, \
    HyperActivityTroubleTeacherService, ImpulsivityTroubleTeacherService, InattentionTroubleTeacherService

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


behavior_trouble_teacher_list = BehaviorTroubleTeacherViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

behavior_trouble_teacher_object = BehaviorTroubleTeacherViewSet.as_view({
    'get': 'retreive',
    'put': 'update',
    'delete': 'delete'
})

impulsivity_trouble_teacher_list = ImpulsivityTroubleTeacherViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

impulsivity_trouble_teacher_object = ImpulsivityTroubleTeacherViewSet.as_view({
    'get': 'retreive',
    'put': 'update',
    'delete': 'delete'
})


hyperactivity_trouble_teacher_list = HyperActivityTroubleTeacherViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

hyperactivity_trouble_teacher_object = HyperActivityTroubleTeacherViewSet.as_view({
    'get': 'retreive',
    'put': 'update',
    'delete': 'delete'
})

extra_trouble_teacher_list = ExtraTroubleTeacherViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

extra_trouble_teacher_object = ExtraTroubleTeacherViewSet.as_view({
    'get': 'retreive',
    'put': 'update',
    'delete': 'delete'
})

inattention_trouble_teacher_list = InattentionTroubleTeacherViewSet.as_view({
    'get': 'list',
    'post': 'create'
})

inattention_trouble_teacher_object = InattentionTroubleTeacherViewSet.as_view({
    'get': 'retreive',
    'put': 'update',
    'delete': 'delete'
})

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
    path('inattention_trouble_teacher_list/<int:id>', inattention_trouble_teacher_object)
]
