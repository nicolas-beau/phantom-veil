# Phantom-Veil API Reference

## Core API

### `PhantomVeil`

```python
from phantom_veil import PhantomVeil
from phantom_veil.core import VeilConfig

# Initialize
veil = PhantomVeil(VeilConfig(
    mode="enforce",
    algorithm="AES-256-GCM",
    key_rotation_interval=86400,
))
veil.init()
```

#### Methods

| Method | Returns | Description |
|--------|---------|-------------|
| `init(config)` | `bool` | Initialize protection engine |
| `encrypt_region(addr, size)` | `bool` | Encrypt memory region |
| `decrypt_region(addr, size)` | `bytes` | Decrypt memory region |
| `quarantine(pid)` | `bool` | Isolate process memory |
| `attest()` | `AttestationReport` | Generate integrity report |
| `rotate_keys()` | `bool` | Rotate encryption keys |
| `get_status()` | `dict` | Get protection status |

### `EncryptionEngine`

```python
from phantom_veil.engine import EncryptionEngine

engine = EncryptionEngine(key_manager)
engine.init()
engine.encrypt(addr=0x7f000000, size=4096)
```

### `KeyManager`

```python
from phantom_veil.key_manager import KeyManager

km = KeyManager(algorithm="AES-256-GCM")
km.generate_master_key()
km.rotate()
report = km.export_key_report()
```

### `MemoryGuard`

```python
from phantom_veil.memory_guard import MemoryGuard, IsolationLevel

guard = MemoryGuard(mode="enforce")
guard.start()
guard.quarantine_process(pid=1234, reason="injection_detected")
guard.snapshot_memory(pid=1234)
```

### `DMAGuard`

```python
from phantom_veil.dma_guard import DMAGuard, DeviceTrustLevel

dma = DMAGuard()
dma.register_device("gpu0", "0000:01:00.0", DeviceTrustLevel.TRUSTED)
dma.check_access("gpu0", addr=0x10000000, size=256)
```

## Integration API

### `SpecterNetIntegration`

```python
from phantom_veil.integrations import SpecterNetIntegration, ThreatEvent

integration = SpecterNetIntegration(memory_guard)
# Called automatically when specter-net sends threat events
integration.on_threat_event(ThreatEvent(
    event_id="evt_001",
    source="specter-net",
    severity="critical",
    event_type="process_injection",
    target_pid=1234,
    confidence=0.95,
    timestamp=time.time(),
    details={"technique": "process_hollowing"},
))
```

### `CerebroIntegration`

```python
from phantom_veil.integrations import CerebroIntegration

cerebro = CerebroIntegration(phantom_veil)
cerebro.store_model_encrypted("anomaly_v1", model_bytes, metadata)
model = cerebro.load_model_encrypted("anomaly_v1")
```
