from rest_framework import serializers
from django.urls import reverse
from opd.models import Appointment, Doctor, Address, InventoryItem, Opd
from django.contrib.auth.models import User


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password", "password2"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError({"error": "email already exist"})
        return value

    """
    running the validation of the password2.

    initial_data : this represent the data that is being passed from the input and not yet validated
    validated_data: this represent the data that is being used after the is_valid() method is called

    """

    def validate_password2(self, value):
        if value != self.initial_data["password"]:  # type: ignore
            raise serializers.ValidationError(
                {"error": "password and confirm password does not match"}
            )
        return value

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User.objects.create(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


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
            "user",
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


class OpdSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField()

    class Meta:
        model = Opd
        fields = [
            "url",
            "name",
            "days_of_operation",
            "max_patient_capacity",
            "active_patient",
            "no_of_appointment",
            "last_updated",
        ]

    def validate(self, attrs):
        if "active_patient" in attrs and "max_patient_capacity" in attrs:
            if attrs["active_patient"] > attrs["max_patient_capacity"]:
                raise serializers.ValidationError({"error": "No capacity Available"})
        return attrs

    def get_url(self, obj):
        # Generate a URL without a lookup field
        request = self.context.get("request")
        return reverse("opd:doctor")


class InventoryItemSerializer(serializers.ModelSerializer):
    total_item = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = InventoryItem
        fields = [
            "item_name",
            "item_quantity",
            "item_price",
            "last_updated",
            "total_item",
        ]

    def get_total_item(self, obj):
        return InventoryItem.objects.count()


class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = [
            "id",
            "name",
            "active",
            "date_time",
            "last_updated",
        ]
