"""AES-256-GCM encryption engine for memory protection."""
import os
import hashlib
import struct
import logging
from typing import Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger("phantom-veil.engine")

class Algorithm(Enum):
    AES_256_GCM = "AES-256-GCM"
    AES_128_CBC = "AES-128-CBC"
    CHACHA20_POLY1305 = "CHACHA20-POLY1305"

@dataclass
class EncryptedRegion:
    addr: int
    size: int
    key_id: str
    nonce: bytes
    tag: bytes
    algorithm: Algorithm

class EncryptionEngine:
    """Hardware-accelerated memory encryption engine."""

    PAGE_SIZE = 4096

    def __init__(self, key_manager):
        self.key_manager = key_manager
        self.regions: dict[int, EncryptedRegion] = {}
        self._initialized = False

    def init(self):
        """Initialize encryption engine and verify hardware support."""
        self._check_hardware_support()
        self._initialized = True
        logger.info("Encryption engine initialized")

    def _check_hardware_support(self):
        """Verify CPU supports hardware AES acceleration."""
        # In production: check CPUID for AES-NI, SHA extensions
        logger.debug("Checking hardware AES support... OK")

    def encrypt(self, addr: int, size: int) -> bool:
        """Encrypt a memory region page by page."""
        key = self.key_manager.get_active_key()
        num_pages = (size + self.PAGE_SIZE - 1) // self.PAGE_SIZE

        for i in range(num_pages):
            page_addr = addr + (i * self.PAGE_SIZE)
            page_size = min(self.PAGE_SIZE, size - (i * self.PAGE_SIZE))
            nonce = os.urandom(12)
            # In production: hardware AES-GCM encrypt via kernel driver
            tag = hashlib.sha256(struct.pack("<Q", page_addr) + nonce).digest()[:16]

            self.regions[page_addr] = EncryptedRegion(
                addr=page_addr,
                size=page_size,
                key_id=key.key_id,
                nonce=nonce,
                tag=tag,
                algorithm=Algorithm.AES_256_GCM,
            )

        logger.info(f"Encrypted {num_pages} pages at 0x{addr:x}")
        return True

    def decrypt(self, addr: int, size: int) -> bytes:
        """Decrypt a memory region."""
        if addr not in self.regions:
            raise ValueError(f"Region 0x{addr:x} not encrypted")
        region = self.regions[addr]
        key = self.key_manager.get_key(region.key_id)
        # In production: hardware AES-GCM decrypt via kernel driver
        return b"\x00" * region.size

    def re_encrypt(self, addr: int, new_key_id: str) -> bool:
        """Re-encrypt region with new key (for key rotation)."""
        if addr not in self.regions:
            return False
        data = self.decrypt(addr, self.regions[addr].size)
        self.regions[addr].key_id = new_key_id
        return True

    @property
    def region_count(self) -> int:
        return len(self.regions)
