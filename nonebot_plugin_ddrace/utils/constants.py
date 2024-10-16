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


# region 生成图片相关
# Player Global Ranks
PLAYER_GLOBAL_RANKS_ELEMENT_IDS = "global" 
PLAYER_GLOBAL_RANKS_FILTER_IDS = "remote"
