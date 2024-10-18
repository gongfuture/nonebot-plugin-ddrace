import asyncio
import importlib.metadata
from typing import Union
from nonebot import get_driver, get_plugin_config, require, logger, on_command
from nonebot.adapters import Bot as BaseBot, Event as BaseEvent, Message as BaseMessage , MessageSegment as BaseMessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent as V11MessageEvent
from nonebot.adapters.onebot.v12.event import MessageEvent as V12MessageEvent
from nonebot.params import CommandArg, Depends
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule, to_me
from nonebot.typing import T_State

from .models import *
from .utils import *
from .config import PluginConfig
from . import _version

require("nonebot_plugin_htmlrender")
require("nonebot_plugin_saa")

from nonebot_plugin_saa import MessageFactory, MessageSegmentFactory, Image, Text

driver = get_driver()
plugin_config = get_plugin_config(PluginConfig)

#region metadata
__version__ = _version.__version__
__usage__ = f"""
    points <name> - 查询 <name> 的 DDNet 成绩
""".strip()

__plugin_meta__ = PluginMetadata(
    name="DDNet 成绩查询",
    description="提供 DDNet 成绩查询功能",
    usage=__usage__,
    type="application",
    homepage="https://github.com/gongfuture/nonebot-plugin-ddrace",
    config=PluginConfig,
    supported_adapters={"~onebot.v11"},
    extra={
        "author": "Github @gongfuture",
        "version": __version__
    },
)
#endregion

def check_empty_arg_rule(arg: BaseMessage = CommandArg()):
    return not arg.extract_plain_text()

def trigger_rule():
    rule = Rule()
    if plugin_config.ddr_need_at:
        rule = rule & to_me()
    return rule


points = on_command("point",aliases={"points","查分","rank","ranks","分数"}, rule=trigger_rule(), priority=13, block=True)
# test = on_command("test", priority=13,
#                 #   rule=trigger_rule(),
#                   block=True)

# @test.handle()
# @test.got("args", prompt="请提供查询参数")
# async def test_handle(bot: ConsoleBot, event: BaseEvent,args: T_State):
#     logger.debug(f"test_handle: {args}")
#     await test.finish()


@points.handle()
async def points_handle(bot: BaseBot, event: Union[V12MessageEvent, V11MessageEvent], args: BaseMessage = CommandArg()):
    if name := args.extract_plain_text():
        html = await result_page("player", name)
        logger.debug(f"points_handle: {html}")
        if "404error" in html:
            await Text(f"未找到 {name} 的成绩信息如下：").send(at_sender=True, reply=True)
            await points.reject()
        pic = await html2pic(html,True,filter_css="static/player_global_ranks.css")
        message = Text(f" {name} 的成绩") + Image(pic)
        await message.send(at_sender=True, reply=True)
        await points.finish()

