"""Tests for memory guard quarantine functionality."""
import pytest
from phantom_veil.memory_guard import MemoryGuard, IsolationLevel

class TestMemoryGuard:
    def setup_method(self):
        self.guard = MemoryGuard(mode="enforce")
        self.guard.start()

    def test_quarantine_process(self):
        assert self.guard.quarantine_process(1234, "test") is True
        assert self.guard.quarantine_count == 1

    def test_quarantine_stopped_guard(self):
        self.guard.stop()
        assert self.guard.quarantine_process(1234) is False

    def test_release_process(self):
        self.guard.quarantine_process(1234)
        assert self.guard.release_process(1234) is True
        assert self.guard.quarantine_count == 0

    def test_release_nonexistent(self):
        assert self.guard.release_process(9999) is False

    def test_snapshot_memory(self):
        self.guard.quarantine_process(1234)
        assert self.guard.snapshot_memory(1234) is True

    def test_audit_mode(self):
        guard = MemoryGuard(mode="audit")
        guard.start()
        assert guard.quarantine_process(1234) is True
        assert guard.quarantine_count == 0  # Audit doesn't actually quarantine

    def test_get_isolated_processes(self):
        self.guard.quarantine_process(100, "reason_a")
        self.guard.quarantine_process(200, "reason_b")
        procs = self.guard.get_isolated_processes()
        assert len(procs) == 2
