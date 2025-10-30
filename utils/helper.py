from typing import Any

def safe_serialize(obj: Any):
    """Ensure any object can be safely logged as JSON."""
    if isinstance(obj, dict):
        return {k: safe_serialize(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [safe_serialize(v) for v in obj]
    if hasattr(obj, "model_dump"):
        return obj.model_dump()
    return str(obj)
