from django.db.models import CASCADE, FloatField, Model, OneToOneField, TextField
from common.models import choices, create_model, patient_model_location, create_model_serializer

app_label = 'formparent'
PARENT_FORM_FIELDS = {
    'patient': OneToOneField(null=False, on_delete=CASCADE, to=patient_model_location),
    'score': FloatField(null=False)
}

chew_mib_things = {'chewMibThings': TextField(null=False, db_column="chew_mib_things", choices=choices)}
insolent_wth_grown_ups = {'insolentWithGrownUps': TextField(null=False, db_column='insolent_wth_grown_ups',
                                                           choices=choices)}
trouble_make_keep_friends = {'troubleMakeKeepFriends': TextField(null=False, db_column='trouble_make_keep_friends',
                                                                 choices=choices)}
excitable_impulsive = {'excitableImpulsive': TextField(null=False, db_column='excitable_impulsive', choices=choices)}
want_dominate = {'wantDominate': TextField(null=False, db_column='want_dominate', choices=choices)}
suck_chew_things = {'suckChewThings': TextField(null=False, db_column='suck_chew_things', choices=choices)}
cry_often_easily = {'cryOftenEasily': TextField(null=False, db_column='suck_chew_things', choices=choices)}
feels_attacked_defensive = {'feelsAttackedDefensive': TextField(null=False, db_column='feels_attacked_defensive',
                                                                choices=choices)}
dreamer = {'dreamer': TextField(null=False, db_column='dreamer', choices=choices)}
has_learning_difficulties = {'hasLearningDifficulties': TextField(null=False, db_column='has_learning_difficulties',
                                                                  choices=choices)}
squirms = {'squirms': TextField(null=False, db_column='squirms', choices=choices)}
afraid_new_things = {'afraidNewThings': TextField(null=False, db_column='afraid_new_things', choices=choices)}
restless_needs_do_something = {'restlessNeedsDoSomething': TextField(null=False, choices=choices)}
destructive = {'destructive': TextField(null=False, db_column='descructive', choices=choices)}
lie_made_up_stories = {'lieMadeUpStories': TextField(null=False, db_column='lie_made_up_stories', choices=choices)}
shy = {'shy': TextField(null=False, choices=choices)}
get_troubles_more_than_others = {
    'getTroublesMoreThanOthers': TextField(null=False, db_column='get_troubles_more_than_others', choices=choices)
}
speak_like_baby_stutters = {'speakLikeBabyStutters': TextField(null=False, db_column='speak_like_baby_stutters',
                                                               choices=choices)}
deny_mistakes_blame_others = {'denyMistakesBlameOthers': TextField(null=False, db_column='deny_mistakes_blame_others',
                                                                   choices=choices)}
quarrelsome_get_involved_fight = {
    'quarrelsomeGetInvolvedFight': TextField(null=False, db_column='quarrelsome_get_involved_fight', choices=choices)
}
pout_sulk_easily = {'poutSulkEasily': TextField(null=False, db_column='pout_sulk_easily', choices=choices)}
steal_things = {'stealThings': TextField(null=False, db_column='steal_things', choices=choices)}
disobey_reluctantly_obey = {'disobeyReluctantlyObey': TextField(null=False, db_column='disobey_reluctantly_obey',
                                                                choices=choices)}
worry_much = {'worryMuch': TextField(null=False, db_column='worry_much', choices=choices)}
trouble_finishing_things = {'troubleFinishingThings': TextField(null=False, db_column='trouble_finishing_things',
                                                                choices=choices)}
easily_wrinkled_easily_angry = {'easilyWrinkledEasilyAngry': TextField(null=False, choices=choices,
                                                                       db_column='easily_wrinkled_easily_angry')}
