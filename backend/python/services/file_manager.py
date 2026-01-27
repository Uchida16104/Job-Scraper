import os
from typing import Optional
from config import settings

class FileManager:
    def __init__(self):
        self.output_dir = settings.OUTPUT_DIR
        
    def get_download_url(self, history_id: int) -> str:
        return f"/api/download/{history_id}"
    
    def file_exists(self, filepath: str) -> bool:
        return os.path.exists(filepath)
    
    def get_file_size(self, filepath: str) -> Optional[int]:
        if self.file_exists(filepath):
            return os.path.getsize(filepath)
        return None
    
    def delete_file(self, filepath: str) -> bool:
        try:
            if self.file_exists(filepath):
                os.remove(filepath)
                return True
            return False
        except Exception:
            return False
    
    def cleanup_old_files(self, days: int = 30):
        import time
        current_time = time.time()
        cutoff_time = current_time - (days * 86400)
        
        for filename in os.listdir(self.output_dir):
            filepath = os.path.join(self.output_dir, filename)
            if os.path.isfile(filepath):
                file_time = os.path.getmtime(filepath)
                if file_time < cutoff_time:
                    self.delete_file(filepath)
