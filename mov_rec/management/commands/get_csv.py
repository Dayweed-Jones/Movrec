from django.core.management.base import BaseCommand
from homepage.models import Movies 
import csv


class Command(BaseCommand):
    help = 'Export MyModel data to a CSV file'

    def handle(self, *args, **kwargs):
        # Define the file path
        csv_file_path = 'output.csv'

        # Query all data from the model
        data = Movies.objects.all()

        # Get the model fields
        field_names = [field.name for field in Movies._meta.fields]

        # Write data to CSV file
        with open(csv_file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            # Write column headers
            writer.writerow(field_names)
            # Write data rows
            for obj in data:
                writer.writerow([getattr(obj, field) for field in field_names])

        self.stdout.write(self.style.SUCCESS(f'Data from MyModel has been written to {csv_file_path}'))