from nonebot.rule import Rule, to_me

from ..config import pluginconfig

class Trigger:
    def rule(self) -> Rule:
        rule = Rule()
        if pluginconfig.ddr_need_at:
            rule = rule & to_me()
        return rule

    def send_config(self) -> dict:
        send_config = {}
        if pluginconfig.ddr_at_back:
            send_config["at_sender"] = True
        if pluginconfig.ddr_reply:
            send_config["reply"] = True
        return send_config

    def default_arg(self) -> dict:
        cmd_arg = {} 
        if pluginconfig.ddr_block:
            cmd_arg["block"] = True
        cmd_arg["priority"] = pluginconfig.ddr_priority
        cmd_arg["rule"] = self.rule()
        return cmd_arg

    def command_arg(self, cmd: str, aliases: set) -> dict:
        pre_alias = pluginconfig.ddr_command_pre_alias
        cmd_arg = {}
        cmd_arg["cmd"] =pre_alias+cmd
        cmd_arg["aliases"] = {pre_alias + alias for alias in aliases}
        return cmd_arg
        