from typing import Dict, Any, List
from datetime import datetime

def parse_datetime(dt_str: str) -> datetime:
    return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

def parse_response(response: Dict[str, Any]) -> Dict[str, Any]:
    """Parse common response fields"""
    if "metadata" in response:
        response["metadata"] = {
            "totalItems": response["metadata"].get("totalItems"),
            "currentPage": response["metadata"].get("currentPage"),
            "pageSize": response["metadata"].get("pageSize"),
            "totalPages": response["metadata"].get("totalPages"),
            "nextPage": response["metadata"].get("nextPage"),
            "prevPage": response["metadata"].get("prevPage")
        }
    return response

def create_enum_list(enum_class, values: List[str]) -> List[Any]:
    return [enum_class(value) for value in values]

def safe_get(d: dict, key: str) -> str:
    return d.get(key, None)