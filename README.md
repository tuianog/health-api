
# health-api

## Description

This POC project is a simple REST API implemented using Python and Django Rest framework for a healthcare example use case. Deployment using Docker containers and PostgreSQL database (pgAdmin also used for management).

### Data model

Entities:

- Healthcare Provider (hcp)
- Healthcare Organization (hco)
- Address
- Affiliation

![ERD diagram](/config/health-api-erd-diagram.png)

</details>


### API Specification

- POST `v1/auth/` - Authenticate and retrieve login token
  - Request payload example:
  ```json
  {
    "username": "user",
    "password": "pwd"
  }
  ```
- GET `v1/admin/hco/` - GET all Healthcare Organizations using pagination
    - filter query params:
      - `status`: filter by `A` || `I`, optional, default = `A` (`ACTIVE` || `INACTIVE`)
    - endpoints include pagination query params:
      - `limit`: natural positive number for the max amount of items returned per request
      - `offset`: natural number for the starting position of the page
- GET `v1/admin/hcp/` - GET all Healthcare Providers using pagination
    - filter query params:
      - `status`: filter by `A` || `I`, optional, default = `A` (`ACTIVE` || `INACTIVE`)
    - endpoints include pagination query params:
      - `limit`: natural positive number for the max amount of items returned per request
      - `offset`: natural number for the starting position of the page
- GET `v1/admin/address/` - GET all Addresses using pagination
    - filter query params:
      - `status`: filter by `A` || `I`, optional, default = `A` (`ACTIVE` || `INACTIVE`)
      - `type`: filter by parent type, optional, values = `HCP`, `HCO`
    - endpoints include pagination query params:
      - `limit`: natural positive number for the max amount of items returned per request
      - `offset`: natural number for the starting position of the page
- GET `v1/admin/affiliation/` - GET all Affiliations using pagination
    - filter query params:
      - `status`: filter by `A` || `I`, optional, default = `A` (`ACTIVE` || `INACTIVE`)
      - `type`: filter by parent type, optional, values = `HCP_HCO`, `HCO_HCP`
    - endpoints include pagination query params:
      - `limit`: natural positive number for the max amount of items returned per request
      - `offset`: natural number for the starting position of the page
- GET `v1/hco/{id}/` - Get Healthcare Organization by ID
- GET `v1/hco/{id}/address/` - Get Healthcare Organization addresses by ID
    - endpoints include pagination query params:
      - `limit`: natural positive number for the max amount of items returned per request
      - `offset`: natural number for the starting position of the page
- GET `v1/hco/{id}/address/{addressId}/` - Get Address from Healthcare Organization by ID
- GET `v1/hco/{id}/affiliation/` - Get Healthcare Organization affiliations by ID
    - endpoints include pagination query params:
      - `limit`: natural positive number for the max amount of items returned per request
      - `offset`: natural number for the starting position of the page
- GET `v1/hcp/{id}/` - Get Healthcare Provider by ID
- GET `v1/hcp/{id}/address/` - Get Healthcare Provider adresses by ID
    - endpoints include pagination query params:
      - `limit`: natural positive number for the max amount of items returned per request
      - `offset`: natural number for the starting position of the page
- GET `v1/hcp/{id}/address/{addressId}/` - Get Address from Healthcare Provider by ID
- GET `v1/hcp/{id}/affiliation/` - Get Healthcare Provider affiliations by ID
    - endpoints include pagination query params:
      - `limit`: natural positive number for the max amount of items returned per request
      - `offset`: natural number for the starting position of the page


Note*: all endpoints listed above (except the authenticate) are configured to require authentication (based on Token authentication header or Session CSRF token).

### Package & Deploy

Pre-requirements for local development:
1. virtual env
> python3 -m venv .env

> source .env/bin/activate

> pip3 install -r requirements.txt


Deployment:

Using docker containers for only database:
> docker-compose up

Using docker containers for both server and database:
> docker-compose up --profile dev

Using standalone server:
> docker build -t api-django .
 
> docker run -p 8082:8080 api-django

### Ingesting sample data

There is a custom command to ingest sample data from input files.

Example:
> python3 manage.py ingest_data --hco '../config/hco.json' --hcp '../config/hcp.json' --address '../config/addresses.json' --affiliation '../config/affiliations.json'


### Testing

There are several integration tests implemented to test entities creation and endpoint responses.

To run tests:
> python3 manage.py test

### Useful commands

1. Manage database
> python3 manage.py makemigrations

> python3 manage.py migrate

2. create admin user
> python manage.py createsuperuser

3. Run server: 
> python3 manage.py runserver

4. Access database using psql client:
> psql -h localhost -d dev -U username -W

5. Recreate data tables:
> python manage.py migrate --fake data zero
> python manage.py migrate data


6. Generate OpenAPI specification file:
> python3 manage.py spectacular --color --file config/api-spec.yml


#### Curl examples

Authenticate and retrieve token:
> curl -d '{"username":"username", "password":"PWD" }' -H "Content-Type: application/json" -X POST http://localhost:8000/api/v1/auth/

Admin endpoint Get all HCO entries: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/admin/hco/

Admin endpoint Get all HCP entries: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/admin/hcp/

Admin endpoint Get all Addresses entries: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/admin/address/

Admin endpoint Get all Affiliations entries: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/admin/affiliation/

Endpoint Get Healthcare Organization by ID: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/hco/{id}/

Endpoint Get Healthcare Organization addresses by HCO ID: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/hco/{id}/address/

Endpoint Get Healthcare Organization address by HCO ID and address ID: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/hco/{id}/address/{addressId}/

Endpoint Get Healthcare Organization affiliations by HCO ID: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/hco/{id}/affiliation/

Endpoint Get Healthcare Provider by ID: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/hcp/{id}/

Endpoint Get Healthcare Provider addresses by HCP ID: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/hcp/{id}/address/

Endpoint Get Healthcare Provider address by HCP ID and address ID: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/hcp/{id}/address/{addressId}/

Endpoint Get Healthcare Provider affiliations by HCO ID: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/hcp/{id}/affiliation/

Endpoint Get Affiliation by ID: 
> curl -H "Authorization: Token token" -H "Content-Type: application/json"  -X GET http://localhost:8000/api/v1/affiliation/{id}/
