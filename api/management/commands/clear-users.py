from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import CustomUser


class Command(BaseCommand):
    help = 'Clear User data from the database'

    def handle(self, *args, **kwargs):

        users = CustomUser.objects.all()
        
        for one_user in users:
            try:
                print(f'Deleting user {one_user.email}')
                one_user.delete()
            except Exception as err:
                print('Could not delete ', err)