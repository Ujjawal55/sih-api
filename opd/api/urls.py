from django.urls import path
from . import views

app_name = "opd"

urlpatterns = [
    path("doctors/", views.doctor_list, name="doctor-list"),
]
