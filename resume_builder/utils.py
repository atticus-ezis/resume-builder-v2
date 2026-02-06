import hashlib
import json


def compute_context_hash(value):
    """Return SHA256 hex digest for context value (string or JSON-serializable)."""
    if isinstance(value, str):
        data = value.encode("utf-8")
    else:
        data = json.dumps(value, sort_keys=True).encode("utf-8")
    return hashlib.sha256(data).hexdigest()
