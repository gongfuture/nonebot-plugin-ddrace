from nonebot import get_driver, require, logger, on_command
from nonebot.adapters import Bot as BaseBot, Event as BaseEvent, Message as BaseMessage , MessageSegment as BaseMessageSegment
from nonebot.adapters.onebot.v11.event import MessageEvent as V11MessageEvent
from nonebot.adapters.onebot.v12.event import MessageEvent as V12MessageEvent
from nonebot.adapters.console import Bot as ConsoleBot
from nonebot.params import CommandArg, Depends
from nonebot.plugin import PluginMetadata
from nonebot.rule import Rule, to_me
from nonebot.typing import T_State

from .models import *
from .utils import *
from typing import Union

require("nonebot_plugin_htmlrender")
require("nonebot_plugin_saa")

from nonebot_plugin_saa import MessageFactory, MessageSegmentFactory, Image, Text

import asyncio

driver = get_driver()

#region metadata
__version__ = "0.0.1"
__usage__ = f"""

""".strip()

__plugin_meta__ = PluginMetadata(
    name="DDRace/DDNet成绩查询",
    description="提供DDRace/DDNet成绩查询功能",
    usage=__usage__,
    type="application",
    homepage="https://github.com/gongfuture/nonebot-plugin-ddrace",
    supported_adapters={"~onebot.v11"},
    extra={
        "author": "Github @gongfuture",
        "version": __version__
    },
)
#endregion

def check_empty_arg_rule(arg: BaseMessage = CommandArg()):
    return not arg.extract_plain_text()

# def trigger_rule():
#     rule = Rule(check_empty_arg_rule)
#     if config.ddr_need_at:
#         rule = rule & to_me()
#     return rule

# rank = on_command("rank",aliases={"ranks","排行"}, priority=13)
points = on_command("point",aliases={"points","查分"}, priority=13, block=True)
test = on_command("test", priority=13,
                #   rule=trigger_rule(),
                  block=True)

@test.handle()
@test.got("args", prompt="请提供查询参数")
async def test_handle(bot: ConsoleBot, event: BaseEvent,args: T_State):
    logger.debug(f"test_handle: {args}")
    await test.finish()


@points.handle()
async def points_handle(bot: BaseBot, event: Union[V12MessageEvent, V11MessageEvent], args: BaseMessage = CommandArg()):
    if name := args.extract_plain_text():
        html = await result_page("player", name)
        pic = await html2pic(html)
        message = Image(pic)
        await message.send()
        await points.finish()
        