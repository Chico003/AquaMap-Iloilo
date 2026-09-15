from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render

from farmers.models import Farmer, Municipality
from farms.models import Farm
from production.models import ProductionRecord


def home(request):

    # =====================================================
    # PUBLIC GENERAL INFORMATION
    # =====================================================

    total_farmers = Farmer.objects.count()

    total_farms = Farm.objects.count()

    total_municipalities = Municipality.objects.filter(
        is_active=True
    ).count()

    total_production_records = ProductionRecord.objects.count()

    total_production = (
        ProductionRecord.objects.aggregate(
            total=Sum("quantity")
        )["total"] or 0
    )


    # =====================================================
    # PUBLIC MAP DATA
    # =====================================================

    farms = Farm.objects.select_related(
        "farmer",
        "municipality"
    ).prefetch_related(
        "production_records"
    ).all()


    farm_map_data = []


    for farm in farms:

        production_records = []


        for record in farm.production_records.all():

            production_records.append({

                "species": record.species,

                "quantity": str(record.quantity),

                "unit": record.get_unit_display(),

                "production_date": record.production_date.strftime(
                    "%B %d, %Y"
                ),

            })


        farm_map_data.append({

            "id": farm.pk,

            "name": farm.farm_name,

            "municipality": farm.municipality.name,

            "barangay": farm.barangay,

            "farm_type": farm.farm_type,

            "farm_type_display": farm.get_farm_type_display(),

            "area": str(farm.area),

            "latitude": float(farm.latitude),

            "longitude": float(farm.longitude),

            "production": production_records,

        })


    # =====================================================
    # LANDING PAGE CONTEXT
    # =====================================================

    context = {

        "total_farmers": total_farmers,

        "total_farms": total_farms,

        "total_municipalities": total_municipalities,

        "total_production_records": total_production_records,

        "total_production": total_production,

        "farms": farms,

        "farm_map_data": farm_map_data,

    }


    return render(
        request,
        "landing/home.html",
        context
    )


# =========================================================
# AUTHENTICATED DASHBOARD
# =========================================================

@login_required
def dashboard(request):

    total_farmers = Farmer.objects.count()

    total_farms = Farm.objects.count()

    total_municipalities = Municipality.objects.filter(
        is_active=True
    ).count()

    total_production = (
        ProductionRecord.objects.aggregate(
            total=Sum("quantity")
        )["total"] or 0
    )

    recent_farms = Farm.objects.select_related(
        "farmer",
        "municipality"
    ).order_by("-created_at")[:5]

    farms = Farm.objects.select_related(
        "farmer",
        "municipality"
    ).prefetch_related(
        "production_records"
    ).all()

    municipalities = Municipality.objects.filter(
        is_active=True
    ).order_by("name")


    # =====================================================
    # PREPARE FARM DATA
    # =====================================================

    farm_map_data = []


    for farm in farms:

        production_records = []


        for record in farm.production_records.all():

            production_records.append({

                "species": record.species,

                "quantity": str(record.quantity),

                "unit": record.get_unit_display(),

                "production_date": record.production_date.strftime(
                    "%B %d, %Y"
                ),

                "remarks": record.remarks,

            })


        farm_map_data.append({

            "id": farm.pk,

            "name": farm.farm_name,

            "farmer": str(farm.farmer),

            "municipality": farm.municipality.name,

            "barangay": farm.barangay,

            "farm_type": farm.farm_type,

            "farm_type_display": farm.get_farm_type_display(),

            "area": str(farm.area),

            "latitude": float(farm.latitude),

            "longitude": float(farm.longitude),

            "production": production_records,

        })


    context = {

        "total_farmers": total_farmers,

        "total_farms": total_farms,

        "total_municipalities": total_municipalities,

        "total_production": total_production,

        "recent_farms": recent_farms,

        "farms": farms,

        "municipalities": municipalities,

        "farm_map_data": farm_map_data,

    }


    return render(
        request,
        "dashboard/dashboard.html",
        context
    )