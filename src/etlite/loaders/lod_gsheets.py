
from typing import Literal

import pyarrow as pa
from pydantic import BaseModel, Field

from etlite.registry import register
from etlite.adaptors.gcp import GoogleSheetAdapter



class GoogleSheetsLoaderModel(BaseModel):
    loader_name: Literal['GoogleSheetsLoader'] = Field(
        default='GoogleSheetsLoader'
    )
    spreadsheet_name: str
    worksheet_name: str



@register('loader', GoogleSheetsLoaderModel)
class GoogleSheetsLoader:
    def __init__(self, config):
        self._spreadsheet_name = config['spreadsheet_name']
        self._worksheet_name = config['worksheet_name']

    def __call__(self, table: pa.Table) -> pa.Table:
        df = table.to_pandas()        
        with GoogleSheetAdapter(self._spreadsheet_name, self._worksheet_name) as gs:
            gs.insert_df(df)
        return pa.Table.from_pandas(df)
