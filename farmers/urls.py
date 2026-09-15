from django.urls import path

from . import views


urlpatterns = [
    path(
        "farmers/",
        views.farmer_list,
        name="farmer_list",
    ),
    path(
        "farmers/add/",
        views.farmer_create,
        name="farmer_create",
    ),
    path(
        "farmers/<int:pk>/edit/",
        views.farmer_edit,
        name="farmer_edit",
    ),
    path(
        "farmers/<int:pk>/delete/",
        views.farmer_delete,
        name="farmer_delete",
    ),
]