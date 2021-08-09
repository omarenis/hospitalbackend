from django.db.models import CASCADE, DateField, ForeignKey, Model, SET_NULL, TextField

from common.models import create_model, create_model_serializer

app_label = 'gestionpatient'


class Patient(Model):
    name: TextField = TextField(db_column='name', null=False)
    familyName = TextField(db_column='family_name', null=False)
    birthdate: DateField = DateField()
    school: TextField = TextField(null=False)
    parent = ForeignKey('gestionusers.Parent', on_delete=CASCADE, null=True)
    doctor = ForeignKey('gestionusers.Doctor', on_delete=SET_NULL, null=True)

    class Meta:
        db_table = 'patients'
        unique_together = (('name', 'familyName'),)


class Orientation(Model):
    patient: ForeignKey = ForeignKey(to='Patient', on_delete=CASCADE, null=False)
    doctor: ForeignKey = ForeignKey(to='gestionusers.Doctor', on_delete=SET_NULL, null=True)
    diagnostic: TextField = TextField(null=False)

    class Meta:
        db_table = 'orientations'


Teacher = create_model(name='Teacher', type_model=Model, fields={
    'name': TextField(), 'familyName': TextField(), 'cin': TextField(null=False, unique=True),
    'telephone': TextField()
}, app_label='gestionpatient', options={
    'db_table': 'teacher'
})

OrientationSerializer = create_model_serializer(model=Orientation, name='orientationSerializer')

PatientSerializer = create_model_serializer(model=Patient, name='PatientSerializer', app_label=app_label)

TeacherSerializer = create_model_serializer(model=Teacher, name='TeacherSerializer', app_label='gestionpatient')
