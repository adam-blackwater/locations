## What is implemented
A very simple ETL (extract, transform, load) pipeline that ingests the data form JSON files. Features of the ETL are:
- reading data from JSON files
- transforming the data into ETL models
- calculating `max_electric_power` from volts, amps and phase where `max_electric_power` isn't already present
- modifying the data into Database models ready to be persisted
- when run multiple times an attempt has been made to merge new locations with existing ones based on their coordinates
 
An HTTP API for surfacing the data:
- models are retrieved from the database and parsed into API response objects
- filtering
- ordering

Some basic geo-spacial calculations: 
- finding closest locations using the coordinates of a 
  
## How to use
All the Makefile commands below should be run from the root of the project. If you are using Linux or MacOS make should already be installed.

There is a .env.example that you can use to set some environment variables

### Installing packages
Packages are managed with UV by Astral. Running `make install` will add all the packages need.

### Starting the database
Running `make db_up` will create a new Postgres container with docker compose.

It will create a Docker volume were the data will be stored

### Running the ETL
The data is read into the system by starting the ETL with `make run_etl`.

There is a default value for the `integrated.json` data if you have not set the environment variable for the file location.

### Running the application
To start the application use `make run_app` this starts the application on port 8000

### Executing the tests
Running `make test` starts the tests

## Endpoints
### Single Location
To access a single location use the endpoint http://localhost:8000/api/locations

Locations can be filtered and ordered in the following ways
- distance (order)
- last_updated (order)
- country (filter)
- operator (filter)
- lat/lon (order)

And any combination of ordering/filtering can be used for different results.

### Multiple Locations
To access a single location use the endpoint [http://localhost:8000/api/locations/{location_reference}](http://localhost:8000/api/locations/%7Blocation_reference%7D)

Where \`{location_reference}\` is a placeholder for an ID that references a location.

## Themes
- ETL
- RESTful
- seperation of models. DB models, ETL models and API models

## Libraries
- FastAPI
- geopy
- Pydantic
- SQLAlchemy

## Tools
  - uv
  - ruff
  - ty

## Notes
I haven't used Python in a while so I'm getting used to setting up my environment again.

Extracte the individual items in integrated.json using Pydantics JSON parser.

Using Pydantic validators to mutate types as described in the link below.  
https://docs.pydantic.dev/latest/concepts/validators/

https://docs.pydantic.dev/latest/examples/files/#json-data

https://docs.pydantic.dev/latest/examples/orms/#sqlalchemy

A software concept I'm using is described in the link below.  
https://matklad.github.io/2023/11/15/push-ifs-up-and-fors-down.html

I'm assuming the location added date would be the first time an EVSE was added

Not sure if I should get detailed view on the "name" or "reference" of a  
location. I went with reference

There is something called FastAPI Admin which is similar to Django Admin. But I'm not going to implement it because I don't have the time.

### Improvements
- use FastAPI-Admin for the web pages to manage database models
- make the ETL auto fetch new data
	- cron job
	- serverless functions
	- pulling from queues
- database migrations
- attach object storage for the images
- stop the database tables having duplicates
- could move to postGIS but seems overkill for this application
    - geopy is easy to use but its not been updated in two years
- reduce the time complexity cost of comparing the locations for new data
    - currently O(nxm) I think
- containerise the application
