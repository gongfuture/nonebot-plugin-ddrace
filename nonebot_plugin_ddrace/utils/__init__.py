from .constants import *
from .tools import PathClass, InputCheck
from .triggers import Trigger
from .cache import CacheClass

send_config = Trigger().send_config
default_arg = Trigger().default_arg
command_arg = Trigger().command_arg
input_check = InputCheck()


__all__ = [
    "constants",
    "PathClass",
    "input_check",
    "Trigger",
    "send_config",
    "default_arg",
    "command_arg",
    "CacheClass"
]