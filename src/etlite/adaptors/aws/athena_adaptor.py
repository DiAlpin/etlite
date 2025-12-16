
import io
import time 

import boto3
import pandas as pd
from botocore.exceptions import ClientError



class AthenaAdaptor:
    env_requirements = ['AWS_SECRET_ACCESS_KEY', 'AWS_ACCESS_KEY_ID']
    
    def __init__(self, database, bucket, env):
        self._database = database
        self._bucket = bucket
        self._resource = boto3.resource('s3',
                                    aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY, 
                                    aws_access_key_id=env.AWS_ACCESS_KEY_ID)
        self._client = boto3.client('athena', 
                                aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY, 
                                aws_access_key_id=env.AWS_ACCESS_KEY_ID)
        self._out_tmp_prefix = f'tmp/{self._database}/'
        self._out_tmp_url = f's3://{self._bucket}/{self._out_tmp_prefix}'
 
    def _send_query_request(self, query: str):
        try:
            response = self._client.start_query_execution(
                QueryString=query,
                QueryExecutionContext={
                    'Database': self._database
                },
                ResultsConfiguration={
                    'OutputLocation': self._out_tmp_url
                }
            )
            return response['QueryExecutionId']
        except Exception as e:
            raise RuntimeError(f'An unexpected error occurred while sending query {query} \nerror: {e}')
    
    def _delete_output_data(self, key):
        for suf in ['', '.metadata']:
            try:
                _key = f'{key}{suf}'
                self._resource.Object(self._bucket, _key).delete()
            except Exception as e:
                print(f'Warning: Failed to delete query output data from s3: {_key}\n Error: {e}')
    
    def _retrieve_query_data(self, query_id):
        key = f'{self._out_tmp_prefix}{query_id}.csv'
        
        try:
            obj = self._resource.Object(self._bucket, key)
            body_obj = obj.get()['Body'].read()
            df = pd.read_csv(io.BytesIO(body_obj), encoding='utf8')
            
        except ClientError as ce:
            raise RuntimeError(f'Filed to read query output file {key} due to client error: {ce}')
        except Exception as e:
            raise RuntimeError(f'An unexpected error occurred while reading output file {key} \nerror: {e}')   

        self._delete_output_data(key)
        return df

    def _get_query_status(self, query_id):
        return self._client.get_query_execution(
            QueryExecutionId=query_id
        )['QueryExecution']['Status']['State']
    
    def run_query(self, query):
        qid = self._send_query_request(query)
        
        try:
            qstat = 'QUEUED'
            while qstat in ['QUEUED', 'RUNNING']:
                qstat = self._get_query_status(qid)
                
                if qstat == 'FAILED':
                    raise RuntimeError(f'Athena query {qid} failed \n{query}')
                elif qstat == 'CANCELED':
                    raise RuntimeError(f'Athena query {qid} was canceled\n {query}')
                else:
                    time.sleep(1)
                    
            return self._retrieve_query_data(qid)
        
        except Exception as e:
            raise RuntimeError(f'An unexpected error occurred while executing query {query} \nerror: {e}')
