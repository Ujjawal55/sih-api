from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.db import transaction, models
from django.contrib.auth.models import Group, User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import status
from rest_framework.serializers import ValidationError

from opd.models import Address, Appointment, Doctor, Inventory, Opd, Patient


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


@receiver(post_save, sender=Doctor)
def create_opd_inventory(sender, created, instance, **kwargs):
    if created:
        Inventory.objects.create(doctor=instance)


@receiver(pre_delete, sender=User)
def delete_related_object(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            try:
                doctor = instance.doctor
                if doctor.address:
                    doctor.address.delete()
                doctor.delete()

            except AttributeError:
                print("Doctor does not exist")

    except Exception as e:
        print(f"Some error occurs {e}")


@receiver(post_save, sender=Appointment)
def opd_appointment_increment(sender, created, instance, **kwargs):
    if created:
        try:
            with transaction.atomic():
                try:
                    doctor = instance.doctor
                    opd = Opd.objects.get(doctor_profile=doctor)
                    opd.no_of_appointment = models.F("no_of_appointment") + 1
                    opd.save()

                except Doctor.DoesNotExist:
                    raise ValidationError("Doctor does not exist")

        except Exception as e:
            print(f"some error occurs {e}")


@receiver(post_delete, sender=Appointment)
def opd_appointment_decrement(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            try:
                doctor = instance.doctor
                opd = Opd.objects.get(doctor_profile=doctor)
                opd.no_of_appointment = models.F("no_of_appointment") - 1
                opd.save()

            except Doctor.DoesNotExist:
                raise ValidationError("Doctor does not exist")

    except Exception as e:
        print(f"some error occurs {e}")


@receiver(post_save, sender=Patient)
def opd_active_patient_increment(sender, created, instance, **kwargs):
    if created:
        try:
            with transaction.atomic():
                try:
                    doctor = instance.doctor
                    opd = Opd.objects.get(doctor_profile=doctor)
                    opd.active_patient = models.F("active_patient") + 1
                    opd.save()

                except Doctor.DoesNotExist:
                    raise ValidationError("Doctor does not exist")

        except Exception as e:
            print(f"some error occurs {e}")


@receiver(post_delete, sender=Patient)
def opd_active_patient_decrement(sender, instance, **kwargs):
    try:
        with transaction.atomic():
            try:
                doctor = instance.doctor
                opd = Opd.objects.get(doctor_profile=doctor)
                opd.active_patient = models.F("active_patient") - 1
                opd.save()

            except Doctor.DoesNotExist:
                raise ValidationError("Doctor does not exist")

    except Exception as e:
        print(f"some error occurs {e}")
