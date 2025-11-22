import json
import os
from dataclasses import dataclass, field

@dataclass
class FStream:
    name: str
    path: str
    extension: str
    data_file: str = field(init=False)

    @classmethod
    def load_json_file(cls, path) -> dict:
        """
        Read a JSON file from a directory

        Args:
            path: The path for the JSON file to read

        Returns:
            dict: A hash map with the JSON structure
        """
        with open(path, 'rb') as data_file:
            cls.data_file = json.load(data_file)

        return cls.data_file


    @staticmethod
    def print_json_structure(data_file):
        for id, item in data_file["Items"].items():
            print(id, item)
