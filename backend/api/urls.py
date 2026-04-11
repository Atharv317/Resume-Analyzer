from django.urls import path
from .views import test_api,upload_resume

urlpatterns = [
    path('test/',test_api,name="Testing"),
    path('upload/',upload_resume,name="upload_resume")
]