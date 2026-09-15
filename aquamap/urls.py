from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("dashboard.urls")),
    path("", include("accounts.urls")),
    path("", include("farmers.urls")),
    path("", include("farms.urls")),
    path("", include("production.urls")),
    path("", include ("municipal.urls")),
    path("", include ("bfar.urls")),
]