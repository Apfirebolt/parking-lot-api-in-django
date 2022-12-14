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
    exit_time = models.DateTimeField('Exit Time', auto_now=True)
    price = models.FloatField('Parking Price', default=0)

    def __str__(self):
        return str(self.entry_time) + ' - ' + str(self.exit_time)

    class Meta:
        verbose_name_plural = "Ticket"



