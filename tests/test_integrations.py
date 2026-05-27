"""Integration tests — specter-net + phantom-veil interaction."""
import time
import pytest
from phantom_veil import PhantomVeil
from phantom_veil.core import VeilConfig
from phantom_veil.integrations import SpecterNetIntegration, ThreatEvent, CerebroIntegration

class TestSpecterNetIntegration:
    def setup_method(self):
        self.veil = PhantomVeil(VeilConfig(mode="enforce"))
        self.veil.init()
        self.integration = SpecterNetIntegration(self.veil.memory_guard)

    def test_process_injection_triggers_quarantine(self):
        event = ThreatEvent(
            event_id="evt_001", source="specter-net", severity="critical",
            event_type="process_injection", target_pid=1234,
            confidence=0.95, timestamp=time.time(), details={}
        )
        self.integration.on_threat_event(event)
        assert self.veil.memory_guard.quarantine_count == 1

    def test_low_confidence_no_quarantine(self):
        event = ThreatEvent(
            event_id="evt_002", source="specter-net", severity="medium",
            event_type="process_injection", target_pid=1234,
            confidence=0.50, timestamp=time.time(), details={}
        )
        self.integration.on_threat_event(event)
        assert self.veil.memory_guard.quarantine_count == 0

    def test_fileless_malware_snapshot_and_quarantine(self):
        event = ThreatEvent(
            event_id="evt_003", source="specter-net", severity="critical",
            event_type="fileless_malware", target_pid=5678,
            confidence=0.99, timestamp=time.time(), details={}
        )
        self.integration.on_threat_event(event)
        assert self.veil.memory_guard.quarantine_count == 1

    def test_event_stats(self):
        for i in range(5):
            self.integration.on_threat_event(ThreatEvent(
                event_id=f"evt_{i}", source="specter-net", severity="high",
                event_type="process_injection", target_pid=1000+i,
                confidence=0.90, timestamp=time.time(), details={}
            ))
        stats = self.integration.get_event_stats()
        assert stats["total_events"] == 5

class TestCerebroIntegration:
    def setup_method(self):
        self.veil = PhantomVeil(VeilConfig(mode="enforce"))
        self.veil.init()
        self.cerebro = CerebroIntegration(self.veil)

    def test_store_and_load_model(self):
        assert self.cerebro.store_model_encrypted("model_v1", b"data", {"version": 1}) is True
        data = self.cerebro.load_model_encrypted("model_v1")
        assert data is not None

    def test_load_nonexistent_model(self):
        assert self.cerebro.load_model_encrypted("nonexistent") is None

    def test_attest_model(self):
        self.cerebro.store_model_encrypted("model_v1", b"data", {})
        assert self.cerebro.attest_model_integrity("model_v1") is True
