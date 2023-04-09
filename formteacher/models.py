from django.db.models import CASCADE, ForeignKey, Model
from django.db.models.fields import FloatField, TextField
from rest_framework.serializers import ModelSerializer

from common.models import create_model_serializer


class BehaviorTroubleTeacher(Model):
    arrogant_impolite = TextField(null=False, db_column='arrogant_impolite')
    angry_unexpected_behavior = TextField(null=False, db_column='arrogant_impolite')
    sensitive_criticism = TextField(null=False, db_column='arrogant_impolite')
    pout_sulk_easily = TextField(null=False, db_column='arrogant_impolite')
    moody = TextField(null=False, db_column='arrogant_impolite')
    brawler = TextField(null=False, db_column='arrogant_impolite')
    deny_mistakes_blame_others = TextField(null=False, db_column='arrogant_impolite')
    less_ask_teacher_help = TextField(null=False, db_column='arrogant_impolite')
    patient = ForeignKey(null=False, on_delete=CASCADE, to='gestionpatient.Patient')
    score = FloatField(null=False)
    teacher = ForeignKey(null=False, on_delete=CASCADE, to='gestionusers')

    class Meta:
        db_table = 'behavior_trouble_teacher'


class HyperActivityTroubleTeacher(Model):
    #  1,  2,  3, 8, 14, 15, 16
    restless_squirms_chair = TextField(db_column='restless_squirms_chair', null=False)
    inappropriate_noises = TextField(null=False, db_column='inappropriate_noises')
    immediately_satisfied_needs = TextField(null=False, db_column='immediately_satisfied_needs')
    annoy_students = TextField(null=False, db_column='annoy_students')
    goes_left_right = TextField(null=False, db_column='goes_left_right')
    easily_turn_on_impulsive = TextField(null=False, db_column='easily_turn_on_impulsive')
    excessive_attention_from_teacher = TextField(null=False, db_column='excessive_attention_from_teacher')
    patient = ForeignKey(null=False, on_delete=CASCADE, to=patient_model_location)
    score = FloatField(null=False)
    teacher = ForeignKey(null=False, on_delete=CASCADE, to='gestionusers.Teacher')

    class Meta:
        db_table = 'hyperactivity_form_teacher'


class InattentionTroubleTeacher(Model):
    distracted = TextField(null=False, db_column='distracted')
    dreamer = TextField(null=False, db_column='dreamer')
    led_by_others = TextField(null=False, db_column="led_by_others")
    trouble_guiding_others = TextField(null=False, db_column='trouble_guiding_others')
    trouble_finishing_things = TextField(null=False, db_column='trouble_finishing_things')
    immature = TextField(null=False, db_column='immature')
    upset_easily_make_effort = TextField(null=False, db_column='upset_easily_make_eff')
    has_learning_difficulties = TextField(null=False, db_column='has_learning_difficulties')
    patient = ForeignKey(null=False, on_delete=CASCADE, to=patient_model_location)
    score = FloatField(null=False)
    teacher = ForeignKey(null=False, on_delete=CASCADE, to='gestionusers.Teacher')

    class Meta:
        db_table = 'inattention_disorder_form_teacher'


class FormAbr(Model):
    restless_squirms_chair = TextField(null=False)
    angry_unexpected_behavior = TextField(null=False)
    distracted = TextField(null=False)
    annoy_students = TextField(null=False)
    pout_sulk_easily = TextField(null=False)
    moody = TextField(null=False)
    goes_left_right = TextField(null=False)
    easily_turn_on_impulsive = TextField(null=False)
    trouble_finishing_things = TextField(null=False)
    upset_easily_make_effort = TextField(null=False)
    patient = ForeignKey(null=False, on_delete=CASCADE, to=patient_model_location)
    score = FloatField(null=False)
    teacher = ForeignKey(null=False, on_delete=CASCADE, to='gestionusers.Teacher')

    class Meta:
        db_table = 'form_abr_teacher'


class BehaviorTroubleTeacherSerializer(ModelSerializer):
    class Meta:
        model = BehaviorTroubleTeacher
        fields = '__all__'


class HyperActivityTroubleTeacherSerializer(ModelSerializer):
    class Meta:
        model = HyperActivityTroubleTeacher
        fields = '__all__'


class InattentionTroubleTeacherSerializer(ModelSerializer):
    class Meta:
        model = InattentionTroubleTeacher
        fields = '__all__'


class FormAbrSerializer(ModelSerializer):
    class Meta:
        model = FormAbr
        fields = '__all__'
