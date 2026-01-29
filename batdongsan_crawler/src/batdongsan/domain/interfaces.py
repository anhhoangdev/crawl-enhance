"""
Domain Layer - Abstract Interfaces (Ports)

These interfaces define the contracts that infrastructure must implement.
Following Dependency Inversion Principle - domain defines what it needs,
infrastructure provides the implementation.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, AsyncIterator
from dataclasses import dataclass, field
from enum import Enum

from .entities import PropertyListing


class UrlType(Enum):
    """Type of URL for prioritization"""
    LISTING_PAGE = 1    # Page with multiple listings
    DETAIL_PAGE = 2     # Individual property page


@dataclass
class CrawlUrl:
    """URL item for the frontier queue"""
    url: str
    url_type: UrlType
    priority: int = 1
    depth: int = 0
    retries: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)


class IHttpClient(ABC):
    """
    Abstract HTTP client interface.
    
    Infrastructure layer must provide an implementation
    that can bypass anti-bot protection.
    """
    
    @abstractmethod
    async def get(self, url: str) -> Optional[str]:
        """
        Fetch URL and return HTML content.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        pass
    
    @abstractmethod
    async def close(self) -> None:
        """Close the client and cleanup resources"""
        pass


class IParser(ABC):
    """
    Abstract HTML parser interface.
    
    Each website needs its own parser implementation.
    """
    
    @abstractmethod
    def parse_listing_page(self, html: str, metadata: Dict[str, Any] = None) -> List[PropertyListing]:
        """
        Parse a listing page and extract property listings.
        
        Args:
            html: Raw HTML content
            metadata: Additional context (listing_type, property_type, etc.)
            
        Returns:
            List of PropertyListing entities
        """
        pass
    
    @abstractmethod
    def parse_detail_page(self, html: str, url: str) -> Optional[PropertyListing]:
        """
        Parse a detail page for full property information.
        
        Args:
            html: Raw HTML content
            url: Page URL for reference
            
        Returns:
            PropertyListing with full details or None
        """
        pass
    
    @abstractmethod
    def extract_detail_urls(self, html: str) -> List[str]:
        """
        Extract detail page URLs from a listing page.
        
        Args:
            html: Raw HTML content
            
        Returns:
            List of detail page URLs
        """
        pass


class IStorage(ABC):
    """
    Abstract storage interface for persisting crawled data.
    """
    
    @abstractmethod
    def save(self, listing: PropertyListing) -> None:
        """Save a single listing (streaming)"""
        pass
    
    @abstractmethod
    def save_batch(self, listings: List[PropertyListing]) -> None:
        """Save multiple listings at once"""
        pass
    
    @abstractmethod
    def close(self) -> None:
        """Close storage and finalize files"""
        pass


class IUrlFrontier(ABC):
    """
    Abstract URL frontier for managing crawl queue.
    
    Handles URL deduplication, prioritization, and queue management.
    """
    
    @abstractmethod
    def add(self, crawl_url: CrawlUrl) -> bool:
        """
        Add URL to frontier.
        
        Args:
            crawl_url: URL to add
            
        Returns:
            True if added, False if duplicate
        """
        pass
    
    @abstractmethod
    def get(self) -> Optional[CrawlUrl]:
        """Get next URL to crawl"""
        pass
    
    @abstractmethod
    def complete(self, url: str) -> None:
        """Mark URL as completed"""
        pass
    
    @abstractmethod
    def is_empty(self) -> bool:
        """Check if frontier is empty"""
        pass
    
    @abstractmethod
    def __len__(self) -> int:
        """Return number of URLs in queue"""
        pass
