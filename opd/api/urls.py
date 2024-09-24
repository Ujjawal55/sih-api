from django.urls import path
from . import views

app_name = "opd"

# urlpatterns = [
#     path("doctors/", views.DoctorList.as_view(), name="doctor-list"),
#     path("doctors/<int:pk>/", views.DoctorDetail.as_view(), name="doctor-detail"),
# ]
#


urlpatterns = [
    path("login/", views.doctor_login, name="login"),
    path("logout/", views.doctor_logout, name="logout"),
    path("register/", views.doctor_registration, name="register"),
    path("doctor/", views.DoctorDetail.as_view(), name="doctor"),
]
