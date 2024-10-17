from pathlib import Path
from typing import List, Optional, Union
from bs4 import BeautifulSoup
from nonebot import require,logger
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import html_to_pic,md_to_pic
from ..utils import *



def json2md(json_data: dict, title_filter: list) -> str:
    """
    将 JSON 数据转换为 Markdown 表格格式的字符串。
    
    Args:
        json_data (dict): 包含数据的 JSON 字典。
        title_filter (list): 包含表格标题的列表，用于过滤 JSON 数据中的键。
    
    Returns:
        str: 生成的 Markdown 表格格式的字符串。
    """
    if isinstance(json_data, dict) is False:
        error_message = "json2md: 数据格式错误"
        logger.error(error_message)
        raise ValueError(error_message)
    if isinstance(title_filter, list) is False:
        error_message = "json2md: 标题格式错误"
        logger.error(error_message)
        raise ValueError(error_message)

    md_str = ""
    # 生成表格头
    headers = [key for key in title_filter if key in json_data]
    md_str = "| " + " | ".join(headers) + " |\n"
    md_str += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    logger.trace(f"json2md: header over: {md_str}")

    # 生成表格数据
    for key in title_filter:
        if key in json_data:
            md_str += "| " + " | ".join(str(json_data[key])) + " |\n"
    logger.trace("json2md: data over")

    return md_str


async def md2pic(md_str: str) -> Union[bytes, str]:
    """
    将 Markdown 字符串转换为图片字节流。
    
    Args:
        md_str (str): 要转换的 Markdown 字符串。

    Returns:
        Union[bytes, str]: 生成的图片字节流或错误信息。
    """
    if isinstance(await md_to_pic(md_str), bytes) is False:
        error_message = "md2pic: 图片生成失败"
        logger.error(error_message)
        raise ValueError(error_message)
    else:
        logger.trace("md2pic: success")
        return await md_to_pic(md_str)


def add_css(html_str: str, css_content: str = "", css_path: Union[Path,str] = "") -> str:
    if InputCheck().check_type_empty(html_str, str):
        if InputCheck().check_type(css_path, str):
            css_path = Path(css_path)
        css_content_exists = InputCheck().check_type_empty(css_content, str)
        css_path_exists = InputCheck().check_type_empty(css_path, Path)
        if css_content_exists and css_path_exists:
            logger.warning("add_css: 同时指定 CSS 内容和路径, 优先使用路径")
            css_content_exists = False
        if css_content_exists or css_path_exists:
            css_content = ""
            if css_path_exists:
                logger.trace(f"add_css: path: {css_path}")
                with open(css_path, 'r', encoding='utf-8') as css_file:
                    css_content = css_file.read()
            if css_content_exists:
                logger.trace("add_css: content")
                css_content += css_content
            soup = BeautifulSoup(html_str, 'html.parser')
            head = soup.head
            if not head:
                head = soup.new_tag('head')
                if soup.html is None:
                    logger.debug("add_css: HTML 标签不存在")
                soup.html.insert(0, head)

            # 创建 <style> 标签并插入 CSS 内容
            style_tag = soup.new_tag('style')
            style_tag.string = css_content
            head.append(style_tag)
            logger.trace("add_css: success")
        # 将修改后的 HTML 转换为字符串
        return str(soup)
    logger.error("add_css: HTML 解析失败")
    return html_str


async def html2pic(
    html_str: str,
    dark_mode: bool = False,
    filter_css: str = "",    
    ) -> Union[bytes, str]:
    """
    将 HTML 字符串中的指定元素转换为图片。

    Args:
        html_str (str): 包含 HTML 内容的字符串。
        dark_mode (bool): 是否启用黑暗模式。
        filter_css (str): 用于过滤的 CSS

    Returns:
        bytes: 生成的图片的字节数据。
    """
    if InputCheck().check_type_empty(html_str, str):
        logger.trace("html2pic: HTML 解析成功")
        html_str = add_css(html_str, css_path=(PathClass().rootpathcomplete('static/css.css')))
        logger.trace("html2pic: Base CSS 添加成功")
        if dark_mode:
            html_str = add_css(html_str, css_path=PathClass().rootpathcomplete('static/css-halloween.css'))
            logger.trace("html2pic: Dark Mode CSS 添加成功")
        if InputCheck().check_type_empty(filter_css, str):
            html_str = add_css(html_str, css_path=PathClass().rootpathcomplete(filter_css))
            logger.trace("html2pic: Filter CSS 添加成功")

        result = await html_to_pic(html=html_str)
        if result is None:
            error_message = "html2pic: 图片生成失败"
            logger.error(error_message)
            raise ValueError(error_message)
        else:
            return result
    elif isinstance(html_str, dict):
        error_message = "html2pic: HTML 解析失败"
        logger.error(error_message)
        raise ValueError(error_message)
    else:
        error_message = "html2pic: 未知错误"
        logger.error(error_message)
        raise ValueError(error_message)

