# Learning Log

Comfortable with unix-based systems when coding, so setup WSL2 on my personal machine, using Ubuntu cos im basic


## 2: Prerequisite and Setup 
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


## 3: Software-defined assets

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

## 4: Asset Dependencies
An asset can have upstream or downstream dependencies

Example: 
```
@asset(
    deps = ['upstream_asset_a', 'upstream_asset_b']
)
def some_function():
```

Notes: 
- dependencies can be implicit (asset was used as inputs for another asset) or explicit (asset dependencies were define using the )
- The deps argument for the asset decorator is essentially just the `ref` function in dbt
- Best practices for asset organization includes separating assets into different files by their role/purpose (ETL vs Analysis)
- Did a little load into a duckdb databaes from a file. Apparently thats a thing. Wonder how that works with postgres/the other databases/data warehouses

## 5: Definitions & Code Locations

A `Definitions` object is located in the top-level `__init__.py` in a dagster project. It is where you tell Dagster where to find your "definitions" for that particular Dagster Project. A definition is stuff like `assets`, which we have gone over, as well as other stuff like `resources`, `schedules`, and `sensors`.

Its essentially the central configuration point of the entire dagster project

Example:

```
defs = Definitions(
    assets = [asset_1, *group_of_assets],
    schedules = [some_schedule],
    sensors = [some_sensor],
    jobs = [some_job],
    resources = {
        "some_resource" : some_resource
    }
)
```

This Definitions object maps to a code location. TLDR: 1:1 Definitions Object: Code Location. 

The purpose of the code location(s) is that multiple Dagster projects can be isolated from each other without requiring multiple deployments. 

What the hell does multiple deployments mean?

What worked for me to understand what that is: 
- You have multiple teams managing their own Dagster projects. Or even the same team managing Dagster projects representing different aspects of the business whether that be different sections of a pipeline (ETL vs ML Ops), different departments, etc
- If we do it in different repos its a pain in the ass to make sure they adhere to everything you want
- If you want to make them all into one repository, having multiple code locations means that if you make a change to one you dont need downtime on the others

Notes:

`__init__.py` serves several purposes in Python:
- It indicates that the directory it is present in should be treated as a Python package
- It can be used to initialize package-level data
- It can be used to import specific functions or classes to make them easily accessible when the package is imported

## 6: Resources

Dagsters goal is to be a single pane of glass. Thus, it needs to know about services and systems used in the data pipelines, like cloud storage or a data warehouse







## Random Notes

Imperative vs Declarative
- dagster, sql is declarative. you tell what the final output is
- imperative you tell it what to do