from pathlib import Path
from pydantic import BaseModel
from nonebot import get_driver, logger, get_plugin_config
from pydantic import Field
try:
    import ujson as json
except ModuleNotFoundError:
    import json
from .utils import constants


class PluginConfig(BaseModel):
    ddr_need_at: bool = False
    ddr_at_back: bool = False
    ddr_reply: bool = True
    ddr_priority: int = Field(default=10, ge=1)
    ddr_block: bool = True
    ddr_command_pre_alias: str = ""
    ddr_cache_time: int = Field(default=60, ge=0, description="缓存时间，单位为分钟，为 0 时不缓存，默认为 60 分钟")


driver = get_driver()
pluginconfig = get_plugin_config(PluginConfig)


@driver.on_startup
async def _() -> None:
    ddr_config_path: Path = constants.CONFIG_PATH
    ddr_data_path: Path = constants.DATA_PATH
    ddr_cache_path: Path = constants.CACHE_PATH

    if not ddr_config_path.exists():
        ddr_config_path.mkdir(parents=True, exist_ok=True)
    if not ddr_data_path.exists():
        ddr_data_path.mkdir(parents=True, exist_ok=True)
    if not ddr_cache_path.exists():
        ddr_cache_path.mkdir(parents=True, exist_ok=True)

    config_json_path = constants.CONFIG_JSON_PATH

    _config = {}
    if not config_json_path.exists():
        with open(config_json_path, 'w', encoding='utf-8') as f:
            json.dump(_config, f, ensure_ascii=False, indent=4)
        
        logger.info("Initialized the ddrconfig.json of DDRace plugin")

    data_path = constants.DATA_JSON_PATH

    if not data_path.exists():
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(dict(), f, ensure_ascii=False, indent=4)

        logger.info("Initialized the ddrdata.json of DDRace plugin")
