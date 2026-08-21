from django.db import models

class Park(models.Model):
    name = models.CharField(max_length=200)
    region = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Trail(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard'),
        ('expert', 'Expert'),
    ]

    name = models.CharField(max_length=200)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2)
    elevation_gain = models.IntegerField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    is_open = models.BooleanField(default=True)
    added = models.DateTimeField(auto_now_add=True)
    park = models.ForeignKey(
        Park,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name