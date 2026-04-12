from django.urls import path
from .views import test_api,upload_resume,analyze_resume

urlpatterns = [
    path('test/',test_api,name="Testing"),
    path('upload/',upload_resume,name="upload_resume"),
    path('analyze/',analyze_resume,name='analyze_resume')
]