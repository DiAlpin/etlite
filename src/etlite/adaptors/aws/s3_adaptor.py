
import io 
from typing import Iterator

import boto3
from botocore.exceptions import ClientError

from etlite.environ import EnvLoader as env



class S3Adaptor:
    env_requirements = ['AWS_SECRET_ACCESS_KEY', 'AWS_ACCESS_KEY_ID']
    
    def __init__(self, bucket):
        self._bucket = bucket
        self._client = boto3.client('s3', 
                aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY, 
                aws_access_key_id=env.AWS_ACCESS_KEY_ID)
        self._resource = boto3.resource('s3',
                aws_secret_access_key=env.AWS_SECRET_ACCESS_KEY, 
                aws_access_key_id=env.AWS_ACCESS_KEY_ID)
    
    @property    
    def domain(self):
        return f's3a://{self._bucket}/'
    
    def read_obj(self, key: str):
        try:
            obj = self._resource.Object(self._bucket, key)
            body_obj = obj.get()['Body'].read()
            return io.BytesIO(body_obj)
        except ClientError as ce:
            raise RuntimeError(f'Filed to read file {key} due to client error: {ce}')
        except Exception as e:
            raise RuntimeError(f'An unexpected error occurred while reading file {key}, error: {e}')
    
    def write_object(self, body_obj: io.BytesIO, key: str):
        try:
            obj = self._resource.Object(self._bucket, key)
            obj.put(Body=body_obj)
        except ClientError as ce:
            raise RuntimeError(f'Filed to write file {key} due to client error: {ce}')
        except Exception as e:
            raise RuntimeError(f'An unexpected error occurred while writing file {key}, error: {e}') 
        
    def iter_object_metadata(self, prefix: str) -> Iterator[dict]:
        paginator = self._client.get_paginator('list_objects')
        pages = paginator.paginate(Bucket=self._bucket, Prefix=prefix)
        
        for page in pages:
            if 'Contents' in page:
                for obj in page['Content']:
                    yield obj
