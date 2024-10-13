from .ddr_get_data import ddr_data_get 

ddr = ddr_data_get()
pre_search = ddr.pre_search
result_page = ddr.result_page
profile_json = ddr.profile_json

__all__ = [
    "pre_search",
    "result_page",
    "profile_json"
]