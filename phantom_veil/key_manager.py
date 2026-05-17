"""Hardware-backed key management for Phantom-Veil."""
import os
import uuid
import time
import logging
from typing import Optional, Dict
from dataclasses import dataclass

logger = logging.getLogger("phantom-veil.keys")

@dataclass
class Key:
    key_id: str
    material: bytes
    created_at: float
    algorithm: str
    rotated: bool = False

class KeyManager:
    """Manages encryption keys via hardware secure processor."""

    def __init__(self, algorithm: str = "AES-256-GCM"):
        self.algorithm = algorithm
        self.keys: Dict[str, Key] = {}
        self.active_key_id: Optional[str] = None
        self.rotation_interval = 86400  # 24h

    def generate_master_key(self) -> str:
        """Generate master key in hardware secure processor."""
        key_id = f"master-{uuid.uuid4().hex[:8]}"
        key = Key(
            key_id=key_id,
            material=os.urandom(32),  # In production: PSP-generated
            created_at=time.time(),
            algorithm=self.algorithm,
        )
        self.keys[key_id] = key
        self.active_key_id = key_id
        logger.info(f"Master key generated: {key_id}")
        return key_id

    def get_active_key(self) -> Key:
        """Get the currently active encryption key."""
        if not self.active_key_id:
            raise RuntimeError("No active key — call generate_master_key() first")
        return self.keys[self.active_key_id]

    def get_key(self, key_id: str) -> Key:
        """Get a specific key by ID."""
        if key_id not in self.keys:
            raise KeyError(f"Key {key_id} not found")
        return self.keys[key_id]

    def rotate(self) -> bool:
        """Rotate to a new encryption key."""
        old_key = self.get_active_key()
        old_key.rotated = True
        new_id = self.generate_master_key()
        logger.info(f"Key rotated: {old_key.key_id} -> {new_id}")
        return True

    def needs_rotation(self) -> bool:
        """Check if key rotation is needed."""
        if not self.active_key_id:
            return True
        key = self.keys[self.active_key_id]
        return (time.time() - key.created_at) > self.rotation_interval

    def export_key_report(self) -> Dict:
        """Export key status report (no key material exposed)."""
        return {
            "active_key_id": self.active_key_id,
            "total_keys": len(self.keys),
            "rotation_needed": self.needs_rotation(),
            "keys": [
                {"id": k.key_id, "created": k.created_at, "rotated": k.rotated}
                for k in self.keys.values()
            ],
        }
