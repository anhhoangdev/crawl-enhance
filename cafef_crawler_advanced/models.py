from pydantic import BaseModel, Field, field_validator, AliasChoices
from typing import Optional
from datetime import datetime
import re

class StockData(BaseModel):
    """
    Represents a single day's trading data for VNINDEX (Advanced API)
    """
    date: str = Field(..., alias="Ngay", description="Date of trading (dd/mm/yyyy)")
    close_price: float = Field(..., alias="GiaDongCua", description="Closing price")
    adjusted_close_price: Optional[float] = Field(None, alias="GiaDieuChinh", description="Adjusted closing price")
    
    # "ThayDoi": "-27.59(-1.51 %)"
    change_value: float = Field(default=0.0, description="Price change value")
    change_percent: float = Field(default=0.0, description="Price change percentage")
    raw_change: str = Field(..., alias="ThayDoi", exclude=True) # Input only
    
    match_volume: int = Field(..., alias="KhoiLuongKhopLenh", description="Matching volume")
    match_value: float = Field(..., alias="GiaTriKhopLenh", description="Matching value")
    negotiated_volume: int = Field(..., alias="KLThoaThuan", description="Negotiated volume")
    negotiated_value: float = Field(..., alias="GtThoaThuan", description="Negotiated value")
    
    open_price: float = Field(..., alias="GiaMoCua", description="Opening price")
    high_price: float = Field(..., alias="GiaCaoNhat", description="Highest price")
    low_price: float = Field(..., alias="GiaThapNhat", description="Lowest price")

    @field_validator('date', mode='before')
    def validate_date(cls, v):
        if hasattr(v, 'strftime'): return v.strftime('%d/%m/%Y')
        return v

    @field_validator('change_value', 'change_percent', mode='before')
    def parse_change(cls, v, info):
        # This will run but we really want a root validator or a validator on raw_change
        # But Pydantic V2 model_validator is better for parsing one field into two.
        return v

    def model_post_init(self, __context):
        # We process raw_change here if needed, but in V2 it's better to use model_validator(mode='before')
        pass

    # Better approach for Pydantic V2: model_validator
    from pydantic import model_validator

    @model_validator(mode='before')
    @classmethod
    def split_change_field(cls, data: dict):
        if "ThayDoi" in data:
            raw = data["ThayDoi"]
            # Format: "-27.59(-1.51 %)"
            match = re.match(r'([-\d.]+)\(([-\d.]+) %\)', raw)
            if match:
                data['change_value'] = float(match.group(1))
                data['change_percent'] = float(match.group(2))
            else:
                # Provide defaults if not matching
                data['change_value'] = 0.0
                data['change_percent'] = 0.0
        return data

    class Config:
        populate_by_name = True
