import csv
from django.core.management.base import BaseCommand
from crops.models import Crop

class Command(BaseCommand):
    help = 'Load crops data from CSV'

    def handle(self, *args, **kwargs):
        # Change this path if your CSV file is located elsewhere
        csv_file_path = 'crops/crop_data.csv'  
        
        with open(csv_file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                Crop.objects.create(
                    N=float(row['N']),
                    P=float(row['P']),
                    K=float(row['K']),
                    temperature=float(row['Temperature']),
                    humidity=float(row['Humidity']),
                    pH=float(row['pH']),
                    rainfall=float(row['Rainfall']),
                    crop_name=row['Crop']
                )
        self.stdout.write(self.style.SUCCESS('Data loaded successfully!'))
