
from typing import Literal

import pandas as pd 
from pydantic import BaseModel, Field

from etlite.registry import register
from etlite.transformers.base_pandas_trx import PandasBaseTransformer



class StringFilterTransformerModel(BaseModel):
    transformer_name: Literal['StringFilterTransformer'] = Field(
        default='StringFilterTransformer'
    )
    column: str
    operation: Literal['isin', 'notin']
    args: list



@register('transformer', StringFilterTransformerModel)
class StringFilterTransformer(PandasBaseTransformer):
    def __init__(self, config):
        self._column = config['column']
        self._operation = config['operation']
        self._args = config['args']
        
    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        if self._operation == 'isin':
            df = df[df[self._column].isin(self._args)].copy()

        elif self._operation == 'notin':
            df = df[~df[self._column].isin(self._args)].copy()
        
        return df
