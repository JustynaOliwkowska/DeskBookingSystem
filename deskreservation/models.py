from django.db import models

class OfficeArea(models.Model):
    name = models.CharField(max_length=64)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return self.name

class Reservation(models.Model):
    date = models.DateField()
    area_id = models.ForeignKey(OfficeArea, on_delete=models.CASCADE)
    employee_id = models.TextField()

    class Meta:
        unique_together = ('date', 'employee_id')

    def __str__(self):
        return self.employee_id

class OfficeAreaNotice(models.Model):
    to_area = models.ForeignKey(OfficeArea, on_delete=models.CASCADE)
    content = models.TextField()

class ReservationNotice(models.Model):
    to_reservation = models.ForeignKey(Reservation, on_delete=models.CASCADE)
    content = models.TextField()