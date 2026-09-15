import csv
from datetime import datetime
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from farmers.models import Farmer, Municipality
from farms.models import Farm
from production.models import ProductionRecord


# =========================================================
# BFAR DASHBOARD
# =========================================================

@login_required
def bfar_dashboard(request):

    profile = request.user.profile

    # =====================================================
    # ACCESS CONTROL
    # =====================================================

    if profile.role != "BFAR":
        return render(
            request,
            "bfar/access_denied.html",
            status=403
        )

    # =====================================================
    # MUNICIPALITIES
    # =====================================================

    municipalities = Municipality.objects.filter(
        is_active=True
    ).order_by("name")

    # =====================================================
    # FILTER VALUES
    # =====================================================

    selected_municipality = request.GET.get(
        "municipality",
        ""
    ).strip()

    selected_farm_type = request.GET.get(
        "farm_type",
        ""
    ).strip()

    search_query = request.GET.get(
        "search",
        ""
    ).strip()

    # =====================================================
    # BASE FARM QUERY
    # =====================================================

    farms = Farm.objects.select_related(
        "farmer",
        "municipality"
    ).prefetch_related(
        "production_records"
    )

    # =====================================================
    # FILTERS
    # =====================================================

    if selected_municipality:

        farms = farms.filter(
            municipality__name=selected_municipality
        )

    if selected_farm_type:

        farms = farms.filter(
            farm_type=selected_farm_type
        )

    if search_query:

        farms = farms.filter(
            farm_name__icontains=search_query
        ) | farms.filter(
            barangay__icontains=search_query
        ) | farms.filter(
            farmer__first_name__icontains=search_query
        ) | farms.filter(
            farmer__last_name__icontains=search_query
        )

    farms = farms.distinct()

    # =====================================================
    # FILTERED FARM IDS
    # =====================================================

    filtered_farm_ids = list(
        farms.values_list(
            "id",
            flat=True
        )
    )

    # =====================================================
    # PRODUCTION RECORDS
    # =====================================================

    production_records = (
        ProductionRecord.objects
        .select_related(
            "farm",
            "farm__farmer",
            "farm__municipality"
        )
        .filter(
            farm_id__in=filtered_farm_ids
        )
        .order_by(
            "-production_date"
        )
    )

    # =====================================================
    # BASIC STATISTICS
    # =====================================================

    total_municipalities = municipalities.count()

    total_farmers = Farmer.objects.filter(
        municipality__is_active=True,
        farms__id__in=filtered_farm_ids
    ).distinct().count()

    total_farms = farms.count()

    total_production_records = (
        production_records.count()
    )

    total_farm_area = (
        farms.aggregate(
            total=Sum("area")
        )["total"] or 0
    )

    # =====================================================
    # FARM TYPE SUMMARY
    # =====================================================

    farm_type_summary = []

    for farm_type_code, farm_type_name in Farm.FARM_TYPE_CHOICES:

        count = farms.filter(
            farm_type=farm_type_code
        ).count()

        farm_type_summary.append({
            "code": farm_type_code,
            "name": farm_type_name,
            "count": count,
        })

    # =====================================================
    # MUNICIPALITY SUMMARY
    # =====================================================

    municipality_summary = []

    for municipality in municipalities:

        municipality_farms = farms.filter(
            municipality=municipality
        )

        municipality_farm_ids = list(
            municipality_farms.values_list(
                "id",
                flat=True
            )
        )

        municipality_farmers = Farmer.objects.filter(
            municipality=municipality,
            farms__id__in=filtered_farm_ids
        ).distinct().count()

        municipality_production = (
            production_records.filter(
                farm_id__in=municipality_farm_ids
            ).count()
        )

        municipality_summary.append({
            "municipality": municipality.name,
            "farmers": municipality_farmers,
            "farms": municipality_farms.count(),
            "production_records": municipality_production,
        })

    # =====================================================
    # ANALYTICS - MUNICIPALITY
    # =====================================================

    analytics_municipalities = [
        item["municipality"]
        for item in municipality_summary
    ]

    analytics_farm_counts = [
        item["farms"]
        for item in municipality_summary
    ]

    analytics_production_counts = [
        item["production_records"]
        for item in municipality_summary
    ]

    # =====================================================
    # ANALYTICS - FARM TYPE
    # =====================================================

    analytics_farm_types = [
        item["name"]
        for item in farm_type_summary
    ]

    analytics_farm_type_counts = [
        item["count"]
        for item in farm_type_summary
    ]

    # =====================================================
    # ANALYTICS - SPECIES
    #
    # KG and Metric Tons are NOT combined.
    # =====================================================

    species_data = {}

    for record in production_records:

        species = record.species.strip()

        unit = record.get_unit_display()

        key = f"{species} ({unit})"

        if key not in species_data:
            species_data[key] = 0

        species_data[key] += float(
            record.quantity
        )

    analytics_species = list(
        species_data.keys()
    )

    analytics_species_quantities = list(
        species_data.values()
    )

    # =====================================================
    # MAP DATA
    # =====================================================

    farm_map_data = []

    for farm in farms:

        production = []

        for record in farm.production_records.all():

            if record.farm_id not in filtered_farm_ids:
                continue

            production.append({
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
            "production": production,
        })

    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "municipalities": municipalities,

        "farms": farms,

        "production_records": production_records,

        "municipality_summary": municipality_summary,

        "farm_type_summary": farm_type_summary,

        "total_municipalities":
            total_municipalities,

        "total_farmers":
            total_farmers,

        "total_farms":
            total_farms,

        "total_production_records":
            total_production_records,

        "total_farm_area":
            total_farm_area,

        "farm_map_data":
            farm_map_data,

        "selected_municipality":
            selected_municipality,

        "selected_farm_type":
            selected_farm_type,

        "search_query":
            search_query,

        # Analytics

        "analytics_municipalities":
            analytics_municipalities,

        "analytics_farm_counts":
            analytics_farm_counts,

        "analytics_production_counts":
            analytics_production_counts,

        "analytics_farm_types":
            analytics_farm_types,

        "analytics_farm_type_counts":
            analytics_farm_type_counts,

        "analytics_species":
            analytics_species,

        "analytics_species_quantities":
            analytics_species_quantities,
    }

    return render(
        request,
        "bfar/dashboard.html",
        context
    )


