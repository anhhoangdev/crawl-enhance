"""
Infrastructure Layer - Storage Implementations

Implements IStorage interface for persisting crawled data.
"""
import json
import csv
from pathlib import Path
from typing import List
from datetime import datetime

from batdongsan.domain.entities import PropertyListing
from batdongsan.domain.interfaces import IStorage


class JsonStorage(IStorage):
    """JSON file storage - saves all listings as a single JSON file"""
    
    def __init__(self, output_dir: str = "output", filename: str = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batdongsan_{timestamp}.json"
            
        self.filepath = self.output_dir / filename
        self._listings: List[PropertyListing] = []
        
    def save(self, listing: PropertyListing) -> None:
        """Save a single listing (buffered)"""
        self._listings.append(listing)
        
    def save_batch(self, listings: List[PropertyListing]) -> None:
        """Save multiple listings"""
        self._listings.extend(listings)
        
    def close(self) -> None:
        """Write all listings to file"""
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(
                [l.to_dict() for l in self._listings],
                f,
                ensure_ascii=False,
                indent=2
            )
        print(f"[+] Saved {len(self._listings)} listings to {self.filepath}")


class JsonLinesStorage(IStorage):
    """JSON Lines storage - streams listings to file"""
    
    def __init__(self, output_dir: str = "output", filename: str = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batdongsan_{timestamp}.jsonl"
            
        self.filepath = self.output_dir / filename
        self._file = open(self.filepath, 'w', encoding='utf-8')
        self._count = 0
        
    def save(self, listing: PropertyListing) -> None:
        """Save a single listing immediately"""
        self._file.write(json.dumps(listing.to_dict(), ensure_ascii=False) + '\n')
        self._file.flush()
        self._count += 1
        
    def save_batch(self, listings: List[PropertyListing]) -> None:
        """Save multiple listings"""
        for listing in listings:
            self.save(listing)
            
    def close(self) -> None:
        """Close the file"""
        self._file.close()
        print(f"[+] Saved {self._count} listings to {self.filepath}")


class CsvStorage(IStorage):
    """CSV file storage"""
    
    HEADERS = [
        'id', 'title', 'url', 'price', 'price_value', 'price_unit',
        'area', 'bedrooms', 'bathrooms', 'direction',
        'address', 'district', 'province',
        'listing_type', 'property_type', 'is_verified', 'is_vip',
        'thumbnail', 'crawled_at'
    ]
    
    def __init__(self, output_dir: str = "output", filename: str = None):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"batdongsan_{timestamp}.csv"
            
        self.filepath = self.output_dir / filename
        self._file = open(self.filepath, 'w', encoding='utf-8', newline='')
        self._writer = csv.writer(self._file)
        self._writer.writerow(self.HEADERS)
        self._count = 0
        
    def save(self, listing: PropertyListing) -> None:
        """Save a single listing"""
        self._writer.writerow([
            listing.id,
            listing.title[:100] if listing.title else '',
            listing.url,
            listing.price.raw,
            listing.price.value,
            listing.price.unit,
            listing.specs.area,
            listing.specs.bedrooms,
            listing.specs.bathrooms,
            listing.specs.direction,
            listing.location.address,
            listing.location.district,
            listing.location.province,
            listing.listing_type.value if listing.listing_type else None,
            listing.property_type.value if listing.property_type else None,
            listing.is_verified,
            listing.is_vip,
            listing.thumbnail,
            listing.crawled_at.isoformat(),
        ])
        self._file.flush()
        self._count += 1
        
    def save_batch(self, listings: List[PropertyListing]) -> None:
        """Save multiple listings"""
        for listing in listings:
            self.save(listing)
            
    def close(self) -> None:
        """Close the file"""
        self._file.close()
        print(f"[+] Saved {self._count} listings to {self.filepath}")


class MultiStorage(IStorage):
    """Composite storage - writes to multiple storage backends"""
    
    def __init__(self, storages: List[IStorage]):
        self._storages = storages
        
    def save(self, listing: PropertyListing) -> None:
        for storage in self._storages:
            storage.save(listing)
            
    def save_batch(self, listings: List[PropertyListing]) -> None:
        for storage in self._storages:
            storage.save_batch(listings)
            
    def close(self) -> None:
        for storage in self._storages:
            storage.close()
