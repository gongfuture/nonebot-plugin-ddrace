
from typing import Union, Dict

from nonebot.log import logger

from ..models import NetWork as Network
from ..utils import constants


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
        try:
            # 对 search_type 进行校验
            if fun in ["pre_search", "result_page"]:
                if search_type not in ["map", "mapper", "player"]:
                    raise ValueError(f"不存在的类型: {search_type}")
            elif fun in ["profile_json"]:
                if search_type not in ["map", "player"]:
                    raise ValueError(f"不存在的类型: {search_type}")
            # 对 search_name 为空 进行校验
            if not search_name:
                raise ValueError("名称不能为空")
            # 更改 search_name 符合 URL 格式
            # hexed_search_name = quote(search_name)
            # if fun in ["pre_search", "profile_json"]:
            #     encoded_search_name = hexed_search_name
            #     logger.debug(f"fun: {fun}, type: {search_type}, name: {search_name}, encoded_name: {encoded_search_name}")
            # elif fun in ["result_page"]:
            #     encoded_search_name = re.sub(
            #         r'%([0-9A-Fa-f]{2})',
            #         # lambda match: f"-{int(match.group(1),16)}-",
            #         # hexed_search_name
            #         lambda match: f"\\u{int(match.group(1), 16):04x}",
            #         hexed_search_name.encode('unicode_escape').decode('ascii')
            #     )
            #     logger.debug(f"fun: {fun}, type: {search_type}, name: {search_name}, encoded_name: {encoded_search_name}")
            
            return {"search_type":search_type,"search_name":search_name}

        except ValueError as ve:
            # 处理无效的 search_type 或 search_name 参数
            error_message = f"ValueError: {ve}"
            logger.error(error_message)
            return {"error": error_message}
        except Exception as e:
            # 处理其他异常，例如网络错误
            error_message = f"An error occurred: {e}"
            logger.error(error_message)
            return {"error": error_message}

    async def pre_search(self, search_type: str, search_name: str) -> Union[dict, Dict[str, str]]:
        """
        预搜索功能，根据类型和名称获取相关数据，异步。

        Args:
            search_type (str): 搜索类型，可以是 "map", "mapper", "player"。
            search_name (str): 搜索名称，不可为空。

        Returns:
            Union[dict, Dict[str, str]]: 返回包含搜索结果的字典，或者包含错误信息的字典。
        """
        # arg_convert 参数合规性检查转换
        converted_args = self.arg_convert(search_type, search_name, "pre_search")
        search_type = converted_args.get("search_type","")
        search_name = converted_args.get("search_name","")
        logger.debug(f"search_type: {search_type}, search_name: {search_name}")
        # 逻辑
        url = ""
        if search_type == "map":
            url = constants.MAP_QUERY_URL.format(search_name)
        elif search_type == "mapper":
            url = constants.MAPPER_QUERY_URL.format(search_name)
        elif search_type == "player":
            url = constants.PLAYER_QUERY_URL.format(search_name)
        logger.debug(f"url: {url}")
        return await self.net.get_json(url)

    async def result_page(self, search_type: str,search_name: str) -> Union[str, Dict[str, str]]:
        """
        获取搜索结果页面，异步。
        
        Args:
            search_type (str): 搜索类型，可以是 "map"、"mapper" 或 "player"。
            search_name (str): 搜索名称，不可为空。
        
        Returns:
            Union[str, Dict[str, str]]: 返回搜索结果页面的 HTML 内容，或者包含错误信息的字典。
        """
        # arg_convert 参数合规性检查转换
        converted_args = self.arg_convert(search_type, search_name, "pre_search")
        search_type = converted_args.get("search_type","")
        search_name = converted_args.get("search_name","")
        # 逻辑
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
        converted_args = self.arg_convert(search_type, search_name, "pre_search")
        search_type = converted_args.get("search_type","")
        search_name = converted_args.get("search_name","")
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


