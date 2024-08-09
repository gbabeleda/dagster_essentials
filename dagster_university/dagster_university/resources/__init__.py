from dagster_duckdb import DuckDBResource
from dagster import EnvVar

database_resource = DuckDBResource(
    # hardcoded path replaced with environment variable
    database = EnvVar("DUCKDB_DATABASE") 
    # database="data/staging/data.duckdb" 
)