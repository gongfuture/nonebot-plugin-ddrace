from pathlib import Path
from pydantic import BaseModel
from nonebot import get_driver, logger, get_plugin_config, require
from nonebot.compat import PYDANTIC_V2
require("nonebot_plugin_localstore")
import nonebot_plugin_localstore as store
if PYDANTIC_V2:
    from pydantic import field_validator as validator
else:
    from pydantic import validator
try:
    import ujson as json
except ModuleNotFoundError:
    import json
from .utils import PathClass


class PluginConfig(BaseModel):
    ddr_need_at: bool = False
    ddr_at_back: bool = False
    ddr_reply: bool = True
    ddr_priority: int = 10
    ddr_block: bool = True
    ddr_command_pre_alias: str = ""

    @validator("ddr_priority")
    @classmethod
    def check_priority(cls, v: int) -> int:
        if v >= 1:
            return v
        raise ValueError("weather command priority must greater than 1")


driver = get_driver()
ddr_config = get_plugin_config(PluginConfig)


@driver.on_startup
async def _() -> None:
    ddr_config_path: Path = store.get_plugin_config_dir()
    ddr_data_path: Path = store.get_plugin_data_dir()
    ddr_cache_path: Path = store.get_plugin_cache_dir()
    if not ddr_data_path.exists():
        ddr_data_path.mkdir(parents=True, exist_ok=True)

    config_json_path: Path = ddr_config_path / "ddrconfig.json"

    _config = {}
    if not config_json_path.exists():
        
        with open(config_json_path, 'w', encoding='utf-8') as f:
            json.dump(_config, f, ensure_ascii=False, indent=4)
        
        logger.info("Initialized the ddrconfig.json of DDRace plugin")

    data_path: Path = ddr_data_path / "ddrdata.json"

    if not data_path.exists():
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(dict(), f, ensure_ascii=False, indent=4)

        logger.info("Initialized the ddrdata.json of DDRace plugin")
