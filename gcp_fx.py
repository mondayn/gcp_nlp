import pydata_google_auth
import pandas_gbq
import pandas as pd
import yaml
from google.cloud import bigquery

##### gcp vars ##########

CREDENTIALS = pydata_google_auth.get_user_credentials('https://www.googleapis.com/auth/cloud-platform')

with open('settings.yaml', 'r') as file:
    PROJECT_ID = yaml.load(file, Loader=yaml.FullLoader)['projectid']



def print_meta_data(_df):
    ''' helper fx
    '''
    print('shape =',_df.shape)
    print('columns = ',list(_df.columns))
    return _df


def query_bq(sql):

    gbq_params = {
        'query':sql
        ,'project_id': PROJECT_ID
        ,'credentials': CREDENTIALS
    }
    # print(f'gbq_params={gbq_params}')
    return (
        pd.read_gbq(**gbq_params)
        .pipe(print_meta_data)
    )


# from google.cloud.exceptions import NotFound

def delete_bq_table(dataset_name, table_name):
    client = bigquery.Client(PROJECT_ID,CREDENTIALS)
    table_id = f'{dataset_name}.{table_name}'
    client.delete_table(table_id, not_found_ok=True) 
    print("Deleted table '{}'.".format(table_id))