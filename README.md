# 🛡️ Phantom-Veil

Encrypted memory protection and secure data isolation for the Obsidian Labs security platform.

## Overview

Phantom-Veil provides hardware-backed memory encryption, secure key management, and memory isolation at the kernel level. It integrates with [specter-net](https://github.com/nicolas-beau/specter-net) for threat-triggered containment and [obsidian-core](https://github.com/nicolas-beau/obsidian-labs) for policy orchestration.

## Features

- **AES-256 memory encryption** — Transparent per-page encryption
- **Hardware key management** — Keys generated and stored in secure processor
- **DMA protection** — IOMMU enforcement for device isolation
- **Memory quarantine** — Instant process isolation on threat detection
- **Zero-copy attestation** — Hardware-signed memory integrity reports

## Architecture

```
┌─────────────────────────────────────────┐
│        Application Layer                 │
│  ┌──────────────────────────────────┐   │
│  │  Phantom-Veil Python API         │   │
│  └──────────────┬───────────────────┘   │
│  ┌──────────────┴───────────────────┐   │
│  │  Encryption Engine (AES-256)     │   │
│  │  Per-VM key, hardware-managed    │   │
│  └──────────────┬───────────────────┘   │
│  ┌──────────────┴───────────────────┐   │
│  │  Kernel Driver (HSL interface)   │   │
│  └──────────────┬───────────────────┘   │
│  ┌──────────────┴───────────────────┐   │
│  │  Hardware Security Layer         │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

## Integration

| Component | Integration Point |
|-----------|------------------|
| [specter-net](https://github.com/nicolas-beau/specter-net) | Threat events trigger memory quarantine |
| [cerebro](https://github.com/nicolas-beau/cerebro) | ML models stored in encrypted memory |
| [ironclad](https://github.com/nicolas-beau/ironclad) | Build artifacts integrity-verified |
| [obsidian-labs](https://github.com/nicolas-beau/obsidian-labs) | Architecture & company docs |

## Quick Start

```python
from phantom_veil import PhantomVeil

veil = PhantomVeil()
veil.init(config={"mode": "enforce", "algorithm": "AES-256-GCM"})

# Encrypt a memory region
veil.encrypt_region(addr=0x7f000000, size=4096)

# Attest memory integrity
report = veil.attest()
print(report.status)  # "verified"
```

## License

Apache 2.0 — See [LICENSE](LICENSE)
