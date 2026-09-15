from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ProductionRecordForm
from .models import ProductionRecord


@login_required
def production_list(request):

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

        records = ProductionRecord.objects.filter(
            farm__municipality=profile.municipality
        ).select_related(
            "farm",
            "farm__farmer",
            "farm__municipality",
        )

    # =====================================================
    # BFAR USERS
    # =====================================================

    elif profile.role == "BFAR":

        records = ProductionRecord.objects.select_related(
            "farm",
            "farm__farmer",
            "farm__municipality",
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
        "production/production_list.html",
        {
            "records": records,
        }
    )


@login_required
def production_create(request):

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

            form = ProductionRecordForm(
                request.POST
            )

            if form.is_valid():

                record = form.save(
                    commit=False
                )

                # -----------------------------------------
                # SECURITY CHECK
                # -----------------------------------------

                if record.farm.municipality_id != (
                    profile.municipality.id
                ):

                    form.add_error(
                        "farm",
                        "You can only select a farm "
                        "from your municipality."
                    )

                else:

                    record.save()

                    messages.success(
                        request,
                        "Production record added successfully."
                    )

                    return redirect(
                        "production_list"
                    )

        else:

            form = ProductionRecordForm()

        # -----------------------------------------
        # RESTRICT FARM DROPDOWN
        # -----------------------------------------

        form.fields["farm"].queryset = (
            form.fields["farm"]
            .queryset
            .filter(
                municipality=profile.municipality
            )
        )

        return render(
            request,
            "production/production_form.html",
            {
                "form": form,
                "page_title": "Add Production Record",
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
def production_edit(request, pk):

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

        record = get_object_or_404(
            ProductionRecord,
            pk=pk,
            farm__municipality=profile.municipality
        )

        if request.method == "POST":

            form = ProductionRecordForm(
                request.POST,
                instance=record
            )

            if form.is_valid():

                updated_record = form.save(
                    commit=False
                )

                # -----------------------------------------
                # PREVENT CROSS-MUNICIPALITY FARM
                # -----------------------------------------

                if updated_record.farm.municipality_id != (
                    profile.municipality.id
                ):

                    form.add_error(
                        "farm",
                        "You can only select a farm "
                        "from your municipality."
                    )

                else:

                    updated_record.save()

                    messages.success(
                        request,
                        "Production record updated successfully."
                    )

                    return redirect(
                        "production_list"
                    )

        else:

            form = ProductionRecordForm(
                instance=record
            )

        # -----------------------------------------
        # RESTRICT FARM DROPDOWN
        # -----------------------------------------

        form.fields["farm"].queryset = (
            form.fields["farm"]
            .queryset
            .filter(
                municipality=profile.municipality
            )
        )

        return render(
            request,
            "production/production_form.html",
            {
                "form": form,
                "page_title": "Edit Production Record",
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
def production_delete(request, pk):

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

        record = get_object_or_404(
            ProductionRecord,
            pk=pk,
            farm__municipality=profile.municipality
        )

        if request.method == "POST":

            record.delete()

            messages.success(
                request,
                "Production record deleted successfully."
            )

            return redirect(
                "production_list"
            )

        return render(
            request,
            "production/production_confirm_delete.html",
            {
                "record": record
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