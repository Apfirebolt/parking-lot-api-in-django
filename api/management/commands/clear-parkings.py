from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Parking


class Command(BaseCommand):
    help = 'Clear Parking data from the database'

    def handle(self, *args, **kwargs):

        parkings = Parking.objects.all()
        
        for one_parking in parkings:
            try:
                print(f'Deleting parking {one_parking.size}')
                one_parking.delete()
            except Exception as err:
                print('Could not delete ', err)