
from typing import Literal

import pandas as pd 
from pydantic import BaseModel, Field

from etlite.registry import register
from etlite.transformers.base_pandas_trx import PandasBaseTransformer



class RenameTransformerModel(BaseModel):
    transformer_name: Literal['RenameTransformer'] = Field(
        default='RenameTransformer'
    )
    columns_map: dict



@register('transformer', RenameTransformerModel)
class RenameTransformer(PandasBaseTransformer):
    def __init__(self, config):
        self._columns_map = config['columns_map']

    def main_transformation(self, df: pd.DataFrame) -> pd.DataFrame:
        df.rename(columns=self._columns_map, inplace=True)
        return df
