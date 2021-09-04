from django.db.models import ForeignKey, Model, SET_NULL, TextField
from common.models import create_model, create_model_serializer
MESSAGE_FIELD = {
    "subject": TextField(null=False, db_column='subject'),
    "content": TextField(null=False, db_column='content'),
    "sender": ForeignKey(to='gestionusers.Person', on_delete=SET_NULL),
    "receiver": ForeignKey(to='gestionusers.Person', on_delete=SET_NULL)
}

Message = create_model(name="MESSAGE", type_model=Model, fields=MESSAGE_FIELD, app_label="messages",
                       options={'db_table': 'messages'})


MessageSerializer = create_model_serializer(name='MessageSerializer', model=Message, options={
    'fields': '__all__',
    'depth': 1
})
