from django.contrib import admin

from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = (
        "user",
        "role",
        "municipality",
    )

    list_filter = (
        "role",
        "municipality",
    )

    search_fields = (
        "user__username",
        "user__email",
    )