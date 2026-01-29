"""
Infrastructure Layer - URL Frontier

Implements IUrlFrontier interface for managing crawl queue.
"""
import hashlib
from typing import Optional, Set
from collections import deque
from urllib.parse import urlparse

from batdongsan.domain.interfaces import IUrlFrontier, CrawlUrl


class MemoryUrlFrontier(IUrlFrontier):
    """
    In-memory URL frontier with deduplication.
    
    Features:
    - O(1) URL deduplication via hash set
    - FIFO queue for URL processing
    - Pending URL tracking
    """
    
    def __init__(self):
        self._queue: deque = deque()
        self._seen: Set[str] = set()
        self._pending: Set[str] = set()
        
    def add(self, crawl_url: CrawlUrl) -> bool:
        """
        Add URL to frontier if not seen.
        
        Args:
            crawl_url: URL to add
            
        Returns:
            True if added, False if duplicate
        """
        url_hash = self._normalize_url(crawl_url.url)
        
        if url_hash in self._seen:
            return False
            
        self._seen.add(url_hash)
        self._queue.append(crawl_url)
        return True
    
    def get(self) -> Optional[CrawlUrl]:
        """Get next URL to crawl"""
        if not self._queue:
            return None
            
        url = self._queue.popleft()
        self._pending.add(url.url)
        return url
    
    def complete(self, url: str) -> None:
        """Mark URL as completed"""
        self._pending.discard(url)
        
    def is_empty(self) -> bool:
        """Check if frontier is empty (no queued or pending)"""
        return len(self._queue) == 0 and len(self._pending) == 0
    
    def __len__(self) -> int:
        """Return number of URLs in queue"""
        return len(self._queue)
    
    def _normalize_url(self, url: str) -> str:
        """Normalize URL for deduplication"""
        parsed = urlparse(url)
        normalized = f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"
        if parsed.query:
            normalized += f"?{parsed.query}"
        return hashlib.md5(normalized.encode()).hexdigest()
    
    @property
    def pending_count(self) -> int:
        """Number of URLs currently being processed"""
        return len(self._pending)
    
    @property
    def seen_count(self) -> int:
        """Total unique URLs seen"""
        return len(self._seen)
