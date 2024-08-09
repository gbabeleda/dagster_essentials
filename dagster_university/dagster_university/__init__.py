# fmt: off
from dagster import Definitions, load_assets_from_modules

from .assets import metrics, trips

trip_assets = load_assets_from_modules([trips])
metric_assets = load_assets_from_modules([metrics])

# this can be any variable. It just has to contain the definitions object
# the * is called the unpacking operator. Used to unpack elements of an iterable
# combines all elements from both lists into a single list
defs = Definitions(
    assets=[*trip_assets, *metric_assets] 
)
