from rest_framework import serializers
from .models import (
    CustomUser,
    Parking,
    Ticket,
    ParkingPrice,
    ParkingSection,
    ParkingSlot,
    Vehicle,
    Passes,
)


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ("username", "email", "is_staff", "password")
        extra_kwargs = {"password": {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user


class ParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parking
        fields = "__all__"
        read_only_fields = ["user",]


class TicketSerializer(serializers.ModelSerializer):

    class Meta:
        model = Ticket
        fields = "__all__"
        read_only_fields = ["user"]
        

class VehicleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Vehicle
        fields = "__all__"
        read_only_fields = ["user"]


class ParkingPriceSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingPrice
        fields = "__all__"

    def validate(self, data):
        if data["price"] < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return data


class ParkingSectionSerializer(serializers.ModelSerializer):

    class Meta:
        model = ParkingSection
        fields = "__all__"


class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = "__all__"

    def validate(self, data):
        if data["slot_number"] == "":
            raise serializers.ValidationError("Slot number cannot be empty.")
        return data


class PassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passes
        fields = "__all__"
        read_only_fields = ["user",]

    def validate(self, data):
        if data["start_date"] >= data["end_date"]:
            raise serializers.ValidationError("Start date must be before end date.")
        if data["price"] < 0:
            raise serializers.ValidationError("Price cannot be negative.")
        return data
