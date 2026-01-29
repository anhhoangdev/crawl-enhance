"""Domain Layer"""
from .entities import (
    PropertyListing,
    Location,
    PropertySpecs,
    ContactInfo,
    Price,
    ListingType,
    PropertyType,
    CrawlResult,
)
from .interfaces import (
    IHttpClient,
    IParser,
    IStorage,
    IUrlFrontier,
    CrawlUrl,
    UrlType,
)

__all__ = [
    "PropertyListing",
    "Location",
    "PropertySpecs",
    "ContactInfo",
    "Price",
    "ListingType",
    "PropertyType",
    "CrawlResult",
    "IHttpClient",
    "IParser",
    "IStorage",
    "IUrlFrontier",
    "CrawlUrl",
    "UrlType",
]
