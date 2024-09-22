from pydantic import BaseModel


class Config(BaseModel):
    """DDRace/DDNet成绩查询插件配置类。

    """
    ddr_plugin_enabled: bool = True
    """是否启用DDR插件"""
    ddr_command_priority: int = 10
    """用于设置DDR命令的优先级。"""
    ddr_command_alias: str = ""
    """用于设置DDR命令的别名。"""
    ddr_command_tobot: bool = False
    """用于设置DDR命令是否需要at机器人。"""


