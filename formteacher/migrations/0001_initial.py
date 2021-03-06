# Generated by Django 3.2.1 on 2021-08-07 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BehaviorTroubleTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('immediatelySatisfiedNeeds', models.TextField(db_column='immediately_satisfied_needs')),
                ('angryUnexpectedBehavior', models.TextField(db_column='angry_unexpected_behavior')),
                ('sensitiveCriticism', models.TextField(db_column='sensitive_criticism')),
                ('poutSulkEasily', models.TextField(db_column='pout_sulk_easily')),
                ('moody', models.TextField()),
                ('brawler', models.TextField()),
                ('denyMistakesBlameOthers', models.TextField(db_column='deny_mistakes_blame_others')),
                ('lessAskTeacherHelp', models.TextField(db_column='less_ask_teacher_help')),
                ('score', models.FloatField()),
            ],
            options={
                'db_table': 'behavoir_trouble_teacher',
            },
        ),
        migrations.CreateModel(
            name='ExtraTroubleTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submissiveAttitudeTowardsAuthority', models.TextField(db_column='submissive_attitude_towards_authority')),
                ('lessAcceptedByGroup', models.TextField(db_column='less_accepted_by_group')),
                ('unacceptDefeat', models.TextField(db_column='unaccept_defeat')),
                ('troubleIntegratingWithOtherStudents', models.TextField(db_column='trouble_integrating_with_other_students')),
                ('lessCooperateWithOthers', models.TextField(db_column='less_cooperate_with_others')),
                ('score', models.FloatField()),
            ],
            options={
                'db_table': 'extra_trouble_teacher',
            },
        ),
        migrations.CreateModel(
            name='HyperActivityTroubleTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restlessSquirmsChair', models.TextField(db_column='restless_squirms_chair')),
                ('angryUnexpectedBehavior', models.TextField(db_column='angry_unexpected_behavior')),
                ('distracted', models.TextField()),
                ('annoyStudents', models.TextField(db_column='sensitive_criticism')),
                ('poutSulkEasily', models.TextField(db_column='pout_sulk_easily')),
                ('moody', models.TextField()),
                ('goesLeftRight', models.TextField(db_column='goes_left_right')),
                ('easilyTurnOnImpulsive', models.TextField(db_column='easily_turn_on_impulsive')),
                ('troubleFinishingThings', models.TextField(db_column='trouble_finishing_things')),
                ('upsetEasilyMakeEffort', models.TextField(db_column='upset_easily_make_effort')),
                ('score', models.FloatField()),
            ],
            options={
                'db_table': 'hyperactivity_trouble_teacher',
            },
        ),
        migrations.CreateModel(
            name='ImpulsivityTroubleTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('restlessSquirmsChair', models.TextField(db_column='restless_squirms_chair')),
                ('inappropriateNoises', models.TextField(db_column='inappropriate_noises')),
                ('arrogantImpolite', models.TextField(db_column='arrogant_impolite')),
                ('annoyStudents', models.TextField(db_column='sensitive_criticism')),
                ('goesLeftRight', models.TextField(db_column='goes_left_right')),
                ('easilyTurnOnImpulsive', models.TextField(db_column='easily_turn_on_impulsive')),
                ('excessiveAttentionFromTeacher', models.TextField(db_column='excessive_attention_from_teacher')),
                ('score', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='InattentionTroubleTeacher',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('distracted', models.TextField()),
                ('dreamer', models.TextField()),
                ('beLedByOthers', models.TextField(db_column='be_led_by_others')),
                ('troubleGuidingOthers', models.TextField(db_column='trouble_guiding_others')),
                ('troubleFinishingThings', models.TextField(db_column='trouble_finishing_things')),
                ('immature', models.TextField()),
                ('upsetEasilyMakeEffort', models.TextField(db_column='upset_easily_make_effort')),
                ('hasLearningDifficulties', models.TextField(db_column='has_learning_difficulties')),
                ('score', models.FloatField()),
            ],
            options={
                'db_table': 'inattention_trouble_teacher',
            },
        ),
    ]
