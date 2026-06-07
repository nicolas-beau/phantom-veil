"""Automated threat response with specter-net integration."""
import time
from phantom_veil import PhantomVeil
from phantom_veil.integrations import SpecterNetIntegration, ThreatEvent

# Initialize
veil = PhantomVeil()
veil.init()

# Connect specter-net integration
integration = SpecterNetIntegration(veil.memory_guard)

# Simulate threat event from specter-net
event = ThreatEvent(
    event_id="evt_demo_001",
    source="specter-net",
    severity="critical",
    event_type="process_injection",
    target_pid=1337,
    confidence=0.95,
    timestamp=time.time(),
    details={"technique": "process_hollowing", "source_pid": 42},
)

# Process — auto-quarantine triggered
integration.on_threat_event(event)

# Check result
print(f"Quarantined processes: {veil.memory_guard.quarantine_count}")
print(f"Isolated: {veil.memory_guard.get_isolated_processes()}")
