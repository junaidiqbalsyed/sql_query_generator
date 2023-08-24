from databse.base import SQLDatabase
from sqlalchemy import create_engine
import  gc

def my_sql(username, password, host, port, database_name):
    """
    This function generates the url for the MySQL database connectivity
    input : details of database
    output : database url
    """

    url = f"mysql+mysqlconnector://{username}:{password}@{host}:{port}/{database_name}"
    engine = create_engine(url= url)

    try:
        SQLDatabase(engine= engine)
    except :
        print("please check your my_sql credentials")

    gc.collect()

    return  engine

def pg_sql(username, password, host, port, database_name):

    url =  f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
    engine = create_engine(url=url)

    try:
        SQLDatabase(engine=engine)
    except:
        print("please check your my_sql credentials")

    gc.collect()

    return engine