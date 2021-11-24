from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, CoreCompanies


class CoreCompaniesModel(admin.ModelAdmin):

    list_display = (
        "society", "rif_type", "name", "rif", "company_image", "email",
        "web_site", "phone1", "phone2", "description", "address", "date", "id")
    search_fields = (
        "society", "rif_type", "name", "rif", "email", "web_site", "phone1",
        "phone2", "description", "address", "date", "id")
    list_filter = (
        "society", "rif_type", "name", "rif", "email", "web_site", "phone1",
        "phone2", "description", "address", "date", "id")


admin.site.register(User, UserAdmin)
admin.site.register(CoreCompanies, CoreCompaniesModel)
