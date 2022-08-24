from django.core.management.base import BaseCommand
from django.utils import timezone
from api.models import Ticket


class Command(BaseCommand):
    help = 'Clear Ticket data from the database'

    def handle(self, *args, **kwargs):

        tickets = Ticket.objects.all()
        
        for one_ticket in tickets:
            try:
                print(f'Deleting ticket {one_ticket.entry_time}')
                one_ticket.delete()
            except Exception as err:
                print('Could not delete ', err)