
import os
import re
import json
import random
import string
import datetime

import requests
import pandas as pd
from websocket import create_connection

from etlite.adaptors.tradingview.retry_decorator import retry
from etlite.adaptors.tradingview.constants import TradingviewAdaptorConstants



class TradingviewAdapter:
    def __init__(self, exchange='BVB'):
        self._exchange = exchange
        self._token = self._get_token()
        self._ws = None
        self._session_id = self._generate_random_id('qs')
        self._chart_id = self._generate_random_id('cs')
        self._cons = TradingviewAdaptorConstants()
        
    def _get_token(self):
        credentials = {
            'username': os.environ.get('TRADINGVIEW_USER'),
            'password': os.environ.get('TRADINGVIEW_PASSWORD'),
            'remember': 'on'
        }
        
        token = "unauthorized_user_token"
        if credentials['username'] and credentials['password']:
            try:
                response = requests.post(
                    url=self._cons.sign_in_url, data=credentials, headers=self._cons.signin_headers)
                token = response.json()['user']['auth_token']
            except Exception as e:
                print(e)
        return token
    
    def _create_connection(self):
        self._ws = create_connection(
            self._cons.ws_tradingview_url, headers=self._cons.ws_headers, timeout=self._cons.ws_timeout
        )

    @staticmethod
    def _generate_random_id(code, length=12):
        random_sring = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
        return f'{code}_{random_sring}'

    @staticmethod
    def _append_header(message):
        return f"~m~{len(message)}~m~{message}"

    @staticmethod
    def _construct_message(func, param_list):
        return json.dumps({"m": func, "p": param_list}, separators=(",", ":"))

    def _create_message(self, func, paramList):
        return self._append_header(self._construct_message(func, paramList))
    
    def _send_message(self, func, args):
        m = self._create_message(func, args)
        self._ws.send(m)

    def _convert2df(self, data, symbol):
        df = pd.DataFrame(data, columns=self._cons.prices_df_cols)
        df.insert(0, "symbol", value=symbol)

        return df

    @staticmethod
    def _get_row(row):
        splited_row = re.split(r"\[|:|,|\]", row)
        dt = datetime.datetime.fromtimestamp(float(splited_row[4]))
        row_values = [dt]

        for i in range(5, 10):
            try:
                row_values.append(float(splited_row[i]))
            except ValueError:
                row_values.append(0.0)

        return row_values

    def _create_df(self, raw_data, symbol):
        try:
            out = re.search(r'"s":\[(.+?)\}\]', raw_data)[1]
            body = out.split(',{"')
            data = []

            for chunk in body:
                row = self._get_row(chunk)
                data.append(row)

            return self._convert2df(data, symbol)

        except AttributeError as e:
            raise ValueError(f"No data for {symbol}, please check the exchange and symbol") from e
        
        except Exception as e:
            raise ValueError(e) from e
        
    def _check_interval(self, interval):
        assert interval in self._cons.intervals_map.keys(), f"'{interval}' is not a valid interval"

        return self._cons.intervals_map[interval]
    
    @staticmethod
    def _compose_symbol_arg(symbol, extended_session):
        session_type = '"extended"' if extended_session else '"regular"'
        return '={"symbol":"' + symbol + '","adjustment":"splits","session":' + session_type + '}'

    def _send_messages(self, symbol, interval, n_bars, extended_session):
        self._create_connection()
        self._send_message("set_auth_token", [self._token])
        self._send_message("chart_create_session", [self._chart_id, ""])
        self._send_message("quote_create_session", [self._session_id])
        self._send_message("quote_set_fields", [self._session_id, *self._cons.quote_fields])
        self._send_message("quote_add_symbols", [self._session_id, symbol, self._cons.flags])
        self._send_message("quote_fast_symbols", [self._session_id, symbol])
        self._send_message("resolve_symbol", [self._chart_id, 
                                              "symbol_1", 
                                              self._compose_symbol_arg(symbol, extended_session)])
        self._send_message("create_series", [self._chart_id, 
                                             "s1", 
                                             "s1", 
                                             "symbol_1", 
                                             interval, 
                                             n_bars])
        self._send_message("switch_timezone", [self._chart_id, "exchange"])

    @retry(max_attempts=5, delay=1, backoff_factor=2)
    def get_data(self, 
                 symbol: str, 
                 interval: str, 
                 n_bars: int, 
                 extended_session: bool = False
        ) -> pd.DataFrame:
        """
        Get historical prices for a given symbol.

        Args:
            symbol (str): The symbol for which to retrieve historical prices.
            interval (str, optional): The interval of the historical prices.
            n_bars (int, optional): The number of historical bars to retrieve. Max 5_000.
            extended_session (bool, optional): Whether to include extended session data. Defaults to False.

        Returns:
            pd.DataFrame: A DataFrame containing the historical prices.

        """

        std_symbol = f'{self._exchange}:{symbol.upper()}'
        std_interval = self._check_interval(interval)
        self._send_messages(std_symbol, std_interval, n_bars, extended_session)

        raw_data = ""
        while True:
            try:
                result = self._ws.recv()
                raw_data = raw_data + result + "\n"
            
            except Exception as e:
                break
            if "series_completed" in result:
                break

        return self._create_df(raw_data, symbol)
