import json
from django.core.management.base import BaseCommand
from instruments.models import Instrument

class Command(BaseCommand):
    help = 'Seed Instrument model from a JSON file'

    def handle(self, *args, **kwargs):
        with open('instruments/data/instrument_data.json', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            Instrument.objects.create(
                name     = item['name'],
                category = item['category']
            )

        self.stdout.write(self.style.SUCCESS('Instrumentos creados desde JSON'))