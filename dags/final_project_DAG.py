
import psycopg2 as db
import datetime as dt
from datetime import datetime
from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
import pandas as pd
from elasticsearch import Elasticsearch
 
def retrievingData():
    '''
    This function connects to a PostgreSQL database, retrieves data from the "finalproject" table,
    and saves it as a CSV file. 
    
    Parameters:
        None

    Returns:
        None

    Usage: 
        retrievingData()
    '''
    # Postgre Connection
    conn_string = "dbname='airflow' host='postgres' user='airflow' password='airflow'"
    conn = db.connect(conn_string) 

    # Retrieve data from table finalproject
    df = pd.read_sql("SELECT * FROM finalproject;", conn)
    conn.close()

    # Save and convert into .csv file
    df.to_csv('/opt/survey_financial_ref_dataset_raw.csv', index=False)
    print("-----Data Saved-----") 

def cleaningData():
    '''
    This function reads a CSV file containing survey data, cleans the column names by
    converting them to lowercase and replacing spaces with underscores, and handling missing values.
    
    Parameters:
        None
    
    Returns:
        None

    Usage: 
        cleaningData()
    '''
    # Read data
    df = pd.read_csv('/opt/airflow/survey_financial_ref_dataset_raw.csv')

    # Remove duplicate
    df = df.drop_duplicates()

    # Remaining columns names
    df.columns = [x.lower().replace(" ", "_") for x in df.columns]

    # Handle missing values by dropping rows with any missing values
    df = df.dropna()

    # Save the cleaned data to a new CSV file
    df.to_csv('/opt/airflow/survey_cleaned_data.csv', index=False)


def postToElasticsearch():
    '''Inserts the cleaned data into Elasticsearch
    
    Parameters:
        None
        
    Returns:
        None

    Usage example:
        insert_data()
    '''
    # Read data
    df = pd.read_csv('/opt/airflow/survey_cleaned_data.csv')

    # Define Elasticsearch
    es = Elasticsearch("http://elasticsearch:9200")
    print(f'Connection status: {es.ping()}')

    for index, row in df.iterrows(): 
        doc = row.to_dict()
        es.index(index='finance_ref', body=doc)

# Define default arguments for the DAG
default_args = { 
    'owner': 'group1',
    'start_date': datetime(2024, 7, 27, 14, 45, 0) - timedelta(hours=7),
    'retries': 1,
    'retry_delay': dt.timedelta(minutes=1),
} 

# Define the DAG with the given name, default arguments, and schedule interval
with DAG('TransformData',
         default_args=default_args,
         schedule_interval='30 6 * * *',
         ) as dag:
        
        # First task : calling 'get_data' function
        retrievingData = PythonOperator(task_id='fetch_from_postgresql',
                                     python_callable=retrievingData)

        # Second task : calling 'clean_data' function
        cleaningData = PythonOperator(task_id='data_cleaning',
                                 python_callable=cleaningData)

        # Third task : calling 'insert_data' function                     
        postToElasticsearch = PythonOperator(task_id='post_to_elasticsearch',
                                          python_callable=postToElasticsearch)

# Set up the task dependencies
retrievingData >> cleaningData >> postToElasticsearch