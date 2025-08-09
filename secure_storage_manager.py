import os
import json
import hashlib
from cryptography.fernet import Fernet
from datetime import datetime


class SecureStorageManager:
    """Handles encrypted file system where even filenames and folder structure are encrypted"""
    
    def __init__(self, base_path, fernet):
        self.base_path = base_path
        self.fernet = fernet
        self.secure_path = os.path.join(base_path, "secure_storage")
        self.index_file = os.path.join(self.secure_path, "index.enc")
        os.makedirs(self.secure_path, exist_ok=True)
        
        # Load or create the encrypted index
        self.file_index = self._load_index()
    
    def _generate_secure_filename(self, original_path):
        """Generate a secure hash-based filename for the original path"""
        path_hash = hashlib.sha256(original_path.encode()).hexdigest()
        return f"{path_hash[:16]}.dat"
    
    def _load_index(self):
        """Load the encrypted file index that maps original paths to secure filenames"""
        if os.path.exists(self.index_file):
            try:
                with open(self.index_file, "rb") as f:
                    encrypted_data = f.read()
                decrypted_data = self.fernet.decrypt(encrypted_data)
                return json.loads(decrypted_data.decode())
            except Exception:
                return {}
        return {}
    
    def _save_index(self):
        """Save the encrypted file index"""
        try:
            index_json = json.dumps(self.file_index).encode()
            encrypted_index = self.fernet.encrypt(index_json)
            with open(self.index_file, "wb") as f:
                f.write(encrypted_index)
        except Exception as e:
            raise Exception(f"Failed to save secure index: {str(e)}")
    
    def store_file(self, virtual_path, data):
        """Store a file with encrypted filename and content"""
        try:
            secure_filename = self._generate_secure_filename(virtual_path)
            secure_filepath = os.path.join(self.secure_path, secure_filename)
            
            # Encrypt and store the actual file content
            if isinstance(data, str):
                data = data.encode()
            elif isinstance(data, dict):
                data = json.dumps(data).encode()
            
            encrypted_data = self.fernet.encrypt(data)
            
            with open(secure_filepath, "wb") as f:
                f.write(encrypted_data)
            
            # Update the index
            self.file_index[virtual_path] = {
                "secure_filename": secure_filename,
                "created_time": datetime.now().isoformat(),
                "size": len(encrypted_data)
            }
            
            self._save_index()
            return True
            
        except Exception as e:
            raise Exception(f"Failed to store file: {str(e)}")
    
    def load_file(self, virtual_path):
        """Load a file by its virtual path"""
        try:
            if virtual_path not in self.file_index:
                return None
            
            secure_filename = self.file_index[virtual_path]["secure_filename"]
            secure_filepath = os.path.join(self.secure_path, secure_filename)
            
            if not os.path.exists(secure_filepath):
                # Clean up invalid index entry
                del self.file_index[virtual_path]
                self._save_index()
                return None
            
            with open(secure_filepath, "rb") as f:
                encrypted_data = f.read()
            
            decrypted_data = self.fernet.decrypt(encrypted_data)
            return decrypted_data
            
        except Exception as e:
            raise Exception(f"Failed to load file: {str(e)}")
    
    def delete_file(self, virtual_path):
        """Delete a file by its virtual path"""
        try:
            if virtual_path not in self.file_index:
                return False
            
            secure_filename = self.file_index[virtual_path]["secure_filename"]
            secure_filepath = os.path.join(self.secure_path, secure_filename)
            
            # Remove the physical file
            if os.path.exists(secure_filepath):
                os.remove(secure_filepath)
            
            # Remove from index
            del self.file_index[virtual_path]
            self._save_index()
            return True
            
        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}")
    
    def list_files(self, path_prefix=""):
        """List all files that match the given path prefix"""
        matching_files = []
        for virtual_path in self.file_index.keys():
            if virtual_path.startswith(path_prefix):
                matching_files.append({
                    "virtual_path": virtual_path,
                    "created_time": self.file_index[virtual_path]["created_time"],
                    "size": self.file_index[virtual_path]["size"]
                })
        return matching_files
    
    def create_virtual_folder(self, folder_path):
        """Create a virtual folder by storing a marker file"""
        marker_path = f"{folder_path}/.folder_marker"
        marker_data = {"created_time": datetime.now().isoformat(), "type": "folder"}
        return self.store_file(marker_path, marker_data)
    
    def list_virtual_folders(self):
        """List all virtual folders"""
        folders = set()
        for virtual_path in self.file_index.keys():
            if "/.folder_marker" in virtual_path:
                folder_path = virtual_path.replace("/.folder_marker", "")
                folders.add(folder_path)
            else:
                # Extract folder path from file path
                path_parts = virtual_path.split("/")
                if len(path_parts) > 1:
                    folder_path = "/".join(path_parts[:-1])
                    folders.add(folder_path)
        return sorted(list(folders))
    
    def get_file_info(self, virtual_path):
        """Get information about a file"""
        if virtual_path in self.file_index:
            return self.file_index[virtual_path].copy()
        return None
    
    def cleanup_orphaned_files(self):
        """Remove physical files that are not in the index"""
        cleaned_count = 0
        try:
            for filename in os.listdir(self.secure_path):
                if filename == "index.enc":
                    continue
                    
                filepath = os.path.join(self.secure_path, filename)
                if os.path.isfile(filepath):
                    # Check if this file is referenced in the index
                    found = False
                    for entry in self.file_index.values():
                        if entry["secure_filename"] == filename:
                            found = True
                            break
                    
                    if not found:
                        os.remove(filepath)
                        cleaned_count += 1
            
            return cleaned_count
        except Exception as e:
            raise Exception(f"Failed to cleanup orphaned files: {str(e)}")
    
    def get_storage_stats(self):
        """Get statistics about the secure storage"""
        total_files = len(self.file_index)
        total_size = 0
        physical_files = 0
        
        try:
            for filename in os.listdir(self.secure_path):
                filepath = os.path.join(self.secure_path, filename)
                if os.path.isfile(filepath):
                    physical_files += 1
                    total_size += os.path.getsize(filepath)
        except Exception:
            pass
        
        return {
            "virtual_files": total_files,
            "physical_files": physical_files,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }