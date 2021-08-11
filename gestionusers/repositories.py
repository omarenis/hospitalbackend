from common.repositories import Repository
from .models import Person, Localisation


class UserRepository(Repository):
    def __init__(self, model=Person):
        super().__init__(model)

    def put(self, _id: int, data: dict):
        _object = self.model.objects.get(id=_id)
        if _object is None:
            return Exception('object not found')
        else:
            for i in data:
                if hasattr(_object, i) and getattr(_object, i) != data[i]:
                    setattr(_object, i, data[i])
            if data.get('password'):
                _object.set_password(data.get('password'))
            _object.save()
        return _object


class LocalisationRepository(Repository):
    def __init__(self, model=Localisation):
        super().__init__(model)
