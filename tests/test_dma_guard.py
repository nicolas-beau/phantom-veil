"""Tests for DMA protection."""
import pytest
from phantom_veil.dma_guard import DMAGuard, DeviceTrustLevel

class TestDMAGuard:
    def setup_method(self):
        self.guard = DMAGuard()

    def test_register_device(self):
        assert self.guard.register_device("gpu0", "0000:01:00.0", DeviceTrustLevel.TRUSTED) is True
        assert "gpu0" in self.guard.devices

    def test_check_access_trusted(self):
        self.guard.register_device("gpu0", "0000:01:00.0", DeviceTrustLevel.TRUSTED)
        self.guard.add_allowed_region("gpu0", 0x10000000, 0x1000)
        assert self.guard.check_access("gpu0", 0x10000000, 256) is True

    def test_check_access_blocked_device(self):
        self.guard.register_device("usb0", "0000:02:00.0", DeviceTrustLevel.BLOCKED)
        assert self.guard.check_access("usb0", 0x10000000, 256) is False

    def test_check_access_unknown_device(self):
        assert self.guard.check_access("unknown", 0x10000000, 256) is False

    def test_dma_status(self):
        self.guard.register_device("gpu0", "0000:01:00.0", DeviceTrustLevel.TRUSTED)
        self.guard.register_device("usb0", "0000:02:00.0", DeviceTrustLevel.BLOCKED)
        status = self.guard.get_status()
        assert status["trusted"] == 1
        assert status["blocked"] == 1
