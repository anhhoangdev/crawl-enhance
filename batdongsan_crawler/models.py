"""
Pydantic models for BatDongSan crawler
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class Location(BaseModel):
    """Location information"""
    address: Optional[str] = None
    street: Optional[str] = None
    ward: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None


class PropertySpecs(BaseModel):
    """Property specifications"""
    area: Optional[float] = None          # m²
    frontage: Optional[float] = None      # meters
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    floors: Optional[int] = None
    direction: Optional[str] = None       # Đông Nam, Tây Bắc, etc.
    legal_status: Optional[str] = None    # Sổ đỏ, Sổ hồng, etc.
    interior: Optional[str] = None        # Nội thất đầy đủ, etc.


class ContactInfo(BaseModel):
    """Contact information"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


class PropertyListing(BaseModel):
    """Main property listing model"""
    id: str
    title: str
    url: str
    price: str = "Thỏa thuận"
    price_value: Optional[float] = None
    price_unit: Optional[str] = None
    
    listing_type: Optional[str] = None    # Bán, Cho thuê
    property_type: Optional[str] = None   # Căn hộ, Nhà riêng, etc.
    
    location: Optional[Location] = None
    specs: Optional[PropertySpecs] = None
    contact: Optional[ContactInfo] = None
    
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    image_count: Optional[int] = None
    
    posted_date: Optional[str] = None
    is_verified: bool = False
    is_vip: bool = False
    crawled_at: datetime = Field(default_factory=datetime.now)
