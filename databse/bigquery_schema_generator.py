

from google.cloud import bigquery
from sqlalchemy import create_engine, MetaData, Table, Column, String, Integer
from google.cloud import bigquery

# Replace with your own credentials
# You can also set up Application Default Credentials or use environment variables


def generate_schema(project_id = None, database_id = None):

    client = bigquery.Client()

    # Set up the SQLAlchemy engine
    engine = create_engine(f"bigquery://{project_id}/{database_id}")

    metadata = MetaData()
    metadata.reflect(bind=engine)

    # Extract tables, columns, and relationships for this database
    tables = {}

    for table in metadata.sorted_tables:
        table_info = {
            "columns": [col.name for col in table.columns],
            "foreign_keys": [fk.column.name for fk in table.foreign_keys],
            "primary_key": [col.name for col in table.primary_key]
        }
        tables[table.name] = table_info

    # Store the schema information for this database
    erd_json = {"tables": tables}

    # Convert to JSON and save to a file
    with open(f'./schemas/{project_id}_{database_id}.json', 'w') as json_file:
        import json
        json.dump(erd_json, json_file, indent=4)

    print("generated schema")








