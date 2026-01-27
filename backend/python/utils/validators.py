from typing import Optional
from urllib.parse import urlparse

class URLValidator:
    SUPPORTED_SITES = {
        "atgp.jp": "atgp",
        "snabi.jp": "litalico",
        "litalico": "litalico",
        "mynavi.jp": "mynavi",
        "mynavi-agent": "mynavi"
    }
    
    @classmethod
    def validate_url(cls, url: str) -> tuple[bool, Optional[str]]:
        try:
            parsed = urlparse(url)
            
            if not parsed.scheme or not parsed.netloc:
                return False, "Invalid URL format"
            
            for domain, site_name in cls.SUPPORTED_SITES.items():
                if domain in parsed.netloc:
                    return True, site_name
            
            return False, "Unsupported job site"
            
        except Exception:
            return False, "Invalid URL"
    
    @classmethod
    def get_site_name(cls, url: str) -> Optional[str]:
        is_valid, site_name = cls.validate_url(url)
        return site_name if is_valid else None
