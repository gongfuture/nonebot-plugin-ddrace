from nonebot.rule import Rule, to_me

from ..config import PluginConfig


class Trigger:
    def rule(self) -> Rule:
        rule = Rule()
        if PluginConfig().ddr_need_at:
            rule = rule & to_me()
        return rule

    def send_config(self) -> dict:
        send_config = {}
        if PluginConfig().ddr_at_back:
            send_config["at_sender"] = True
        if PluginConfig().ddr_reply:
            send_config["reply"] = True
        return send_config

    def default_arg(self) -> dict:
        cmd_arg = {} 
        if PluginConfig().ddr_block:
            cmd_arg["block"] = True
        cmd_arg["priority"] = PluginConfig().ddr_priority
        cmd_arg["rule"] = self.rule()
        return cmd_arg