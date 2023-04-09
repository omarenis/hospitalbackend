from django.urls import path
from common.views import FormViewSet, ViewSet
from formteacher.models import BehaviorTroubleTeacher, BehaviorTroubleTeacherSerializer, \
    HyperActivityTroubleTeacherSerializer, InattentionTroubleTeacherSerializer, FormAbrSerializer
from formteacher.services import BehaviorTroubleTeacherService, \
    HyperActivityTroubleTeacherService, InattentionTroubleTeacherService, FormAbrService


class BehaviorTroubleTeacherViewSet(FormViewSet):
    def __init__(self, serializer_class=BehaviorTroubleTeacherSerializer, service=BehaviorTroubleTeacherService(),
                 **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class HyperActivityTroubleTeacherViewSet(FormViewSet):
    def __init__(self, serializer_class=HyperActivityTroubleTeacherSerializer,
                 service=HyperActivityTroubleTeacherService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)

class InattentionTroubleTeacherViewSet(ViewSet):
    def __init__(self, serializer_class=InattentionTroubleTeacherSerializer,
                 service=InattentionTroubleTeacherService(), **kwargs):
        super().__init__(serializer_class=serializer_class, service=service, **kwargs)


class FormAbrViewSet(ViewSet):

    def __init__(self, serializer_class=FormAbrSerializer, service=FormAbrService(), **kwargs):
        super().__init__(serializer_class, service, **kwargs)


behavior_trouble_teacher_list, behavior_trouble_teacher_object = BehaviorTroubleTeacherViewSet.get_urls()

hyperactivity_trouble_teacher_list, hyperactivity_trouble_teacher_object = HyperActivityTroubleTeacherViewSet.get_urls()

inattention_trouble_teacher_list, inattention_trouble_teacher_object = InattentionTroubleTeacherViewSet.get_urls()

form_abr_teacher_list, form_abr_teacher_object = FormAbrViewSet.get_urls()

urlpatterns = [
    path('behavior_trouble_teacher_list', behavior_trouble_teacher_list),
    path('behavior_trouble_teacher_list/<int:id>', behavior_trouble_teacher_object),
    path('hyperactivity_trouble_teacher_list', hyperactivity_trouble_teacher_list),
    path('hyperactivity_trouble_teacher_list/<int:id>', hyperactivity_trouble_teacher_object),
    path('inattention_trouble_teacher_list', inattention_trouble_teacher_list),
    path('inattention_trouble_teacher_list/<int:id>', inattention_trouble_teacher_object),
    path('form_abr', form_abr_teacher_list),
    path('form_abr/<int:id>', form_abr_teacher_object)
]
