from django.db.models import CASCADE, ForeignKey, Model
from django.db.models.fields import FloatField, TextField
from common.models import create_model_serializer, patient_model_location, create_model

app_label = 'formteacher'

restless_squirms_chair = {'restlessSquirmsChair': TextField(db_column='restless_squirms_chair', null=False)}

inappropriate_noises = {'inappropriateNoises': TextField(null=False, db_column='inappropriate_noises')}

immediately_satisfied_needs = {'immediatelySatisfiedNeeds': TextField(db_column='immediately_satisfied_needs', null=False)}

arrogant_impolite = {'arrogantImpolite': TextField(db_column='arrogant_impolite', null=False)}

angry_unexpected_behavior = {'angryUnexpectedBehavior': TextField(db_column='angry_unexpected_behavior', null=False)}

sensitive_criticism = {'sensitiveCriticism': TextField(db_column='sensitive_criticism', null=False)}

distracted = {'distracted': TextField(null=False)}

annoy_students = {'annoyStudents': TextField(db_column='sensitive_criticism', null=False)}

dreamer = {'dreamer': TextField(null=False)}

pout_sulk_easily = {'poutSulkEasily': TextField(db_column='pout_sulk_easily', null=False)}

moody = {'moody': TextField(null=False)}

brawler = {'brawler': TextField(null=False)}

submissive_attitude_towards_authority = {
    'submissiveAttitudeTowardsAuthority': TextField(db_column='submissive_attitude_towards_authority', null=False)
}

goes_left_right = {'goesLeftRight': TextField(db_column='goes_left_right', null=False)}

easily_turn_on_impulsive = {'easilyTurnOnImpulsive': TextField(db_column='easily_turn_on_impulsive', null=False)}

excessive_attention_from_teacher = {
    'excessiveAttentionFromTeacher': TextField(db_column='excessive_attention_from_teacher', null=False)
}

less_accepted_by_group = {'lessAcceptedByGroup': TextField(db_column='less_accepted_by_group', null=False)}

be_led_by_others = {'beLedByOthers': TextField(db_column='be_led_by_others', null=False)}

unaccept_defeat = {'unacceptDefeat': TextField(db_column='unaccept_defeat', null=False)}

trouble_guiding_others = {'troubleGuidingOthers': TextField(db_column='trouble_guiding_others', null=False)}

trouble_finishing_things = {'troubleFinishingThings': TextField(db_column='trouble_finishing_things', null=False)}

immature = {'immature': TextField(null=False)}

deny_mistakes_blame_others = {'denyMistakesBlameOthers': TextField(db_column='deny_mistakes_blame_others', null=False)}

trouble_integrating_with_other_students = {
    'troubleIntegratingWithOtherStudents': TextField(db_column='trouble_integrating_with_other_students', null=False)
}
less_cooperate_with_others = {'lessCooperateWithOthers': TextField(db_column='less_cooperate_with_others', null=False)}
upset_easily_make_effort = {'upsetEasilyMakeEffort': TextField(db_column='upset_easily_make_effort', null=False)}
less_ask_teacher_help = {'lessAskTeacherHelp': TextField(db_column='less_ask_teacher_help', null=False)}
has_learning_difficulties = {'hasLearningDifficulties': TextField(db_column='has_learning_difficulties', null=False)}

FORM_FIELDS = {
    'patient': ForeignKey(null=False, on_delete=CASCADE, to=patient_model_location),
    'score': FloatField(null=False)
}

BEHAVIOR_TROUBLE_TEACHER_FIELDS = {
    **immediately_satisfied_needs,
    **angry_unexpected_behavior,
    **sensitive_criticism,
    **pout_sulk_easily,
    **moody,
    **brawler,
    **deny_mistakes_blame_others,
    **less_ask_teacher_help
}
IMPULSIVITY_TROUBLE_TEACHER_FIELDS = {
    **restless_squirms_chair,
    **inappropriate_noises,
    **arrogant_impolite,
    **annoy_students,
    **goes_left_right,
    **easily_turn_on_impulsive,
    **excessive_attention_from_teacher
}
INATTENTION_TROUBLE_TEACHER = {
    **distracted,
    **dreamer,
    **be_led_by_others,
    **trouble_guiding_others,
    **trouble_finishing_things,
    **immature,
    **upset_easily_make_effort,
    **has_learning_difficulties
}
HYPER_ACTIVITY_TROUBLE_TEACHER_FIELDS = {
    **restless_squirms_chair,
    **angry_unexpected_behavior,
    **distracted,
    **annoy_students,
    **pout_sulk_easily,
    **moody,
    **goes_left_right,
    **easily_turn_on_impulsive,
    **trouble_finishing_things,
    **upset_easily_make_effort
}
EXTRA_TROUBLE_TEACHER_FIELDS = {
    **submissive_attitude_towards_authority,
    **less_accepted_by_group,
    **unaccept_defeat,
    **trouble_integrating_with_other_students,
    **less_cooperate_with_others
}

Form = create_model(name='Form', type_model=Model, fields=FORM_FIELDS, app_label=app_label, options={'abstract': True})
BehaviorTroubleTeacher = create_model(name='BehaviorTroubleTeacher', type_model=Form, app_label=app_label,
                                      options={'db_table': 'behavoir_trouble_teacher'},
                                      fields=BEHAVIOR_TROUBLE_TEACHER_FIELDS)
HyperActivityTroubleTeacher = create_model(name='HyperActivityTroubleTeacher', type_model=Form,
                                           fields=HYPER_ACTIVITY_TROUBLE_TEACHER_FIELDS, app_label=app_label,
                                           options={'db_table': 'hyperactivity_trouble_teacher'})
ImpulsivityTroubleTeacher = create_model(name='ImpulsivityTroubleTeacher', app_label=app_label, type_model=Form,
                                         fields=IMPULSIVITY_TROUBLE_TEACHER_FIELDS)
InattentionTroubleTeacher = create_model(name='InattentionTroubleTeacher', type_model=Form, app_label=app_label,
                                         fields=INATTENTION_TROUBLE_TEACHER,
                                         options={'db_table': 'inattention_trouble_teacher'})
ExtraTroubleTeacher = create_model(name='ExtraTroubleTeacher', type_model=Form, fields=EXTRA_TROUBLE_TEACHER_FIELDS,
                                   app_label=app_label, options={'db_table': 'extra_trouble_teacher'})

BehaviorTroubleTeacherSerializer = create_model_serializer(model=BehaviorTroubleTeacher,
                                                           name='BehaviorTroubleTeacherSerializer')
HyperActivityTroubleTeacherSerializer = create_model_serializer(model=HyperActivityTroubleTeacher,
                                                                name='HyperActivityTroubleTeacherSerializer')

ImpulsivityTroubleTeacherSerializer = create_model_serializer(name="ImpulsivityTroubleTeacherSerializer",
                                                              model=ImpulsivityTroubleTeacher)
ExtraTroubleTeacherSerializer = create_model_serializer(name='ExtraTroubleTeacherSerializer',
                                                        model=ExtraTroubleTeacher)
InattentionTroubleTeacherSerializer = create_model_serializer(name='InattentionTroubleTeacherSerializer',
                                                              model=InattentionTroubleTeacher)
