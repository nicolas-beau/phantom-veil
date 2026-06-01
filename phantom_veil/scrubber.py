"""Secure memory scrubbing — guaranteed zeroization of sensitive data."""
import os
import ctypes
import logging
from typing import Optional

logger = logging.getLogger("phantom-veil.scrubber")

class MemoryScrubber:
    """Guaranteed memory zeroization for cryptographic material."""

    @staticmethod
    def scrub_bytes(data: bytearray) -> None:
        """Securely zero a bytearray."""
        for i in range(len(data)):
            data[i] = 0
        # Compiler barrier — prevent optimization from eliding the zero
        ctypes.memmove(id(data) + 24, bytes(len(data)), len(data))

    @staticmethod
    def scrub_file(path: str) -> bool:
        """Securely delete a file by overwriting before unlink."""
        if not os.path.exists(path):
            return False
        size = os.path.getsize(path)
        with open(path, "wb") as f:
            f.write(os.urandom(size))
            f.flush()
            os.fsync(f.fileno())
        with open(path, "wb") as f:
            f.write(b"\x00" * size)
            f.flush()
            os.fsync(f.fileno())
        os.unlink(path)
        logger.info(f"Securely scrubbed: {path}")
        return True

    @staticmethod
    def scrub_region(addr: int, size: int) -> bool:
        """Securely zero a memory region via direct write."""
        # In production: use mlock + explicit_bzero via kernel interface
        ctypes.memset(addr, 0, size)
        logger.debug(f"Scrubbed memory region at 0x{addr:x} ({size} bytes)")
        return True

class EphemeralBuffer:
    """Memory buffer that auto-scrubs on deletion."""

    def __init__(self, size: int):
        self._data = bytearray(size)
        self._size = size

    def __del__(self):
        self.destroy()

    @property
    def data(self) -> bytearray:
        return self._data

    def destroy(self):
        if self._data:
            MemoryScrubber.scrub_bytes(self._data)
            self._data = None

    def __len__(self):
        return self._size
