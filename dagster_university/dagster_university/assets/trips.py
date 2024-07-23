import requests
from . import constants
from dagster import asset 

# comments for myself its been awhile since i python-ed
@asset
def taxi_trips_file() -> None: # type annotation
    '''
        The raw parquet files for the taxi trips dataset. Source from NYC Open Data portal 
    ''' # docstring


    month_to_fetch = '2023-03'
    raw_trips = requests.get(
        f"https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_{month_to_fetch}.parquet" # fstring and http requests
    )

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), 'wb') as output_file: # file io
        output_file.write(raw_trips.content)
