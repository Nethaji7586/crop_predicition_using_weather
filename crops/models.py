from django.db import models

class Crop(models.Model):
    N = models.FloatField(verbose_name='Nitrogen (N)')  # Improved field name for clarity
    P = models.FloatField(verbose_name='Phosphorus (P)')  # Improved field name for clarity
    K = models.FloatField(verbose_name='Potassium (K)')  # Improved field name for clarity
    temperature = models.FloatField(verbose_name='Temperature (°C)')  # Improved field name for clarity
    humidity = models.FloatField(verbose_name='Humidity (%)')  # Improved field name for clarity
    pH = models.FloatField(verbose_name='pH Level')  # Improved field name for clarity
    rainfall = models.FloatField(verbose_name='Rainfall (mm)')  # Improved field name for clarity
    crop_name = models.CharField(max_length=100, verbose_name='Crop Name')  # Improved field name for clarity

    def __str__(self):
        return self.crop_name
