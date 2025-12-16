
import os
import pydantic
import pyarrow as pa
from etlite.utils.error_parsing import parse_pydantic_error



_registry: dict = {
    'extractor': {},
    'blender': {},
    'transformer': {},
    'loader': {},
}

class InvalidComponent:
    def __init__(self, config):
        self._config = config
        
    def __call__(self):
        return pa.Table.from_pydict({})
    

def register(group: str, base_model, env_requirements: list|None=None):
    def decorator(cls):
        assert group in _registry, f'Invalid group: {group}'
        adaptor_requirements = env_requirements
        _registry[group][cls.__name__] = (base_model, adaptor_requirements, cls)
        return cls

    return decorator


class Registry:
    def __init__(self):
        self._registry = _registry
        self._errors = []
    
    @property
    def is_healthy(self):
        return len(self._errors) == 0
        
    def _check_config(self, name: str, model, config: dict) -> None:
        try:
            model(**config)  
        except pydantic.ValidationError as ve:
            msg = parse_pydantic_error(ve.errors())
            self._errors.append((name, msg))

    def _check_env(self, name: str, req: list) -> None:
        if req:
            missing_vars = []
            for var in req:
                if not os.environ.get(var):
                    missing_vars.append(var)
            
            if len(missing_vars) > 0:
                msg = f"Missing environment variables: {','.join(missing_vars)}"
                self._errors.append((name, msg))
    
    def check_comp(self, comp: str, name: str, config: dict) -> None:
        model, req, comp_class = self._registry[comp][name]
        self._check_config(name, model, config)
        self._check_env(name, req)
    
    
    @property      
    def all_errors_as_str(self):
        if not self.is_healthy:
            msg = 'Pipeline have invalid components:\n'
            for name, error in self._errors:
                msg += f'\t{name}: {error}\n'
        return msg

    def get_extractor_class(self, name):
        model, req, comp_class = self._registry['extractor'][name]
        if self.is_healthy:
            return comp_class
        return InvalidComponent
    
    def get_blender_class(self, name):
        model, req, comp_class = self._registry['blender'][name]
        if self.is_healthy:
            return comp_class
        return InvalidComponent
    
    def get_transformer_class(self, name):
        model, req, comp_class = self._registry['transformer'][name]
        if self.is_healthy:
            return comp_class
        return InvalidComponent

    def get_loader_class(self, name):
        model, req, comp_class = self._registry['loader'][name]
        if self.is_healthy:
            return comp_class
        return InvalidComponent
