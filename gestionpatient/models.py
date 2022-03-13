from django.db.models import BooleanField, CASCADE, DateField, DateTimeField, ForeignKey, ManyToManyField, Model, \
    OneToOneField, TextField
from common.models import create_model_serializer
import django.utils.timezone as timezone
from gestionusers.models import PersonSerializer
app_label = 'gestionpatient'
doctor_model = 'gestionusers.Doctor'


class Patient(Model):
    parent = ForeignKey(to='gestionusers.Parent', on_delete=CASCADE, null=True)
    name: TextField = TextField(null=False)
    familyName: TextField = TextField(null=False)
    birthdate: DateField = DateField(null=False)
    sick: BooleanField = BooleanField(default=False, null=False)

    class Meta:
        db_table = 'patients'
        unique_together = (('parent_id', 'name', 'familyName', 'birthdate'),)


class Supervise(Model):
    patient: OneToOneField = OneToOneField(to='Patient', on_delete=CASCADE, null=False)
    doctor: ForeignKey = ForeignKey(to=doctor_model, on_delete=CASCADE, null=False)
    accepted: BooleanField = BooleanField(null=False, default=False)

    class Meta:
        db_table = 'supervises'


class Consultation(Model):
    doctor: ForeignKey = ForeignKey(to=doctor_model, on_delete=CASCADE, null=False)
    parent: ForeignKey = ForeignKey(to='gestionusers.Parent', on_delete=CASCADE, null=False)
    date: DateTimeField = DateTimeField(null=False, default=timezone.now)
    accepted: BooleanField = BooleanField(null=False, default=False)

    class Meta:
        db_table = 'consultations'


class Diagnostic(Model):
    consultation: OneToOneField = OneToOneField(to='Consultation', on_delete=CASCADE)
    patient: ForeignKey = ForeignKey(to='Patient', on_delete=CASCADE, null=False)
    diagnostic: TextField = TextField(null=False)

    class Meta:
        db_table = 'diagnostics'


SuperviseSerializer = create_model_serializer(model=Supervise, app_label=app_label, name='SuperviseSerializer')
PatientGetSerializer = create_model_serializer(model=Patient, name='PatientGetSerializer', app_label=app_label,
                                               options={
                                                   'fields': 'all'
                                               })
PatientSerializer = create_model_serializer(model=Patient, name='PatientSerializer', app_label=app_label, options={
    'fields': ['id', 'name', 'familyName', 'birthdate', 'parent', 'behaviortroubleparent',
               'impulsivitytroubleparent', 'learningtroubleparent', 'anxitytroubleparent',
               'somatisationtroubleparent', 'hyperactivitytroubleparent', 'extratroubleparent', 'supervise', 'sick'],
    'depth': 1
}, fields={
    'supervise': SuperviseSerializer(read_only=True)
})

DiagnosticSerializer = create_model_serializer(model=Diagnostic, name='DiagnosticSerializer', app_label=app_label)

ConsultationSerilaizer = create_model_serializer(model=Consultation, name='ConsultationSerilaizer', fields={
    'parent': PersonSerializer(read_only=True),
    'doctor': PersonSerializer(read_only=True),
    'diagnostic': PersonSerializer(read_only=True)
}, options={
    'fields': ['parent_id', 'doctor_id', 'parent', 'doctor', 'date', 'accepted', 'diagnostic', 'id']
}, app_label=app_label)
