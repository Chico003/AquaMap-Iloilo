from django.db import models

from farmers.models import Farmer, Municipality


class Farm(models.Model):

    FARM_TYPE_CHOICES = [
        ("FISHPOND", "Fishpond"),
        ("FISH_CAGE", "Fish Cage"),
        ("FISH_PEN", "Fish Pen"),
        ("OTHER", "Other"),
    ]

    farmer = models.ForeignKey(
        Farmer,
        on_delete=models.CASCADE,
        related_name="farms"
    )

    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        related_name="farms"
    )

    barangay = models.CharField(
        max_length=100
    )

    farm_name = models.CharField(
        max_length=150
    )

    farm_type = models.CharField(
        max_length=20,
        choices=FARM_TYPE_CHOICES
    )

    area = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Farm area in hectares"
    )

    latitude = models.DecimalField(
        max_digits=10,
        decimal_places=7
    )

    longitude = models.DecimalField(
        max_digits=10,
        decimal_places=7
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["municipality", "barangay", "farm_name"]

    def __str__(self):
        return self.farm_name