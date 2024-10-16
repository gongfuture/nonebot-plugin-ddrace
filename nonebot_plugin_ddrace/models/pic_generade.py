from pathlib import Path
from typing import List, Optional, Union
from bs4 import BeautifulSoup
from nonebot import require,logger
require("nonebot_plugin_htmlrender")
from nonebot_plugin_htmlrender import html_to_pic,md_to_pic
from ..utils import PathClass as PathClass



# @handle_exceptions
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
        raise ValueError("数据格式错误")
    if isinstance(title_filter, list) is False:
        raise ValueError("标题格式错误")

    md_str = ""
    # 生成表格头
    headers = [key for key in title_filter if key in json_data]
    md_str = "| " + " | ".join(headers) + " |\n"
    md_str += "| " + " | ".join(["---"] * len(headers)) + " |\n"

    # 生成表格数据
    for key in title_filter:
        if key in json_data:
            md_str += "| " + " | ".join(str(json_data[key])) + " |\n"

    return md_str

# @handle_exceptions
async def md2pic(md_str: str) -> Union[bytes, str]:
    """
    将 Markdown 字符串转换为图片字节流。
    
    Args:
        md_str (str): 要转换的 Markdown 字符串。

    Returns:
        Union[bytes, str]: 生成的图片字节流或错误信息。
    """
    if isinstance(await md_to_pic(md_str), bytes) is False:
        raise ValueError("图片生成失败")
    else:
        return await md_to_pic(md_str)


def add_css(html_str: str, css_content: str = "", css_path: Path = Path("")) -> str:
    if isinstance(html_str, str):
        css_content_exists = isinstance(css_content, str) and css_content != ""
        css_path_exists = isinstance(css_path, Path) and css_path != Path("")
        if css_content_exists or css_path_exists:
            css_content = ""
            if css_path_exists:
                with open(css_path, 'r', encoding='utf-8') as css_file:
                    css_content = css_file.read()
            if css_content_exists:
                css_content += css_content
            soup = BeautifulSoup(html_str, 'html.parser')
            head = soup.head
            if not head:
                head = soup.new_tag('head')
                soup.html.insert(0, head)

            # 创建 <style> 标签并插入 CSS 内容
            style_tag = soup.new_tag('style')
            style_tag.string = css_content
            head.append(style_tag)
            logger.debug(f"add_css: {css_path}")
        # 将修改后的 HTML 转换为字符串
        return str(soup)

# @handle_exceptions
async def html2pic(
    html_str: str, 
    
    ) -> Union[bytes, str]:
    """
    将 HTML 字符串中的指定元素转换为图片。

    Args:
        html_str (str): 包含 HTML 内容的字符串。
        element_ids (List[str]): 需要提取的元素的 ID 列表。
        filter_ids (List[str], optional): 需要过滤掉的元素的 ID 列表。默认为 None。

    Returns:
        bytes: 生成的图片的字节数据。
    """
    if isinstance(html_str, str):  
        html_with_base_css = add_css(html_str, css_path=Path((PathClass().rootpathcomplete('static/css.css'))))
        html_with_dark_css = add_css(html_with_base_css,  css_path=Path(PathClass().rootpathcomplete('static/css-halloween.css')))
        html_with_filter_css = add_css(html_with_dark_css,  css_path=Path(PathClass().rootpathcomplete('static/player_global_ranks.css')))

        result = await html_to_pic(html=html_with_filter_css)
        if result is None:
            raise ValueError("图片生成失败")
        else:
            return result
    elif isinstance(html_str, dict):
        raise ValueError("HTML 解析失败")
    else:
        raise ValueError("未知错误")


