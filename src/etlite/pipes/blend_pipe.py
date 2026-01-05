
from typing import Dict, Any, Union, List

import pyarrow as pa
from pydantic import BaseModel

from etlite.registry import Registry
from etlite.pipes.base_pipe import BasePipe

type ConfigType = Union[Dict[str, Any], BaseModel]


class Blend(BasePipe):
    def __init__(self, tables: List[pa.Table], config: Dict[str, Any]):
        super().__init__(
            **self._args(tables, config)
        )
    
    def _args(self, tables: List[pa.Table], config: ConfigType) -> Dict[str, Any]:
        cfg = self._parse_config(config)
        registry = Registry()
        
        name = cfg['blender_name']
        registry.check_comp('blender', name, cfg)

        bld = registry.get_blender_class(name)
        blend = bld(cfg)
        table = blend(tables)

        return {
            'table': table,
            'registry': registry
        }
