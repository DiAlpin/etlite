
from typing import Literal

import pandas as pd
import pyarrow as pa
from pydantic import BaseModel, Field, PositiveInt

from etlite.registry import register
from etlite.adaptors.aws import S3Adaptor



class S3ExtractorModel(BaseModel):
    extractor_name: Literal['S3Extractor'] = Field(
        default='S3Extractor'
    )
    bucket: str
    file_key: str
    delimiter: str | None = None
    skiprows: PositiveInt | None = None



@register('extractor', S3ExtractorModel, env_requirements=S3Adaptor.env_requirements)
class S3Extractor:
    def __init__(self, config: dict):
        self._adaptor = S3Adaptor(
            bucket=config['bucket']
        )
        self._file_key = config['file_key']
        self._extension = self._file_key.rsplit('.', 1)[1].lower()
        self._delimiter = config.get('delimiter', None)
        self._skiprows = config.get('skiprows', None)

    def __call__(self) -> pa.Table:
        obj = self._adaptor.read_obj(self._file_key)
        
        if self._extension == 'csv':
            df = pd.read_csv(obj, delimiter=self._delimiter, skiprows=self._skiprows)
        elif self._extension == 'parquet':
            df = pd.read_parquet(obj, engine='fastparquet')
        else:
            raise RuntimeError(f'Unknown extension: {self._extension}')
        
        return pa.Table.from_pandas(df)
