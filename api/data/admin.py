from django.contrib import admin
from .models import Address, HealthCareOrganization, HealthCareProvider, Affiliation
from uuid import uuid4
# Register your models here.

# docs: https://docs.djangoproject.com/en/4.2/ref/contrib/admin/#working-with-many-to-many-models


class HealthCareProviderAddressAdmin(admin.TabularInline):
    model = HealthCareProvider.addresses.through


class HealthCareOrganizationAddressAdmin(admin.TabularInline):
    model = HealthCareOrganization.addresses.through


class HealthCareOrganizationAdmin(admin.ModelAdmin):
    model = HealthCareOrganization
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['status']})
    ]
    list_display = ('name', 'status')
    exclude = ['addresses']
    inlines = [
        HealthCareOrganizationAddressAdmin
    ]


class HealthCareProviderAdmin(admin.ModelAdmin):
    model = HealthCareProvider
    fieldsets = [
        (None,               {'fields': ['name']}),
        (None,               {'fields': ['status']})
    ]
    list_display = ('name', 'status')
    exclude = ['addresses']
    inlines = [
        HealthCareProviderAddressAdmin
    ]


class AddressAdmin(admin.ModelAdmin):
    model = Address
    fieldsets = [
        (None,               {'fields': ['parent_type']}),
        (None,               {'fields': ['addr1']}),
        (None,               {'fields': ['addr2']}),
        (None,               {'fields': ['city']}),
        (None,               {'fields': ['state']}),
        (None,               {'fields': ['zip']}),
        (None,               {'fields': ['status']}),
    ]
    list_display = ('parent_type', 'addr1', 'addr2', 'city', 'state', 'zip', 'status')
    inlines = [
        HealthCareProviderAddressAdmin,
        HealthCareOrganizationAddressAdmin
    ]

class AffiliationAdmin(admin.ModelAdmin):
    model = Affiliation
    fieldsets = [
        (None,               {'fields': ['type']}),
        (None,               {'fields': ['status']}),
        (None,               {'fields': ['hcp_link']}),
        (None,               {'fields': ['hco_link']}),
    ]
    list_display = ('type', 'status', 'hcp_link', 'hcp_link')


admin.site.register(Affiliation, AffiliationAdmin)
admin.site.register(Address, AddressAdmin)
admin.site.register(HealthCareOrganization, HealthCareOrganizationAdmin)
admin.site.register(HealthCareProvider, HealthCareProviderAdmin)
