from pathlib import Path
from pydantic import BaseModel, Extra
from nonebot import get_driver, logger
try:
    import ujson as json
except ModuleNotFoundError:
    import json

class PluginConfig(BaseModel, extra=Extra.ignore):
    ddr_need_at: bool = False
    ddr_command_pre_alias: str = ""
    ddr_data_path: Path = Path(__file__).parent / "data"

    # @validator("weather_command_priority")
    # @classmethod
    # def check_priority(cls, v: int) -> int:
    #     if v >= 1:
    #         return v
    #     raise ValueError("weather command priority must greater than 1")


# 参考自[nonebot_plugin_morning](https://github.com/MinatoAquaCrews/nonebot_plugin_morning) 感谢

driver = get_driver()
ddr_config: PluginConfig = PluginConfig.parse_obj(driver.config.dict())


@driver.on_startup
async def _() -> None:
    if not ddr_config.ddr_data_path.exists():
        ddr_config.ddr_data_path.mkdir(parents=True, exist_ok=True)

    # config_json_path: Path = ddr_config.ddr_data_path / "ddrconfig.json"

    # _config = {}
    # if not config_json_path.exists():
    #     with open(config_json_path, 'w', encoding='utf-8') as f:
    #         json.dump(_config, f, ensure_ascii=False, indent=4)

    #     logger.info("Initialized the ddrconfig.json of DDRace plugin")

    data_path: Path = ddr_config.ddr_data_path / "ddrdata.json"

    if not data_path.exists():
        with open(data_path, 'w', encoding='utf-8') as f:
            json.dump(dict(), f, ensure_ascii=False, indent=4)

        logger.info("Initialized the ddrdata.json of DDRace plugin")
