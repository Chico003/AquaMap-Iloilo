from django.urls import path

from . import views


urlpatterns = [

    path(
        "bfar/",
        views.bfar_dashboard,
        name="bfar_dashboard",
    ),

    path(
        "bfar/reports/farms/csv/",
        views.farm_inventory_csv,
        name="bfar_farm_inventory_csv",
    ),

    path(
        "bfar/reports/farms/pdf/",
        views.farm_inventory_pdf,
        name="bfar_farm_inventory_pdf",
    ),

    path(
        "bfar/reports/production/csv/",
        views.production_csv,
        name="bfar_production_csv",
    ),

    path(
        "bfar/reports/production/pdf/",
        views.production_pdf,
        name="bfar_production_pdf",
    ),

]