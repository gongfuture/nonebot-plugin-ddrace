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
require("nonebot_plugin_localstore")
require("nonebot_plugin_apscheduler")

from nonebot_plugin_saa import MessageFactory, MessageSegmentFactory, Image, Text

from .commands import *


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

