from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class SellerInfo(BaseModel):
    """Information about the car seller"""
    name: str = Field(..., description="Name of the seller or dealership")
    phone: str = Field(..., description="Contact phone number")
    address: Optional[str] = Field(None, description="Address of the seller")
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Auto Hùng Cường",
                "phone": "0987654321",
                "address": "123 Nguyễn Văn Cừ, Long Biên, Hà Nội"
            }
        }

class CarSpecs(BaseModel):
    """Technical specifications of the car"""
    engine: Optional[str] = Field(None, description="Engine type/capacity (e.g. 2.0L, Máy dầu)")
    transmission: Optional[str] = Field(None, description="Transmission type (e.g. Số tự động, Số sàn)")
    drivetrain: Optional[str] = Field(None, description="Drivetrain (e.g. RWD, AWD)")
    mileage: Optional[str] = Field(None, description="Mileage (e.g. 50,000 km)")
    color: Optional[str] = Field(None, description="Exterior color")
    interior_color: Optional[str] = Field(None, description="Interior color")
    
class CarListing(BaseModel):
    """Main model representing a car listing on Bonbanh.com"""
    id: str = Field(..., description="Unique ID of the listing")
    title: str = Field(..., description="Title of the listing")
    url: str = Field(..., description="URL of the listing")
    price: str = Field(..., description="Price as string (e.g. '639 Triệu')")
    price_value: Optional[float] = Field(None, description="Numeric price in millions VND")
    year: int = Field(..., description="Year of manufacture")
    origin: Optional[str] = Field(None, description="Origin (e.g. Nhập khẩu, Lắp ráp)")
    status: Optional[str] = Field(None, description="Status (e.g. Xe cũ, Xe mới)")
    
    seller: SellerInfo
    specs: CarSpecs
    
    description: Optional[str] = Field(None, description="Full description text")
