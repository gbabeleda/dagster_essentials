import requests
from . import constants
from dagster import asset 

# comments for myself its been awhile since i python-ed
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
        output_file.write(raw_trips.content)
