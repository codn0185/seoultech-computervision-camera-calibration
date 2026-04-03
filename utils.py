from config import App

import os
import json
import numpy as np


class Json:
    FILE_EXTENSION: str = "json"

    @staticmethod
    def _to_serializable(data):
        if isinstance(data, np.ndarray):
            return data.tolist()
        if isinstance(data, np.generic):
            return data.item()
        if isinstance(data, dict):
            return {k: Json._to_serializable(v) for k, v in data.items()}
        if isinstance(data, (list, tuple)):
            return [Json._to_serializable(v) for v in data]
        return data

    @staticmethod
    def _to_file_path(file_name: str) -> str:
        if file_name.endswith(f".{Json.FILE_EXTENSION}"):
            return file_name
        return f"{file_name}.{Json.FILE_EXTENSION}"

    @staticmethod
    def save(data: dict, file_name: str) -> None:
        file_path = Json._to_file_path(file_name)
        directory = os.path.dirname(file_path)

        if directory:
            os.makedirs(directory, exist_ok=True)

        serializable_data = Json._to_serializable(data)

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(serializable_data, f, indent=4, ensure_ascii=False)

    @staticmethod
    def load(file_name: str) -> dict:
        file_path = Json._to_file_path(file_name)

        with open(file_path, "r", encoding="utf-8") as f:
            return json.load(f)