# =========================================================
# BFAR ACCESS CHECK
# =========================================================

def get_bfar_profile(request):

    profile = request.user.profile

    if profile.role != "BFAR":
        return None

    return profile


# =========================================================
# BFAR FARM INVENTORY CSV
# =========================================================

@login_required
def farm_inventory_csv(request):

    profile = get_bfar_profile(request)

    if profile is None:

        return HttpResponse(
            "Access denied.",
            status=403
        )

    farms = Farm.objects.select_related(
        "farmer",
        "municipality"
    ).prefetch_related(
        "production_records"
    ).order_by(
        "municipality",
        "barangay",
        "farm_name"
    )

    filename = (
        "aquamap_bfar_consolidated_farm_inventory.csv"
    )

    response = HttpResponse(
        content_type="text/csv; charset=utf-8"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    writer = csv.writer(response)

    # =====================================================
    # REPORT HEADER
    # =====================================================

    writer.writerow([
        "AquaMap Iloilo"
    ])

    writer.writerow([
        "BFAR Region VI Consolidated Farm Inventory Report"
    ])

    writer.writerow([
        "Coverage",
        "All Participating Municipalities"
    ])

    writer.writerow([
        "Date Generated",
        datetime.now().strftime(
            "%B %d, %Y %I:%M %p"
        )
    ])

    writer.writerow([])

    # =====================================================
    # TABLE HEADER
    # =====================================================

    writer.writerow([
        "Farm Name",
        "Farmer",
        "Municipality",
        "Barangay",
        "Farm Type",
        "Area (ha)",
        "Latitude",
        "Longitude",
        "Production Records",
    ])

    # =====================================================
    # DATA
    # =====================================================

    for farm in farms:

        writer.writerow([
            farm.farm_name,
            str(farm.farmer),
            farm.municipality.name,
            farm.barangay,
            farm.get_farm_type_display(),
            farm.area,
            farm.latitude,
            farm.longitude,
            farm.production_records.count(),
        ])

    return response


# =========================================================
# BFAR FARM INVENTORY PDF
# =========================================================

@login_required
def farm_inventory_pdf(request):

    profile = get_bfar_profile(request)

    if profile is None:

        return HttpResponse(
            "Access denied.",
            status=403
        )

    farms = Farm.objects.select_related(
        "farmer",
        "municipality"
    ).prefetch_related(
        "production_records"
    ).order_by(
        "municipality",
        "barangay",
        "farm_name"
    )

    context = {
        "farms": farms,
        "generated_at": datetime.now(),
    }

    return create_pdf(
        request,
        "bfar/farm_inventory_pdf.html",
        context,
        "aquamap_bfar_consolidated_farm_inventory.pdf"
    )


# =========================================================
# BFAR PRODUCTION CSV
# =========================================================

@login_required
def production_csv(request):

    profile = get_bfar_profile(request)

    if profile is None:

        return HttpResponse(
            "Access denied.",
            status=403
        )

    records = ProductionRecord.objects.select_related(
        "farm",
        "farm__farmer",
        "farm__municipality"
    ).order_by(
        "-production_date"
    )

    filename = (
        "aquamap_bfar_consolidated_production.csv"
    )

    response = HttpResponse(
        content_type="text/csv; charset=utf-8"
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    writer = csv.writer(response)

    # =====================================================
    # REPORT HEADER
    # =====================================================

    writer.writerow([
        "AquaMap Iloilo"
    ])

    writer.writerow([
        "BFAR Region VI Consolidated Production Report"
    ])

    writer.writerow([
        "Coverage",
        "All Participating Municipalities"
    ])

    writer.writerow([
        "Date Generated",
        datetime.now().strftime(
            "%B %d, %Y %I:%M %p"
        )
    ])

    writer.writerow([])

    # =====================================================
    # TABLE HEADER
    # =====================================================

    writer.writerow([
        "Production Date",
        "Farm",
        "Farmer",
        "Municipality",
        "Barangay",
        "Species",
        "Quantity",
        "Unit",
        "Remarks",
    ])

    # =====================================================
    # DATA
    # =====================================================

    for record in records:

        writer.writerow([
            record.production_date,
            record.farm.farm_name,
            str(record.farm.farmer),
            record.farm.municipality.name,
            record.farm.barangay,
            record.species,
            record.quantity,
            record.get_unit_display(),
            record.remarks,
        ])

    return response


# =========================================================
# BFAR PRODUCTION PDF
# =========================================================

@login_required
def production_pdf(request):

    profile = get_bfar_profile(request)

    if profile is None:

        return HttpResponse(
            "Access denied.",
            status=403
        )

    records = ProductionRecord.objects.select_related(
        "farm",
        "farm__farmer",
        "farm__municipality"
    ).order_by(
        "-production_date"
    )

    context = {
        "records": records,
        "generated_at": datetime.now(),
    }

    return create_pdf(
        request,
        "bfar/production_pdf.html",
        context,
        "aquamap_bfar_consolidated_production.pdf"
    )


# =========================================================
# PDF GENERATOR
# =========================================================

def create_pdf(
    request,
    template_name,
    context,
    filename,
):

    from django.template.loader import render_to_string

    from xhtml2pdf import pisa

    html = render_to_string(
        template_name,
        context,
        request=request,
    )

    result = BytesIO()

    pdf = pisa.CreatePDF(
        src=html,
        dest=result,
        encoding="UTF-8",
    )

    if pdf.err:

        return HttpResponse(
            "PDF generation failed.",
            status=500,
            content_type="text/plain",
        )

    response = HttpResponse(
        result.getvalue(),
        content_type="application/pdf",
    )

    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )

    return response