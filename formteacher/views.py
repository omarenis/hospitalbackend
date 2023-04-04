from django.urls import path
from common.views import FormViewSet, ViewSet
from formteacher.models import BehaviorTroubleTeacherSerializer, ExtraTroubleTeacherSerializer, \
    HyperActivityTroubleTeacherSerializer, ImpulsivityTroubleTeacherSerializer, InattentionTroubleTeacherSerializer
from formteacher.services import BehaviorTroubleTeacherService, ExtraTroubleTeacherService, \
    HyperActivityTroubleTeacherService, ImpulsivityTroubleTeacherService, InattentionTroubleTeacherService


class BehaviorTroubleTeacherViewSet(FormViewSet):
    def __init__(self, serializer_class=BehaviorTroubleTeacherSerializer, service=BehaviorTroubleTeacherService(),
                 **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class HyperActivityTroubleTeacherViewSet(FormViewSet):
    def __init__(self, serializer_class=HyperActivityTroubleTeacherSerializer,
                 service=HyperActivityTroubleTeacherService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class ImpulsivityTroubleTeacherViewSet(FormViewSet):
    def __init__(self, serializer_class=ImpulsivityTroubleTeacherSerializer,
                 service=ImpulsivityTroubleTeacherService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class ExtraTroubleTeacherViewSet(FormViewSet):
    def __init__(self, serializer_class=ExtraTroubleTeacherSerializer, service=ExtraTroubleTeacherService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class InattentionTroubleTeacherViewSet(ViewSet):
    def __init__(self, serializer_class=InattentionTroubleTeacherSerializer,
                 service=InattentionTroubleTeacherService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


behavior_trouble_teacher_list, behavior_trouble_teacher_object = BehaviorTroubleTeacherViewSet.get_urls()

impulsivity_trouble_teacher_list, impulsivity_trouble_teacher_object = ImpulsivityTroubleTeacherViewSet.get_urls()

hyperactivity_trouble_teacher_list, hyperactivity_trouble_teacher_object = HyperActivityTroubleTeacherViewSet.get_urls()

extra_trouble_teacher_list, extra_trouble_teacher_object = ExtraTroubleTeacherViewSet.get_urls()

inattention_trouble_teacher_list, inattention_trouble_teacher_object = InattentionTroubleTeacherViewSet.get_urls()

urlpatterns = [
    path('behavior_trouble_teacher_list', behavior_trouble_teacher_list),
    path('behavior_trouble_teacher_list/<int:id>', behavior_trouble_teacher_object),
    path('impulsivity_trouble_teacher_list', impulsivity_trouble_teacher_list),
    path('impulsivity_trouble_teacher_list/<int:id>', impulsivity_trouble_teacher_list),
    path('hyperactivity_trouble_teacher_list', hyperactivity_trouble_teacher_list),
    path('hyperactivity_trouble_teacher_list/<int:id>', hyperactivity_trouble_teacher_object),
    path('extra_trouble_teacher_list', extra_trouble_teacher_list),
    path('extra_trouble_teacher_list/<int:id>', extra_trouble_teacher_object),
    path('inattention_trouble_teacher_list', inattention_trouble_teacher_list),
    path('inattention_trouble_teacher_list/<int:id>', inattention_trouble_teacher_object),
]
