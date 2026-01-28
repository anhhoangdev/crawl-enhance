"""
Pydantic Models for CafeF API Data
===================================

Full model matching the API response structure

The API returns Vietnamese field names, so we map them to English
"""

from pydantic import BaseModel, Field

class StockData(BaseModel):
    """
    Complete stock data from CafeF API
    
    Note: CafeF API uses Vietnamese field names
    We map them to English for clarity
    """
    
    # Map Vietnamese API fields to English model fields
    date: str = Field(alias="Ngay", description="Trading date (dd/mm/yyyy)")
    close_price: float = Field(alias="GiaDongCua", description="Closing price")
    adjusted_close: float = Field(alias="GiaDieuChinh", description="Adjusted closing price")
    change_value: float = Field(alias="ThayDoi", description="Change in value")
    change_percent: float = Field(alias="PhanTramThayDoi", description="Percent change")
    
    match_volume: int = Field(alias="KLKhopLenh", description="Matching volume")
    match_value: int = Field(alias="GTKhopLenh", description="Matching value")
    
    negotiated_volume: int = Field(alias="KLThoaThuan", description="Negotiated volume")
    negotiated_value: int = Field(alias="GTThoaThuan", description="Negotiated value")
    
    open_price: float = Field(alias="GiaMoCua", description="Opening price")
    high_price: float = Field(alias="GiaCaoNhat", description="Highest price")
    low_price: float = Field(alias="GiaThapNhat", description="Lowest price")
    
    class Config:
        # Allow field population by alias (Vietnamese names)
        populate_by_name = True
        
        json_schema_extra = {
            "example": {
                "Ngay": "28/01/2026",
                "GiaDongCua": 1250.5,
                "GiaDieuChinh": 1250.5,
                "ThayDoi": 10.2,
                "PhanTramThayDoi": 0.82,
                "KLKhopLenh": 1000000,
                "GTKhopLenh": 5000000000,
                "KLThoaThuan": 50000,
                "GTThoaThuan": 250000000,
                "GiaMoCua": 1240.3,
                "GiaCaoNhat": 1255.0,
                "GiaThapNhat": 1238.0
            }
        }

# Example usage
if __name__ == "__main__":
    # Test with Vietnamese field names (as the API returns)
    api_response = {
        "Ngay": "28/01/2026",
        "GiaDongCua": 1250.5,
        "GiaDieuChinh": 1250.5,
        "ThayDoi": 10.2,
        "PhanTramThayDoi": 0.82,
        "KLKhopLenh": 1000000,
        "GTKhopLenh": 5000000000,
        "KLThoaThuan": 50000,
        "GTThoaThuan": 250000000,
        "GiaMoCua": 1240.3,
        "GiaCaoNhat": 1255.0,
        "GiaThapNhat": 1238.0
    }
    
    stock = StockData(**api_response)
    
    print("Stock data created from Vietnamese API:")
    print(stock)
    
    print("\nAccessing fields (English names):")
    print(f"Date: {stock.date}")
    print(f"Close: {stock.close_price}")
    print(f"Open: {stock.open_price}")
    
    print("\nAs JSON (English field names):")
    print(stock.model_dump_json(indent=2, by_alias=False))
