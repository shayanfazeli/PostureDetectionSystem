from django.urls import path, include, re_path
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('histogram', views.HistogramViewSet)

urlpatterns = [
	path('', include(router.urls)),
	re_path(r'^upload', views.FileUploadView.as_view()),
	re_path(r'^notify/(?P<id>.+)', views.NotifyView.as_view()),
	re_path(r'^sensor', views.SensorDataUploadView.as_view()),
]