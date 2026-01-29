"""
Interface Layer - Command Line Interface

Entry point for the application using Click.
"""
import sys
import asyncio
import click
from rich.console import Console
from rich.table import Table

# Fix Windows console encoding
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

from batdongsan.container import create_container
from batdongsan.domain.entities import PropertyType


console = Console()


@click.group()
@click.version_option(version="1.0.0")
def main():
    """
    BatDongSan.com.vn Crawler
    
    A web crawler for Vietnamese real estate listings.
    Uses curl-cffi to bypass Cloudflare protection.
    """
    pass


@main.command()
@click.option('--pages', '-p', default=3, help='Pages per category')
@click.option('--concurrent', '-c', default=3, help='Concurrent requests')
@click.option('--listing-type', '-l', default='ban', 
              type=click.Choice(['ban', 'cho-thue']),
              help='Listing type: ban (sale) or cho-thue (rent)')
@click.option('--property-type', '-t', multiple=True,
              help='Property types to crawl (e.g., can-ho-chung-cu, nha-rieng)')
@click.option('--output', '-o', default='output', help='Output directory')
@click.option('--details/--no-details', default=False, 
              help='Also crawl detail pages for full info')
def crawl(pages, concurrent, listing_type, property_type, output, details):
    """
    Crawl property listings from batdongsan.com.vn
    
    Examples:
    
        batdongsan crawl --pages 5
        
        batdongsan crawl -l cho-thue -t can-ho-chung-cu
        
        batdongsan crawl --details --concurrent 5
    """
    console.print("\n[bold blue]BatDongSan.com.vn Crawler[/bold blue]\n")
    
    # Show config
    table = Table(title="Configuration")
    table.add_column("Setting", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Listing Type", listing_type)
    table.add_row("Property Types", ", ".join(property_type) if property_type else "default")
    table.add_row("Pages", str(pages))
    table.add_row("Concurrent", str(concurrent))
    table.add_row("Crawl Details", str(details))
    table.add_row("Output", output)
    console.print(table)
    console.print()
    
    # Create container
    container = create_container(
        output_dir=output,
        max_concurrent=concurrent,
        crawl_details=details,
    )
    
    # Add seed URLs
    prop_types = list(property_type) if property_type else None
    count = container.spider_service.add_seed_urls(
        listing_types=[listing_type],
        property_types=prop_types,
        max_pages=pages,
    )
    console.print(f"[green]Added {count} URLs to queue[/green]\n")
    
    # Run
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
        
    result = asyncio.run(container.spider_service.run())
    
    # Summary
    console.print()
    table = Table(title="Results")
    table.add_column("Metric", style="cyan")
    table.add_column("Value", style="green")
    table.add_row("Total Listings", str(result.total_found))
    table.add_row("Pages Crawled", str(result.pages_crawled))
    table.add_row("Errors", str(result.errors))
    table.add_row("Duration", f"{result.duration_seconds:.1f}s")
    console.print(table)


@main.command()
def types():
    """
    Show available property types
    """
    table = Table(title="Property Types")
    table.add_column("Slug", style="cyan")
    table.add_column("Name", style="green")
    
    for pt in PropertyType:
        table.add_row(pt.value, pt.display_name)
        
    console.print(table)


if __name__ == '__main__':
    main()
