from django.db import models
from rest_framework.validators import ValidationError

# addresses
class Address(models.Model):
    PARENT_TYPE_ENUM = [
        ('hcp', 'HCP'),
        ('hco', 'HCO')
    ]
    STATUS_ENUM = [
        ('I', 'INACTIVE'),
        ('A', 'ACTIVE')
    ]
    parent_type = models.CharField(max_length=3, choices=PARENT_TYPE_ENUM)
    addr1 = models.CharField(max_length=200)
    addr2 = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=10)
    status = models.CharField(max_length=1, choices=STATUS_ENUM)

    class Meta:
        db_table = 'address'


# hcp
class HealthCareProvider(models.Model):
    STATUS_ENUM = [
        ('I', 'INACTIVE'),
        ('A', 'ACTIVE')
    ]
    name = models.CharField(max_length=200)
    addresses = models.ManyToManyField(
        Address
    )
    status = models.CharField(max_length=1, choices=STATUS_ENUM)
    
    class Meta:
        db_table = 'hcp'


# hco
class HealthCareOrganization(models.Model):
    STATUS_ENUM = [
        ('I', 'INACTIVE'),
        ('A', 'ACTIVE')
    ]
    name = models.CharField(max_length=200)
    addresses = models.ManyToManyField(
        Address
    )
    status = models.CharField(max_length=1, choices=STATUS_ENUM)

    class Meta:
        db_table = 'hco'


# affiliation
class Affiliation(models.Model):
    STATUS_ENUM = [
        ('I', 'INACTIVE'),
        ('A', 'ACTIVE')
    ]
    TYPE_ENUM = [
        ('HCP_HCO', 'HCP_HCO'),
        ('HCO_HCP', 'HCO_HCP'),
        ('HCO_HCO', 'HCO_HCO'),
        ('HCP_HCP', 'HCP_HCP')
    ]
    parent_hcp_link = models.ForeignKey(HealthCareProvider, related_name='parent_hcp_link', on_delete=models.CASCADE, null=True, blank=True)
    parent_hco_link = models.ForeignKey(HealthCareOrganization, related_name='parent_hco_link', on_delete=models.CASCADE, null=True, blank=True)
    child_hcp_link = models.ForeignKey(HealthCareProvider, related_name='child_hcp_link', on_delete=models.CASCADE, null=True, blank=True)
    child_hco_link = models.ForeignKey(HealthCareOrganization, related_name='child_hco_link', on_delete=models.CASCADE, null=True, blank=True)
    type = models.CharField(max_length=7, choices=TYPE_ENUM)
    status = models.CharField(max_length=1, choices=STATUS_ENUM)

    @staticmethod
    def create(**data):
        Affiliation.AffiliationValidator.validate_hcp_hcp(**data)
        Affiliation.AffiliationValidator.validate_hcp_hco(**data)
        Affiliation.AffiliationValidator.validate_hco_hcp(**data)
        Affiliation.AffiliationValidator.validate_hco_hco(**data)

        return Affiliation.objects.create(**data)
    
    class Meta:
        db_table = 'affiliation'
        # a given parent and child can only have one affiliation for the same type
        constraints = [
            models.UniqueConstraint(fields=['parent_hcp_link', 'child_hcp_link', 'type'], name='unique_affiliation_link_hcp_hcp'),
            models.UniqueConstraint(fields=['parent_hcp_link', 'child_hco_link', 'type'], name='unique_affiliation_link_hcp_hco'),
            models.UniqueConstraint(fields=['parent_hco_link', 'child_hcp_link', 'type'], name='unique_affiliation_link_hco_hcp'),
            models.UniqueConstraint(fields=['parent_hco_link', 'child_hco_link', 'type'], name='unique_affiliation_link_hco_hco')
        ]

    class AffiliationValidator:
        exception = ValidationError('Invalid type and parent/child')

        @staticmethod
        def validate_hcp_hcp(**data):
            if (data.get('parent_hcp_link') and data.get('child_hcp_link') and data.get('type') != 'HCP_HCP'):
                raise Affiliation.AffiliationValidator.exception
        
        @staticmethod
        def validate_hcp_hco(**data):
            if (data.get('parent_hcp_link') and data.get('child_hco_link') and data.get('type') != 'HCP_HCO'):
                raise Affiliation.AffiliationValidator.exception
            
        @staticmethod
        def validate_hco_hcp(**data):
            if (data.get('parent_hco_link') and data.get('child_hcp_link') and data.get('type') != 'HCO_HCP'):
                raise Affiliation.AffiliationValidator.exception
            
        @staticmethod
        def validate_hco_hco(**data):
            if (data.get('parent_hco_link') and data.get('child_hco_link') and data.get('type') != 'HCO_HCO'):
                raise Affiliation.AffiliationValidator.exception
        