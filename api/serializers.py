from rest_framework import serializers
from . models import CustomUser, Parking, Area, Ticket


class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'is_staff', 'password')
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        user = super(CustomUserSerializer, self).create(validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class AreaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Area
        fields = '__all__'



class ParkingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parking
        fields = '__all__'
        read_only_fields = ['user', 'area']


class TicketSerializer(serializers.ModelSerializer):

    parking_charge = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['user']

    def get_parking_charge(self, obj):
        hours = (obj.exit_time - obj.entry_time).seconds / 3600
        return "{:.2f}".format(hours * obj.price)
