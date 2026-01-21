from django.urls import path
from .views import ResearchAPIView

urlpatterns = [
    path("", ResearchAPIView.as_view(), name="research"),
]
