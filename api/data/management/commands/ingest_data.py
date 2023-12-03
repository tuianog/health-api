import json
from django.core.management.base import BaseCommand
from data.models import Address, HealthCareProvider, HealthCareOrganization, Affiliation

# docs: https://docs.djangoproject.com/en/4.2/howto/custom-management-commands/

# to run: python3 manage.py ingest_data --hco '../config/hco.json' --hcp '../config/hcp.json' --address '../config/addresses.json' --affiliation '../config/affiliations.json'

class Command(BaseCommand):
    help = "Ingest example data"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_processor = DataProcessor()

    def add_arguments(self, parser):
        parser.add_argument("--address", dest="address", type=str, required=False, default=None)
        parser.add_argument("--hco", dest="hco", type=str, required=False, default=None)
        parser.add_argument("--hcp", dest="hcp", type=str, required=False, default=None)
        parser.add_argument("--affiliation", dest="affiliation", type=str, required=False, default=None)

    def handle(self, *args, **options):
        filenames_args = {
            'address': options.get('address'), 
            'hco': options.get('hco'), 
            'hcp': options.get('hcp'),
            'affiliation': options.get('affiliation')
        }
        data = self.data_processor.read_data_files(filenames_args)

        self.stdout.write(
            self.style.SUCCESS('Successfully read input files')
        )

        self.data_processor.save_entities(data)
        
        report = {
            'address': len(data.get('address')),
            'hcp': len(data.get('hcp')),
            'hco': len(data.get('hco')),
            'affiliation': len(data.get('affiliation'))
        }
        self.stdout.write(
            self.style.SUCCESS('Finished ingesting sample data')
        )
        self.stdout.write(
            self.style.SUCCESS(f'Report: {report}')
        )


class DataProcessor:

    def read_data_files(self, filenames):
        data = {}
        for entity, filename in filenames.items():
            if filename:
                with open(filename) as file:
                    data[entity] = json.load(file)
        return data
    
    def save_entities(self, data):
        address_entities = list(map(self.save_address, data.get('address', [])))
        hco_entities = list(map(self.save_hco, data.get('hco', [])))
        hcp_entities = list(map(self.save_hcp, data.get('hcp', [])))
        
        self.handle_address_relations(address_entities, hco_entities, hcp_entities)
        self.handle_affiliations(data.get('affiliation', []), hco_entities, hcp_entities)
        
    def save_address(self, address):
        address_entity = Address(**DataProcessor.map_address(address))
        address_entity.save()
        return address_entity
    
    def save_hco(self, organization):
        organization_entity = HealthCareOrganization(**DataProcessor.map_hco(organization))
        organization_entity.save()
        return organization_entity
    
    def save_hcp(self, provider):
        provider_entity = HealthCareProvider(**DataProcessor.map_hcp(provider))
        provider_entity.save()
        return provider_entity
    
    def save_affiliation(self, affiliation, hco_entity, hcp_entity):
        affiliation_entity = Affiliation(**DataProcessor.map_affiliation(affiliation, hco_entity, hcp_entity))
        affiliation_entity.save()
        return affiliation_entity

    def handle_address_relations(self, address_entities, hco_entities, hcp_entities):
        address_hco_counter, address_hcp_counter = 0, 0
        # use positions to determine which hco/hcp, since parent_link IDs from input are disregarded
        for address in address_entities:
            match address.parent_type:
                case 'HCO':
                    if len(hco_entities) >= address_hco_counter+1:
                        hco = hco_entities[address_hco_counter]
                        hco.addresses.set([address])
                        hco.save()
                    address_hco_counter += 1
                case 'HCP':
                    if len(hcp_entities) >= address_hcp_counter+1:
                        hcp = hcp_entities[address_hcp_counter]
                        hcp.addresses.set([address])
                        hcp.save()
                    address_hcp_counter += 1

    def handle_affiliations(self, affiliations, hco_entities, hcp_entities):
        # use parent/child link IDs from input data to determine which hco/hcp positions
        for affiliation in affiliations:
            match affiliation['type']:
                case 'HCP_HCO':
                    hcp_link = hcp_entities[affiliation['parent_link']-1]
                    hco_link = hco_entities[affiliation['child_link']-1]
                    self.save_affiliation(affiliation, hco_link, hcp_link)
                case 'HCO_HCP':
                    hcp_link = hcp_entities[affiliation['child_link']-1]
                    hco_link = hco_entities[affiliation['parent_link']-1]
                    self.save_affiliation(affiliation, hco_link, hcp_link)
                    
    @staticmethod
    def map_address(address_entity):
        return {
            'parent_type': address_entity['parent_type'],
            'addr1': address_entity['addr1'],
            'addr2': address_entity.get('addr2'),
            'city': address_entity['city'],
            'state': address_entity['state'],
            'zip': address_entity['zip'],
            'status': address_entity['status'],
        }
    
    @staticmethod
    def map_hco(organization_entity):
        return {
            'name': organization_entity['name'],
            'status': organization_entity['status'],
        }
    
    @staticmethod
    def map_hcp(provider_entity):
        return {
            'name': provider_entity['name'],
            'status': provider_entity['status'],
        }
    
    @staticmethod
    def map_affiliation(affiliation_entity, hco_entity, hcp_entity):
        return {
            'type': affiliation_entity['type'],
            'status': affiliation_entity['status'],
            'hcp_link': hcp_entity,
            'hco_link': hco_entity
        }
