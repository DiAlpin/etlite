
from typing import Literal
from pathlib import Path

import pandas as pd
import pyarrow as pa
from pydantic import BaseModel, Field, PositiveInt

from etlite.registry import register



class LocalExtractorModel(BaseModel):
    extractor_name: Literal['LocalExtractor'] = Field(
        default='LocalExtractor'
    )
    path: str
    delimiter: str | None = None
    skiprows: PositiveInt | None = None

@register('extractor', LocalExtractorModel)
class LocalExtractor:
    def __init__(self, config: dict):
        self._path = config['path']
        self._extension = self._path.rsplit('.', 1)[1].lower()
        self._delimiter = config.get('delimiter', None)
        self._skiprows = config.get('skiprows', None)
        
    def __call__(self) -> pa.Table:
        path = Path(self._path)
        assert path.exists(), f'File {path.as_posix()} dose not exist!'
        
        if self._extension == 'parquet':
            df = pd.read_parquet(path, engine='fastparquet')
        elif self._extension == 'csv':
            df = pd.read_csv(path, delimiter=self._delimiter, skiprows=self._skiprows)
    
        else:
            try:
                df = pd.read_csv(path, delimiter=self._delimiter, skiprows=self._skiprows)
            except Exception as e:
                print(f'Can read as csv: {e}')
                raise RuntimeError(f'Unknown extension: {self._extension}')
        
        return pa.Table.from_pandas(df)
    