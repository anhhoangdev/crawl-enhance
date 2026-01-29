"""
Infrastructure Layer - HTTP Client using curl-cffi

Implements IHttpClient interface with TLS fingerprint impersonation
to bypass Cloudflare protection.
"""
import asyncio
import random
from typing import Optional, Dict

from curl_cffi.requests import AsyncSession

from batdongsan.domain.interfaces import IHttpClient
from batdongsan.infrastructure.config import settings


class CurlCffiClient(IHttpClient):
    """
    HTTP client using curl-cffi for Cloudflare bypass.
    
    curl-cffi impersonates real browser TLS fingerprints,
    which helps bypass Cloudflare's bot detection.
    """
    
    def __init__(
        self,
        impersonate: str = None,
        delay_range: tuple = None,
        timeout: int = None,
    ):
        """
        Initialize the HTTP client.
        
        Args:
            impersonate: Browser to impersonate (chrome120, firefox, safari)
            delay_range: (min, max) seconds between requests
            timeout: Request timeout in seconds
        """
        self.impersonate = impersonate or settings.impersonate
        self.delay_range = delay_range or settings.delay_range
        self.timeout = timeout or settings.timeout
        self._session: Optional[AsyncSession] = None
        
    async def _get_session(self) -> AsyncSession:
        """Get or create async session"""
        if self._session is None:
            self._session = AsyncSession(impersonate=self.impersonate)
        return self._session
    
    def _get_headers(self) -> Dict[str, str]:
        """Get request headers"""
        return {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "vi-VN,vi;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "no-cache",
            "Referer": settings.base_url,
        }
    
    async def get(self, url: str) -> Optional[str]:
        """
        Fetch URL with rate limiting.
        
        Args:
            url: URL to fetch
            
        Returns:
            HTML content or None if failed
        """
        # Rate limiting
        await asyncio.sleep(random.uniform(*self.delay_range))
        
        try:
            session = await self._get_session()
            response = await session.get(
                url,
                headers=self._get_headers(),
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.text
            
        except Exception as e:
            print(f"[!] HTTP Error: {url} - {e}")
            return None
    
    async def close(self) -> None:
        """Close the session"""
        if self._session:
            await self._session.close()
            self._session = None
