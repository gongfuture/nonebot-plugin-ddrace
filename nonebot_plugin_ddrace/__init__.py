from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import on_command
from nonebot.rule import to_me
from nonebot.exception import MatcherException

from .config import Config\


__ddr_version__ = "0.0.1"
__ddr_usage__ = f"""

""".strip()

__plugin_meta__ = PluginMetadata(
    name="DDRace/DDNet成绩查询",
    description="提供DDRace/DDNet成绩查询功能",
    usage=__ddr_usage__,
    type="application",
    homepage="https://github.com/gongfuture/nonebot-plugin-ddrace",
    config=Config,
    supported_adapters={"~onebot.v11"},
    extra={
        "author": "Github @gongfuture",
        "version": __ddr_version__
    },
)

config = get_plugin_config(Config)

