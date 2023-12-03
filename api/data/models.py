from django.db import models

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
        ('HCO_HCP', 'HCO_HCP')
    ]
    hcp_link = models.ForeignKey(HealthCareProvider, on_delete=models.CASCADE)
    hco_link = models.ForeignKey(HealthCareOrganization, on_delete=models.CASCADE)
    type = models.CharField(max_length=7, choices=TYPE_ENUM)
    status = models.CharField(max_length=1, choices=STATUS_ENUM)

    class Meta:
        db_table = 'affiliation'
        # a given HCP and HCO can only have one affiliation for the same type
        constraints = [
            models.UniqueConstraint(fields=['hcp_link', 'hco_link', 'type'], name='unique_affiliation_link')
        ]
