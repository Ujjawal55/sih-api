from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.


class Address(models.Model):
    house_number = models.CharField(
        "House-Number", max_length=10, null=True, blank=True
    )
    street_name = models.CharField("Street-Name", max_length=200)
    city = models.CharField("City-Name", max_length=200)
    state = models.CharField("State-Name", max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        address = f"Address is {self.house_number}, {self.street_name}, {self.city}, {self.state}"
        if hasattr(self, "doctor") and self.doctor:  # type: ignore
            return f"Address  | {self.doctor.name}"  # type: ignore
        return address


class Doctor(models.Model):
    name = models.CharField("Full Name", max_length=200)
    profile_image = models.ImageField(
        "Image",
        upload_to="profile/",
        default="profile/default-profile.png",
    )
    speciality = models.CharField("Speciality", max_length=200)
    phone_number = PhoneNumberField("Phone Number", region="IN")
    experience = models.PositiveIntegerField("Year of Experience", default=0)
    about = models.TextField(blank=True)
    education = models.TextField()
    address = models.OneToOneField(
        Address, on_delete=models.CASCADE, related_name="doctor"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Dr. " + self.name
