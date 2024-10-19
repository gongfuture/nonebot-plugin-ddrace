from typing import Union
from nonebot import require, logger, on_command
from nonebot.adapters import Bot as BaseBot, Event as BaseEvent, Message as BaseMessage , MessageSegment as BaseMessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent as V11MessageEvent
from nonebot.adapters.onebot.v12.event import MessageEvent as V12MessageEvent
from nonebot.params import CommandArg, Depends
from nonebot.rule import Rule, to_me
from nonebot.typing import T_State

from ..models import *
from ..utils import *
from ..config import PluginConfig

require("nonebot_plugin_htmlrender")
require("nonebot_plugin_saa")

from nonebot_plugin_saa import MessageFactory, MessageSegmentFactory, Image, Text

points = on_command(
    "point",
    aliases={"points","查分","rank","ranks","分数"},
    **Trigger().default_arg())

# @points.got("name", prompt="名字呢？不给我名字我怎么查分？")
@points.handle()
async def points_handle(bot: BaseBot, event: Union[V12MessageEvent, V11MessageEvent], state: T_State, args: BaseMessage = CommandArg()):
    if name := args.extract_plain_text():
        html = await result_page("player", name)
        # logger.debug(f"points_handle: {html}")
        if "404error" in html:
            await Text(f"没找到 '{name}' 的成绩呢，换个关键词试试？").send(**Trigger().send_config())
            await points.reject_arg("name")
        pic = await html2pic(html,True,filter_css="static/player_global_ranks.css")
        message = Text(f" {name} 的成绩信息如下：") + Image(pic)
        await message.send(**Trigger().send_config())
        logger.info(f"points_handle: {name} 成绩查询完成")
        await points.finish()

