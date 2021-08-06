from common.repositories import Repository
from .models import Person, Localisation


class UserRepository(Repository):
    def __init__(self, model=Person):
        super().__init__(model)


class LocalisationRepository(Repository):
    def __init__(self, model=Localisation):
        super().__init__(model)
