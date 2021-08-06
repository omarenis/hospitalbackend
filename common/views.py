from requests import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR, \
    HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response

from common.services import calculate_score


def extract_data_with_validation(request, fields: dict):
    output = {}
    attrs = list(request.data.keys()) + list(request.files.keys())
    for i in set(attrs):
        if i in fields:
            value = request.files.get(i) if fields[i].get('type') == 'file' \
                                            or fields[i].get('type') == 'image' else request.data.get(i)
            if value is None and fields[i]['required']:
                return Exception(f'{i} is required')
            else:
                output[i] = value
        else:
            return Exception(f'{i} is not an attribute for the model')
    return output


class ViewSet(ModelViewSet):
    def __init__(self, fields: dict, serializer_class, service, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = serializer_class
        self.fields = fields
        self.service = service

    def list(self, request, *args, **kwargs):
        _objects = self.service.list()
        if not _objects:
            return Response(data=[], status=HTTP_200_OK)
        return Response(data=[self.serializer_class(i).data for i in _objects], status=HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        data = extract_data_with_validation(request=request, fields=self.fields)
        if isinstance(data, Exception):
            return Response(data={'error': str(data)}, status=HTTP_400_BAD_REQUEST)
        else:
            _object = self.service.create(data)
            if isinstance(_object, Exception):
                return Response(data={"error": str(_object)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
            else:
                return Response(data=self.serializer_class(_object).data, status=HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        data = self.service.retreive(_id=pk)
        if data is None:
            return Response(data={'error': 'object not found'}, status=HTTP_404_NOT_FOUND)
        else:
            return Response(data=self.serializer_class(data).data, status=HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=HTTP_400_BAD_REQUEST)
        _object = self.service.retrieve(_id=pk)
        if _object is None:
            return Response(data={'error': 'object not found'}, status=HTTP_404_NOT_FOUND)
        return Response(data=self.serializer_class(_object).data, status=HTTP_201_CREATED)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=HTTP_400_BAD_REQUEST)
        deleted = self.service.delete(pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=HTTP_404_NOT_FOUND)
        return Response(data={'response': True}, status=200)

    @classmethod
    def get_urls(cls):
        return cls.as_view({'get': 'list', 'post': 'create'}), cls.as_view(
            {'get': 'retreive', 'put': 'update', 'delete': 'delete'}
        )


class FormViewSet(ViewSet):
    def __init__(self, fields: dict, serializer_class, service, **kwargs):
        super().__init__(fields, serializer_class, service, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        fields = list(self.fields.keys())
        score = calculate_score(data=data, fields=fields)
        if isinstance(score, Exception):
            return Response(data={'error': str(score)}, status=HTTP_400_BAD_REQUEST)
        request.data['score'] = score
        return super().create(request=request, *args, **kwargs)


class ParentFormViewSet(FormViewSet):
    def __init__(self, fields: dict, serializer_class, service, **kwargs):
        super().__init__(fields, serializer_class, service, **kwargs)

    def list(self, request, *args, **kwargs):
        patient_id = request.GET.get('patient_id')
        if patient_id is not None:
            data = self.service.filter_by({'patien__id': patient_id}).first()
            if data is None:
                return Response(data={'error': 'data not found'}, status=HTTP_404_NOT_FOUND)
            else:
                return Response(data=self.serializer_class(data).data, status=HTTP_200_OK)
        else:
            return super().create(request=request, *args, **kwargs)
