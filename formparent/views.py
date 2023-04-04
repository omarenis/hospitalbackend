from django.urls import path

from common.models import text_field
from common.views import ViewSet
from formparent.models import AnxityTroubleParentSerializer, ExtraTroubleParentSerializer, \
    HyperActivityTroubleParentSerializer, ImpulsivityTroubleParentSerializer, \
    LearningTroubleParentSerializer, SomatisationTroubleParentSerializer
from formparent.services import AnxityTroubleParentService, ExtraTroubleParentService, \
    HyperActivityTroubleParentService, ImpulsivityTroubleParentService, \
    LearningTroubleParentService, SomatisationTroubleParentService


class AnxityTroubleParentViewSet(ViewSet):
    def __init__(self, serializer_class=AnxityTroubleParentSerializer,
                 service=AnxityTroubleParentService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class ImpulsivityTroubleParentViewSet(ViewSet):
    def __init__(self, serializer_class=ImpulsivityTroubleParentSerializer,
                 service=ImpulsivityTroubleParentService, **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class LearningTroubleParentViewSet(ViewSet):
    def __init__(self, serializer_class=LearningTroubleParentSerializer,
                 service=LearningTroubleParentService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class SomatisationTroubleParentViewSet(ViewSet):
    def __init__(self, serializer_class=SomatisationTroubleParentSerializer,
                 service=SomatisationTroubleParentService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class HyperActivityTroubleParentViewSet(ViewSet):
    def __init__(self, serializer_class=HyperActivityTroubleParentSerializer,
                 service=HyperActivityTroubleParentService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class ExtraTroubleParentViewSet(ViewSet):
    def __init__(self, serializer_class=ExtraTroubleParentSerializer, service=ExtraTroubleParentService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


anxity_trouble_parent_list, anxity_trouble_parent_object = AnxityTroubleParentViewSet.get_urls()
impulsivity_trouble_parent_list, impulsivity_trouble_parent_object = ImpulsivityTroubleParentViewSet.get_urls()
learning_trouble_parent_list, learning_trouble_parent_object = LearningTroubleParentViewSet.get_urls()

urlpatterns = [
    path('anxity_trouble_parent_list', anxity_trouble_parent_list),
    path('anxity_trouble_parent_list/<int:id>', anxity_trouble_parent_object),
    path('impulsivity_trouble_parent_list', impulsivity_trouble_parent_list),
    path('impulsivity_trouble_parent_list/<int:id>', impulsivity_trouble_parent_object),
    path('learning_trouble_parent_list', learning_trouble_parent_list),
    path('learning_trouble_parent_list/<int:id>', learning_trouble_parent_object)
]
