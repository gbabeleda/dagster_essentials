import requests
from dagster_duckdb import DuckDBResource # new import after resource definition
from . import constants
from dagster import asset 
# import duckdb
# import os

# comments for myself its been awhile since i python-ed

# This corresponds to Extract
@asset
def taxi_trips_file() -> None: # type annotation
    # docstring
    # displays in the asset description in the global asset lineage
    '''
        The raw parquet files for the taxi trips dataset. Source from NYC Open Data portal 
    ''' 


    month_to_fetch = '2023-03'

    # fstring and http requests
    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet" 
    )

    # file io
    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), 'wb') as output_file: 
        output_file.write(raw_trips.content) # parquet

@asset
def taxi_zones_file() -> None:
    '''
        The raw CSV file for the taxi zones dataset. Sourced from the NYC Open Data portal.
    '''

    raw_zones = requests.get(
        'https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD'
    )

    with open(constants.TAXI_ZONES_FILE_PATH, 'wb') as output_file:
        output_file.write(raw_zones.content) # csv



# This corresponds to Load in ETL
@asset(
    deps=['taxi_trips_file'] # this is essentially dbt ref() function 
)
def taxi_trips(database: DuckDBResource) -> None: #
    '''
        The raw taxi trips dataset, loaded into a DuckDB database
    '''

    sql_query = '''
        create or replace table trips as (
            select

                VendorID as vendor_id,
                PULocationID as pickup_zone_id,
                DOLocationID as dropoff_zone_id,
                RatecodeID as rate_code_id,
                payment_type as payment_type,
                tpep_dropoff_datetime as dropoff_datetime,
                tpep_pickup_datetime as pickup_datetime,
                trip_distance as trip_distance,
                passenger_count as passenger_count,
                total_amount as total_amount

            from 'data/raw/taxi_trips_2023-03.parquet'        
        
        );
    ''' # apparently duck db allows for directly querying from a file 

    # connection old
    # conn = duckdb.connect(os.getenv("DUCKDB_DATABASE")) 
    # conn.execute(sql_query)

    # connection new, uses with syntax, envvar, and dagster resources
    # get_connection() is a DuckDBResource method
    with database.get_connection() as conn: 
        conn.execute(sql_query)

@asset(
    deps=['taxi_zones_file']
)
def taxi_zones(database: DuckDBResource) -> None:
    '''
        The taxi zones dataset, loaded into DuckDB
    '''

    sql_query = f'''
        create or replace table zones as (
            select 

                LocationID as zone_id,
                zone,
                borough,
                the_geom as geometry

            from '{constants.TAXI_ZONES_FILE_PATH}'
        
        );
    '''

    with database.get_connection() as conn: 
        conn.execute(sql_query)