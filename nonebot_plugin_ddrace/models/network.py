from typing import Any, Awaitable, Callable, Union, Dict
from urllib.parse import urljoin
from nonebot.log import logger
from httpx import HTTPError, AsyncClient, HTTPStatusError
from bs4 import BeautifulSoup


async def catch_error(func: Callable[..., Awaitable[Any]], *args, **kwargs) -> Any:
    """
    安全执行异步函数，捕获异常并记录错误日志。

    Args:
        func (Callable[..., Awaitable[Any]]): 要执行的异步函数。
        *args: 传递给函数的位置参数。
        **kwargs: 传递给函数的关键字参数。

    Returns:
        Any: 函数的返回值，如果发生异常则返回包含错误信息的字典。
    """
    try:
        return await func(*args, **kwargs)
    except HTTPStatusError as e:
        if e.response.status_code == 404:
            error_message = f"Client error '404 Not Found' for url '{args[0]}'"
            logger.error(error_message)
            return {"404error": error_message}
        else:
            error_message = f"HTTP error occurred: {e}"
            logger.error(error_message)
            return {"error": error_message}
    except HTTPError as e:
        error_message = f"HTTP error occurred: {e}"
        logger.error(error_message)
        return {"error": error_message}
    except Exception as e:
        error_message = f"An error occurred: {e}"
        logger.error(error_message)
        return {"error": error_message}


class NetWork:
    """
    NetWork 类用于处理 HTTP 请求，提供获取 HTML 和 JSON 数据的方法。

    Attributes:
        client (AsyncClient): HTTP 客户端，用于发送异步请求。

    Methods:
        close_client():
            关闭 HTTP 客户端。

        convert_relative_to_absolute(self, html_content: str, base_url: str) -> str:
            将 HTML 内容中的相对 URL 转换为绝对 URL。
        
        get_html(url: str) -> Union[str, Dict[str, str]]:
            获取指定 URL 的 HTML 内容。
        
        get_json(url: str) -> Union[dict, Dict[str, str]]:
            获取指定 URL 的 JSON 数据。
    """
    def __init__(self):
        self.client = AsyncClient(follow_redirects=True ,timeout=15)

    async def close_client(self):
        """
        关闭 HTTP 客户端。
        """
        await self.client.aclose()

    def convert_relative_to_absolute(self, html_content: str, base_url: str) -> str:
        """
        将 HTML 内容中的相对 URL 转换为绝对 URL。
        
        Args:
            html_content (str): 包含 HTML 内容的字符串。
            base_url (str): 用于转换相对 URL 的基准 URL。
        
        Returns:
            str: 转换后的 HTML 内容，所有相对 URL 均已转换为绝对 URL。
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        tags = soup.find_all(
            ['a', 'script', 'img', 'iframe', 'audio', 'video', 'source', 'object', 'embed']
        )

        for tag in tags:
            attr = None
            if tag.name == 'a':
                attr = 'href'
            elif tag.name in 'script':
                attr = 'href' if tag.has_attr('href') else 'src'
            elif tag.name in ['img', 'iframe', 'audio', 'video', 'source', 'object', 'embed']:
                attr = 'src'

            if attr and tag.get(attr):
                tag[attr] = urljoin(base_url, tag[attr])

        return str(soup)

    async def _fetch(self, url: str) -> Any:
        """
        发送 HTTP GET 请求并返回响应。

        Args:
            url (str): 目标 URL。

        Returns:
            Any: HTTP 响应对象。
        """
        response = await self.client.get(url)
        response.raise_for_status()
        return response

    async def get_html(self, url: str) -> Union[str, Dict[str, str]]:
        """
        获取指定 URL 的 HTML 内容。

        Args:
            url (str): 目标 URL。

        Returns:
            Union[str, Dict[str, str]]: HTML 内容，如果请求失败则返回包含错误信息的字典。
        """
        response = await catch_error(self._fetch, url)
        if isinstance(response, dict):
            return response
        return self.convert_relative_to_absolute(response.text, url)

    async def get_json(self, url: str) -> Union[dict, Dict[str, str]]:
        """
        获取指定 URL 的 JSON 数据。

        Args:
            url (str): 目标 URL。

        Returns:
            Union[dict, Dict[str, str]]: JSON 数据，如果请求失败则返回包含错误信息的字典。
        """
        response = await catch_error(self._fetch, url)
        if isinstance(response, dict):
            return response
        return response.json()