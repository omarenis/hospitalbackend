from django.urls import path
from rest_framework.response import Response
from common.repositories import Repository
from common.services import Service
from common.views import ViewSet
from .models import Message, MessageSerializer
from django.db.models import Q
MESSAGE_FIELDS = {
    'sender': {'type': 'text', 'required': True},
    'receivers': {'type': 'text', 'required': True},
    'subject': {'type': 'text', 'required': True},
    'content': {'type': 'text', 'required': True},
    'date': {'type': 'date', 'required': True},
    'read': {'type': 'bool', 'required': False}
}


class MessageRepository(Repository):
    def __init__(self, model=Message):
        super().__init__(model)


class MessageServise(Service):
    def __init__(self, repository=MessageRepository()):
        super().__init__(repository, fields=MESSAGE_FIELDS)


class MessageViewSet(ViewSet):
    def __init__(self, serializer_class=MessageSerializer, service=MessageServise(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)

    def list(self, request, *args, **kwargs):
        email = request.GET.get('email')
        if email is None:
            return super().list(request=request)
        messeges = Message.objects.filter(Q(sender__contains=email) | Q(receivers__contains=email))
        if messeges:
            return Response(data=[self.serializer_class(i).data for i in messeges])
        return Response(data=[])


messages, message = MessageViewSet.get_urls()


urlpatterns = [
    path('', messages),
    path('<int:pk>', message)
]
