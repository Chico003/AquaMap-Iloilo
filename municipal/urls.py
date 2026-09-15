from django.urls import path

from . import views


urlpatterns = [
    path(
        "municipal/",
        views.municipal_dashboard,
        name="municipal_dashboard",
    ),

    path(
        "municipal/reports/farms/csv/",
        views.farm_inventory_csv,
        name="municipal_farm_inventory_csv",
    ),

    path(
        "municipal/reports/farms/pdf/",
        views.farm_inventory_pdf,
        name="municipal_farm_inventory_pdf",
    ),

    path(
        "municipal/reports/production/csv/",
        views.production_csv,
        name="municipal_production_csv",
    ),

    path(
        "municipal/reports/production/pdf/",
        views.production_pdf,
        name="municipal_production_pdf",
    ),
]