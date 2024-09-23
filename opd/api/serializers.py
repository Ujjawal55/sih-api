from rest_framework import serializers
from opd.models import Doctor, Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        exclude = [
            "created_at",
        ]


class DoctorSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
        view_name="opd:doctor-detail",  # NOTE: don't forget about the name-space
        lookup_field="pk",
    )

    class Meta:
        model = Doctor
        fields = [
            "url",
            "name",
            "speciality",
            "experience",
        ]


class DoctorDetailSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Doctor
        exclude = [
            "created_at",
        ]

    def update(self, instance, validated_data):
        # handle the address serialization seprately
        doctor_address = validated_data.pop("address", None)
        if doctor_address:
            address_serializer = AddressSerializer(
                instance.address, data=doctor_address
            )
            if address_serializer.is_valid():
                address_serializer.save()

        profile_image = validated_data.pop("profile_image", None)

        if profile_image is not None:
            instance.profile_image = profile_image

        # update the other attribute
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
