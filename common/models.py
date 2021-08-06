from django.db.models import Model
from rest_framework.serializers import ModelSerializer

patient_model_location = 'gestionpatient.Patient'
choices = (('never', 'never'), ('sometimes', 'sometimes'), ('usual', 'usual'), ('always', 'always'))

text_field = {'type': 'text', 'required': True}


def create_model(name, type_model, fields=None, app_label='', module='', options=None):
    class Meta:
        pass

    if app_label:
        setattr(Meta, 'app_label', app_label)

    # Update Meta with any options that were provided
    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)

    # Set up a dictionary to simulate declarations within a class
    attrs = {'__module__': module, 'Meta': Meta}

    if fields:
        attrs.update(fields)

    # Create the class, which automatically triggers ModelBase processing
    model = type(name, (type_model,), attrs)
    return model


def create_model_serializer(name, model, app_label='', fields='__all__'):
    class Meta:
        pass

    setattr(Meta, 'model', model)
    setattr(Meta, 'fields', fields)

    if app_label:
        setattr(Meta, 'app_label', app_label)

    return type(name, (ModelSerializer,), {'Meta': Meta})
