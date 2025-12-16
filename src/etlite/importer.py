
import pkgutil
import importlib



def import_extractors() -> None:
    import etlite.extractors
    
    for _, module_name, _ in pkgutil.iter_modules(etlite.extractors.__path__):
        importlib.import_module(f"etlite.extractors.{module_name}")

def import_blenders() -> None:
    import etlite.blenders
    
    for _, module_name, _ in pkgutil.iter_modules(etlite.blenders.__path__):
        importlib.import_module(f"etlite.blenders.{module_name}")

def import_loaders() -> None:
    import etlite.loaders
    
    for _, module_name, _ in pkgutil.iter_modules(etlite.loaders.__path__):
        importlib.import_module(f"etlite.loaders.{module_name}")

def import_transformers() -> None:
    import etlite.transformers
    
    for _, module_name, _ in pkgutil.iter_modules(etlite.transformers.__path__):
        importlib.import_module(f"etlite.transformers.{module_name}")



def import_components() -> None:
    import_extractors()
    import_blenders()
    import_transformers()
    import_loaders()
