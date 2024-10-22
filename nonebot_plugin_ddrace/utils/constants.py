import nonebot
from .tools import PathClass
from ..config import pluginconfig

config = nonebot.get_driver().config

PRE_ALIAS = pluginconfig.ddr_command_pre_alias
COMMAND_START = config.command_start
COMMADN_SEP = config.command_sep

# region Path
CONFIG_PATH = PathClass().ddrconfigpath()
DATA_PATH = PathClass().ddrdatapath()
CACHE_PATH = PathClass().ddrcachepath()

CONFIG_JSON_PATH = CONFIG_PATH / "ddrconfig.json"
DATA_JSON_PATH = DATA_PATH / "ddrdata.json"
CACHE_TIME_FILE = CACHE_PATH / "_cache_time_record.json"

# endregion

# region Cache

# 图片缓存文件名
PLAYER_GLOBAL_RANKS_PICTURE_CACHE = "player_global_ranks_{player_name}.png"
MAP_GLOBAL_RANKS_PICTURE_CACHE = "map_global_ranks_{map_name}.png"

# 数据JSON缓存文件名
PLAYER_PROFILE_JSON_CACHE = "player_profile_{player_name}.json"
MAP_PROFILE_JSON_CACHE = "map_profile_{map_name}.json"

# 预搜索JSON缓存文件名
PLAYER_PRESEARCH_JSON_CACHE = "player_presearch_{player_name}.json"
MAP_PRESEARCH_JSON_CACHE = "map_presearch_{map_name}.json"

# endregion



# region DDRace相关内容

# 主域名
DDR_ROOT_URL = "https://ddnet.org/"


# region STATUS
# STATUS总览URL
STATUS_ROOT_URL = DDR_ROOT_URL + "status/"
# 服务器总览URL
SERVER_ROOT_URL = DDR_ROOT_URL + "stats/server/"

# endregion


# region RANK
# RANK总览URL
RANK_ROOT_URL = DDR_ROOT_URL + "ranks/"
# 预查询URL，下方补全提示，GET
# 参数格式例The ZyZya的参数为The%20ZyZya,特殊符号%HEX
MAP_QUERY_URL = DDR_ROOT_URL + "maps/?query={}"
MAPPER_QUERY_URL = DDR_ROOT_URL + "maps/?qmapper={}"
PLAYER_QUERY_URL = DDR_ROOT_URL + "players/?query={}"
# 子页面URL
# 参数格式例Sunny Side Up的参数为Sunny-32-Side-32-Up，特殊符号-DEC-
# 可使用 JSON website 获取
MAP_PAGE_URL= DDR_ROOT_URL + "maps/{}"
MAPPER_PAGE_URL = DDR_ROOT_URL + "mappers/{}"
PLAYER_PAGE_URL = DDR_ROOT_URL + "players/{}/"
# JSON URL
# 参数格式例Sunny Side Up的参数为Sunny+Side+Up，空格为+，特殊符号%HEX，测试后发现%20也可
MAP_JSON_URL = DDR_ROOT_URL + "maps/?json={}"
# NO MAPPER_JSON_URL
PLAYER_JSON_URL = DDR_ROOT_URL + "players/?json2={}"

# endregion


# region SKIN DATABASE
# SKIN总览URL，查询参数?search=
SKIN_ROOT_URL = DDR_ROOT_URL + "skins/index.php"

# endregion

# endregion
