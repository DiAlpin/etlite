
from typing import Literal

import pandas as pd 
from pydantic import BaseModel, Field

from etlite.registry import register
from etlite.transformers.base_pandas_trx import PandasBaseTransformer



class FillnaTransformerModel(BaseModel):
    transformer_name: Literal['FillnaTransformer'] = Field(
        default='FillnaTransformer'
    )
    columns_map: dict



@register('transformer', FillnaTransformerModel)
class FillnaTransformer(PandasBaseTransformer):
    def __init__(self, config):
        self._columns_map = config['columns_map']
        
    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        current_cols = set(df.columns.tolist())

        for c in self._columns_map.keys():
            assert c in current_cols, f'Column {c} not found in DataFrame'
        
        df.fillna(self._columns_map, inplace=True)
        
        return df
