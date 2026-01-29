"""
Domain Layer - Core business entities

These entities are pure Python with no external dependencies.
They represent the core business concepts of the crawler.
"""
from dataclasses import dataclass, field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class ListingType(Enum):
    """Type of property listing"""
    SALE = "ban"
    RENT = "cho-thue"


class PropertyType(Enum):
    """Type of property"""
    APARTMENT = "can-ho-chung-cu"
    HOUSE = "nha-rieng"
    VILLA = "nha-biet-thu"
    TOWNHOUSE = "nha-mat-pho"
    LAND_PROJECT = "dat-nen"
    LAND = "dat"
    FARM = "trang-trai"
    WAREHOUSE = "kho-xuong"
    OTHER = "bat-dong-san-khac"
    
    @property
    def display_name(self) -> str:
        names = {
            "can-ho-chung-cu": "Căn hộ chung cư",
            "nha-rieng": "Nhà riêng",
            "nha-biet-thu": "Nhà biệt thự, liền kề",
            "nha-mat-pho": "Nhà mặt phố",
            "dat-nen": "Đất nền dự án",
            "dat": "Đất",
            "trang-trai": "Trang trại, khu nghỉ dưỡng",
            "kho-xuong": "Kho, nhà xưởng",
            "bat-dong-san-khac": "Bất động sản khác",
        }
        return names.get(self.value, self.value)


@dataclass
class Location:
    """Location information for a property"""
    address: Optional[str] = None
    street: Optional[str] = None
    ward: Optional[str] = None
    district: Optional[str] = None
    province: Optional[str] = None
    
    def __str__(self) -> str:
        parts = [p for p in [self.street, self.ward, self.district, self.province] if p]
        return ", ".join(parts) if parts else self.address or ""


@dataclass
class PropertySpecs:
    """Technical specifications of a property"""
    area: Optional[float] = None          # m²
    frontage: Optional[float] = None      # meters
    bedrooms: Optional[int] = None
    bathrooms: Optional[int] = None
    floors: Optional[int] = None
    direction: Optional[str] = None       # Đông Nam, Tây Bắc, etc.
    legal_status: Optional[str] = None    # Sổ đỏ, Sổ hồng, etc.
    interior: Optional[str] = None        # Nội thất đầy đủ, etc.


@dataclass
class ContactInfo:
    """Contact information for a listing"""
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None


@dataclass
class Price:
    """Value object representing a price"""
    raw: str                              # Original string: "2.5 tỷ"
    value: Optional[float] = None         # Numeric: 2500000000
    unit: Optional[str] = None            # "tỷ", "triệu", "triệu/tháng"
    per_m2: Optional[float] = None        # Price per square meter
    
    def __str__(self) -> str:
        return self.raw


@dataclass
class PropertyListing:
    """
    Core domain entity representing a property listing.
    
    This is the main aggregate root for the crawler domain.
    """
    id: str
    title: str
    url: str
    price: Price
    
    # Classification
    listing_type: Optional[ListingType] = None
    property_type: Optional[PropertyType] = None
    
    # Details
    location: Location = field(default_factory=Location)
    specs: PropertySpecs = field(default_factory=PropertySpecs)
    contact: ContactInfo = field(default_factory=ContactInfo)
    
    # Content
    description: Optional[str] = None
    thumbnail: Optional[str] = None
    image_count: Optional[int] = None
    
    # Metadata
    posted_date: Optional[str] = None
    is_verified: bool = False
    is_vip: bool = False
    crawled_at: datetime = field(default_factory=datetime.now)
    
    def to_dict(self) -> dict:
        """Convert to dictionary for serialization"""
        return {
            "id": self.id,
            "title": self.title,
            "url": self.url,
            "price": self.price.raw,
            "price_value": self.price.value,
            "price_unit": self.price.unit,
            "listing_type": self.listing_type.value if self.listing_type else None,
            "property_type": self.property_type.value if self.property_type else None,
            "location": {
                "address": self.location.address,
                "district": self.location.district,
                "province": self.location.province,
            },
            "specs": {
                "area": self.specs.area,
                "bedrooms": self.specs.bedrooms,
                "bathrooms": self.specs.bathrooms,
                "direction": self.specs.direction,
            },
            "contact": {
                "name": self.contact.name,
                "phone": self.contact.phone,
            },
            "description": self.description[:200] if self.description else None,
            "thumbnail": self.thumbnail,
            "is_verified": self.is_verified,
            "is_vip": self.is_vip,
            "crawled_at": self.crawled_at.isoformat(),
        }


@dataclass
class CrawlResult:
    """Result of a crawl operation"""
    success: bool
    listings: List[PropertyListing] = field(default_factory=list)
    total_found: int = 0
    pages_crawled: int = 0
    errors: int = 0
    duration_seconds: float = 0.0
    error_message: Optional[str] = None
