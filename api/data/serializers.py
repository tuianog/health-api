from rest_framework import serializers
from .models import Address, HealthCareProvider, HealthCareOrganization, Affiliation

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "parent_type", "addr1", "addr2", "city", "state", "zip", "status"]
        read_only_fields = ['id']

class HealthCareProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCareProvider
        fields = ["id", "name", "status"]
        read_only_fields = ['id']

class HealthCareOrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCareOrganization
        fields = ["id", "name", "status"]
        read_only_fields = ['id']

class HealthCareOrganizationAddressesSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = HealthCareOrganization
        fields = ["addresses"]

class HealthCareProviderAddressesSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = HealthCareProvider
        fields = ["addresses"]


class AffiliationSerializer(serializers.ModelSerializer):
    parent_link = serializers.SerializerMethodField(method_name='parse_parent_link')
    child_link = serializers.SerializerMethodField(method_name='parse_child_link')

    def parse_parent_link(self, affiliation):
        return affiliation.hcp_link.id if affiliation.type == 'HCP_HCO' else affiliation.hco_link.id

    def parse_child_link(self, affiliation):
        return affiliation.hcp_link.id if affiliation.type == 'HCO_HCP' else affiliation.hco_link.id
    
    class Meta:
        model = Affiliation
        fields = ["id", "status", "type", "parent_link", "child_link"]
        read_only_fields = ['id', 'parent_link', 'child_link']
