from pydantic import BaseModel

class Config(BaseModel):
    ddr_need_at: bool = False
    ddr_command_pre_alias: str = ""

    # @field_validator("weather_command_priority")
    # @classmethod
    # def check_priority(cls, v: int) -> int:
    #     if v >= 1:
    #         return v
    #     raise ValueError("weather command priority must greater than 1")