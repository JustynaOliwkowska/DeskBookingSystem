from django.db import models


class OfficeArea(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.PositiveIntegerField()


class Reservation(models.Model):
    date = models.DateField()
    area_id = models.ForeignKey(OfficeArea, on_delete=models.CASCADE)
    employee_id = models.TextField()

    class Meta:
        unique_together = ('date', 'employee_id')