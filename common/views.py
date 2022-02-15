from requests import Response
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, \
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_201_CREATED, HTTP_200_OK
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from common.services import calculate_score


def return_serialized_data_or_error_response(_object, serializer_class, response_code) -> Response:
    try:
        return Response(data=serializer_class(_object).data, status=response_code)
    except Exception as exception:
        return Response(data=dict(error=str(exception)), status=HTTP_500_INTERNAL_SERVER_ERROR)


def extract_data_with_validation(request, fields: dict) -> dict or Exception:
    data = request.data
    if request.content_type == 'application/json':
        data += request.files
    output = {}
    for i in data:
        if fields.get(i) is None:
            return Exception(f'{i} is not an attribute for the model')
        value = data.get(i) if fields[i].get('type') == 'file' or fields[i].get('type') == 'image' \
            else request.data.get(i)
        if value is None and fields[i]['required']:
            return Exception(f'{i} is required')
        else:
            output[i] = value
    return output


def extract_get_data(request):
    output = {}
    for i in request.GET:
        try:
            output[i] = int(request.GET.get(i)) if request.GET.get(i).find('.') == -1 else float(request.GET.get(i))
        except Exception as exception:
            print(exception)
            if request.GET.get(i) == 'true' or request.GET.get(i) == 'false':
                output[i] = request.GET.get(i) == 'true'
            else:
                output[i] = request.GET.get(i)
    return output


def extract_serialized_objects_response(_objects, serializer_class) -> Response:
    output = []
    if _objects:
        try:
            for i in _objects:
                output.append(serializer_class(i).data)
        except Exception as exception:
            return Response(data={'error': str(exception)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
    return Response(data=output, status=HTTP_200_OK)


class ViewSet(ModelViewSet):
    def __init__(self, serializer_class, service, **kwargs):
        super().__init__(**kwargs)
        self.serializer_class = serializer_class
        self.service = service
        self.fields = self.service.fields

    def list(self, request, *args, **kwargs):
        _objects = self.service.filter_by(extract_get_data(request=request)) if request.GET is not None \
            else self.service.list()
        return extract_serialized_objects_response(_objects, self.serializer_class)

    def create(self, request, *args, **kwargs):
        data = request.data
        if request.content_type == 'application/json':
            data += request.files
        output = {}
        for i in data:
            if self.fields.get(i) is None:
                return Response(data={'error': f'{i} is not an attribute for the model'}, status=HTTP_400_BAD_REQUEST)
            value = data.get(i) if self.fields[i].get('type') == 'file' or self.fields[i].get('type') == 'image' \
                else request.data.get(i)
            if value is None and self.fields[i]['required']:
                return Response(data={'error': f'{i} is required'}, status=HTTP_400_BAD_REQUEST)
            output[i] = value
            if isinstance(data, Exception):
                return Response(data={'error': str(data)}, status=HTTP_400_BAD_REQUEST)
        _object = self.service.create(data)
        if isinstance(_object, Exception):
            return Response(data={"error": str(_object)}, status=HTTP_500_INTERNAL_SERVER_ERROR)
        output['id'] = _object.id
        return return_serialized_data_or_error_response(_object=output, serializer_class=self.serializer_class,
                                                        response_code=HTTP_201_CREATED)

    def retrieve(self, request, pk=None, *args, **kwargs):
        data = self.service.retreive(_id=pk)
        if data is None:
            return Response(data={'error': 'object not found'}, status=HTTP_404_NOT_FOUND)
        else:
            return return_serialized_data_or_error_response(_object=data, serializer_class=self.serializer_class,
                                                            response_code=HTTP_200_OK)

    def update(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=HTTP_400_BAD_REQUEST)
        _object = self.service.retreive(_id=pk)
        if _object is None:
            return Response(data={'error': 'object not found'}, status=HTTP_404_NOT_FOUND)
        _object = self.service.put(_id=pk, data=request.data)
        return return_serialized_data_or_error_response(_object=_object, serializer_class=self.serializer_class,
                                                        response_code=HTTP_201_CREATED)

    def delete(self, request, pk=None, *args, **kwargs):
        if pk is None:
            return Response(data={'error': 'id must not be null'}, status=HTTP_400_BAD_REQUEST)
        deleted = self.service.delete(pk)
        if isinstance(deleted, Exception):
            return Response(data={'error': str(deleted)}, status=HTTP_404_NOT_FOUND)
        return Response(status=HTTP_204_NO_CONTENT)

    @classmethod
    def get_urls(cls):
        return cls.as_view({'get': 'list', 'post': 'create'}), cls.as_view(
            {'get': 'retrieve', 'put': 'update', 'delete': 'delete'}
        )


class FormViewSet(ViewSet):
    def __init__(self, fields: dict, serializer_class, service, **kwargs):
        super().__init__(serializer_class, service, **kwargs)

    def create(self, request, *args, **kwargs):
        data = request.data
        fields = list(self.fields.keys())
        score = calculate_score(data=data, fields=fields)
        if isinstance(score, Exception):
            return Response(data={'error': str(score)}, status=HTTP_400_BAD_REQUEST)
        request.data['score'] = score
        return super().create(request=request, *args, **kwargs)
