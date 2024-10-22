from pathlib import Path
from typing import List, Union
from bs4 import BeautifulSoup
from nonebot import require, logger
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import html_to_pic, md_to_pic
from ..utils import input_check, PathClass

def json2md(json_data: dict, title_filter: List[str]) -> str:
    """
    将 JSON 数据转换为 Markdown 表格格式的字符串。
    
    Args:
        json_data (dict): 包含数据的 JSON 字典。
        title_filter (List[str]): 包含表格标题的列表，用于过滤 JSON 数据中的键。
    
    Returns:
        str: 生成的 Markdown 表格格式的字符串。
    """
    if not isinstance(json_data, dict):
        error_message = "json2md: 数据格式错误"
        logger.error(error_message)
        raise ValueError(error_message)
    if not isinstance(title_filter, list):
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
    将 Markdown 字符串转换为图片。

    Args:
        md_str (str): Markdown 格式的字符串。

    Returns:
        Union[bytes, str]: 生成的图片的二进制数据，如果失败则返回错误信息。
    """
    try:
        return await md_to_pic(md_str)
    except Exception as e:
        error_message = f"md2pic: 图片生成失败: {e}"
        logger.error(error_message)
        return error_message

def add_css(html_str: str, css_content: str = "", css_path: Union[Path, str] = "") -> str:
    """
    为 HTML 字符串添加 CSS 样式。

    Args:
        html_str (str): HTML 格式的字符串。
        css_content (str, optional): CSS 样式内容。默认为空字符串。
        css_path (Union[Path, str], optional): CSS 文件路径。默认为空字符串。

    Returns:
        str: 添加 CSS 样式后的 HTML 字符串。
    """
    if input_check.check_type_empty(html_str, str):
        if input_check.check_type(css_path, str):
            css_path = Path(css_path)
        css_content_exists = input_check.check_type_empty(css_content, str)
        css_path_exists = input_check.check_type_empty(css_path, Path)
        if css_content_exists and css_path_exists:
            logger.warning("add_css: 同时指定 CSS 内容和路径, 优先使用路径")
            css_content_exists = False
        if css_content_exists or css_path_exists:
            css_content = ""
            if css_path_exists:
                logger.trace(f"add_css: path: {css_path}")
                try:
                    with open(css_path, 'r', encoding='utf-8') as css_file:
                        css_content = css_file.read()
                except Exception as e:
                    logger.error(f"add_css: 读取 CSS 文件失败: {e}")
                    return html_str
            if css_content_exists:
                logger.trace("add_css: content")
                css_content += css_content
            soup = BeautifulSoup(html_str, 'html.parser')
            head = soup.head
            if not head:
                head = soup.new_tag('head')
                if soup.html is None:
                    logger.debug("add_css: HTML 标签不存在")
                    return html_str
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

def add_footer(html_str: str) -> str:
    """
    将 section 下的 p 元素使用 div 包裹起来，并在 div 中原有 p 元素之前添加一个 <p>test</p> 元素。

    Args:
        html_str (str): 包含 HTML 内容的字符串。

    Returns:
        str: 修改后的 HTML 字符串。
    """
    soup = BeautifulSoup(html_str, 'html.parser')

    # 查找所有 section 元素
    section = soup.select_one('body > article > section')

    if section:
        # 查找 section 下的所有直接子元素 p
        p_elements = section.find_all('p', recursive=False)

        if p_elements:
            # 创建新的 div 元素
            new_div = soup.new_tag('div')
            new_div['style'] = 'display: flex; justify-content: space-around;'

            # 创建新的 <p>Support by nonebot-plugin-ddrace</p> 元素
            new_p = soup.new_tag('p')
            new_p['style'] = 'padding-left: 1em;'
            new_p.string = 'Support by nonebot-plugin-ddrace'

            # 将新的 <p>Support by nonebot-plugin-ddrace</p> 元素添加到新的 div 中
            new_div.append(new_p)

            # 将所有原有 p 元素添加到新的 div 中
            for p in p_elements:
                new_div.append(p.extract())

            # 将新的 div 元素插入到 section 中
            section.append(new_div)

    return str(soup)


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
        Union[bytes, str]: 生成的图片的字节数据，如果失败则返回错误信息。
    """
    if input_check.check_type_empty(html_str, str):
        logger.trace("html2pic: HTML 解析成功")
        try:
            html_str = add_css(html_str, css_path=PathClass().rootpathcomplete('static/css.css'))
            logger.trace("html2pic: Base CSS 添加成功")
            if dark_mode:
                html_str = add_css(html_str, css_path=PathClass().rootpathcomplete('static/css-halloween.css'))
                logger.trace("html2pic: Dark Mode CSS 添加成功")
            if input_check.check_type_empty(filter_css, str):
                html_str = add_css(html_str, css_path=PathClass().rootpathcomplete(filter_css))
                logger.trace("html2pic: Filter CSS 添加成功")
            html_str = add_footer(html_str)
            result = await html_to_pic(html=html_str)
            if result is None:
                error_message = "html2pic: 图片生成失败"
                logger.error(error_message)
                return error_message
            return result
        except Exception as e:
            error_message = f"html2pic: 图片生成过程中发生错误: {e}"
            logger.error(error_message)
            return error_message
    else:
        error_message = "html2pic: HTML 解析失败"
        logger.error(error_message)
        return error_message
