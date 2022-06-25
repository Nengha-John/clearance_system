from django.contrib import admin
from clearance.models import ClearanceRequests, ControlNumbers

# Register your models here.

class ClearanceRequestAdmin(admin.ModelAdmin):
    model = ClearanceRequests

    list_display = ['student','requested_on','status']
    list_display_links =['student','requested_on','status']
    list_filter = ['student']
    ordering = ('student',)

    fieldsets = (
        ('Clearance Information:', {'fields': ('student','requested_on','status',)}),
    )

    add_fieldsets = (
        ('Add Clearance Information:', {'fields': ('student','requested_on','status',)}),
    )
    search_field =['student']


class ControlNumbersAdmin(admin.ModelAdmin):
    model = ControlNumbers

    list_display = ['request','amount','control_no']
    list_display_links =['request','amount','control_no']
    list_filter = ['request']
    ordering = ('request',)

    fieldsets = (
        ('Clearance Information:', {'fields': ('request','amount','control_no',)}),
    )

    add_fieldsets = (
        ('Add Clearance Information:', {'fields': ('request','amount','control_no',)}),
    )
    search_field =['request']


admin.site.register(ClearanceRequests, ClearanceRequestAdmin)
admin.site.register(ControlNumbers, ControlNumbersAdmin)
