from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import FarmForm
from .models import Farm


@login_required
def farm_list(request):

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

        farms = Farm.objects.filter(
            municipality=profile.municipality
        ).select_related(
            "farmer",
            "municipality"
        )

    # =====================================================
    # BFAR USERS
    # =====================================================

    elif profile.role == "BFAR":

        farms = Farm.objects.select_related(
            "farmer",
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
        "farms/farm_list.html",
        {
            "farms": farms,
        }
    )


@login_required
def farm_create(request):

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

            form = FarmForm(request.POST)

            if form.is_valid():

                farm = form.save(
                    commit=False
                )

                # -----------------------------------------
                # SECURITY CHECK
                # -----------------------------------------

                if farm.farmer.municipality_id != (
                    profile.municipality.id
                ):

                    form.add_error(
                        "farmer",
                        "You can only select a farmer "
                        "from your municipality."
                    )

                else:

                    # Force municipality
                    farm.municipality = (
                        profile.municipality
                    )

                    farm.save()

                    messages.success(
                        request,
                        "Farm added successfully."
                    )

                    return redirect(
                        "farm_list"
                    )

        else:

            # -----------------------------------------
            # ONLY SHOW FARMERS FROM THIS MUNICIPALITY
            # -----------------------------------------

            form = FarmForm()

            form.fields["farmer"].queryset = (
                form.fields["farmer"]
                .queryset
                .filter(
                    municipality=profile.municipality
                )
            )

        # Make sure the farmer dropdown is restricted
        if "farmer" in form.fields:

            form.fields["farmer"].queryset = (
                form.fields["farmer"]
                .queryset
                .filter(
                    municipality=profile.municipality
                )
            )

        return render(
            request,
            "farms/farm_form.html",
            {
                "form": form,
                "page_title": "Add Farm",
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
def farm_edit(request, pk):

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
        # SECURITY CHECK
        # -----------------------------------------

        farm = get_object_or_404(
            Farm,
            pk=pk,
            municipality=profile.municipality
        )

        if request.method == "POST":

            form = FarmForm(
                request.POST,
                instance=farm
            )

            if form.is_valid():

                updated_farm = form.save(
                    commit=False
                )

                # -----------------------------------------
                # PREVENT CROSS-MUNICIPALITY FARMER
                # -----------------------------------------

                if updated_farm.farmer.municipality_id != (
                    profile.municipality.id
                ):

                    form.add_error(
                        "farmer",
                        "You can only select a farmer "
                        "from your municipality."
                    )

                else:

                    # Prevent municipality manipulation
                    updated_farm.municipality = (
                        profile.municipality
                    )

                    updated_farm.save()

                    messages.success(
                        request,
                        "Farm updated successfully."
                    )

                    return redirect(
                        "farm_list"
                    )

        else:

            form = FarmForm(
                instance=farm
            )

        # -----------------------------------------
        # RESTRICT FARMER DROPDOWN
        # -----------------------------------------

        form.fields["farmer"].queryset = (
            form.fields["farmer"]
            .queryset
            .filter(
                municipality=profile.municipality
            )
        )

        return render(
            request,
            "farms/farm_form.html",
            {
                "form": form,
                "page_title": "Edit Farm",
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
def farm_delete(request, pk):

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
        # SECURITY CHECK
        # -----------------------------------------

        farm = get_object_or_404(
            Farm,
            pk=pk,
            municipality=profile.municipality
        )

        if request.method == "POST":

            farm.delete()

            messages.success(
                request,
                "Farm deleted successfully."
            )

            return redirect(
                "farm_list"
            )

        return render(
            request,
            "farms/farm_confirm_delete.html",
            {
                "farm": farm
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