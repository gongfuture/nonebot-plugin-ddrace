import re
import html as htmllib
from typing import Union
from nonebot import require, logger, on_command
from nonebot.adapters import Bot as BaseBot, Event as BaseEvent, Message as BaseMessage , MessageSegment as BaseMessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent as V11MessageEvent
from nonebot.adapters.onebot.v12.event import MessageEvent as V12MessageEvent
from nonebot.params import CommandArg
from nonebot.typing import T_State

from ..models import DDRDataGet, html2pic
from ..utils import Trigger, CacheClass, constants, InputCheck
from ..config import PluginConfig

require("nonebot_plugin_htmlrender")
require("nonebot_plugin_saa")

from nonebot_plugin_saa import MessageFactory, MessageSegmentFactory, Image, Text

ddr_data_get = DDRDataGet()

points = on_command(
    "point",
    aliases={"points","查分","分数","破i你同事","ponits","poinst"},
    **Trigger().default_arg())

force_points = on_command(
    "fpoint",
    aliases={"fpoints","强制查分","刷新分数"},
    **Trigger().default_arg())

@points.handle()
async def points_handle(bot: BaseBot, event: Union[V12MessageEvent, V11MessageEvent], state: T_State, args: BaseMessage = CommandArg()):
    if name := args.extract_plain_text():
        cache = CacheClass()
        cache_name = constants.PLAYER_GLOBAL_RANKS_PICTURE_CACHE.format(player_name=name)
        if cache.cache_check(cache_name):
            if pic := cache.get_pic_cache(cache_name):
                message = Text(f" {name} 的成绩信息如下：") + Image(pic) + Text(f"""
                                                                        自动使用{cache.get_cache_exist_time(cache_name)}分钟前的缓存数据
                                                                        """)
                await message.send(**Trigger().send_config())
                logger.info(f"points_handle: {name} 成绩查询完成")
                await points.finish()
        else:
            return await force_points_handle(bot, event, state, args)
    else:
        await Text("名字呢？不给我名字我怎么查分？").send(**Trigger().send_config())
        await points.finish()

@force_points.handle()         
async def force_points_handle(bot: BaseBot, event: Union[V12MessageEvent, V11MessageEvent], state: T_State, args: BaseMessage = CommandArg()):
    if name := args.extract_plain_text():
        name = InputCheck().custom_escape(name)
        cache = CacheClass()
        cache_name = constants.PLAYER_GLOBAL_RANKS_PICTURE_CACHE.format(player_name=name)
        html = await ddr_data_get.result_page("player", name)
        # logger.debug(f"points_handle: {html}")
        if "error" in html:
            await Text("好像出了什么问题唔~").send(**Trigger().send_config())
            await points.finish()
        if "404error" in html:
            try:
                fuzzy_search_result = await ddr_data_get.fuzzy_search("player", name)
                if fuzzy_search_result:
                    formatted_result = "\n".join(
                        [f"{index + 1}. {item['name']} (分数:{item['points']})" for index, item in enumerate(fuzzy_search_result)]
                    )
                    await Text(f"没搜到呢，看看有你想要搜的嘛:\n{formatted_result}").send(**Trigger().send_config())
                else:
                    await Text(f"没找到 '{name}' 的成绩呢，换个关键词试试？").send(**Trigger().send_config())
                await points.finish()
            except ValueError:
                await Text(f"没找到 '{name}' 的成绩呢，换个关键词试试？").send(**Trigger().send_config())
                await points.finish()
        if isinstance(html, str):
            pic = await html2pic(html,True,filter_css="static/player_global_ranks.css")
        else:
            await Text("图片生成失败").send(**Trigger().send_config())
            await points.finish()
        if isinstance(pic, bytes):
            cache.store_pic_cache(cache_name, pic)
        else:
            await Text("图片生成失败").send(**Trigger().send_config())
            await points.finish()
        message = Text(f" {name} 的成绩信息如下：") + Image(pic)
        await message.send(**Trigger().send_config())
        logger.info(f"points_handle: {name} 成绩查询完成")
        await points.finish()
    else:
        await Text("名字呢？不给我名字我怎么查分？").send(**Trigger().send_config())
        await points.finish()
