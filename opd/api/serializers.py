from rest_framework import serializers
from opd.models import Doctor


class DoctorSerializer(serializers.ModelSerializer):
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
