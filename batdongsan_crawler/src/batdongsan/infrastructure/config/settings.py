"""
Infrastructure Layer - Configuration Settings

Uses pydantic-settings for environment variable support.
"""
from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Tuple


class CrawlerSettings(BaseSettings):
    """
    Crawler configuration with environment variable support.
    
    Environment variables are prefixed with BATDONGSAN_
    Example: BATDONGSAN_MAX_CONCURRENT=5
    """
    
    # HTTP Client settings
    max_concurrent: int = Field(default=3, description="Maximum concurrent requests")
    delay_min: float = Field(default=2.0, description="Minimum delay between requests")
    delay_max: float = Field(default=4.0, description="Maximum delay between requests")
    timeout: int = Field(default=30, description="Request timeout in seconds")
    max_retries: int = Field(default=3, description="Maximum retry attempts")
    
    # Browser impersonation
    impersonate: str = Field(default="chrome120", description="Browser to impersonate")
    
    # Crawl settings
    crawl_details: bool = Field(default=False, description="Also crawl detail pages")
    max_pages: int = Field(default=10, description="Maximum pages per category")
    
    # Output settings
    output_dir: str = Field(default="output", description="Output directory")
    
    # Base URL
    base_url: str = Field(default="https://batdongsan.com.vn", description="Base URL")
    
    @property
    def delay_range(self) -> Tuple[float, float]:
        return (self.delay_min, self.delay_max)
    
    class Config:
        env_prefix = "BATDONGSAN_"
        env_file = ".env"
        extra = "ignore"


# Global settings instance
settings = CrawlerSettings()
