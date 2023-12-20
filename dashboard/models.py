from django.db import models

class TemperatureData(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    temperature = models.FloatField()

    def __str__(self):
        return f'TemperatureData {self.id}'

class ProductionData(models.Model):
    id = models.AutoField(primary_key=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    production = models.FloatField()

    def __str__(self):
        return f'ProductionData {self.id}'
