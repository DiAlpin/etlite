
from typing import Literal

import pandas as pd
import pyarrow as pa
from pydantic import BaseModel, Field

from etlite.registry import register



class HtmlExtractorModel(BaseModel):
    extractor_name: Literal['HtmlExtractor'] = Field(
        default='HtmlExtractor'
    )
    url: str
    table_id: int



@register('extractor', HtmlExtractorModel)
class HtmlExtractor:
    def __init__(self, config: dict):
        self._url = config['url']
        self._table_id = config['table_id']

    def __call__(self) -> pa.Table:
        dfs = pd.read_html(self._url)
        df = dfs[self._table_id]
        return pa.Table.from_pandas(df)
