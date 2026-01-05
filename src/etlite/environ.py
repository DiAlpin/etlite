
import os
from pathlib import Path
from typing import Protocol

from dotenv import load_dotenv


class EnvironmentVars(Protocol):
    _vars: dict
    AWS_ACCESS_KEY_ID: str = 'AWS_ACCESS_KEY_ID'
    AWS_SECRET_ACCESS_KEY: str = 'AWS_SECRET_ACCESS_KEY'
    GCP_TOKEN_PATH: str = 'GCP_TOKEN_PATH'
    TRADINGVIEW_USER: str = 'TRADINGVIEW_USER'
    TRADINGVIEW_PASSWORD: str = 'TRADINGVIEW_PASSWORD'


class _EnvLoader:
    _vars = {
        # <key>: (<env_type>, <is_mandatory>' <default>)
        EnvironmentVars.AWS_ACCESS_KEY_ID: ('env', True, ''),
        EnvironmentVars.AWS_SECRET_ACCESS_KEY: ('env', True, ''),
        EnvironmentVars.GCP_TOKEN_PATH: ('env', True, ''),
        EnvironmentVars.TRADINGVIEW_USER: ('env', True, ''),
        EnvironmentVars.TRADINGVIEW_PASSWORD: ('env', True, ''),
    }
    
    
    def __init__(self):
        self._load_dotenv_file()
    
    def _load_dotenv_file(self):
        env_path = Path.cwd() / '.env'
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
        else:
            load_dotenv()
    
    def __getattr__(self, item: str):
        if var := os.environ.get(item):
            return var
        else:
            return super().__getattribute__(item)


EnvLoader: EnvironmentVars = _EnvLoader()
