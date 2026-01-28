"""
Pydantic Models for Stock Data
===============================

Simplified model for VNINDEX stock data

Why simplified?
- Focus on core OHLC (Open, High, Low, Close) data
- Easier to understand for teaching
- Can be extended later with more fields
"""

from pydantic import BaseModel, Field

class StockData(BaseModel):
    """
    Represents one day of VNINDEX trading data
    
    Attributes:
        date: Trading date in format "dd/mm/yyyy"
        open_price: Opening price
        close_price: Closing price
        high_price: Highest price of the day
        low_price: Lowest price of the day
    """
    date: str = Field(..., description="Trading date (dd/mm/yyyy)")
    open_price: float = Field(default=0.0, description="Opening price")
    close_price: float = Field(default=0.0, description="Closing price")
    high_price: float = Field(default=0.0, description="Highest price")
    low_price: float = Field(default=0.0, description="Lowest price")
    
    class Config:
        json_schema_extra = {
            "example": {
                "date": "28/01/2026",
                "open_price": 1240.5,
                "close_price": 1250.8,
                "high_price": 1255.2,
                "low_price": 1238.0
            }
        }

# Example usage (for testing):
if __name__ == "__main__":
    # Create sample stock data
    stock = StockData(
        date="28/01/2026",
        open_price=1240.5,
        close_price=1250.8,
        high_price=1255.2,
        low_price=1238.0
    )
    
    print("Stock data created:")
    print(stock)
    
    print("\nAs JSON:")
    print(stock.model_dump_json(indent=2))
    
    # Pydantic validates types automatically
    try:
        invalid = StockData(
            date="28/01/2026",
            open_price="not-a-number",  # This will fail!
            close_price=1250.8,
            high_price=1255.2,
            low_price=1238.0
        )
    except Exception as e:
        print(f"\n❌ Validation error (expected): {e}")
