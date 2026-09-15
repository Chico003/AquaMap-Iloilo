from django.urls import path

from . import views


urlpatterns = [
    path(
        "production/",
        views.production_list,
        name="production_list"
    ),

    path(
        "production/add/",
        views.production_create,
        name="production_create"
    ),

    path(
        "production/<int:pk>/edit/",
        views.production_edit,
        name="production_edit"
    ),

    path(
        "production/<int:pk>/delete/",
        views.production_delete,
        name="production_delete"
    ),
]