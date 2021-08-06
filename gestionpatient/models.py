from django.db.models import CASCADE, DateField, EmailField, ForeignKey, Model, SET_DEFAULT, SET_NULL, TextField
from rest_framework.serializers import ModelSerializer


class Patient(Model):
    name: TextField = TextField(db_column='name', null=False)
    familyName = TextField(db_column='family_name', null=False)
    birthdate: DateField = DateField()
    school: TextField = TextField(null=False)
    parent = ForeignKey('gestionusers.Parent', on_delete=CASCADE, null=True)
    doctor = ForeignKey('gestionusers.Doctor', on_delete=SET_NULL, null=True)

    class Meta:
        db_table = 'patients'
        unique_together = (('name', 'familyName'), )


class Orientation(Model):
    patient: ForeignKey = ForeignKey(to='Patient', on_delete=CASCADE, null=False)
    doctor: ForeignKey = ForeignKey(to='gestionusers.Doctor', on_delete=SET_NULL, null=True)
    diagnostic: TextField = TextField(null=False)

    class Meta:
        db_table = 'orientations'


class PatientSerializer(ModelSerializer):
    class Meta:
        model = Patient
        fields = '__all__'


class OrientationSerializer(ModelSerializer):
    class Meta:
        model = Orientation
        fields = '__all__'
