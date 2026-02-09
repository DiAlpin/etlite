
import yfinance as yf
from etlite.environ import EnvLoader as env



class YFinanceAdapter:
    def __init__(self, symbol, exchange):
        self._symbol = symbol
        self._exchange = exchange
        self._ticker = f'{symbol}.{exchange}' if exchange else symbol
    
    def get_index_weights(self):
        etf = yf.Ticker(self._ticker)
        df_weights = etf.funds_data.top_holdings.reset_index()
        return df_weights