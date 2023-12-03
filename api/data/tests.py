from django.test import TestCase
from rest_framework.validators import ValidationError
from django.db.utils import DataError
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import User
from .models import Address, HealthCareProvider, HealthCareOrganization, Affiliation
from .views import get_all_addresses, get_affiliation_by_id, get_all_affiliations, get_all_providers, get_healthcare_provider_by_id, get_healthcare_addresses_by_provider_by_id, get_healthcare_provider_address_by_id
# doc: https://docs.djangoproject.com/en/4.2/topics/testing/overview/
# doc: https://www.django-rest-framework.org/api-guide/testing/


class AddressCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user('user', 'user@gmail.com', 'pwd')

    def test_create_address_has_expected_properties(self):
        Address.objects.create(addr1="Address 1", city="City 1", status="A")

        address = Address.objects.get(addr1="Address 1")
        
        self.assertEqual(address.addr1, 'Address 1')
        self.assertEqual(address.status, 'A')
        self.assertTrue(address.id is not None)

    
    def test_create_address_with_invalid_status_should_fail(self):
        with self.assertRaises(DataError):
            Address.objects.create(addr1="addr 1", city="City 1", status="invalid")

    def test_endpoint_admin_get_all_addresses_should_return_403(self):
        request = self.factory.get('/v1/admin/address/')
        
        response = get_all_addresses(request)

        self.assertEqual(response.status_code, 403)

    def test_endpoint_admin_get_all_addresses_should_return_expected_result(self):
        Address.objects.create(addr1="Address 1", city="City 1", status="A")

        request = self.factory.get('/v1/admin/address/')
        force_authenticate(request, user=self.user)
        
        response = get_all_addresses(request)
        parsed_response_headers = dict(response.headers)
        parsed_response_data = dict(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(parsed_response_headers.items(), {
            'Content-Type': 'application/json'
        }.items())
        self.assertGreaterEqual(parsed_response_data.items(), {
            'count': 1,
            'previous': None,
            'next': None,
        }.items())
        parsed_result_items = dict(parsed_response_data['results'][0])
        self.assertGreaterEqual(parsed_result_items.items(), {
            'addr1': 'Address 1',
            'city': 'City 1',
            'status': 'A',
            'addr2': None
        }.items())


class HealthCareProviderCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user('user', 'user@gmail.com', 'pwd')

    def test_create_hcp_with_no_addresses_has_expected_properties(self):
        HealthCareProvider.objects.create(name='hco', status='I')

        hco = HealthCareProvider.objects.get(name='hco')
        
        self.assertEqual(hco.status, 'I')
        self.assertTrue(hco.id is not None)

    def test_create_hcp_with_addresses_has_expected_properties(self):
        address = Address.objects.create(addr1="Address 1", city="City 1", status="A")

        hco = HealthCareProvider.objects.create(name='hco', status='I')
        hco.addresses.set([address])
        
        self.assertEqual(hco.status, 'I')
        self.assertTrue(hco.id is not None)

    def test_endpoint_admin_get_all_hcp_should_return_403(self):
        request = self.factory.get('/v1/admin/hcp/')
        
        response = get_all_addresses(request)

        self.assertEqual(response.status_code, 403)

    def test_endpoint_admin_get_all_hcp_filtered_by_status_should_return_expected_result(self):
        HealthCareProvider.objects.create(name='hco1', status='A')
        HealthCareProvider.objects.create(name='hco2', status='I')
        HealthCareProvider.objects.create(name='hco3', status='A')

        request = self.factory.get('/v1/admin/hcp/')
        force_authenticate(request, user=self.user)
        
        response = get_all_providers(request)
        parsed_response_headers = dict(response.headers)
        parsed_response_data = dict(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(parsed_response_headers.items(), {
            'Content-Type': 'application/json'
        }.items())
        self.assertGreaterEqual(parsed_response_data.items(), {
            'count': 2,
            'previous': None,
            'next': None,
        }.items())
        parsed_result_items = dict(parsed_response_data['results'][0])
        self.assertGreaterEqual(parsed_result_items.items(), {
            'name': 'hco1',
            'status': 'A'
        }.items())
        parsed_result_items = dict(parsed_response_data['results'][1])
        self.assertGreaterEqual(parsed_result_items.items(), {
            'name': 'hco3',
            'status': 'A'
        }.items())

    def test_endpoint_get_hcp_by_id_should_return_404(self):
        hco_id = '1'
        request = self.factory.get(f'/v1/hcp/{hco_id}/')
        
        response = get_healthcare_provider_by_id(request)
        force_authenticate(request, user=self.user)

        response = get_healthcare_provider_by_id(request, hco_id)

        self.assertEqual(response.status_code, 404)

    def test_endpoint_get_hcp_by_id_should_return_expected_result(self):
        hco = HealthCareProvider.objects.create(name='hco', status='I')
        
        request = self.factory.get(f'/v1/hcp/{hco.id}/')
        force_authenticate(request, user=self.user)
        
        response = get_healthcare_provider_by_id(request, hco.id)
        parsed_response_headers = dict(response.headers)
        parsed_response_data = dict(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(parsed_response_headers.items(), {
            'Content-Type': 'application/json'
        }.items())
        self.assertGreaterEqual(parsed_response_data.items(), {
            'name': 'hco',
            'status': 'I'
        }.items())

    def test_endpoint_get_hcp_addresses_by_id_should_return_expected_result(self):
        address = Address.objects.create(addr1="Address 1", city="City 1", status="A")
        hco = HealthCareProvider.objects.create(name='hco', status='I')
        hco.addresses.set([address])

        request = self.factory.get(f'/v1/hcp/{hco.id}/address/')
        force_authenticate(request, user=self.user)
        
        response = get_healthcare_addresses_by_provider_by_id(request, hco.id)
        parsed_response_headers = dict(response.headers)
        parsed_response_data = dict(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(parsed_response_headers.items(), {
            'Content-Type': 'application/json'
        }.items())
        self.assertGreaterEqual(parsed_response_data.items(), {
            'count': 1,
            'previous': None,
            'next': None,
        }.items())
        parsed_result_items = dict(parsed_response_data['results'][0])
        self.assertGreaterEqual(parsed_result_items.items(), {
            'addr1': 'Address 1',
            'city': 'City 1',
            'status': 'A'
        }.items())

    def test_endpoint_get_hcp_address_by_id_should_return_expected_result(self):
        address = Address.objects.create(addr1="Address 1", city="City 1", status="A")
        hco = HealthCareProvider.objects.create(name='hco', status='I')
        hco.addresses.set([address])

        request = self.factory.get(f'/v1/hcp/{hco.id}/address/{address.id}/')
        force_authenticate(request, user=self.user)
        
        response = get_healthcare_provider_address_by_id(request, hco.id, address.id)
        parsed_response_headers = dict(response.headers)
        parsed_response_data = dict(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(parsed_response_headers.items(), {
            'Content-Type': 'application/json'
        }.items())
        self.assertGreaterEqual(parsed_response_data.items(), {
            'addr1': 'Address 1',
            'city': 'City 1',
            'status': 'A'
        }.items())


class AffiliationCase(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user('user', 'user@gmail.com', 'pwd')

    def test_create_affiliation_with_invalid_parent_child_type_should_fail(self):
        hco = HealthCareOrganization.objects.create(name='hco', status='I')
        with self.assertRaises(ValidationError):
            Affiliation.create(parent_hco_link=hco, child_hco_link=hco, type='HCO_HCP')

    def test_create_affiliation_hco_hcp_has_expected_properties(self):
        hco = HealthCareOrganization.objects.create(name='hco', status='I')
        hcp = HealthCareProvider.objects.create(name='hcp', status='I')

        affiliation = Affiliation.create(child_hcp_link=hcp, parent_hco_link=hco, status='A', type='HCO_HCP')
        
        affiliation_fetched = Affiliation.objects.get(id=affiliation.id)
        
        self.assertEqual(affiliation_fetched.parent_hco_link, hco)
        self.assertEqual(affiliation_fetched.child_hcp_link, hcp)
        self.assertEqual(affiliation_fetched.status, 'A')
        self.assertEqual(affiliation_fetched.type, 'HCO_HCP')

    def test_endpoint_admin_get_all_affiliation_should_return_expected_result(self):
        hco = HealthCareOrganization.objects.create(name='hco', status='I')
        hcp = HealthCareProvider.objects.create(name='hcp', status='I')
        hcp2 = HealthCareProvider.objects.create(name='hcp', status='I')

        affiliation1 = Affiliation.create(parent_hcp_link=hcp, child_hco_link=hco, status='A', type='HCP_HCO')
        affiliation2 = Affiliation.create(child_hcp_link=hcp, parent_hco_link=hco, status='A', type='HCO_HCP')
        affiliation3 = Affiliation.create(parent_hcp_link=hcp, child_hcp_link=hcp2, status='A', type='HCP_HCP')

        request = self.factory.get('/v1/admin/affiliation/')
        force_authenticate(request, user=self.user)
        
        response = get_all_affiliations(request)
        parsed_response_headers = dict(response.headers)
        parsed_response_data = dict(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(parsed_response_headers.items(), {
            'Content-Type': 'application/json'
        }.items())
        self.assertGreaterEqual(parsed_response_data.items(), {
            'count': 3,
            'previous': None,
            'next': None,
        }.items())
        parsed_result_items = dict(parsed_response_data['results'][0])
        self.assertGreaterEqual(parsed_result_items.items(), {
            'id': affiliation1.id,
            'parent_link': hcp.id,
            'child_link': hco.id,
        }.items())
        parsed_result_items = dict(parsed_response_data['results'][1])
        self.assertGreaterEqual(parsed_result_items.items(), {
            'id': affiliation2.id,
            'parent_link': hco.id,
            'child_link': hcp.id,
        }.items())
        parsed_result_items = dict(parsed_response_data['results'][2])
        self.assertGreaterEqual(parsed_result_items.items(), {
            'id': affiliation3.id,
            'parent_link': hcp.id,
            'child_link': hcp2.id,
        }.items())

    def test_endpoint_get_affiliation_by_id_should_return_expected_result(self):
        hco = HealthCareOrganization.objects.create(name='hco', status='I')
        hcp = HealthCareProvider.objects.create(name='hcp', status='I')

        affiliation = Affiliation.create(parent_hcp_link=hcp, child_hco_link=hco, status='A', type='HCP_HCO')

        request = self.factory.get(f'/v1/affiliation/{affiliation.id}')
        force_authenticate(request, user=self.user)
        
        response = get_affiliation_by_id(request, affiliation.id)
        parsed_response_headers = dict(response.headers)
        parsed_response_data = dict(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(parsed_response_headers.items(), {
            'Content-Type': 'application/json'
        }.items())
        self.assertGreaterEqual(parsed_response_data.items(), {
            'id': affiliation.id,
            'parent_link': hcp.id,
            'child_link': hco.id,
            'status': 'A',
            'type': 'HCP_HCO'
        }.items())
