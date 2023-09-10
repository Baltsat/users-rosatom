from django.urls import path
from .models import QAItem
from .views import QAItemAPIView

urlpatterns = [
    path('v1/courses/', QAItemAPIView.as_view({'post': 'create', 'get': 'list'}), name="all_QA_api")
]