"""Audit logging for compliance and forensics."""
import json
import time
import logging
from typing import Optional, Dict, Any
from pathlib import Path
from dataclasses import dataclass, asdict

logger = logging.getLogger("phantom-veil.audit")

@dataclass
class AuditEvent:
    timestamp: float
    event_type: str
    component: str
    action: str
    target: Optional[str]
    result: str  # success, failure, blocked
    details: Dict[str, Any]
    actor: str  # system, user, specter-net, cerebro

class AuditLogger:
    """Tamper-proof audit logging for Phantom-Veil operations."""

    def __init__(self, log_path: str = "/var/log/phantom-veil/audit.jsonl"):
        self.log_path = Path(log_path)
        self.events: list = []
        self._hash_chain: list = []

    def log(self, event: AuditEvent):
        """Log an audit event with hash chain integrity."""
        event_dict = asdict(event)

        # Hash chain for tamper detection
        prev_hash = self._hash_chain[-1] if self._hash_chain else "genesis"
        import hashlib
        chain_hash = hashlib.sha256(
            (prev_hash + json.dumps(event_dict, sort_keys=True)).encode()
        ).hexdigest()
        event_dict["_chain_hash"] = chain_hash

        self.events.append(event_dict)
        self._hash_chain.append(chain_hash)

        # Write to file
        self.log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.log_path, "a") as f:
            f.write(json.dumps(event_dict) + "\n")

        logger.debug(f"Audit: {event.event_type}/{event.action} -> {event.result}")

    def verify_chain(self) -> bool:
        """Verify audit log hash chain integrity."""
        prev_hash = "genesis"
        for event in self.events:
            expected = event.get("_chain_hash")
            import hashlib
            actual = hashlib.sha256(
                (prev_hash + json.dumps({k: v for k, v in event.items() if k != "_chain_hash"}, sort_keys=True)).encode()
            ).hexdigest()
            if actual != expected:
                return False
            prev_hash = expected
        return True

    def query(self, event_type: Optional[str] = None, component: Optional[str] = None, limit: int = 100) -> list:
        """Query audit events."""
        results = self.events
        if event_type:
            results = [e for e in results if e["event_type"] == event_type]
        if component:
            results = [e for e in results if e["component"] == component]
        return results[-limit:]
