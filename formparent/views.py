from django.urls import path

from common.models import text_field
from common.views import ViewSet
from formparent.models import AnxityTroubleParentSerializer, ExtraTroubleParentSerializer, \
    HyperActivityTroubleParentSerializer, ImpulsivityTroubleParentSerializer, \
    LearningTroubleParentSerializer, SomatisationTroubleParentSerializer
from formparent.services import AnxityTroubleParentService, ExtraTroubleParentService, \
    HyperActivityTroubleParentService, ImpulsivityTroubleParentService, \
    LearningTroubleParentService, SomatisationTroubleParentService
BEHAVIOR_TROUBLE_PARENTS = {
    'insolentWthGrownUps': text_field,
    'feelsAttackedDefensive': text_field,
    'descructive': text_field,
    'denyMistakesBlameOthers': text_field,
    'quarrelsomeGetInvolvedFight': text_field,
    'bullyIntimidateComrades': text_field,
    'constantlyFight': text_field,
    'unhappy': text_field
}
LEARNING_TROUBLE_PARENT_FIELDS = {
    'hasLearningDifficuties': text_field,
    'troubleFinishingThings': text_field,
    'easilyBeingDistracted': text_field,
    'enabilityFinishWhenDoEffort': text_field
}
SOMATISATION_TROUBLE_PARENT_FIELDS = {
    'headaches': text_field,
    'upsetStomach': text_field,
    'physicalAches': text_field,
    'vomitingNausea': text_field
}
IMPULSIVITY_TROUBLE_PARENT_FIELD = {
    'excitableImpulsif': text_field,
    'wantDominate': text_field,
    'squirms': text_field,
    'restlessNeedsDoSomething': text_field
}
ANXITY_TROUBLE_PARENT_FIELDS = {
    'afraidNewThings': text_field,
    'shy': text_field,
    'worryMuch': text_field,
    'beingCrashedManipulated': text_field
}

HYPERACTIVITY_TROUBLE_PARENT_FIELDS = {
    'excitableImpulsif': text_field,
    'cryOftenEasily': text_field,
    'squirms': text_field,
    'restlessNeedsDoSomething': text_field,
    'desctructive': text_field,
    'troubleFinishingThings': text_field,
    'easilyBeingDistracted': text_field,
    'moody': text_field,
    'enabilityFinishWhenDoEffort': text_field,
    'disrurbOtherChildren': text_field
}

EXTRA_TROUBLE_PARENT_FIELDS = {
    'chewMibThings': text_field,
    'troubleMakeKeepFriends': text_field,
    'suckChewThings': text_field,
    'dreamer': text_field,
    'lieMadeUpStories': text_field,
    'getTroublesMoreThanOthers': text_field,
    'speakLikeBabyStutters': text_field,
    'poutSulkEasily': text_field,
    'stealThings': text_field,
    'disobeyReluctantlyObey': text_field,
    'easilyWrinkledEasilyAngry': text_field,
    'troubleFinishRepetitiveActivity': text_field,
    'cruel': text_field,
    'immature': text_field,
    'breakRules': text_field,
    'notGetAlongWithBrothers': text_field,
    'feedingProblems': text_field,
    'sleepingProblems': text_field,
    'feelWrongedCryOutInjustice': text_field,
    'bragsBoastful': text_field,
    'bowelMovementProblems': text_field
}


class AnxityTroubleParentViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=AnxityTroubleParentSerializer,
                 service=AnxityTroubleParentService(), **kwargs):
        if fields is None:
            fields = ANXITY_TROUBLE_PARENT_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


class ImpulsivityTroubleParentViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=ImpulsivityTroubleParentSerializer,
                 service=ImpulsivityTroubleParentService, **kwargs):
        if fields is None:
            fields = IMPULSIVITY_TROUBLE_PARENT_FIELD
        super().__init__(fields, serializer_class, service, **kwargs)


class LearningTroubleParentViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=LearningTroubleParentSerializer,
                 service=LearningTroubleParentService(), **kwargs):
        if fields is None:
            fields = LEARNING_TROUBLE_PARENT_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


class SomatisationTroubleParentViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=SomatisationTroubleParentSerializer,
                 service=SomatisationTroubleParentService(), **kwargs):
        if fields is None:
            fields = SOMATISATION_TROUBLE_PARENT_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


class HyperActivityTroubleParentViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=HyperActivityTroubleParentSerializer,
                 service=HyperActivityTroubleParentService(), **kwargs):
        if fields is None:
            fields = HYPERACTIVITY_TROUBLE_PARENT_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


class ExtraTroubleParentViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=ExtraTroubleParentSerializer,
                 service=ExtraTroubleParentService(), **kwargs):
        if fields is None:
            fields = EXTRA_TROUBLE_PARENT_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)


anxity_trouble_parent_list, anxity_trouble_parent_object = AnxityTroubleParentViewSet.get_urls()
impulsivity_trouble_parent_list, impulsivity_trouble_parent_object = ImpulsivityTroubleParentViewSet.get_urls()
learning_trouble_parent_list, learning_trouble_parent_object = LearningTroubleParentViewSet.get_urls()

urlpatterns = [
    path('anxity_trouble_parent_list', anxity_trouble_parent_list),
    path('anxity_trouble_parent_list/<int:id>', anxity_trouble_parent_object),
    path('impulsivity_trouble_parent_list', impulsivity_trouble_parent_list),
    path('impulsivity_trouble_parent_list/<int:id>', impulsivity_trouble_parent_object),
    path('learning_trouble_parent_list', learning_trouble_parent_list),
    path('learning_trouble_parent_list/<int:id>', learning_trouble_parent_object)
]
