from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
# Create your models here.


class Address(models.Model):
    house_number = models.CharField(
        "House Number", max_length=60, null=True, blank=True
    )
    street_name = models.CharField("Street Name", max_length=200)
    city = models.CharField("City Name", max_length=200)
    state = models.CharField("State Name", max_length=200)
    pincode = models.CharField("PinCode", max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        address = f"Address is {self.house_number}, {self.street_name}, {self.city}, {self.state}"
        if hasattr(self, "doctor") and self.doctor:  # type: ignore
            return f"Address  | {self.doctor.name}"  # type: ignore
        return address


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="doctor")
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
        Address, on_delete=models.SET_NULL, null=True, related_name="doctor"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Dr. " + self.name


class Opd(models.Model):
    doctor_profile = models.OneToOneField(
        Doctor, on_delete=models.CASCADE, related_name="opd"
    )
    name = models.CharField("Name of OPD", max_length=255)
    days_of_operation = models.CharField("Days of Operation", max_length=100)
    max_patient_capacity = models.PositiveIntegerField(
        "Maximum Patient Capacity", default=0
    )
    active_patient = models.PositiveIntegerField("No. of Active_Patient", default=0)
    no_of_appointment = models.PositiveIntegerField("No. of Appointment", default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.name != "Not Specified":
            return self.name + " | " + self.doctor_profile.name
        return self.doctor_profile.name + "'s | OPD"

    """
    we can run the custom validation inside the clean() method and this validation
    is run everytime the instance is saved..

    clean() : global validation 
    clean_<field-name> : valdation on that field only
    NOTE: by default the django does not run the single attribute validtion.
    we have to explicitly call the methon in the clean field

    super().clean()
    This line calls the clean() method of the parent class (models.Model). 
    It's important to call the parent class’s clean() method to ensure that 
    any built-in validations defined by Django or the parent class are not 
    bypassed.
    """

    def clean_active_patient(self):
        if self.active_patient > self.max_patient_capacity:
            raise ValidationError("No beds are available")

    def clean(self):
        super().clean()
        self.clean_active_patient()


class Inventory(models.Model):
    doctor = models.OneToOneField(
        Doctor, on_delete=models.CASCADE, related_name="inventory"
    )

    def __str__(self):
        if hasattr(self, "opd"):
            return "Inventory of Dr." + self.doctor.name
        return "Inventory"


class InventoryItem(models.Model):
    inventory = models.ForeignKey(
        Inventory, on_delete=models.CASCADE, related_name="inventory_items"
    )
    item_name = models.CharField("Name of Item", max_length=255)
    item_quantity = models.PositiveIntegerField("Quantity of Item", default=0)
    # TODO: add the decimal points
    item_price = models.FloatField("Price of Item", default=0)
    last_updated = models.DateTimeField(auto_now=True)
    created_id = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "Inventory of " + self.inventory.doctor.name + " | " + self.item_name

    def clean_item_price(self):
        if self.item_price < 0:
            raise ValidationError("Item price cannot be negative")


class Appointment(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="appointments"
    )
    name = models.CharField("Name of Patient", max_length=256)
    date_time = models.DateTimeField("Date of appointment", auto_now_add=True)
    active = models.BooleanField(default=False)
    last_updated = models.DateTimeField("Last Updated", auto_now=True)

    def __str__(self):
        return "Appointment | " + self.name + " | " + self.doctor.name


class MedicalData(models.Model):
    BLOOD_TYPE = [
        ("A+", "A+"),
        ("A-", "A-"),
        ("B+", "B+"),
        ("B-", "B-"),
        ("AB+", "AB+"),
        ("AB-", "AB-"),
        ("O+", "O+"),
        ("O-", "O-"),
    ]
    blood_group = models.CharField("Blood Type", max_length=6, choices=BLOOD_TYPE)
    height = models.CharField("Height", max_length=10)
    weight = models.CharField("Weight", max_length=10)
    medical_history = models.TextField("Medical History")

    def __str__(self):
        if hasattr(self, "patient") and self.patient:  # type: ignore
            return "Medical-Data | " + self.patient.first_name  # type: ignore

        return "Medical-Date"


class Patient(models.Model):
    GENDER_CHOICES = [
        ("male", "male"),
        ("female", "female"),
        ("other", "other"),
    ]
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name="patients"
    )
    medical_data = models.OneToOneField(
        MedicalData, on_delete=models.SET_NULL, null=True, related_name="patient"
    )

    address = models.OneToOneField(
        Address, on_delete=models.SET_NULL, null=True, related_name="patient"
    )

    first_name = models.CharField("First Name", max_length=100)
    last_name = models.CharField("Last Name", max_length=100)
    date_of_birth = models.DateField("Date of Birth")
    gender = models.CharField("Gender", max_length=6, choices=GENDER_CHOICES)
    contact = PhoneNumberField("Contact", region="IN")
    email = models.EmailField("Email")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.first_name + " | " + self.doctor.name
