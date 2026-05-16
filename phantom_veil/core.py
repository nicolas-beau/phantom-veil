"""Core Phantom-Veil orchestrator."""
import logging
from typing import Optional, Dict, Any
from dataclasses import dataclass
from .engine import EncryptionEngine
from .key_manager import KeyManager
from .memory_guard import MemoryGuard
from .attestation import AttestationService

logger = logging.getLogger("phantom-veil")

@dataclass
class VeilConfig:
    mode: str = "detect"  # detect | enforce | audit
    algorithm: str = "AES-256-GCM"
    key_rotation_interval: int = 86400  # 24h in seconds
    quarantine_on_threat: bool = True
    attestation_interval: int = 300  # 5 min

class PhantomVeil:
    """Main entry point for Phantom-Veil memory protection."""

    def __init__(self, config: Optional[VeilConfig] = None):
        self.config = config or VeilConfig()
        self.key_manager = KeyManager(algorithm=self.config.algorithm)
        self.engine = EncryptionEngine(self.key_manager)
        self.memory_guard = MemoryGuard(mode=self.config.mode)
        self.attestation = AttestationService()
        self._initialized = False

    def init(self, config: Optional[Dict[str, Any]] = None) -> bool:
        """Initialize the protection engine."""
        if config:
            for k, v in config.items():
                if hasattr(self.config, k):
                    setattr(self.config, k, v)

        logger.info(f"Initializing Phantom-Veil in {self.config.mode} mode")
        self.key_manager.generate_master_key()
        self.engine.init()
        self.memory_guard.start()
        self._initialized = True
        return True

    def encrypt_region(self, addr: int, size: int) -> bool:
        """Encrypt a memory region with hardware-backed keys."""
        if not self._initialized:
            raise RuntimeError("Phantom-Veil not initialized")
        return self.engine.encrypt(addr, size)

    def decrypt_region(self, addr: int, size: int) -> bytes:
        """Decrypt a memory region."""
        if not self._initialized:
            raise RuntimeError("Phantom-Veil not initialized")
        return self.engine.decrypt(addr, size)

    def quarantine(self, process_id: int) -> bool:
        """Isolate a process memory (triggered by specter-net threat events)."""
        logger.warning(f"Quarantining process {process_id}")
        return self.memory_guard.quarantine_process(process_id)

    def attest(self):
        """Generate hardware-signed attestation report."""
        return self.attestation.generate_report()

    def rotate_keys(self) -> bool:
        """Rotate encryption keys via hardware secure processor."""
        return self.key_manager.rotate()

    def get_status(self) -> Dict[str, Any]:
        """Return current protection status."""
        return {
            "initialized": self._initialized,
            "mode": self.config.mode,
            "algorithm": self.config.algorithm,
            "quarantined_processes": self.memory_guard.quarantine_count,
            "encrypted_regions": self.engine.region_count,
            "last_attestation": self.attestation.last_timestamp,
        }
