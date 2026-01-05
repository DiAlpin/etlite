
import json

from dataclasses import dataclass



@dataclass
class TradingviewAdaptorConstants:
    sign_in_url = 'https://www.tradingview.com/accounts/signin/'
    signin_headers = {'Referer': 'https://www.tradingview.com'}
    ws_tradingview_url = 'wss://data.tradingview.com/socket.io/websocket'
    ws_headers = json.dumps({"Origin": "https://data.tradingview.com"})
    ws_timeout = 5
    flags = {"flags": ["force_permission"]}
    prices_df_cols = [
        'datetime', 'open', 'high',
        'low', 'close', 'volume',
        ]
    intervals_map = {
        '1m': "1", '3m': "3", '5m': "5", '15m': "15",
        '30m': "30", '45m': "45", '1H': "1H", '2H': "2H",
        '3H': "3H", '4H': "4H", '1D': "1D", '1W': "1W",
        '1M': "1M",
        }
    quote_fields = [
        "ch", "chp", "current_session", "description",
        "local_description", "language", "exchange",
        "fractional", "is_tradable", "lp", "lp_time",
        "minmov", "minmove2", "original_name", "pricescale",
        "pro_name", "short_name", "type", "update_mode", 
        "volume", "currency_code", "rchp", "rtc",
        ]
