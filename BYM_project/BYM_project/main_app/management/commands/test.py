from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'test'

    def handle(self, *args, **options):
        pass
