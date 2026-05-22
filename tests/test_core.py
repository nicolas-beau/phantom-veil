"""Tests for Phantom-Veil core functionality."""
import pytest
from phantom_veil import PhantomVeil
from phantom_veil.core import VeilConfig

class TestPhantomVeil:
    def setup_method(self):
        self.veil = PhantomVeil(VeilConfig(mode="detect"))

    def test_init(self):
        assert self.veil.init() is True
        assert self.veil._initialized is True

    def test_encrypt_region(self):
        self.veil.init()
        result = self.veil.encrypt_region(0x7f000000, 4096)
        assert result is True

    def test_encrypt_before_init_raises(self):
        with pytest.raises(RuntimeError):
            self.veil.encrypt_region(0x7f000000, 4096)

    def test_quarantine(self):
        self.veil.init()
        assert self.veil.quarantine(1234) is True

    def test_attestation(self):
        self.veil.init()
        report = self.veil.attest()
        assert report.status == "verified"

    def test_status(self):
        self.veil.init()
        status = self.veil.get_status()
        assert status["initialized"] is True
        assert status["mode"] == "detect"
