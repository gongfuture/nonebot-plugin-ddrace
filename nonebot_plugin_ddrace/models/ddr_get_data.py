import re
from typing import Union, Dict

from nonebot.log import logger

from ..models import NetWork as Network
from ..utils import constants, CacheClass


class DDRDataGet:
    """
    用于处理 DDR 数据的获取和转换。

    Methods:
        __init__:
        close:
        arg_convert:
        pre_search:
        result_page:
        profile_json:
    """

    def __init__(self):
        """
        初始化 ddr_data_get 类，创建一个 Network 实例。
        """
        self.net = Network()
        self.cache = CacheClass()

    async def close(self):
        """
        关闭网络客户端连接。
        """
        await self.net.close_client()

    def arg_convert(self, search_type: str, search_name: str, fun: str) -> Dict[str, str]:
        """
        将输入参数转换为适合 URL 的格式，并进行校验。

        Args:
            search_type (str): 搜索类型，可以是 "map", "mapper", "player"。
            search_name (str): 搜索名称，不可为空。
            fun (str): 功能类型，可以是 "pre_search", "result_page", "profile_json"。

        Returns:
            Dict[str, str]: 包含转换后参数的字典。

        Raises:
            ValueError: 当 search_type 或 search_name 无效时抛出。
        """
        # 对 search_type 进行校验
        if fun in ["pre_search", "result_page"]:
            if search_type not in ["map", "mapper", "player"]:
                raise ValueError(f"不存在的类型: {search_type}")
        elif fun in ["profile_json"]:
            if search_type not in ["map", "player"]:
                raise ValueError(f"不存在的类型: {search_type}")
        else:
            raise ValueError(f"不存在的功能: {fun}")
        # 对 search_name 为空 进行校验
        if not search_name:
            raise ValueError("名称不能为空")
        return {"search_type": search_type, "search_name": search_name}

    async def pre_search(self, search_type: str, search_name: str) -> Union[list, Dict[str, str]]:
        """
        预搜索功能，根据类型和名称获取相关数据，异步。

        Args:
            search_type (str): 搜索类型，可以是 "map", "mapper", "player"。
            search_name (str): 搜索名称，不可为空。

        Returns:
            Union[dict, Dict[str, str]]: 返回包含搜索结果的字典，或者包含错误信息的字典。
        """
        converted_args = self.arg_convert(
            search_type, search_name, "pre_search")
        search_type = converted_args.get("search_type", "")
        search_name = converted_args.get("search_name", "")
        logger.debug(f"search_type: {search_type}, search_name: {search_name}")

        url = ""
        if search_type == "map":
            url = constants.MAP_QUERY_URL.format(search_name)
        elif search_type == "mapper":
            url = constants.MAPPER_QUERY_URL.format(search_name)
        elif search_type == "player":
            url = constants.PLAYER_QUERY_URL.format(search_name)
        logger.debug(f"url: {url}")
        file_name = constants.PLAYER_PRESEARCH_JSON_CACHE.format(player_name=search_name)
        if self.cache.cache_check(file_name):
            result = self.cache.get_list_cache(file_name)
            logger.debug(f"pre_search: result: {result}")
            if isinstance(result, list):
                return result
            return {"error": "缓存文件错误"}
        else:
            result = await self.net.get_json(url)
            self.cache.store_list_cache(file_name, result)
            return result

    async def result_page(self, search_type: str, search_name: str) -> Union[str, Dict[str, str]]:
        """
        获取搜索结果页面，异步。

        Args:
            search_type (str): 搜索类型，可以是 "map"、"mapper" 或 "player"。
            search_name (str): 搜索名称，不可为空。

        Returns:
            Union[str, Dict[str, str]]: 返回搜索结果页面的 HTML 内容，或者包含错误信息的字典。
        """
        converted_args = self.arg_convert(
            search_type, search_name, "result_page")
        search_type = converted_args.get("search_type", "")
        search_name = converted_args.get("search_name", "")
        logger.debug(f"search_type: {search_type}, search_name: {search_name}")

        url = ""
        if search_type == "map":
            url = constants.MAP_PAGE_URL.format(search_name)
        elif search_type == "mapper":
            url = constants.MAPPER_PAGE_URL.format(search_name)
        elif search_type == "player":
            url = constants.PLAYER_PAGE_URL.format(search_name)
        logger.debug(f"url: {url}")
        return await self.net.get_html(url)

    async def profile_json(self, search_type: str, search_name: str) -> Union[dict, Dict[str, str]]:
        """
        获取指定类型和名称的数据，异步。

        Args:
            search_type (str): 搜索类型，可以是 "map" 或 "player"。
            search_name (str): 搜索名称，不可为空。

        Returns:
            Union[dict, Dict[str, str]]: 返回包含数据的字典，或者包含错误信息的字典。
        """
        # arg_convert 参数合规性检查转换
        converted_args = self.arg_convert(
            search_type, search_name, "pre_search")
        search_type = converted_args.get("search_type", "")
        search_name = converted_args.get("search_name", "")
        # 逻辑
        url = ""
        if search_type == "map":
            url = constants.MAP_JSON_URL.format(search_name)
        # elif search_type == "mapper":
        #     url = MAPPER_QUERY_URL.format(search_name)
        elif search_type == "player":
            url = constants.PLAYER_JSON_URL.format(search_name)
        logger.debug(f"url: {url}")
        return await self.net.get_json(url)

    async def fuzzy_search(self, search_type: str, search_str: str) -> dict:
        """
        模糊搜索功能，根据输入的字符串和类型获取相关数据，异步。

        Args:
            search_str (str): 搜索字符串。
            search_type (str): 搜索类型，可以是 "player" 或 "map"。

        Returns:
            dict: 包含搜索结果的字典。

        """
        # 限制非英文字符不超过五个，英文字符不超过十个，总长度限制
        if search_type not in ["player", "map"]:
            logger.error("player_fuzzy_search: 不存在的搜索类型")
            raise ValueError("不存在的搜索类型")

        if search_type == "player":
            max_length = 10
            current_length = 0
            truncated_str = ""

            for char in search_str:
                if re.match(r'[^\x00-\x7F]', char):
                    if current_length + 2 > max_length:
                        break
                    current_length += 2
                else:
                    if current_length + 1 > max_length:
                        break
                    current_length += 1
                truncated_str += char

            search_str = truncated_str

        while search_str:
            result = await self.pre_search(search_type, search_str)
            logger.debug(f"player_fuzzy_search: 搜索结果 '{result}'")
            if result and "404error" not in result and "error" not in result:
                return result
            search_str = search_str[:-1]  # 去掉末尾字符
            logger.debug(f"player_fuzzy_search: 当前搜索字符串 '{search_str}'")

        logger.error("player_fuzzy_search: 未找到匹配的玩家信息")
        raise ValueError("未找到匹配的玩家信息")
