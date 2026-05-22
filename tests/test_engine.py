"""Tests for encryption engine."""
import pytest
from phantom_veil.engine import EncryptionEngine
from phantom_veil.key_manager import KeyManager

class TestEncryptionEngine:
    def setup_method(self):
        km = KeyManager()
        km.generate_master_key()
        self.engine = EncryptionEngine(km)
        self.engine.init()

    def test_encrypt_single_page(self):
        result = self.engine.encrypt(0x7f000000, 4096)
        assert result is True
        assert self.engine.region_count == 1

    def test_encrypt_multiple_pages(self):
        result = self.engine.encrypt(0x7f000000, 16384)  # 4 pages
        assert result is True
        assert self.engine.region_count == 4

    def test_decrypt_encrypted_region(self):
        self.engine.encrypt(0x7f000000, 4096)
        data = self.engine.decrypt(0x7f000000, 4096)
        assert len(data) == 4096

    def test_decrypt_unencrypted_raises(self):
        with pytest.raises(ValueError):
            self.engine.decrypt(0xdead0000, 4096)
