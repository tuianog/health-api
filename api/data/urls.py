from django.urls import path
from . import views

urlpatterns = [
    path('admin/hcp/', views.get_all_providers, name='get_all_providers'),
    path('admin/hco/', views.get_all_organizations, name='get_all_organizations'),
    path('admin/address/', views.get_all_addresses, name='get_all_addresses'),
    path('admin/affiliation/', views.get_all_affiliations, name='get_all_affiliations'),
    path('hco/<str:organization_id>/', views.get_healthcare_organization_by_id, name='get_healthcare_organization_by_id'),
    path('hco/<str:organization_id>/address/', views.get_healthcare_addresses_by_organization_by_id, name='get_healthcare_addresses_by_organization_by_id'),
    path('hco/<str:organization_id>/address/<str:address_id>/', views.get_healthcare_organization_address_by_id, name='get_healthcare_organization_address_by_id'),
    path('hco/<str:organization_id>/affiliation/', views.get_healthcare_organization_affiliations, name='get_healthcare_organization_affiliations'),
    path('hcp/<str:provider_id>/', views.get_healthcare_provider_by_id, name='get_healthcare_provider_by_id'),
    path('hcp/<str:provider_id>/address/', views.get_healthcare_addresses_by_provider_by_id, name='get_healthcare_addresses_by_provider_by_id'),
    path('hcp/<str:provider_id>/address/<str:address_id>/', views.get_healthcare_provider_address_by_id, name='get_healthcare_provider_address_by_id'),
    path('hcp/<str:provider_id>/affiliation/', views.get_healthcare_provider_affiliations, name='get_healthcare_provider_affiliations'),
    path('affiliation/<str:affiliation_id>/', views.get_affiliation_by_id, name='get_affiliation_by_id')
]
