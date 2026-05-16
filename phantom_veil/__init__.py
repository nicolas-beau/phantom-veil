"""Phantom-Veil: Encrypted memory protection for Obsidian Labs."""
from .engine import EncryptionEngine
from .key_manager import KeyManager
from .memory_guard import MemoryGuard
from .attestation import AttestationService
from .core import PhantomVeil

__version__ = "0.1.0"
__all__ = ["PhantomVeil", "EncryptionEngine", "KeyManager", "MemoryGuard", "AttestationService"]
