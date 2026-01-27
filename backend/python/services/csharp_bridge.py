import asyncio
import json
import os
from typing import Optional, Dict, Any
from config import settings

class CSharpScraperBridge:
    def __init__(self):
        self.scraper_path = settings.CSHARP_SCRAPER_PATH
        
    async def scrape(self, url: str) -> Optional[Dict[Any, Any]]:
        try:
            if not os.path.exists(self.scraper_path):
                return {"error": f"C# scraper not found at {self.scraper_path}"}
            
            process = await asyncio.create_subprocess_exec(
                "dotnet",
                self.scraper_path,
                url,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=60.0
            )
            
            if process.returncode != 0:
                error_message = stderr.decode().strip()
                return {"error": f"C# scraper failed: {error_message}"}
            
            result_json = stdout.decode().strip()
            
            if not result_json:
                return {"error": "No data returned from scraper"}
            
            result = json.loads(result_json)
            return result
            
        except asyncio.TimeoutError:
            return {"error": "Scraping timeout (60 seconds)"}
        except json.JSONDecodeError as e:
            return {"error": f"Failed to parse scraper output: {str(e)}"}
        except Exception as e:
            return {"error": f"Scraping error: {str(e)}"}
