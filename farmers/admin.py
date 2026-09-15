from django.contrib import admin

from .models import Municipality, Farmer


@admin.register(Municipality)
class MunicipalityAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "province",
        "is_active",
    )

    list_filter = (
        "province",
        "is_active",
    )

    search_fields = (
        "name",
    )


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = (
        "last_name",
        "first_name",
        "municipality",
        "sex",
        "contact_number",
    )

    list_filter = (
        "municipality",
        "sex",
    )

    search_fields = (
        "first_name",
        "last_name",
        "contact_number",
    )