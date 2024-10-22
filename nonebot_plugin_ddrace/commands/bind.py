from nonebot_plugin_saa import MessageFactory, MessageSegmentFactory, Image, Text
from typing import Union
from nonebot import logger, on_command, require
from nonebot.adapters import Message as BaseMessage
from nonebot.adapters.onebot.v11.event import PrivateMessageEvent as V11PrivateMessageEvent, GroupMessageEvent as V11GroupMessageEvent
from nonebot.adapters.onebot.v12.event import PrivateMessageEvent as V12PrivateMessageEvent, GroupMessageEvent as V12GroupMessageEvent
from nonebot.params import CommandArg

from ..utils import command_arg, default_arg, send_config, constants, input_check
from ..models import userbind

require("nonebot_plugin_saa")

bind = userbind

_bind_usage = """群聊：
/binds(绑定) <name> - 在本群绑定 <name> 
/unbinds(解绑) - 在本群解绑

私聊：
/binds(绑定) <name> - 在私聊绑定 <name>
/unbinds(解绑) - 在私聊解绑
/bindg(绑定群) <group_id> <name> - 在指定群绑定 <name>
/bindg(绑定群)  * <name> - 在所有群绑定 <name>
/unbindg(解绑群) <group_id> - 在指定群解绑
/unbindg(解绑群) * - 在所有群解绑

例子：
/binds 洛初
/解绑 
/bindg 123456789 洛初
/unbindg *
"""

bind_cmd = on_command(**command_arg(
    cmd="binds",
    aliases={"绑定"}),
    **default_arg())

bind_group = on_command(**command_arg(
    cmd="bindg",
    aliases={"绑定群", "bindq"}),
    **default_arg())

unbind_cmd = on_command(**command_arg(
    cmd="unbinds",
    aliases={"解绑"}),
    **default_arg())

unbind_group = on_command(**command_arg(
    cmd="unbindg",
    aliases={"解绑群", "unbindq"}),
    **default_arg())


@bind_cmd.handle()
async def group_bind_handle(event: Union[V11GroupMessageEvent, V12GroupMessageEvent], args: BaseMessage = CommandArg()):
    if name := args.extract_plain_text():
        group_id = event.group_id
        user_id = event.user_id
        bind.add_group_user(group_id, user_id, name)
        await Text(f"已绑定 {name} ").send(**send_config())
        await bind_cmd.finish()
    await Text(_bind_usage).send(**send_config())
    await bind_cmd.finish()


@bind_cmd.handle()
async def private_bind_handle(event: Union[V11PrivateMessageEvent, V12PrivateMessageEvent], args: BaseMessage = CommandArg()):
    if name := args.extract_plain_text():
        user_id = event.user_id
        bind.add_private_user(user_id, name)
        await Text(f"已绑定 {name} ").send(**send_config())
        await bind_cmd.finish()
    await Text(_bind_usage).send(**send_config())


@bind_group.handle()
async def private_group_bind_handle(event: Union[V11PrivateMessageEvent, V12PrivateMessageEvent], args: BaseMessage = CommandArg()):
    if arg := args.extract_plain_text():
        parts = arg.split()
        if len(parts) < 2:
            error_msg = "Invalid arguments. Usage: <group_id> <name>"
            logger.error(f"group_bind: {error_msg}")
            await Text(error_msg).send(**send_config())
            await bind_cmd.finish()
            return

        group_id, name = parts[0], " ".join(parts[1:])
        user_id = event.user_id
        bind.add_group_user(group_id, user_id, name)
        if group_id == "*":
            await Text(f"已在所有查询过的群绑定 {name}").send(**send_config())
        else:
            await Text(f"已在群 {group_id} 绑定 {name}").send(**send_config())
        await bind_cmd.finish()


@unbind_cmd.handle()
async def unbind_handle(event: Union[V11GroupMessageEvent, V12GroupMessageEvent]):
    group_id = event.group_id
    user_id = event.user_id
    bind.del_group_user_bind(group_id, user_id)
    await Text("已解绑").send(**send_config())
    await unbind_cmd.finish()


@unbind_cmd.handle()
async def private_unbind_handle(event: Union[V11PrivateMessageEvent, V12PrivateMessageEvent]):
    user_id = event.user_id
    bind.del_private_user_bind(user_id)
    await Text("已解绑").send(**send_config())
    await unbind_cmd.finish()


@unbind_group.handle()
async def unbind_group_handle(event: Union[V11PrivateMessageEvent, V12PrivateMessageEvent], args: BaseMessage = CommandArg()):
    if arg := args.extract_plain_text():
        group_id = arg
        user_id = event.user_id
        bind.del_group_user_bind(group_id, user_id)
        if group_id == "*":
            await Text("已在所有查询过的群解绑").send(**send_config())
        else:
            await Text(f"已在群 {group_id} 解绑").send(**send_config())
        await unbind_group.finish()
    await Text(_bind_usage).send(**send_config())
    await unbind_group.finish()
