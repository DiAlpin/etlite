
from typing import Callable, Literal

import pandas as pd 
from pydantic import BaseModel, Field

from etlite.registry import register
from etlite.transformers.base_pandas_trx import PandasBaseTransformer



class PandasCustomTransformerModel(BaseModel):
    transformer_name: Literal['PandasCustomTransformer'] = Field(
        default='PandasCustomTransformer'
    )
    transformation_func: Callable
    args: dict = {}



@register('transformer', PandasCustomTransformerModel)
class PandasCustomTransformer(PandasBaseTransformer):
    def __init__(self, config):
        self._transformation_func = config['transformation_func']
        self._args = config.get('args', {})
        
    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._transformation_func(df, **self._args)
