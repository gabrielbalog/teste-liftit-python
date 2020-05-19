from django.contrib import admin
from rest_framework.authtoken.admin import TokenAdmin

from .models import Vehicle


class VehicleAdmin(admin.ModelAdmin):
    exclude = ("owner",)
    list_display = ("name", "registration", "brand", "type", "owner")
    list_filter = ("brand", "type")
    search_fields = ("name", "registration", "owner__username")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        obj.save()

    def get_queryset(self, request):
        # For Django < 1.6, override queryset instead of get_queryset
        qs = super(VehicleAdmin, self).get_queryset(request)
        if request.user.is_superuser:
            return qs

        return qs.filter(owner=request.user)

    def has_change_permission(self, request, obj=None):
        if not obj or request.user.is_superuser:
            # the changelist itself
            return True
        return obj.owner == request.user



TokenAdmin.raw_id_fields = ['user']

admin.site.register(Vehicle, VehicleAdmin)
