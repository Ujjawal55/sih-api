from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views


app_name = "opd"

# urlpatterns = [
#     path("doctors/", views.DoctorList.as_view(), name="doctor-list"),
#     path("doctors/<int:pk>/", views.DoctorDetail.as_view(), name="doctor-detail"),
# ]
#
# NOTE: do not add the trailing ('/') at the end of the router defination
router = DefaultRouter()
router.register(
    "doctor/inventory-item",
    views.InventoryItemViewSet,
    basename="inventory-item",
)

router.register(
    "doctor/appointment",
    views.AppointmentViewSet,
    basename="appointment",
)

router.register(
    "doctor/patient",
    views.PatientViewSet,
    basename="patient",
)

urlpatterns = [
    path("login/", views.doctor_login, name="login"),
    path("logout/", views.doctor_logout, name="logout"),
    path("register/", views.doctor_registration, name="register"),
    path("doctor/", views.DoctorDetail.as_view(), name="doctor"),
    path("doctor/opd/", views.OpdDetail.as_view(), name="opd"),
]


urlpatterns += router.urls
