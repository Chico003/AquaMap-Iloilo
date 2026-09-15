from django.contrib import admin

from .models import ProductionRecord


@admin.register(ProductionRecord)
class ProductionRecordAdmin(admin.ModelAdmin):
    list_display = (
        "farm",
        "species",
        "quantity",
        "unit",
        "production_date",
    )

    list_filter = (
        "species",
        "unit",
        "production_date",
    )

    search_fields = (
        "farm__farm_name",
        "species",
    )

    date_hierarchy = "production_date"