### Learning Log

Comfortable with unix-based systems when coding, so setup WSL2 on my personal machine, using Ubuntu cos im basic

Installed python3 and pip on the Ubuntu VM

```
sudo apt update
sudo apt install python3.10
sudo apt install python3-pip
```

Setup a directory for dagster essentials
Initialized git for directory probably through the vscode UI
Published repository to github using vscode UI 


Setup a virtual environment, in line with python best practices (apparently) using venv

```
python -m venv de_venv
source de_venv/bin/activate
```

Created requirements.txt file, apparently not in vogue accdg to dagster but ill take it for now

```
pip install -r requirements.txt
```

Downloaded the dagster_university project/directory/whatever using the command below and followed the instructions to setup the .env file and install the dagster dev thing in editable mode (?) dunno what that means yet

```
dagster project from-example --example project_dagster_university_start --name dagster_university
cd dagster_university
cp .env.example .env
pip install -e ".[dev]"
```

Ran the dagster app/webserver/whatever `dagster dev`

Notes from the terminal logs:
- dagster dev loads the environment variables from the .env file
- for persistent infromation across sessions, set environment variable DAGSTER_HOME to a directory


Moved on to Lesson 3: Software-defined assets

Dagster Software-Defined Asset (DSA) 
- asset decorator: a function decorator REVIEW THIS
- asset key: aka the function name, can have prefixes 
- upstream asset dependencies: references using asset keys, essentially just the inputs to the python function
- python function: defines how the asset is computed

```
@asset
def cookie_dough(dry_ingredients, wet_ingredients):
    return dry_ingredients + wet_ingredients
```

Defined my first asset. Looks like the E part of ELT. 

After defining the asset in code, you need to materialize it to run the assets function and creates the asset by persisting results in storage

Okay so lesson 3 tldr. 
- how to define an asset.
- what are the componenets of an asset
- how to materialize an asset thru dagster ui
- dagster run ui
- made two assets taxi_trips_file.parquet and taxi_zones_file.csv

Lesson 4: dependencies
- downstream vs upstream

Did a little load into a duckdb databaes from a file. Apparently thats a thing. Wonder how that works with postgres/the other databases/data warehouses

The deps argument(?) to the @asset decorator is just the _ref function in dbt

Asset organization tip: separate assets into diff files by their purpose. i.e. put analysis-focused assets in a different file the assets that ingest data

I made a mapppp

The analytic assets in the metrics.py is essentially transform components. 

Were moving on to definition objects

