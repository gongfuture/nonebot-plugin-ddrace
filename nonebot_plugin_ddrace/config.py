from pathlib import Path
from pydantic import BaseModel
from nonebot import get_driver, logger, get_plugin_config
from pydantic import Field
try:
    import ujson as json
except ModuleNotFoundError:
    import json
from .utils import PathClass, constants


class PluginConfig(BaseModel):
    ddr_need_at: bool = False
    ddr_at_back: bool = False
    ddr_reply: bool = True
    ddr_priority: int = Field(10, ge=1)
    ddr_block: bool = True
    ddr_command_pre_alias: str = ""


driver = get_driver()
ddr_config = get_plugin_config(PluginConfig)


@driver.on_startup
async def _() -> None:
    ddr_config_path: Path = PathClass().ddrconfigpath()
    ddr_data_path: Path = PathClass().ddrdatapath()

    if not ddr_data_path.exists():
        ddr_data_path.mkdir(parents=True, exist_ok=True)

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
