from django.contrib import admin
from user.models import user


class useradmin(admin.ModelAdmin):
    list_display = [
        "number",
        "password",
    ]
    list_display_links = ["number"]


admin.site.register(user, useradmin)
