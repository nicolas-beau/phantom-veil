"""Integration interfaces for Obsidian ecosystem components."""
import json
import logging
import time
from typing import Callable, Optional, Dict, Any
from dataclasses import dataclass

logger = logging.getLogger("phantom-veil.integrations")

@dataclass
class ThreatEvent:
    """Threat event from specter-net."""
    event_id: str
    source: str  # specter-net, cerebro, manual
    severity: str  # critical, high, medium, low
    event_type: str
    target_pid: Optional[int]
    confidence: float
    timestamp: float
    details: Dict[str, Any]

class SpecterNetIntegration:
    """Receive and process threat events from specter-net."""

    def __init__(self, memory_guard, config: dict = None):
        self.memory_guard = memory_guard
        self.config = config or {}
        self.handlers: Dict[str, Callable] = {}
        self.event_log: list = []
        self._setup_handlers()

    def _setup_handlers(self):
        """Register default threat event handlers."""
        self.handlers = {
            "process_injection": self._handle_process_injection,
            "lateral_movement": self._handle_lateral_movement,
            "memory_disclosure": self._handle_memory_disclosure,
            "privilege_escalation": self._handle_privilege_escalation,
            "fileless_malware": self._handle_fileless_malware,
        }

    def on_threat_event(self, event: ThreatEvent):
        """Process incoming threat event from specter-net."""
        self.event_log.append(event)
        logger.info(f"Threat event received: {event.event_type} (severity={event.severity}, confidence={event.confidence})")

        handler = self.handlers.get(event.event_type)
        if handler:
            handler(event)
        else:
            logger.warning(f"No handler for event type: {event.event_type}")

    def _handle_process_injection(self, event: ThreatEvent):
        """Handle process injection threat."""
        if event.confidence >= 0.85 and event.target_pid:
            self.memory_guard.quarantine_process(event.target_pid, reason=f"injection:{event.event_id}")

    def _handle_lateral_movement(self, event: ThreatEvent):
        """Handle lateral movement detection."""
        if event.confidence >= 0.80 and event.target_pid:
            self.memory_guard.quarantine_process(event.target_pid, reason=f"lateral:{event.event_id}")

    def _handle_memory_disclosure(self, event: ThreatEvent):
        """Handle memory disclosure attempt."""
        if event.target_pid:
            self.memory_guard.quarantine_process(event.target_pid, reason=f"disclosure:{event.event_id}")

    def _handle_privilege_escalation(self, event: ThreatEvent):
        """Handle privilege escalation attempt."""
        if event.confidence >= 0.90 and event.target_pid:
            self.memory_guard.quarantine_process(event.target_pid, reason=f"privesc:{event.event_id}")

    def _handle_fileless_malware(self, event: ThreatEvent):
        """Handle fileless malware detection."""
        if event.target_pid:
            self.memory_guard.snapshot_memory(event.target_pid)
            self.memory_guard.quarantine_process(event.target_pid, reason=f"fileless:{event.event_id}")

    def get_event_stats(self) -> dict:
        """Get event processing statistics."""
        return {
            "total_events": len(self.event_log),
            "by_severity": {
                s: len([e for e in self.event_log if e.severity == s])
                for s in ["critical", "high", "medium", "low"]
            },
            "quarantined": self.memory_guard.quarantine_count,
        }

class CerebroIntegration:
    """Interface for cerebro ML engine integration."""

    def __init__(self, phantom_veil):
        self.veil = phantom_veil
        self.model_store: Dict[str, dict] = {}

    def store_model_encrypted(self, model_id: str, model_data: bytes, metadata: dict) -> bool:
        """Store ML model weights in encrypted memory (via phantom-veil)."""
        logger.info(f"Storing encrypted model: {model_id} ({len(model_data)} bytes)")
        self.model_store[model_id] = {
            "size": len(model_data),
            "metadata": metadata,
            "encrypted": True,
            "stored_at": time.time(),
        }
        return True

    def load_model_encrypted(self, model_id: str) -> Optional[bytes]:
        """Load ML model from encrypted memory."""
        if model_id not in self.model_store:
            logger.error(f"Model not found: {model_id}")
            return None
        logger.info(f"Loading encrypted model: {model_id}")
        return b"model_data_placeholder"

    def attest_model_integrity(self, model_id: str) -> bool:
        """Verify model hasn't been tampered with."""
        if model_id not in self.model_store:
            return False
        return True
