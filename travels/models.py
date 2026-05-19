from django.db import models

from cats.models import Cat


class Destination(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    class Meta:
        unique_together = ('name', 'country')

    def __str__(self):
        return f'{self.name}, {self.country}'


class Travel(models.Model):
    STATUS_PLANNED = 'planned'
    STATUS_ONGOING = 'ongoing'
    STATUS_COMPLETED = 'completed'
    STATUS_CHOICES = (
        (STATUS_PLANNED, 'Запланировано'),
        (STATUS_ONGOING, 'В пути'),
        (STATUS_COMPLETED, 'Завершено'),
    )

    cat = models.ForeignKey(Cat, related_name='travels', on_delete=models.CASCADE)
    destination = models.ForeignKey(
        Destination, related_name='travels', on_delete=models.CASCADE
    )
    departure_date = models.DateField()
    arrival_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=STATUS_PLANNED)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f'{self.cat} → {self.destination} ({self.departure_date})'
