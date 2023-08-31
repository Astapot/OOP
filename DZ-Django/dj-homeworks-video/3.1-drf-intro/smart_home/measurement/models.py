from django.db import models

# TODO: опишите модели датчика (Sensor) и измерения (Measurement)


class Sensor(models.Model):
    # id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100, null=False)
    description = models.TextField()

    def __str__(self):
        return self.name


class Measurement(models.Model):
    sensor_id = models.ForeignKey(Sensor, to_field='id', on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=5, decimal_places=1)
    date_and_time = models.DateTimeField(auto_now_add=True)
