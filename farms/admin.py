from django.contrib import admin

from .models import Farm


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = (
        "farm_name",
        "farmer",
        "municipality",
        "barangay",
        "farm_type",
        "area",
        "latitude",
        "longitude",
    )

    list_filter = (
        "municipality",
        "farm_type",
    )

    search_fields = (
        "farm_name",
        "farmer__first_name",
        "farmer__last_name",
        "barangay",
    )