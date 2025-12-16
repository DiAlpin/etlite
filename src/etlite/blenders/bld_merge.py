
from typing import List, Literal, Tuple

import pandas as pd
import pyarrow as pa
from pydantic import BaseModel, Field

from etlite.registry import register
from etlite.blenders.utils import set_suffixes



class MergeBlenderModel(BaseModel):
    blender_name: Literal['MergeBlender'] = Field(
        default='MergeBlender'
    )
    blend_method: Literal[
        'LeftJoin', 'RightJoin', 
        'OuterJoin', 'InnerJoin', 
        'CrossJoin'
        ] = Field(default='LeftJoin')
    on_column: str
    suffixes: tuple=("_x", "_y")



@register('blender', MergeBlenderModel)
class MergeBlender:
    def __init__(self, config: dict):
        self._on_column = config['on_column']
        self._suffixes = set_suffixes(config)
        self._blend_method = config['blend_method']
    
    def _get_tables(self, tables: List[pa.Table]) -> Tuple[pd.DataFrame, pd.DataFrame]:
        assert len(tables) == 2, \
            "Invalid tables, list should contain 2 pyarrow Table's."
        assert all(isinstance(table, pa.Table) for table in tables), \
            "Not all tables in the list are instances of pyarrow Table."
        return tables[0].to_pandas(), tables[1].to_pandas()

    def _blend_tables(self, tables: List[pa.Table]) -> pd.DataFrame:
        how = self._blend_method.replace('Join', '').lower()
        left, right = self._get_tables(tables)
        df = pd.merge(
            left,
            right,
            how=how,
            on=self._on_column,
            suffixes=self._suffixes
        )
        return df

    def __call__(self, tables: List[pa.Table]) -> pa.Table:
        df = self._blend_tables(tables)
        return pa.Table.from_pandas(df)
    

