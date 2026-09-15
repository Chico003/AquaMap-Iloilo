import csv
from datetime import datetime
from io import BytesIO

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render
from django.template.loader import get_template

from farmers.models import Farmer
from farms.models import Farm
from production.models import ProductionRecord


# =========================================================
# MUNICIPAL DASHBOARD
# =========================================================

@login_required
def municipal_dashboard(request):

    profile = request.user.profile

    # =====================================================
    # ACCESS CONTROL
    # =====================================================

    if profile.role != "MUNICIPAL":

        return render(
            request,
            "municipal/access_denied.html",
            status=403,
        )


    if profile.municipality is None:

        return render(
            request,
            "municipal/no_municipality.html",
            status=403,
        )


    municipality = profile.municipality


    # =====================================================
    # FARMERS
    # =====================================================

    farmers = Farmer.objects.filter(
        municipality=municipality
    ).order_by(
        "last_name",
        "first_name",
    )


    # =====================================================
    # FARMS
    # =====================================================

    farms = Farm.objects.select_related(
        "farmer",
        "municipality",
    ).prefetch_related(
        "production_records",
    ).filter(
        municipality=municipality
    ).order_by(
        "-created_at",
    )


    # =====================================================
    # PRODUCTION
    # =====================================================

    production_records = ProductionRecord.objects.select_related(
        "farm",
        "farm__farmer",
        "farm__municipality",
    ).filter(
        farm__municipality=municipality
    ).order_by(
        "-production_date",
    )


    # =====================================================
    # FARM MAP DATA
    # =====================================================

    farm_map_data = []


    for farm in farms:

        production = []


        for record in farm.production_records.all():

            production.append({

                "species":
                    record.species,

                "quantity":
                    str(record.quantity),

                "unit":
                    record.get_unit_display(),

                "production_date":
                    record.production_date.strftime(
                        "%B %d, %Y"
                    ),

                "remarks":
                    record.remarks,

            })


        farm_map_data.append({

            "id":
                farm.pk,

            "name":
                farm.farm_name,

            "farmer":
                str(farm.farmer),

            "municipality":
                farm.municipality.name,

            "barangay":
                farm.barangay,

            "farm_type":
                farm.farm_type,

            "farm_type_display":
                farm.get_farm_type_display(),

            "area":
                str(farm.area),

            "latitude":
                float(farm.latitude),

            "longitude":
                float(farm.longitude),

            "production":
                production,

        })


    # =====================================================
    # CONTEXT
    # =====================================================

    context = {

        "municipality":
            municipality,

        "farmers":
            farmers,

        "farms":
            farms,

        "recent_farms":
            farms[:5],

        "production_records":
            production_records,

        "total_farmers":
            farmers.count(),

        "total_farms":
            farms.count(),

        "total_production_records":
            production_records.count(),

        "farm_map_data":
            farm_map_data,

    }


    # =====================================================
    # RENDER MUNICIPAL DASHBOARD
    #
    # IMPORTANT:
    # This matches the actual dashboard template:
    #
    # templates/municipal/dashboard.html
    # =====================================================

    return render(
        request,
        "municipal/dashboard.html",
        context,
    )


# =========================================================
# MUNICIPAL REPORT ACCESS CHECK
# =========================================================

def get_municipal_profile(request):

    profile = request.user.profile


    if profile.role != "MUNICIPAL":

        return None


    if profile.municipality is None:

        return None


    return profile


# =========================================================
# FARM INVENTORY CSV
# =========================================================

@login_required
def farm_inventory_csv(request):

    profile = get_municipal_profile(request)


    if profile is None:

        return HttpResponse(
            "Access denied.",
            status=403,
        )


    municipality = profile.municipality


    farms = Farm.objects.select_related(
        "farmer",
        "municipality",
    ).prefetch_related(
        "production_records",
    ).filter(
        municipality=municipality
    ).order_by(
        "barangay",
        "farm_name",
    )


    filename = (
        f"aquamap_{municipality.name.lower().replace(' ', '_')}"
        "_farm_inventory.csv"
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
        "Farm Inventory Report"
    ])


    writer.writerow([
        "Municipality",
        municipality.name,
    ])


    writer.writerow([
        "Date Generated",
        datetime.now().strftime(
            "%B %d, %Y %I:%M %p"
        ),
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
# FARM INVENTORY PDF
# =========================================================

@login_required
def farm_inventory_pdf(request):

    profile = get_municipal_profile(request)


    if profile is None:

        return HttpResponse(
            "Access denied.",
            status=403,
        )


    municipality = profile.municipality


    farms = Farm.objects.select_related(
        "farmer",
        "municipality",
    ).prefetch_related(
        "production_records",
    ).filter(
        municipality=municipality
    ).order_by(
        "barangay",
        "farm_name",
    )


    context = {

        "municipality":
            municipality,

        "farms":
            farms,

        "generated_at":
            datetime.now(),

    }


    return create_pdf(

        request,

        "municipal/farm_inventory_pdf.html",

        context,

        (
            f"aquamap_{municipality.name.lower().replace(' ', '_')}"
            "_farm_inventory.pdf"
        ),

    )


# =========================================================
# PRODUCTION CSV
# =========================================================

@login_required
def production_csv(request):

    profile = get_municipal_profile(request)


    if profile is None:

        return HttpResponse(
            "Access denied.",
            status=403,
        )


    municipality = profile.municipality


    records = ProductionRecord.objects.select_related(
        "farm",
        "farm__farmer",
        "farm__municipality",
    ).filter(
        farm__municipality=municipality
    ).order_by(
        "-production_date",
    )


    filename = (
        f"aquamap_{municipality.name.lower().replace(' ', '_')}"
        "_production_report.csv"
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
        "Production Report"
    ])


    writer.writerow([
        "Municipality",
        municipality.name,
    ])


    writer.writerow([
        "Date Generated",
        datetime.now().strftime(
            "%B %d, %Y %I:%M %p"
        ),
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
# PRODUCTION PDF
# =========================================================

@login_required
def production_pdf(request):

    profile = get_municipal_profile(request)


    if profile is None:

        return HttpResponse(
            "Access denied.",
            status=403,
        )


    municipality = profile.municipality


    records = ProductionRecord.objects.select_related(
        "farm",
        "farm__farmer",
        "farm__municipality",
    ).filter(
        farm__municipality=municipality
    ).order_by(
        "-production_date",
    )


    context = {

        "municipality":
            municipality,

        "records":
            records,

        "generated_at":
            datetime.now(),

    }


    return create_pdf(

        request,

        "municipal/production_pdf.html",

        context,

        (
            f"aquamap_{municipality.name.lower().replace(' ', '_')}"
            "_production_report.pdf"
        ),

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

    from xhtml2pdf import pisa


    template = get_template(
        template_name
    )


    html = template.render(
        context,
        request,
    )


    result = BytesIO()


    pdf = pisa.CreatePDF(
        html,
        dest=result,
    )


    if pdf.err:

        return HttpResponse(
            "PDF generation failed.",
            status=500,
        )


    response = HttpResponse(
        result.getvalue(),
        content_type="application/pdf",
    )


    response["Content-Disposition"] = (
        f'attachment; filename="{filename}"'
    )


    return response