# your_app/management/commands/load_departments.py
from django.core.management.base import BaseCommand
import requests
from fpt.orders.models import Department, Country


class Command(BaseCommand):
    help = "Carga los departamentos de Colombia desde una API gratuita"

    def handle(self, *args, **kwargs):
        url = "https://api-colombia.com/api/v1/Department"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            country = Country.objects.get(name="Colombia")
            for dept in data:
                Department.objects.update_or_create(
                    country=country,
                    name=dept["name"],
                    defaults={"code": str(dept["id"])},
                )
            self.stdout.write(
                self.style.SUCCESS("Departamentos cargados exitosamente.")
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f"Error al obtener los departamentos: {response.status_code}"
                )
            )
