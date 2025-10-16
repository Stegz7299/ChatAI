import os
import uuid

class FileHandler:
    UPLOAD_DIR = "uploads"

    def __init__(self):
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)

    def save_file(self, file, token: str) -> str:
        filename = f"{token}_{uuid.uuid4().hex}_{file.filename}"
        filepath = os.path.join(self.UPLOAD_DIR, filename)

        with open(filepath, "wb") as f:
            f.write(file.file.read())

        return filepath
    
    def read_file(self, filepath: str) -> str:
        if filepath.endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                return f.read()
        
        return f"Unsupported file type: {filepath}"