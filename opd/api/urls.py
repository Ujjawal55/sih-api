from django.urls import path
from . import views


app_name = "opd"

urlpatterns = [
    path("", views.home_page, name="home-page"),
]
