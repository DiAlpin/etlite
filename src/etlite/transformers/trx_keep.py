
from typing import Literal

import pandas as pd 
from pydantic import BaseModel, Field

from etlite.registry import register
from etlite.transformers.base_pandas_trx import PandasBaseTransformer



class KeepTransformerModel(BaseModel):
    transformer_name: Literal['KeepTransformer'] = Field(
        default='KeepTransformer'
    )
    columns_to_keep: list
    ascending_by: str | None = None
    descending_by: str | None = None



@register('transformer', KeepTransformerModel)
class KeepTransformer(PandasBaseTransformer):
    def __init__(self, config):
        self._columns = config['columns_to_keep']
        self._ascending_by = config.get('ascending_by')
        self._descending_by = config.get('descending_by')
        
    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        df = df[self._columns].copy()

        if self._ascending_by:
            df = df.sort_values(self._ascending_by, ascending=True)
        if self._descending_by:
            df = df.sort_values(self._descending_by, ascending=False)

        return df
