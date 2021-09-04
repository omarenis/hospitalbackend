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


def create_model_serializer(name, model, module='', app_label='', fields=None, options=None):
    class Meta:
        pass

    attrs = {'__module__': module, 'Meta': Meta}
    setattr(Meta, 'model', model)
    if fields:
        attrs.update(fields)

    if options is not None:
        for key, value in options.items():
            setattr(Meta, key, value)
    else:
        setattr(Meta, 'fields', '__all__')

    if app_label:
        setattr(Meta, 'app_label', app_label)

    return type(name, (ModelSerializer,), {'Meta': Meta})
