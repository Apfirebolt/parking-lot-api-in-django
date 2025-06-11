from django.db import models
from uuid import uuid4
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from parking.settings import AUTH_USER_MODEL

STATUS_CHOICES = (
    ("EMPTY", "Empty"),
    ("OCCUPIED", "Occupied"),
    ("IN REPAIR", "In Repair"),
)

SIZE_CHOICES = (
    ("TWO", "Two"),
    ("FOUR-SMALL", "Four-Small"),
    ("FOUR-LARGE", "Four-Large"),
)

PARKING_TYPE_CHOICES = (
    ("HOURLY", "Hourly"),
    ("DAILY", "Daily"),
    ("MONTHLY", "Monthly"),
)


class UserManager(BaseUserManager):

    def create_user(self, email, username=None, password=None, **extra_fields):
        """Creates and saves a new user"""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, username, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, username, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom user model that suppors using email instead of username"""
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name_plural = "Users"


class Area(models.Model):
    name = models.CharField('Area Name', max_length=100, null=True, blank=True)
    capacity = models.IntegerField('Capacity', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Areas"



class Parking(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parking_created')
    name = models.CharField('Parking Name', max_length=100, null=True, blank=True)
    location = models.CharField('Parking Location', max_length=255, null=True, blank=True)
    description = models.TextField('Parking Description', null=True, blank=True)
    size = models.CharField('Parking Size', max_length=150, choices=SIZE_CHOICES, default="Four-Small")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='area_parkings')

    def __str__(self):
        return self.size

    class Meta:
        verbose_name_plural = "Parking"


class ParkingSection(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='parking_section')
    floor = models.IntegerField('Floor Number', default=0)
    parking_type = models.CharField('Parking Type', max_length=50, choices=SIZE_CHOICES, default="FOUR-SMALL")
    name = models.CharField('Section Name', max_length=100, null=True, blank=True)
    capacity = models.IntegerField('Capacity', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Parking Section"


class ParkingPrice(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    type = models.CharField('Parking Type', max_length=50, choices=PARKING_TYPE_CHOICES, default="HOURLY")
    parking_section = models.ForeignKey(ParkingSection, on_delete=models.CASCADE, related_name='parking_price')
    price = models.FloatField('Parking Price', default=0)
    vehicle_size = models.CharField('Vehicle Size', max_length=50, choices=SIZE_CHOICES, default="FOUR-SMALL")
    has_charging = models.BooleanField('Has Charging', default=False)


class ParkingSlot(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    section = models.ForeignKey(ParkingSection, on_delete=models.CASCADE, related_name='parking_slot')
    slot_number = models.CharField('Slot Number', max_length=50, null=True, blank=True)
    type = models.CharField('Slot Type', max_length=50, choices=SIZE_CHOICES, default="FOUR-SMALL")
    is_charging_available = models.BooleanField('Is Charging Available', default=False)
    is_booked = models.BooleanField('Is Booked', default=False)
    is_reserved = models.BooleanField('Is Reserved', default=False)
    is_available = models.BooleanField('Is Available', default=True)

    def __str__(self):
        return self.slot_number

    class Meta:
        verbose_name_plural = "Parking Slot"


class Vehicle(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parking_user_vehicle')
    vehicle_number = models.CharField('Vehicle Number', max_length=50, unique=True)
    vehicle_type = models.CharField('Vehicle Type', max_length=50, choices=SIZE_CHOICES, default="FOUR-SMALL")
    is_electric = models.BooleanField('Is Electric', default=False)
    is_active = models.BooleanField('Is Active', default=True)

    def __str__(self):
        return self.vehicle_number

    class Meta:
        verbose_name_plural = "Vehicle"


class Passes(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parking_user_passes')
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='parking_passes')
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle_passes')
    start_date = models.DateField('Start Date', null=True, blank=True)
    end_date = models.DateField('End Date', null=True, blank=True)
    price = models.FloatField('Pass Price', default=0)

    def __str__(self):
        return str(self.start_date) + ' - ' + str(self.end_date)

    class Meta:
        verbose_name_plural = "Passes"


class Ticket(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parking_user_tickets')
    parking_slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE, related_name='parking_slot_ticket', null=True, blank=True)
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='vehicle_ticket', null=True, blank=True)
    entry_time = models.DateTimeField('Entry Time', auto_now_add=True)
    exit_time = models.DateTimeField('Exit Time', auto_now=True)
    parking_price = models.ForeignKey(ParkingPrice, on_delete=models.CASCADE, related_name='parking_price_ticket', null=True, blank=True)

    def __str__(self):
        return str(self.entry_time) + ' - ' + str(self.exit_time)

    class Meta:
        verbose_name_plural = "Ticket"



