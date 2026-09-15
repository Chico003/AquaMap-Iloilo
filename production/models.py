from django.db import models
from farms.models import Farm


class ProductionRecord(models.Model):

    farm = models.ForeignKey(
        Farm,
        on_delete=models.PROTECT,
        related_name="production_records"
    )

    species = models.CharField(
        max_length=100
    )

    quantity = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    UNIT_CHOICES = [
        ("KG", "Kilograms"),
        ("TON", "Metric Tons"),
    ]

    unit = models.CharField(
        max_length=10,
        choices=UNIT_CHOICES,
        default="KG"
    )

    production_date = models.DateField()

    remarks = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-production_date"]

    def __str__(self):
        return f"{self.farm} - {self.production_date}"