try:
    import ujson as json
except ModuleNotFoundError:
    import json
import os
from nonebot import logger
from typing import Dict, Union, List
from ..utils import constants


data_file = constants.DATA_JSON_PATH

class UserBindClass:
    GroupUserBind = Dict[str, str]
    GroupBind = Dict[str, GroupUserBind]
    PrivateBind = Dict[str, str]
    UserData = Dict[str, Union[GroupBind, PrivateBind]]
    
    def __init__(self):
        self.data = self.load_data()
        logger.debug(f"Initialized data: {self.data}")
        
    def load_data(self) -> UserData:
        if not os.path.exists(data_file):
            with open(data_file, 'w', encoding='utf-8') as f:
                json.dump({"group": {}, "private": {}}, f, ensure_ascii=False, indent=4)
                logger.info("Initialized the ddrdata.json of DDRace plugin")
            return {"group": {}, "private": {}}
        with open(data_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not isinstance(data, dict):
                return {"group": {}, "private": {}}
            if "group" not in data:
                data["group"] = {}
            if "private" not in data:
                data["private"] = {}
            logger.debug(data)
            return data

    def save_data(self) -> None:
        with open(data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)
        logger.debug(f"Data saved to ddrdata.json: {self.data}")

    def add_group_user(self, group_id: Union[str, int], user_id: Union[str, int], user_bind: str) -> None:
        if isinstance(group_id, int):
            group_id = str(group_id)
        if isinstance(user_id, int):
            user_id = str(user_id)
        if group_id.startswith("*"):
            for group in self.data["group"]:
                if user_id in self.data["group"][group]:
                    self.data["group"][group][user_id] = user_bind
        else:
            if group_id not in self.data["group"]:
                self.data["group"][group_id] = {}
            self.data["group"][group_id][user_id] = user_bind
        logger.debug(f"Added group user: group_id={group_id}, user_id={user_id}, user_bind={user_bind}")
        self.save_data()

    def add_private_user(self, user_id: Union[str, int], user_bind: Union[str, int]) -> None:
        if isinstance(user_id, int):
            user_id = str(user_id)
        if "private" not in self.data:
            self.data["private"] = {}
        self.data["private"][user_id] = user_bind
        logger.debug(f"Added private user: user_id={user_id}, user_bind={user_bind}")
        self.save_data()

    def get_data(self) -> UserData:
        return self.data

    def get_group_user_bind(self, group_id: Union[str, int], user_id: Union[str, int]) -> str:
        if isinstance(group_id, int):
            group_id = str(group_id)
        if isinstance(user_id, int):
            user_id = str(user_id)
        if group_id in self.data["group"]:
            if user_id in self.data["group"][group_id]:
                return self.data["group"][group_id][user_id]
        logger.debug(f"Group user bind not found: group_id={group_id}, user_id={user_id}")
        return ""

    def get_private_user_bind(self, user_id: Union[str, int]) -> str:
        if isinstance(user_id, int):
            user_id = str(user_id)
        if user_id in self.data["private"]:
            return self.data["private"][user_id]
        logger.debug(f"Private user bind not found: user_id={user_id}")
        return ""

    def del_group_user_bind(self, group_id: Union[str, int], user_id: Union[str, int]) -> None:
        if isinstance(group_id, int):
            group_id = str(group_id)
        if isinstance(user_id, int):
            user_id = str(user_id)
        if group_id.startswith("*"):
            for group in self.data["group"]:
                if user_id in self.data["group"][group]:
                    del self.data["group"][group][user_id]
            self.save_data()
            return
        if group_id in self.data["group"]:
            if user_id in self.data["group"][group_id]:
                del self.data["group"][group_id][user_id]
                logger.debug(f"Deleted group user bind: group_id={group_id}, user_id={user_id}")
                self.save_data()
                return
        logger.debug(f"Group user bind not found: group_id={group_id}, user_id={user_id}")

    def del_private_user_bind(self, user_id: Union[str, int]) -> None:
        if isinstance(user_id, int):
            user_id = str(user_id)
        if user_id in self.data["private"]:
            del self.data["private"][user_id]
            logger.debug(f"Deleted private user bind: user_id={user_id}")
            self.save_data()
            return
        logger.debug(f"Private user bind not found: user_id={user_id}")
        