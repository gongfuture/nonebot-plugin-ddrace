from nonebot import get_driver
from nonebot.log import logger
from pathlib import Path
from pydantic import BaseModel
from typing import Dict, Union
try:
    import ujson as json
except ModuleNotFoundError:
    import json


class PluginConfig(BaseModel, extra="ignore"):
    ddr_path: Path = Path(__file__).parent / "resource"


driver = get_driver()
ddr_config: PluginConfig = PluginConfig.model_validate(driver.config.model_dump()))


@driver.on_startup
async def _() -> None:
    if not ddr_config.ddr_path.exists():
        ddr_config.ddr_path.mkdir(parents=True, exist_ok=True)

    config_json_path: Path = ddr_config.ddr_path / "config.json"

    # Initial default config
    _config: Dict[str, Dict[str, Dict[str, Union[bool, int]]]] = {
        "morning": {
            "morning_intime": {
                "enable": True,
                "early_time": 6,
                "late_time": 12
            },
            "multi_get_up": {
                "enable": False,
                "interval": 6
            },
            "super_get_up": {
                "enable": False,
                "interval": 3
            }
        },
        "night": {
            "night_intime": {
                "enable": True,
                "early_time": 21,
                "late_time": 6
            },
            "good_sleep": {
                "enable": True,
                "interval": 6
            },
            "deep_sleep": {
                "enable": False,
                "interval": 3
            }
        }
    }

    if not config_json_path.exists():
        with open(config_json_path, 'w', encoding='utf-8') as f:
            json.dump(_config, f, ensure_ascii=False, indent=4)

        logger.info("Initialized the config.json of DDRace plugin")


    new_data_path: Path = ddr_config.ddr_path / "ddr_data.json"

    if not new_data_path.exists():
        with open(new_data_path, 'w', encoding='utf-8') as f:
            json.dump(dict(), f, ensure_ascii=False, indent=4)

        logger.warning("数据文件不存在，已重新创建数据文件！")