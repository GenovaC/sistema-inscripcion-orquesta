import json
from django.core.management.base import BaseCommand
from orchestral_projects.models import OrchestralProject

class Command(BaseCommand):
    help = 'Seed Orchestral Projects model from a JSON file'

    def handle(self, *args, **kwargs):
        with open('orchestral_projects/data/project_data.json', encoding='utf-8') as f:
            data = json.load(f)

        for item in data:
            OrchestralProject.objects.create(
                name = item['name'],
                code = item['code']
            )

        self.stdout.write(self.style.SUCCESS('Proyectos Orquestales creados desde JSON'))