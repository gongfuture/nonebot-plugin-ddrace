from .ddr_get_data import DDRDataGet 

ddr = DDRDataGet()
pre_search = ddr.pre_search
result_page = ddr.result_page
profile_json = ddr.profile_json

__all__ = [
    "pre_search",
    "result_page",
    "profile_json"
]