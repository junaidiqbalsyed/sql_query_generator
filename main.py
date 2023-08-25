import langchain
from langchain.chat_models import ChatOpenAI
import warnings
warnings.filterwarnings('ignore')
from api_key import openai_aip_return_key
import os
os.environ["OPENAI_API_KEY"] =  openai_aip_return_key()
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "./secondpproject-ddd0394b4352.json"
from databse.sql_connection import my_sql, pg_sql
from databse.base import SQLDatabase
from root.sql_query_generator import  Sql_Query_Generator
from databse.bigquery_schema_generator import generate_schema
import json
from pathlib import Path



def generate_query(input_type,
                   file_path = "schemas/secondpproject_target.json",
                   username="root",
                    password = "15021996",
                    host = "localhost",
                    port = "3306",
                    database_name = "classicmodels"
                   ):

    llm = ChatOpenAI(model = 'gpt-4')

    if input_type == 'upload_schema':
        schema = json.loads(Path(file_path).read_text())
    else:
        # for pg sql
        engine = pg_sql(username, password, host, port, database_name)

        # for my sql
        #engine = my_sql( username, password, host, port, database_name )

        db = SQLDatabase(engine = engine)
        schema = db.get_table_info()

    gen = Sql_Query_Generator(llm= llm)
    task = input("enter the question you want to ask ")
    sql_language = input('in which language you want to generate the query ')
    gen.execute_task(task= task, schema = schema, sql_language = sql_language)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # generate schema for big query
    #generate_schema(project_id='secondpproject', database_id='target')

    input_type = input('how do you want to generate your query ')
    generate_query(input_type = input_type)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
