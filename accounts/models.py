from django.conf import settings
from django.db import models

from farmers.models import Municipality


class UserProfile(models.Model):

    ROLE_CHOICES = [
        ("MUNICIPAL", "Municipal Agriculture Office"),
        ("BFAR", "BFAR Region VI"),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="MUNICIPAL",
    )

    municipality = models.ForeignKey(
        Municipality,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="user_profiles",
    )

    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"