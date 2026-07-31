from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("analyze/", views.analyze, name="analyze"),
    path("analyze_csv/", views.analyze_csv, name="analyze_csv"),
]