from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Area


class Command(BaseCommand):
    help = 'Clear User data from the database'

    def handle(self, *args, **kwargs):

        areas = Area.objects.all()
        
        for one_area in areas:
            try:
                print(f'Deleting area {one_area.name}')
                one_area.delete()
            except Exception as err:
                print('Could not delete ', err)