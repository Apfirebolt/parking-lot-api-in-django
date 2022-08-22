from django.db import models
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


class CustomUserManager(BaseUserManager):
    def create_superuser(self, email, password):
        user = self.model(email=email)
        user.set_password(password)
        user.is_superuser = True
        user.is_active = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField("Email", unique=True, max_length=255, blank=True, null=True)
    username = models.CharField("User Name", unique=True, max_length=255, blank=True, null=True)
    is_active = models.BooleanField('Active', default=True)
    is_staff = models.BooleanField('Staff', default=False)
    is_superuser = models.BooleanField('Super User', default=False)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.username

    class Meta:
        '''Doc string for meta'''
        verbose_name_plural = "User"


class Area(models.Model):
    name = models.CharField('Area Name', max_length=100, null=True, blank=True)
    capacity = models.IntegerField('Capacity', default=0)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Areas"



class Parking(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parking_created')
    size = models.CharField('Parking Size', max_length=150, choices=SIZE_CHOICES, default="Four-Small")
    status = models.CharField('Status', max_length=150, choices=STATUS_CHOICES, default="Empty")
    area = models.ForeignKey(Area, on_delete=models.CASCADE, related_name='area_parkings')

    def __str__(self):
        return self.size

    class Meta:
        verbose_name_plural = "Parking"


class Ticket(models.Model):
    user = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='parking_user_tickets')
    parking = models.ForeignKey(Parking, on_delete=models.CASCADE, related_name='parking_ticket')
    entry_time = models.DateTimeField('Entry Time', auto_now_add=True)
    exit_time = models.DateTimeField('Exit Time')
    price = models.FloatField('Parking Price', default=0)

    def __str__(self):
        return str(self.entry_time) + ' - ' + str(self.exit_time)

    class Meta:
        verbose_name_plural = "Ticket"



