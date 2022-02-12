from common.models import text_field
from common.services import FormService
from .repositories import AnxityTroubleParentRepository, BehaviorTroubleParentRepository, \
    ExtraTroubleParentRepository, HyperActivityTroubleParentRepository, ImpulsivityTroubleParentRepository, \
    LearningTroubleParentRepository, SomatisationTroubleParentRepository

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


class AnxityTroubleParentService(FormService):
    def __init__(self, repository=AnxityTroubleParentRepository()):
        super().__init__(repository, fields=ANXITY_TROUBLE_PARENT_FIELDS)


class ImpulsivityTroubleParentService(FormService):
    def __init__(self, repository=ImpulsivityTroubleParentRepository()):
        super().__init__(repository, IMPULSIVITY_TROUBLE_PARENT_FIELD)


class LearningTroubleParentService(FormService):
    def __init__(self, repository=LearningTroubleParentRepository()):
        super().__init__(repository, LEARNING_TROUBLE_PARENT_FIELDS)


class SomatisationTroubleParentService(FormService):
    def __init__(self, repository=SomatisationTroubleParentRepository()):
        super().__init__(repository, fields=SOMATISATION_TROUBLE_PARENT_FIELDS)


class HyperActivityTroubleParentService(FormService):
    def __init__(self, repository=HyperActivityTroubleParentRepository()):
        super().__init__(repository, fields=HYPERACTIVITY_TROUBLE_PARENT_FIELDS)


class BehaviorTroubleParentService(FormService):
    def __init__(self, repository=BehaviorTroubleParentRepository()):
        super().__init__(repository, fields=BEHAVIOR_TROUBLE_PARENTS)


class ExtraTroubleParentService(FormService):
    def __init__(self, repository=ExtraTroubleParentRepository()):
        super().__init__(repository, fields=EXTRA_TROUBLE_PARENT_FIELDS)
