import json
from typing import Dict, Any


class FileIO:
    """
    Handles file input/output operations for JSON files.
    """
    
    @staticmethod
    def load_json_file(file_path: str) -> Dict[str, Any]:
        """
        Load and parse a JSON file.
        
        Args:
            file_path: Path to the JSON file to load
        
        Returns:
            dict: Parsed JSON data as a dictionary
        
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file contains invalid JSON
        """
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    
    @staticmethod
    def save_json_file(file_path: str, data: Dict[str, Any]) -> None:
        """
        Save data to a JSON file.
        
        Args:
            file_path: Path to the JSON file to save
            data: Dictionary data to save as JSON
        
        Raises:
            IOError: If the file cannot be written
        """
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