bully_intimidate_comrades = {'bullyIntimidateComrades': TextField(null=False, db_column='bully_intimidate_comrades')}
trouble_finish_repetitive_activity = {
    'troubleFinishRepetitiveActivity': TextField(null=False, db_column='trouble_finish_repetitive_activity')
}
cruel = {'cruel': TextField(null=False, db_column='cruel')}
immature = {'immature': TextField(null=False, db_column='immature')}
easily_being_distracted = {'easilyBeingDistracted': TextField(null=False, db_column='easily_being_distracted')}
headaches = {'headaches': TextField(null=False, db_column='headaches')}
moody = {'moody': TextField(null=False, db_column='moody')}
break_rules = {'breakRules': TextField(null=False, db_column='break_rules')}
constantly_fight = {'constantlyFight': TextField(null=False, db_column='constantly_fight')}
not_get_along_with_brothers = {
    'notGetAlongWithBrothers': TextField(null=False, db_column='not_get_along_with_brothers')
}
enability_finish_when_do_effort = {
    'enabilityFinishWhenDoEffort': TextField(null=False, db_column='enability_finish_when_do_effort')
}
disturb_other_children = {'disturbOtherChildren': TextField(null=False, db_column='disrurb_other_children')}
unhappy = {'unhappy': TextField(null=False, db_column='unhappy')}
feeding_problems = {'feedingProblems': TextField(null=False, db_column='feeding_problems')}
upset_stomach = {'upsetStomach': TextField(null=False, db_column='upset_stomach')}
sleeping_problems = {'sleepingProblems': TextField(null=False, db_column='sleeping_problems')}
physical_aches = {'physicalAches': TextField(null=False, db_column='physical_aches')}
vomiting_nausea = {'vomitingNausea': TextField(null=False, db_column='vomiting_nausea')}
feel_wronged_cry_out_injustice = {
    'feelWrongedCryOutInjustice': TextField(null=False, db_column='feel_wronged_cry_out_injustice')
}
brags_boastful = {'bragsBoastful': TextField(null=False, db_column='brags_boastful')}
being_crashed_manipulated = {'beingCrashedManipulated': TextField(null=False, db_column='being_crashed_manipulated')}
bowel_movement_problems = {'bowelMovementProblems': TextField(null=False, db_column='bowel_movement_problems')}
BEHAVIOR_TROUBLE_PARENTS = {
    **insolent_wth_grown_ups,
    **feels_attacked_defensive,
    **destructive,
    **deny_mistakes_blame_others,
    **quarrelsome_get_involved_fight,
    **bully_intimidate_comrades,
    **constantly_fight,
    **unhappy
}
LEARNING_TROUBLE_PARENTS = {
    **has_learning_difficulties,
    **trouble_finishing_things,
    **easily_being_distracted,
    **enability_finish_when_do_effort
}
SOMATISATION_TORUBLE_PARENTS = {
    **headaches,
    **upset_stomach,
    **physical_aches,
    **vomiting_nausea
}
IMPULSIVITY_TROUBLE_PARENTS = {
    **excitable_impulsive,
    **want_dominate,
    **squirms,
    **restless_needs_do_something
}
ANXITY_TROUBLE_PARENTS = {
    **afraid_new_things,
    **shy,
    **worry_much,
    **being_crashed_manipulated
}
HYPERACTIVITY_TROUBLE_PARENTS = {
    **excitable_impulsive,
    **cry_often_easily,
    **squirms,
    **restless_needs_do_something,
    **destructive,
    **trouble_finishing_things,
    **easily_being_distracted,
    **moody,
    **enability_finish_when_do_effort,
    **disturb_other_children
}
EXTRA_TROUBLE_PARENTS = {
    **chew_mib_things,
    **trouble_make_keep_friends,
    **suck_chew_things,
    **dreamer,
    **lie_made_up_stories,
    **get_troubles_more_than_others,
    **speak_like_baby_stutters,
    **pout_sulk_easily,
    **steal_things,
    **disobey_reluctantly_obey,
    **easily_wrinkled_easily_angry,
    **trouble_finish_repetitive_activity,
    **cruel,
    **immature,
    **break_rules,
    **not_get_along_with_brothers,
    **feeding_problems,
    **sleeping_problems,
    **feel_wronged_cry_out_injustice,
    **brags_boastful,
    **bowel_movement_problems
}
ParentForm = create_model(type_model=Model, name='ParentForm', fields=PARENT_FORM_FIELDS, options={'abstract': True})

BehaviorTroubleParent = create_model(name='BehaviorTroubleParent', app_label=app_label, type_model=ParentForm,
                                     options={'db_table': 'behavior_trouble_parent'}, fields=BEHAVIOR_TROUBLE_PARENTS)
ImpulsivityTroubleParent = create_model(name='ImpulsivityTroubleParent', app_label=app_label, type_model=ParentForm,
                                        options={'db_table': 'impulisivity_trouble_parent'},
                                        fields=IMPULSIVITY_TROUBLE_PARENTS)
LearningTroubleParent = create_model(name='LearningTroubleParent', type_model=ParentForm, app_label=app_label,
                                     options={'db_table': 'learning_trouble_parent'}, fields=LEARNING_TROUBLE_PARENTS)
AnxityTroubleParent = create_model(type_model=ParentForm, fields=ANXITY_TROUBLE_PARENTS, name='AnxityTroubleParent',
                                   options={'db_table': 'anxity_trouble_parent'}, app_label=app_label)
SomatisationTroubleParent = create_model(name='SomatisationTroubleParent', type_model=ParentForm, app_label=app_label,
                                         fields=SOMATISATION_TORUBLE_PARENTS,
                                         options={'db_table': 'somatisation_trouble_parent'})
HyperActivityTroubleParent = create_model(name='HyperActivityTroubleParent', type_model=ParentForm, app_label=app_label,
                                          fields=HYPERACTIVITY_TROUBLE_PARENTS,
                                          options={'db_table': 'hyperactivity_trouble_parent'})
ExtraTroubleParent = create_model(name='ExtraTroubleParent', type_model=ParentForm, app_label=app_label,
                                  options={'db_table': 'extra_trouble_parent'}, fields=EXTRA_TROUBLE_PARENTS)

BehaviorTroubleParentSerializer = create_model_serializer(name='BehaviorTroubleParentSerializer', app_label=app_label,
                                                          model=BehaviorTroubleParent)
ImpulsivityTroubleParentSerializer = create_model_serializer(name='ImpulsivityTroubleParentSerializer',
                                                             app_label=app_label, model=ImpulsivityTroubleParent)
LearningTroubleParentSerializer = create_model_serializer(name='LearningTroubleParentSerializer', app_label=app_label,
                                                          model=LearningTroubleParent)
AnxityTroubleParentSerializer = create_model_serializer(name='AnxityTroubleParentSerializer', app_label=app_label,
                                                        model=AnxityTroubleParent)
SomatisationTroubleParentSerializer = create_model_serializer(name='SomatisationTroubleParentSerializer',
                                                              app_label=app_label, model=SomatisationTroubleParent)
HyperActivityTroubleParentSerializer = create_model_serializer(name='HyperActivityTroubleParentSerializer',
                                                               app_label=app_label, model=HyperActivityTroubleParent)
ExtraTroubleParentSerializer = create_model_serializer(name='ExtraTroubleParentSerializer', app_label=app_label,
                                                       model=ExtraTroubleParent)
