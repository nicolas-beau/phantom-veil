"""Tests for key management."""
import time
import pytest
from phantom_veil.key_manager import KeyManager

class TestKeyManager:
    def setup_method(self):
        self.km = KeyManager()

    def test_generate_master_key(self):
        key_id = self.km.generate_master_key()
        assert key_id.startswith("master-")
        assert self.km.active_key_id == key_id

    def test_get_active_key(self):
        self.km.generate_master_key()
        key = self.km.get_active_key()
        assert key.key_id == self.km.active_key_id
        assert len(key.material) == 32

    def test_rotate(self):
        old_id = self.km.generate_master_key()
        assert self.km.rotate() is True
        assert self.km.active_key_id != old_id

    def test_needs_rotation_false(self):
        self.km.generate_master_key()
        assert self.km.needs_rotation() is False

    def test_needs_rotation_true(self):
        self.km.generate_master_key()
        self.km.keys[self.km.active_key_id].created_at = time.time() - 90000
        assert self.km.needs_rotation() is True

    def test_export_report_no_material(self):
        self.km.generate_master_key()
        report = self.km.export_key_report()
        assert "active_key_id" in report
        # Ensure no key material in report
        for k in report["keys"]:
            assert "material" not in k
