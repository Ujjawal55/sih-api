from django.urls import path
from . import views

app_name = "opd"

urlpatterns = [
    path("doctors/", views.doctor_list, name="doctor-list"),
    path("doctors/<int:pk>/", views.DoctorDetail.as_view(), name="doctor-detail"),
]
