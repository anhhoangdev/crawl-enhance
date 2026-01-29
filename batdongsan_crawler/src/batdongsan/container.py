"""
Dependency Injection Container

Wires up all dependencies following the Composition Root pattern.
"""
import sys
from dataclasses import dataclass

from batdongsan.domain.interfaces import IHttpClient, IParser, IStorage, IUrlFrontier
from batdongsan.infrastructure import (
    CurlCffiClient,
    BatDongSanParser,
    JsonLinesStorage,
    CsvStorage,
    MultiStorage,
    MemoryUrlFrontier,
    settings,
)
from batdongsan.application import SpiderService


@dataclass
class Container:
    """
    Dependency injection container.
    
    Creates and wires up all dependencies for the application.
    This is the only place where concrete implementations are instantiated.
    """
    http_client: IHttpClient
    parser: IParser
    storage: IStorage
    frontier: IUrlFrontier
    spider_service: SpiderService


def create_container(
    output_dir: str = None,
    max_concurrent: int = None,
    crawl_details: bool = None,
) -> Container:
    """
    Create a fully wired container.
    
    Args:
        output_dir: Output directory for storage
        max_concurrent: Maximum concurrent requests
        crawl_details: Whether to crawl detail pages
        
    Returns:
        Container with all dependencies
    """
    # Use settings defaults if not specified
    output_dir = output_dir or settings.output_dir
    max_concurrent = max_concurrent if max_concurrent is not None else settings.max_concurrent
    crawl_details = crawl_details if crawl_details is not None else settings.crawl_details
    
    # Create infrastructure
    http_client = CurlCffiClient()
    parser = BatDongSanParser()
    frontier = MemoryUrlFrontier()
    
    # Multi-storage: both JSONL and CSV
    storage = MultiStorage([
        JsonLinesStorage(output_dir),
        CsvStorage(output_dir),
    ])
    
    # Create application service
    spider_service = SpiderService(
        http_client=http_client,
        parser=parser,
        storage=storage,
        frontier=frontier,
        max_concurrent=max_concurrent,
        crawl_details=crawl_details,
    )
    
    return Container(
        http_client=http_client,
        parser=parser,
        storage=storage,
        frontier=frontier,
        spider_service=spider_service,
    )
