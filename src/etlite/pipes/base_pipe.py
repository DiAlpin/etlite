
from typing import Dict, Any, Union

import pyarrow as pa
from pydantic import BaseModel

type ConfigType = Union[Dict[str, Any], BaseModel]



class BasePipe:    
    def __init__(self, table: pa.Table, registry):
        self._table = table
        self._registry = registry
        self._transformers: list = []
        self._loaders: list = []
    
    @staticmethod
    def _parse_config(config: ConfigType) -> Dict[str, Any]:
        if isinstance(config, dict):
            return config
        elif isinstance(config, BaseModel):
            return config.model_dump()
        else:
            raise ValueError(f'Invalid config type: {type(config)}')
    
    def transform(self, config: ConfigType):
        cfg = self._parse_config(config)
        name = cfg['transformer_name']
        self._registry.check_comp('transformer', name, cfg)
        trx = self._registry.get_transformer_class(name)
        self._transformers.append(trx(cfg))
        return self
    
    def load(self, config: ConfigType):
        cfg = self._parse_config(config)
        name = cfg['loader_name']
        self._registry.check_comp('loader', name, cfg)
        ldr = self._registry.get_loader_class(name)
        self._loaders.append(ldr(cfg))
        return self
        
    def run(self) -> pa.Table:
        if not self._registry.is_healthy:
            # TODO: change with custom exception 
            raise RuntimeError(self._registry.all_errors_as_str)    
        
        for trx in self._transformers:
            try:
                self._table = trx(self._table)
            # TODO: change with custom exception 
            except Exception as e:
                raise RuntimeError(f'{trx.__class__.__name__}: {e}')

        for loader in self._loaders:
            try:
                loader(self._table)
            # TODO: change with custom exception 
            except Exception as e:
                raise RuntimeError(f'{loader.__class__.__name__}: {e}')

        return self._table
     