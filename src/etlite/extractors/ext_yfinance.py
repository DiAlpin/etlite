import functools
from typing import Literal

import pyarrow as pa
from pydantic import BaseModel, Field

from etlite.registry import register
from etlite.adaptors.yahoo_finance import YFinanceAdapter



class IndexWeightsYFExtractorModel(BaseModel):
    extractor_name: Literal['IndexWeightsYFExtractor'] = Field(
        default='IndexWeightsYFExtractor'
    )
    symbol: str 
    exchange: str | None = None


@register('extractor', IndexWeightsYFExtractorModel)
class IndexWeightsYFExtractor:
    def __init__(self, config: dict):
        self._adaptor = YFinanceAdapter(
            symbol=config['symbol'], 
            exchange=config['exchange'])

    def __call__(self) -> pa.Table:
        df = self._adaptor.get_index_weights()
        return pa.Table.from_pandas(df)
