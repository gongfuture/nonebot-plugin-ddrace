from nonebot.log import logger
from httpx import HTTPError, AsyncClient
from typing import Union, Dict

class NetWork:
    """
    NetWork 类用于处理 HTTP 请求，提供获取 HTML 和 JSON 数据的方法。

    属性:
        client (AsyncClient): HTTP 客户端，用于发送异步请求。

    方法:
        close_client():
            关闭 HTTP 客户端。
        
        get_html(url: str) -> str:
            获取指定 URL 的 HTML 内容。
        
        get_json(url: str) -> dict:
            获取指定 URL 的 JSON 数据。
    """
    def __init__(self):
        # self.client = AsyncClient()
        self.client = AsyncClient(follow_redirects=True)

    async def close_client(self):
        """
        关闭 HTTP 客户端。
        """
        await self.client.aclose()

    async def get_html(self,url) -> Union[str, Dict[str, str]]:
        """
        获取指定 URL 的 HTML 内容。

        参数:
            url (str): 目标 URL。

        返回:
            Union[str, Dict[str, str]]: HTML 内容，如果请求失败则返回包含错误信息的字典。
        """
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.text
        except HTTPError as e:
            error_message = f"HTTP error occurred: {e}"
            logger.error(error_message)
            return {"error": error_message}
        except Exception as e:
            error_message = f"An error occurred: {e}"
            logger.error(error_message)
            return {"error": error_message}

    async def get_json(self,url) -> Union[dict, Dict[str, str]]:
        """
        获取指定 URL 的 JSON 数据。

        参数:
            url (str): 目标 URL。

        返回:
            Union[dict, Dict[str, str]]: JSON 数据，如果请求失败则返回包含错误信息的字典。
        """
        try:
            response = await self.client.get(url)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            error_message = f"HTTP error occurred: {e}"
            logger.error(error_message)
            return {"error": error_message}
        except Exception as e:
            error_message = f"An error occurred: {e}"
            logger.error(error_message)
            return {"error": error_message}
