from django.http import Http404
from rest_framework.pagination import LimitOffsetPagination
from .models import Address, HealthCareProvider, HealthCareOrganization, Affiliation
from .serializers import AddressSerializer, HealthCareProviderSerializer, HealthCareOrganizationSerializer, HealthCareOrganizationAddressesSerializer, HealthCareProviderAddressesSerializer, AffiliationSerializer
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

RESPONSE_HEADERS = {
    'Content-Type': 'application/json'
}

def build_return_response(response: Response) -> Response:
    response.headers = {
        **response.headers,
        **RESPONSE_HEADERS
    }
    return response


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_providers(request):
    # get optinal status from query param, default ACTIVE
    status_filter = request.GET.get('status', 'A')

    query_set = HealthCareProvider.objects.filter(status=status_filter)
    paginator = LimitOffsetPagination()
    data = paginator.paginate_queryset(query_set, request)
    
    serializer = HealthCareProviderSerializer(data, many=True)
    paginated_data = paginator.get_paginated_response(serializer.data)
    
    return build_return_response(paginated_data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_organizations(request):
    # get optinal status from query param, default ACTIVE
    status_filter = request.GET.get('status', 'A')

    query_set = HealthCareOrganization.objects.filter(status=status_filter)
    paginator = LimitOffsetPagination()
    data = paginator.paginate_queryset(query_set, request)
    
    serializer = HealthCareOrganizationSerializer(data, many=True)
    paginated_data = paginator.get_paginated_response(serializer.data)
    
    return build_return_response(paginated_data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_addresses(request):
    # get optinal status from query param, default ACTIVE
    filter_params = {}
    filter_params['status'] = request.GET.get('status', 'A')
    type_filter = request.GET.get('type')
    if type_filter:
        filter_params['parent_type'] = type_filter
    
    query_set = Address.objects.filter(**filter_params)
    paginator = LimitOffsetPagination()
    data = paginator.paginate_queryset(query_set, request)
    
    serializer = AddressSerializer(data, many=True)
    paginated_data = paginator.get_paginated_response(serializer.data)
    
    return build_return_response(paginated_data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_all_affiliations(request):
    # get optinal status from query param, default ACTIVE
    filter_params = {}
    filter_params['status'] = request.GET.get('status', 'A')
    type_filter = request.GET.get('type')
    if type_filter:
        filter_params['type'] = type_filter
    
    query_set = Affiliation.objects.filter(**filter_params)

    paginator = LimitOffsetPagination()
    data = paginator.paginate_queryset(query_set, request)
    
    serializer = AffiliationSerializer(data, many=True)
    paginated_data = paginator.get_paginated_response(serializer.data)
    
    return build_return_response(paginated_data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_healthcare_organization_by_id(request, organization_id):
    query_set = HealthCareOrganization.objects.filter(id=organization_id)
    
    response = HealthCareOrganizationSerializer(query_set, many=True)
    if not len(response.data):
        raise Http404("Healthcare organization does not exist")
    
    return Response(response.data[0], status=200, headers=RESPONSE_HEADERS)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_affiliation_by_id(request, affiliation_id):
    query_set = Affiliation.objects.filter(id=affiliation_id)
    
    response = AffiliationSerializer(query_set, many=True)
    if not len(response.data):
        raise Http404("Affiliation does not exist")
    
    return Response(response.data[0], status=200, headers=RESPONSE_HEADERS)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_healthcare_addresses_by_organization_by_id(request, organization_id):
    query_set = HealthCareOrganization.objects.filter(id=organization_id)
    
    paginator = LimitOffsetPagination()
    data = paginator.paginate_queryset(query_set, request)

    serializer = HealthCareOrganizationAddressesSerializer(data, many=True)
    if not len(serializer.data):
        raise Http404("Heathcare organization addresses do not exist")

    mapped_data = list(map(lambda x: x['addresses'], serializer.data)) 

    paginated_data = paginator.get_paginated_response(mapped_data[0])
    return build_return_response(paginated_data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_healthcare_provider_by_id(request, provider_id):
    query_set = HealthCareProvider.objects.filter(id=provider_id)
    
    response = HealthCareProviderSerializer(query_set, many=True)
    if not len(response.data):
        raise Http404("Heathcare provider does not exist")
    
    return Response(response.data[0], status=200, headers=RESPONSE_HEADERS)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_healthcare_addresses_by_provider_by_id(request, provider_id):
    query_set = HealthCareProvider.objects.filter(id=provider_id)

    paginator = LimitOffsetPagination()
    data = paginator.paginate_queryset(query_set, request)
    
    serializer = HealthCareProviderAddressesSerializer(data, many=True)
    if not len(serializer.data):
        raise Http404("Healthcare addresses do not exist")

    mapped_data = list(map(lambda x: x['addresses'], serializer.data)) 

    paginated_data = paginator.get_paginated_response(mapped_data[0])
    return build_return_response(paginated_data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_healthcare_organization_address_by_id(request, organization_id, address_id):
    query_set = HealthCareOrganization.objects.filter(id=organization_id, addresses=address_id)
    
    serializer = HealthCareOrganizationAddressesSerializer(query_set, many=True)
    if not len(serializer.data) or not len(serializer.data[0]['addresses']):
        raise Http404("Healthcare organization address does not exist")
    address = serializer.data[0]['addresses'][0]

    return Response(address, status=200, headers=RESPONSE_HEADERS)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_healthcare_provider_address_by_id(request, provider_id, address_id):
    query_set = HealthCareProvider.objects.filter(id=provider_id, addresses=address_id)
    
    serializer = HealthCareProviderAddressesSerializer(query_set, many=True)
    if not len(serializer.data) or not len(serializer.data[0]['addresses']):
        raise Http404("Healthcare provider address does not exist")
    address = serializer.data[0]['addresses'][0]

    return Response(address, status=200, headers=RESPONSE_HEADERS)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_healthcare_provider_affiliations(request, provider_id):
    query_set = HealthCareProvider.objects.filter(id=provider_id)
    response = HealthCareProviderSerializer(query_set, many=True)
    if not len(response.data):
        raise Http404("Heathcare provider does not exist")

    hcp = dict(response.data[0])
    query_set = Affiliation.objects.filter(Q(parent_hcp_link__id=hcp['id']) | Q(child_hcp_link__id=hcp['id']))

    paginator = LimitOffsetPagination()
    data = paginator.paginate_queryset(query_set, request)
    
    serializer = AffiliationSerializer(data, many=True)
    paginated_data = paginator.get_paginated_response(serializer.data)
    
    return build_return_response(paginated_data)


@api_view(['GET'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def get_healthcare_organization_affiliations(request, organization_id):
    query_set = HealthCareOrganization.objects.filter(id=organization_id)
    response = HealthCareOrganizationSerializer(query_set, many=True)
    if not len(response.data):
        raise Http404("Heathcare organization does not exist")

    hco = dict(response.data[0])
    query_set = Affiliation.objects.filter(Q(parent_hco_link__id=hco['id']) | Q(child_hco_link__id=hco['id']))

    paginator = LimitOffsetPagination()
    data = paginator.paginate_queryset(query_set, request)
    
    serializer = AffiliationSerializer(data, many=True)
    paginated_data = paginator.get_paginated_response(serializer.data)
    
    return build_return_response(paginated_data)
