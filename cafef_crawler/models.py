from pydantic import BaseModel, Field, validator
from typing import Optional
from datetime import datetime

class StockData(BaseModel):
    """
    Represents a single day's trading data for VNINDEX
    """
    date: str = Field(..., description="Date of trading (dd/mm/yyyy)")
    close_price: float = Field(..., description="Closing price")
    adjusted_close_price: Optional[float] = Field(None, description="Adjusted closing price")
    change_value: float = Field(..., description="Price change value")
    change_percent: float = Field(..., description="Price change percentage")
    
    match_volume: int = Field(..., description="Matching volume (KL khớp lệnh)")
    match_value: int = Field(..., description="Matching value (GT khớp lệnh)")
    negotiated_volume: int = Field(..., description="Negotiated volume (KL thỏa thuận)")
    negotiated_value: int = Field(..., description="Negotiated value (GT thỏa thuận)")
    
    open_price: float = Field(..., description="Opening price")
    high_price: float = Field(..., description="Highest price")
    low_price: float = Field(..., description="Lowest price")

    @validator('date')
    def validate_date(cls, v):
        try:
            datetime.strptime(v, '%d/%m/%Y')
        except ValueError:
            raise ValueError("Incorrect date format, should be dd/mm/yyyy")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "date": "28/01/2026",
                "close_price": 1250.5,
                "change_value": 10.5,
                "change_percent": 0.85,
                "match_volume": 1000000,
                "match_value": 5000000000,
                "negotiated_volume": 200000,
                "negotiated_value": 1000000000,
                "open_price": 1240.0,
                "high_price": 1255.0,
                "low_price": 1238.0
            }
        }
