from django.db.models import BooleanField, DateTimeField, Model, TextField
from rest_framework.serializers import ModelSerializer
from django.utils import timezone


class Message(Model):
    sender: TextField = TextField(null=False)
    receivers: TextField = TextField(null=False)
    subject: TextField = TextField(null=False)
    content: TextField = TextField(null=False)
    date: DateTimeField = DateTimeField(null=False, default=timezone.now())
    read: BooleanField = BooleanField(null=False, default=False)

    class Meta:
        db_table = 'messages'


class MessageSerializer(ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'
