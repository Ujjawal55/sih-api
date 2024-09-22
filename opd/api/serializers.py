from rest_framework import serializers
from opd.models import Doctor, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        exclude = [
            "doctor",
        ]


class DoctorSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Doctor
        fields = [
            "name",
            "profile_image",
            "speciality",
            "phone_number",
            "address",
            "experience",
            "about",
            "education",
        ]
