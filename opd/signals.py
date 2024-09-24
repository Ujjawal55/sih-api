from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token

from opd.models import Address, Doctor, Inventory, Opd


@receiver(post_save, sender=User)
def create_token_and_add_group(sender, created, instance, **kwargs):
    if created:
        Token.objects.create(user=instance)
        group = Group.objects.get(name="Doctor")
        instance.groups.add(group)


@receiver(post_save, sender=User)
def create_doctor_object(sender, created, instance, **kwargs):
    if created:
        address = Address.objects.create(
            house_number="Not Specified",
            street_name="Not Specified",
            city="Not Specified",
            state="Not Specified",
            pincode="Not Specified",
        )
        Doctor.objects.create(
            user=instance,
            name="Not Specified",
            speciality="Not Specified",
            phone_number="000-000-0000",
            about="Not Specified",
            education="Not Specified",
            address=address,
        )


@receiver(post_save, sender=Doctor)
def create_opd_object(sender, created, instance, **kwargs):
    if created:
        Opd.objects.create(
            doctor_profile=instance,
            name="Not Specified",
            days_of_operation="Not Specified",
        )


@receiver(post_save, sender=Opd)
def create_opd_inventory(sender, created, instance, **kwargs):
    if created:
        Inventory.objects.create(opd=instance)
