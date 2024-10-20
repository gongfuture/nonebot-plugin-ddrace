import json
from typing import Union
from nonebot import require, logger
from pathlib import Path
from datetime import datetime, timedelta
from ..utils import PathClass, constants
from ..config import PluginConfig
require("nonebot_plugin_apscheduler")
from nonebot_plugin_apscheduler import scheduler
import hashlib

cache_path:Path = PathClass().ddrcachepath()
cache_time_file = constants.CACHE_TIME_FILE
cache_time = PluginConfig().ddr_cache_time

class CacheClass:

    def __init__(self):
        self.cache_path = PathClass().ddrcachepath()
        scheduler.add_job(self.clear_cache, "interval", minutes=cache_time)


    def _get_cache_file_path(self, key: str, suffix:str = "") -> Path:
        # 对 key 进行哈希处理，避免特殊字符和路径分隔符问题
        hashed_key = hashlib.md5(key.encode()).hexdigest()
        return self.cache_path / f"{hashed_key}{suffix}"

    def store_dict_cache(self, key: str, value: dict) -> None:
        cache_file_path = self._get_cache_file_path(key, ".json")
        try:
            if not cache_file_path.exists():
                with open(cache_file_path, "w", encoding="utf-8") as f:
                    json.dump(value, f, ensure_ascii=False, indent=4)
                logger.debug(f"Stored cache: {key}")
        except Exception as e:
            logger.error(f"Failed to store cache: {key}, error: {e}")

    def store_pic_cache(self, key: str, pic_data: bytes) -> None:
        cache_file_path = self._get_cache_file_path(key, ".png")
        try:
            if not cache_file_path.exists():
                with open(cache_file_path, "wb") as f:
                    f.write(pic_data)
                logger.debug(f"Stored pic cache: {key}")
        except Exception as e:
            logger.error(f"Failed to store pic cache: {key}, error: {e}")

    def get_dict_cache(self, key: str) -> Union[dict, str]:
        cache_file_path = self._get_cache_file_path(key, ".json")
        try:
            if cache_file_path.exists():
                with open(cache_file_path, "r", encoding="utf-8") as f:
                    return json.load(f)
            else:
                return "NotExist"
        except Exception as e:
            logger.error(f"Failed to get cache: {key}, error: {e}")
            return "Error"

    def get_pic_cache(self, key: str) -> Union[bytes, str]:
        cache_file_path = self._get_cache_file_path(key, ".png")
        try:
            if cache_file_path.exists():
                with open(cache_file_path, "rb") as f:
                    return f.read()
            else:
                return "NotExist"
        except Exception as e:
            logger.error(f"Failed to get pic cache: {key}, error: {e}")
            return "Error"

    def get_cache_time(self, key: str) -> int:
        cache_file_path = self._get_cache_file_path(key)
        if cache_file_path.exists():
            return int(cache_file_path.stat().st_mtime)
        else:
            return 0
    
    def get_cache_exist_time(self, key: str) -> int:
        cache_exist_time = self.get_cache_time(key)
        if cache_exist_time:
            return int(datetime.now().timestamp()) - cache_exist_time
        else:
            return -1

    def clear_cache(self) -> None:
        now = int(datetime.now().timestamp())
        for file in self.cache_path.iterdir():
            if file.is_file():
                file_time = int(file.stat().st_mtime)
                if now - file_time > cache_time * 60:
                    try:
                        file.unlink()
                        logger.debug(f"Deleted cache: {file.name}")
                    except Exception as e:
                        logger.error(f"Failed to delete cache: {file.name}, error: {e}")
        logger.info("Cleared cache")