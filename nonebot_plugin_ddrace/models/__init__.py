from .network import *
from .pic_generade import json2md, md2pic, html2pic
from .ddr_get_data import DDRDataGet

ddrapi = DDRDataGet()
pre_search = ddrapi.pre_search
result_page = ddrapi.result_page
profile_json = ddrapi.profile_json


__all__ = [
    "json2md",
    "md2pic",
    "html2pic",
    "NetWork",
    "pre_search",
    "result_page",
    "profile_json"
]