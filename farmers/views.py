from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FarmerForm
from .models import Farmer


@login_required
def farmer_list(request):

    # =====================================================
    # GET USER PROFILE
    # =====================================================

    profile = request.user.profile

    # =====================================================
    # MUNICIPAL USERS
    # =====================================================

    if profile.role == "MUNICIPAL":

        if profile.municipality is None:
            return render(
                request,
                "municipal/no_municipality.html",
                status=403
            )

        farmers = Farmer.objects.filter(
            municipality=profile.municipality
        ).select_related(
            "municipality"
        )

    # =====================================================
    # BFAR USERS
    # =====================================================

    elif profile.role == "BFAR":

        farmers = Farmer.objects.select_related(
            "municipality"
        ).all()

    # =====================================================
    # UNKNOWN ROLE
    # =====================================================

    else:

        return render(
            request,
            "municipal/access_denied.html",
            status=403
        )

    return render(
        request,
        "farmers/farmer_list.html",
        {
            "farmers": farmers,
        }
    )


@login_required
def farmer_create(request):

    profile = request.user.profile

    # =====================================================
    # MUNICIPAL USERS
    # =====================================================

    if profile.role == "MUNICIPAL":

        if profile.municipality is None:
            return render(
                request,
                "municipal/no_municipality.html",
                status=403
            )

        if request.method == "POST":

            form = FarmerForm(request.POST)

            if form.is_valid():

                farmer = form.save(
                    commit=False
                )

                # -----------------------------------------
                # FORCE MUNICIPALITY
                # -----------------------------------------

                farmer.municipality = (
                    profile.municipality
                )

                farmer.save()

                messages.success(
                    request,
                    "Farmer added successfully."
                )

                return redirect(
                    "farmer_list"
                )

        else:

            form = FarmerForm()

        return render(
            request,
            "farmers/farmer_form.html",
            {
                "form": form,
                "page_title": "Add Farmer",
            }
        )

    # =====================================================
    # BFAR USERS
    # =====================================================

    elif profile.role == "BFAR":

        # BFAR is VIEW-ONLY
        return render(
            request,
            "municipal/access_denied.html",
            status=403
        )

    # =====================================================
    # UNKNOWN ROLE
    # =====================================================

    return render(
        request,
        "municipal/access_denied.html",
        status=403
    )


@login_required
def farmer_edit(request, pk):

    profile = request.user.profile

    # =====================================================
    # MUNICIPAL USERS
    # =====================================================

    if profile.role == "MUNICIPAL":

        if profile.municipality is None:
            return render(
                request,
                "municipal/no_municipality.html",
                status=403
            )

        # -----------------------------------------
        # IMPORTANT SECURITY CHECK
        # -----------------------------------------

        farmer = get_object_or_404(
            Farmer,
            pk=pk,
            municipality=profile.municipality
        )

        if request.method == "POST":

            form = FarmerForm(
                request.POST,
                instance=farmer
            )

            if form.is_valid():

                updated_farmer = form.save(
                    commit=False
                )

                # -----------------------------------------
                # PREVENT MUNICIPALITY CHANGING
                # -----------------------------------------

                updated_farmer.municipality = (
                    profile.municipality
                )

                updated_farmer.save()

                messages.success(
                    request,
                    "Farmer updated successfully."
                )

                return redirect(
                    "farmer_list"
                )

        else:

            form = FarmerForm(
                instance=farmer
            )

        return render(
            request,
            "farmers/farmer_form.html",
            {
                "form": form,
                "page_title": "Edit Farmer",
            }
        )

    # =====================================================
    # BFAR USERS
    # =====================================================

    elif profile.role == "BFAR":

        return render(
            request,
            "municipal/access_denied.html",
            status=403
        )

    # =====================================================
    # UNKNOWN ROLE
    # =====================================================

    return render(
        request,
        "municipal/access_denied.html",
        status=403
    )


@login_required
def farmer_delete(request, pk):

    profile = request.user.profile

    # =====================================================
    # MUNICIPAL USERS
    # =====================================================

    if profile.role == "MUNICIPAL":

        if profile.municipality is None:
            return render(
                request,
                "municipal/no_municipality.html",
                status=403
            )

        # -----------------------------------------
        # IMPORTANT SECURITY CHECK
        # -----------------------------------------

        farmer = get_object_or_404(
            Farmer,
            pk=pk,
            municipality=profile.municipality
        )

        if request.method == "POST":

            farmer.delete()

            messages.success(
                request,
                "Farmer deleted successfully."
            )

            return redirect(
                "farmer_list"
            )

        return render(
            request,
            "farmers/farmer_confirm_delete.html",
            {
                "farmer": farmer
            }
        )

    # =====================================================
    # BFAR USERS
    # =====================================================

    elif profile.role == "BFAR":

        # BFAR is VIEW-ONLY
        return render(
            request,
            "municipal/access_denied.html",
            status=403
        )

    # =====================================================
    # UNKNOWN ROLE
    # =====================================================

    return render(
        request,
        "municipal/access_denied.html",
        status=403
    )