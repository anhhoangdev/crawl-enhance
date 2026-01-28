"""
Pydantic Models for Car Listings
=================================

This file defines the data structure for car listings using Pydantic.

Why Pydantic?
- Automatic data validation (e.g., year must be an integer)
- Type hints make code clearer
- Easy conversion to/from JSON
- Catches errors early in the scraping process
"""

from pydantic import BaseModel, Field

class CarListing(BaseModel):
    """
    Represents a single car listing from Bonbanh.com
    
    Attributes:
        title: Full title of the listing (e.g., "Toyota Camry 2020")
        price: Price as string (e.g., "500 Triệu", "Contact")
        url: Full URL to the listing page
        year: Year of manufacture (0 if unknown)
    """
    title: str = Field(..., description="Car title")
    price: str = Field(..., description="Price (as displayed)")
    url: str = Field(..., description="Full URL to listing")
    year: int = Field(default=0, description="Year of manufacture")
    
    class Config:
        # Example for documentation
        json_schema_extra = {
            "example": {
                "title": "Toyota Camry 2.5Q 2020",
                "price": "850 Triệu",
                "url": "https://bonbanh.com/xe-toyota-camry-12345.html",
                "year": 2020
            }
        }

# Example usage (for testing):
if __name__ == "__main__":
    # Create a car listing
    car = CarListing(
        title="Honda Civic 2019",
        price="600 Triệu",
        url="https://bonbanh.com/xe-honda-civic-67890.html",
        year=2019
    )
    
    print("Car object created:")
    print(car)
    
    print("\nAs JSON:")
    print(car.model_dump_json(indent=2))
    
    # Try invalid data (uncomment to see validation error)
    # invalid_car = CarListing(
    #     title="Test Car",
    #     price="500 Triệu",
    #     url="not-a-url",
    #     year="not-a-number"  # This will cause a validation error!
    # )
