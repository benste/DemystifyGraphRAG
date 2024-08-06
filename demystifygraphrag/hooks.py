from typing import Dict

from kedro.framework.hooks import hook_impl
from kedro.io import DataCatalog
from kedro.utils import load_obj


def getFromDict(data_dict, map_list):
    if not isinstance(data_dict, dict):
        return None
    
    # Map list empty, return results
    if not map_list:
        return data_dict
        
    value = data_dict[map_list.pop(0)]
    
    # Recursive so we can check if the mapping references dicts or not
    return getFromDict(value, map_list)

def setInDict(data_dict, map_list, value):
    pre_dict = getFromDict(data_dict, map_list[:-1])
    # Only assign if the map returned a value
    if pre_dict:
        pre_dict[map_list[-1]] = value
    

class TypedParameters:
    def __init__(self, type_indicator: str = "type"):
        self._type_indicator = type_indicator

    @hook_impl
    def after_catalog_created(self, catalog: DataCatalog) -> None:
        param_types = self._get_param_types(catalog)
        
        for param, type_string in param_types.items():
            type_obj = load_obj(type_string)
            catalog._datasets[param]._data = type_obj(
                **catalog._datasets[param]._data
            )
            
            # Also adjust the global "parameters" in catalog
            dict_path = param.removeprefix("params:").split(".")
            setInDict(catalog._datasets["parameters"]._data, dict_path, catalog._datasets[param]._data)

    def _get_param_types(self, catalog: DataCatalog) -> Dict[str, str]:
        param_types = {}

        for name, dataset in catalog._datasets.items():
            if name.startswith("params:") and isinstance(dataset._data, dict) and self._type_indicator in dataset._data.keys():
                param_types[name] = dataset._data[self._type_indicator]
        return param_types
