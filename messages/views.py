import africastalking
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST
from common.repositories import Repository
from common.services import Service
from common.views import ViewSet
from .models import Message, MessageSerializer
from backend.settings import ADMIN_NUMBER
import clx.xms.client as client

service = client.Client(service_plan_id="e6a0e9cb31844f44b42ad3ab1cc0fe17", token="bf729d137c1441a6bba5692685fa9985")


MESSAGE_FIELDS = {
    'sender': {'type': 'text', 'required': True},
    'receiver': {'type': 'text', 'required': False},
    'content': {'type': 'text', 'required': True}
}


class MessageRepository(Repository):
    def __init__(self, model=Message):
        super().__init__(model)


class MessageService(Service):
    def __init__(self, repository=MessageRepository()):
        super().__init__(repository)

    def create(self, data: dict):
        if data.get('sender') is None:
            return Exception('sender required')
        if data.get('content') is None:
            return Exception('content required')
        receiver = data.get('receiver') if data.get('receiver') is not None else ADMIN_NUMBER
        try:
            service.create_text_message(sender=data.get('sender'), recipient=receiver, body=data.get('content'))
            message = super().create(data=data)
            if isinstance(message, Exception):
                raise message
            return message
        except Exception as exception:
            return exception


class MessageViewSet(ViewSet):
    def __init__(self, fields=None, serializer_class=MessageSerializer, service=MessageService(), **kwargs):
        if fields is None:
            fields = MESSAGE_FIELDS
        super().__init__(fields, serializer_class, service, **kwargs)
