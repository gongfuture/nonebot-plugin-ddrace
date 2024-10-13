import re
from urllib.parse import quote
from typing import Union, Dict

from nonebot.log import logger

from .network import NetWork as Network
from .constants import *


class ddr_data_get:
    """

    ddr_data_get 类用于处理 DDR 数据的获取和转换。
    方法:
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

    def arg_convert(self, stype: str, sname: str, fun: str) -> Dict[str, str]:
        """
        将输入参数转换为适合 URL 的格式，并进行校验。

        参数:
            stype (str): 搜索类型，可以是 "map", "mapper", "player"。
            sname (str): 搜索名称，不可为空。
            fun (str): 功能类型，可以是 "pre_search", "result_page", "profile_json"。

        返回:
            Dict[str, str]: 包含转换后参数的字典。

        异常:
            ValueError: 当 stype 或 sname 无效时抛出。
        """
        try:
            # 对 stype 进行校验
            if fun in ["pre_search", "result_page"]:
                if stype not in ["map", "mapper", "player"]:
                    raise ValueError(f"不存在的类型: {stype}")
            elif fun in ["profile_json"]:
                if stype not in ["map", "player"]:
                    raise ValueError(f"不存在的类型: {stype}")
            # 对 sname 为空 进行校验
            if not sname:
                raise ValueError("名称不能为空")
            # 更改 sname 符合 URL 格式
            hexed_sname = quote(sname)
            if fun in ["pre_search", "profile_json"]:
                encoded_sname = hexed_sname
                logger.debug(f"fun: {fun}, type: {stype}, name: {sname}, encoded_name: {encoded_sname}")
            elif fun in ["result_page"]:
                encoded_sname = re.sub(
                    r'%([0-9A-Fa-f]{2})',
                    lambda match: f"-{int(match.group(1),16)}-",
                    hexed_sname
                )
                logger.debug(f"fun: {fun}, type: {stype}, name: {sname}, encoded_name: {encoded_sname}")
            
            return {"stype":stype,"sname":sname}

        except ValueError as ve:
            # 处理无效的 stype 或 sname 参数
            error_message = f"ValueError: {ve}"
            logger.error(error_message)
            return {"error": error_message}
        except Exception as e:
            # 处理其他异常，例如网络错误
            error_message = f"An error occurred: {e}"
            logger.error(error_message)
            return {"error": error_message}

    async def pre_search(self, stype: str, sname: str) -> Union[dict, Dict[str, str]]:
        """
        预搜索功能，根据类型和名称获取相关数据，异步。

        参数:
            stype (str): 搜索类型，可以是 "map", "mapper", "player"。
            sname (str): 搜索名称，不可为空。

        返回:
            Union[dict, Dict[str, str]]: 返回包含搜索结果的字典，或者包含错误信息的字典。
        """
        # arg_convert 参数合规性检查转换
        converted_args = self.arg_convert(stype, sname, "pre_search")
        stype = converted_args.get("stype","")
        sname = converted_args.get("sname","")
        logger.debug(f"stype: {stype}, sname: {sname}")
        # 逻辑
        url = ""
        if stype == "map":
            url = MAP_QUERY_URL.format(sname)
        elif stype == "mapper":
            url = MAPPER_QUERY_URL.format(sname)
        elif stype == "player":
            url = PLAYER_QUERY_URL.format(sname)
        logger.debug(f"url: {url}")
        return await self.net.get_json(url)

    async def result_page(self, stype: str,sname: str) -> Union[str, Dict[str, str]]:
        """
        获取搜索结果页面，异步。
        
        参数:
            stype (str): 搜索类型，可以是 "map"、"mapper" 或 "player"。
            sname (str): 搜索名称，不可为空。
        
        返回:
            Union[str, Dict[str, str]]: 返回搜索结果页面的 HTML 内容，或者包含错误信息的字典。
        """
        # arg_convert 参数合规性检查转换
        converted_args = self.arg_convert(stype, sname, "pre_search")
        stype = converted_args.get("stype","")
        sname = converted_args.get("sname","")
        # 逻辑
        url = ""
        if stype == "map":
            url = MAP_URL.format(sname)
        elif stype == "mapper":
            url = MAPPER_URL.format(sname)
        elif stype == "player":
            url = PLAYER_URL.format(sname)
        logger.debug(f"url: {url}")
        return await self.net.get_html(url)

    async def profile_json(self, stype: str, sname: str) -> Union[dict, Dict[str, str]]:
        """
        获取指定类型和名称的配置文件数据，异步。
        
        参数:
            stype (str): 搜索类型，可以是 "map" 或 "player"。
            sname (str): 搜索名称，不可为空。
        
        返回:
            Union[dict, Dict[str, str]]: 返回包含配置文件数据的字典，或者包含错误信息的字典。
        """
        # arg_convert 参数合规性检查转换
        converted_args = self.arg_convert(stype, sname, "pre_search")
        stype = converted_args.get("stype","")
        sname = converted_args.get("sname","")
        # 逻辑
        url = ""
        if stype == "map":
            url = MAP_JSON_URL.format(sname)
        # elif stype == "mapper":
        #     url = MAPPER_QUERY_URL.format(sname)
        elif stype == "player":
            url = PLAYER_JSON_URL.format(sname)
        logger.debug(f"url: {url}")
        return await self.net.get_json(url)
