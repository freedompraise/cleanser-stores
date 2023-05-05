# images/management/commands/createsu.py

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from decouple import config
import os

class Command(BaseCommand):
    help = 'Creates a superuser.'

    def handle(self, *args, **options):
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser(
                username = os.getenv('username'),
                password= os.getenv('password'),
            )
        print('Superuser has been created.')