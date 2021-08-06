from .repositories import Repository


class Service(object):

    def __init__(self, repository: Repository):
        self.repository = repository

    def list(self):
        return self.repository.list()

    def retreive(self, _id: int):
        return self.repository.retreive(_id=_id)

    def create(self, data: dict):
        return self.repository.create(data)

    def put(self, _id: int, data: dict):
        return self.repository.put(_id=_id, data=data)

    def delete(self, _id: int):
        return self.repository.delete(_id)

    def filter_by(self, data: dict):
        return self.repository.filter_by(data=data)


class FormService(Service):
    def __init__(self, repository: Repository):
        super().__init__(repository)

    def create(self, data: dict):
        try:
            data['score'] = calculate_score(data=data, fields=list(data.keys()))
            return super().create(data=data)
        except Exception as exception:
            return exception


def calculate_score(data, fields):
    value = 0
    print(data)
    for i in fields:
        if not data.get(i):
            raise AttributeError(f'{i} is not an attribte for the instance')
        elif data.get(i) == 'sometimes':
            value += 1
        elif data.get(i) == 'usual':
            value += 2
        elif data.get(i) == 'always':
            value += 3
    return value
