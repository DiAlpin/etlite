
from typing import Dict, Any, Union

from pydantic import BaseModel

from etlite.registry import Registry
from etlite.pipes.base_pipe import BasePipe

type ConfigType = Union[Dict[str, Any], BaseModel]



class Extract(BasePipe):
    def __init__(self, config: Dict[str, Any]):
        super().__init__(
            **self._args(config)
        )
    
    def _args(self, config: ConfigType) -> Dict[str, Any]:
        cfg = self._parse_config(config)
        registry = Registry()
        
        name = cfg['extractor_name']
        registry.check_comp('extractor', name, cfg)

        ext = registry.get_extractor_class(name)
        extract = ext(cfg)
        table = extract()

        return {
            'table': table,
            'registry': registry
        }
