
import functools
from typing import List, Literal

import pandas as pd
import pyarrow as pa
from pydantic import BaseModel, Field

from etlite.registry import register
from etlite.adaptors.tradingview import TradingviewAdapter



class LastPriceTradingviewExtractorModel(BaseModel):
    extractor_name: Literal['LastPriceTradingviewExtractor'] = Field(
        default='LastPriceTradingviewExtractor'
    )
    exchange: str
    symbols: List[str]
    interval: str


@register('extractor', LastPriceTradingviewExtractorModel)
class LastPriceTradingviewExtractor:
    def __init__(self, config: dict):
        self._adaptor = TradingviewAdapter(exchange=config['exchange'])
        self._symbols = config['symbols']
        self._interval = config['interval']
        self._n_bar = 1

    def _get_data_for_symbol(self, symbol: str) -> pd.DataFrame:
        try:
            df = self._adaptor.get_data(
                symbol=symbol,
                interval=self._interval, 
                n_bars=self._n_bar
            )
            return df
    
        except Exception as e:
            raise RuntimeError(f'Error extracting data for {symbol} \n{e}')


    def __call__(self) -> pa.Table:
        dfs = [self._get_data_for_symbol(s) for s in self._symbols]        
        df = pd.concat(dfs)
        return pa.Table.from_pandas(df)




class PickDayPriceTradingviewExtractorModel(BaseModel):
    extractor_name: Literal['PickDayPriceTradingviewExtractor'] = Field(
        default='PickDayPriceTradingviewExtractor'
    )
    exchange: str
    symbols: List[str]
    piking_date: str
    data_source_description: str
    dataset_name: str


@register('extractor', PickDayPriceTradingviewExtractorModel)
class PickDayPriceTradingviewExtractor:
    def __init__(self, config: dict):
        self._adaptor = TradingviewAdapter(exchange=config['exchange'])
        self._symbols = config['symbols']
        self._interval = '1D'
        self._piking_date = config['piking_date'] #TODO: add a standard dateformat
        self._n_bar = 1
        
        
    def __call__(self) -> pa.Table:
        get_price_func = functools.partial(
                self._adaptor.get_data, 
                interval=self._interval, 
                n_bars=self._n_bar
            )
        
        dfs = []
        for s in self._symbols:
            _df = get_price_func(s)
            dfs.append(
                _df[_df['datetime'] == self._piking_date].copy()
            )
        df = pd.concat(dfs) 
        
        return pa.Table.from_pandas(df)
    



class OhlcTradingviewExtractorModel(BaseModel):
    extractor_name: Literal['OhlcTradingviewExtractor'] = Field(
        default='OhlcTradingviewExtractor'
    )
    exchange: str
    symbol: str
    interval: str
    candles: int


@register('extractor', OhlcTradingviewExtractorModel)
class OhlcTradingviewExtractor:
    def __init__(self, config: dict):
        self._adaptor = TradingviewAdapter(exchange=config['exchange'])
        self._symbol = config['symbol']
        self._interval = config['interval']
        self._n_bar = config['candles']

    def __call__(self) -> pa.Table:
        df = self._adaptor.get_data(
                symbol=self._symbol, 
                interval=self._interval, 
                n_bars=self._n_bar
            )
        return pa.Table.from_pandas(df)
