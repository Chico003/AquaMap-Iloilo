from django.db import models


class Municipality(models.Model):
    name = models.CharField(max_length=100, unique=True)
    province = models.CharField(max_length=100, default="Iloilo")
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Farmer(models.Model):
    SEX_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        related_name="farmers"
    )

    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(
        max_length=100,
        blank=True
    )
    last_name = models.CharField(max_length=100)

    sex = models.CharField(
        max_length=1,
        choices=SEX_CHOICES
    )

    contact_number = models.CharField(
        max_length=20,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.last_name}, {self.first_name}"