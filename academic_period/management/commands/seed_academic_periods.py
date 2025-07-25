import json
from django.core.management.base import BaseCommand
from academic_period.models import AcademicPeriod

class Command(BaseCommand):
    help = 'Seed Academic Periods model from a JSON file'

    def handle(self, *args, **kwargs):
        with open('academic_period/data/academic_period_data.json', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            AcademicPeriod.objects.create(
                first_year = item['first_year'],
                final_year = item['final_year'],
                is_active  = item['is_active']
            )

        self.stdout.write(self.style.SUCCESS('Periodos Académicos creados desde JSON'))