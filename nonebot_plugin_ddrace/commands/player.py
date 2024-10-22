from typing import Union
from nonebot import logger, on_command, require
from nonebot.adapters import Message as BaseMessage
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent as V11PrivateMessageEvent, GroupMessageEvent as V11GroupMessageEvent
from nonebot.adapters.onebot.v12.event import PrivateMessageEvent as V12PrivateMessageEvent, GroupMessageEvent as V12GroupMessageEvent

from nonebot.params import CommandArg

from ..models import DDRDataGet, html2pic, userbind
from ..utils import CacheClass, constants, input_check, command_arg, default_arg, send_config
require("nonebot_plugin_saa")
from nonebot_plugin_saa import MessageFactory, MessageSegmentFactory, Image, Text

ddr_data_get = DDRDataGet()
bind = userbind


points = on_command(**command_arg(
    cmd = "point",
    aliases={"points","查分","分数","破i你同事","ponits","poinst"}),
    **default_arg())

force_points = on_command(**command_arg(
    cmd = "fpoint",
    aliases={"fpoints","强制查分","刷新分数"}),
    **default_arg())

@points.handle()
async def points_handle(event: Union[V11GroupMessageEvent, V12GroupMessageEvent], args: BaseMessage = CommandArg()):
    name = args.extract_plain_text()
    if not name:
        try:
            input_check.check_id_types(event.group_id, event.user_id)
            name_bind = bind.get_group_user_bind(event.group_id, event.user_id)
            if name_bind:
                name = name_bind
            else:
                name = event.sender.card
                await Text(f"初次在本群使用，自动绑定 {name} ").send(**send_config())
                bind.add_group_user(event.group_id, event.user_id, name)
        except ValueError as e:
            await Text(f"错误的IDs:{event.group_id},{event.user_id}").send(**send_config())
            logger.error(f"points_handle: {e}")
            await points.finish()
            raise e

    cache = CacheClass()
    cache_name = constants.PLAYER_GLOBAL_RANKS_PICTURE_CACHE.format(player_name=name)
    if cache.cache_check(cache_name):
        if pic := cache.get_pic_cache(cache_name):
            message = Text(f" {name} 的成绩信息如下：") + Image(pic) + Text(f"\n自动使用{cache.get_cache_exist_time(cache_name)}分钟前的缓存数据\n强制刷新请使用/fpoint <name>")
            await message.send(**send_config())
            logger.info(f"points_handle: {name} 成绩查询完成")
            await points.finish()
    else:
        return await force_points_handle(event, name)

@force_points.handle()         
async def force_points_handle(event: Union[V11GroupMessageEvent,V12GroupMessageEvent], args: BaseMessage = CommandArg()):
    if args:
        if isinstance(args, str):
            name = args
        if isinstance(args, BaseMessage):
            name = args.extract_plain_text()
        search_name = input_check.custom_escape(name)
        cache = CacheClass()
        cache_name = constants.PLAYER_GLOBAL_RANKS_PICTURE_CACHE.format(player_name=name)
        html = await ddr_data_get.result_page("player", search_name)
        # logger.debug(f"points_handle: {html}")
        if "error" in html:
            await Text("网络波动~ 再试一次？").send(**send_config())
            await points.finish()
        if "404error" in html:
            try:
                fuzzy_search_result = await ddr_data_get.fuzzy_search("player", name)
                if fuzzy_search_result:
                    formatted_result = "\n".join(
                        [f"{index + 1}. {item['name']} (分数:{item['points']})" for index, item in enumerate(fuzzy_search_result)]
                    )
                    await Text(f"没搜到呢，看看有你想要搜的嘛:\n{formatted_result}").send(**send_config())
                else:
                    await Text(f"没找到 '{name}' 的成绩呢，换个关键词试试？").send(**send_config())
                await points.finish()
            except ValueError:
                await Text(f"没找到 '{name}' 的成绩呢，换个关键词试试？").send(**send_config())
                await points.finish()
        if isinstance(html, str):
            pic = await html2pic(html,True,filter_css="static/player_global_ranks.css")
        else:
            await Text("图片生成失败").send(**send_config())
            await points.finish()
        if isinstance(pic, bytes):
            cache.store_pic_cache(cache_name, pic)
        else:
            await Text("图片生成失败").send(**send_config())
            await points.finish()
        message = Text(f" {name} 的成绩信息如下：") + Image(pic)
        await message.send(**send_config())
        logger.info(f"points_handle: {name} 成绩查询完成")
        await points.finish()
    else:
        await Text("名字呢？不给我名字我怎么查分？").send(**send_config())
        await points.finish()
