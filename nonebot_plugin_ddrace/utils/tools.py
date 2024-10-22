from pathlib import Path
import re
from typing import Union
from nonebot import require
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store
class PathClass:

    def rootpath(self) -> Path:
        return Path(__file__).resolve().parent.parent

    def workpath(self) -> Path:
        return Path.cwd()

    def rootpathcomplete(self, path: str) -> Path:
        return self.rootpath() / path

    def workpathcomplete(self, path: str) -> Path:
        return self.workpath() / path

    def ddrconfigpath(self) -> Path:
        return store.get_plugin_config_dir()

    def ddrdatapath(self) -> Path:
        return store.get_plugin_data_dir()

    def ddrcachepath(self) -> Path:
        return store.get_plugin_cache_dir()


class InputCheck:

    def check_type_empty(self, value, types) -> bool:
        """
        检查值的类型是否符合要求，且不为空。

        Args:
            value: 要检查的值。
            types: 要求的类型，可以是单个类型或类型元组。

        Returns:
            bool: 如果值的类型符合要求且不为空，则返回 True；否则返回 False。
        """
        if self.is_empty(value):
            return False
        if not self.check_type(value, types):
            return False
        return True

    def is_empty(self, value) -> bool:
        """
        检查各种类型的值是否为空。

        Args:
            value: 要检查的值，可以是字符串、列表、字典、集合、元组等。

        Returns:
            bool: 如果值为空，则返回 True；否则返回 False。
        """
        if value is None:
            return True
        if isinstance(value, str) and value.strip() == "":
            return True
        if isinstance(value, (list, dict, set, tuple)) and len(value) == 0:
            return True
        return False

    def check_type(self, value, types) -> bool:
        """
        检查值的类型是否符合要求。

        Args:
            value: 要检查的值。
            types: 要求的类型，可以是单个类型或类型元组。

        Returns:
            bool: 如果值的类型符合要求，则返回 True；否则返回 False。
        """
        if isinstance(types, type):
            types = (types,)
        return isinstance(value, types)

    def custom_escape(self, text: str) -> str:
        """
        自定义转义函数，将 URL 中的特殊字符转义成相应的百分比编码，并排除控制字符。
        """
        text = re.sub(r'[\r\n\t]', '', text)
        
        escape_map = {
            ' ': '%20',
            '+': '%2B',
            '&': '%26',
            '=': '%3D',
            '<': '%3C',
            '>': '%3E',
            '"': '%22',
            '#': '%23',
            ',': '%2C',
            '%': '%25',
            '{': '%7B',
            '}': '%7D',
            '|': '%7C',
            '\\': '%5C',
            '^': '%5E',
            # '~': '%7E',
            '[': '%5B',
            ']': '%5D',
            '`': '%60',
            ';': '%3B',
            '/': '%2F',
            '?': '%3F',
            ':': '%3A',
            '@': '%40',
            '$': '%24'
        }
        return ''.join(escape_map.get(c, c) for c in text)

    def check_id_types(self,group_id: Union[int, str] = 0, user_id: Union[int, str] = 0):
        if isinstance(group_id, str):
            error_msg = "group_id must be int" 
            raise ValueError(error_msg)
        if isinstance(user_id, str):
            error_msg = "user_id must be int" 
            raise ValueError(error_msg)


if __name__ == "__main__":
    print(PathClass().rootpath())
    print(type(PathClass().rootpath()))
    print(PathClass().workpath())
    print(type(PathClass().workpath()))