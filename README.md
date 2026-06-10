# 🛡️ Phantom-Veil

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)
[![Status](https://img.shields.io/badge/status-alpha-red.svg)]()
[![Platform](https://img.shields.io/badge/platform-linux-lightgrey.svg)]()

Encrypted memory protection and secure data isolation for the Obsidian Labs security platform.

## What It Does

Phantom-Veil provides **hardware-backed memory encryption** that protects sensitive workloads from memory disclosure, DMA attacks, and cold boot extraction. It integrates with the Obsidian ecosystem for automated threat response.

## Key Features

| Feature | Description |
|---------|-------------|
| 🔐 AES-256-GCM Encryption | Transparent per-page memory encryption |
| 🔑 Hardware Key Management | Keys generated in secure processor, never in host memory |
| 🛡️ DMA Protection | IOMMU enforcement for device isolation |
| 🔒 Process Quarantine | Instant memory isolation on threat detection |
| 📋 Attestation | Hardware-signed integrity reports |
| 🏰 Secure Enclaves | AMD SEV-based confidential computing |

## Ecosystem Integration

```
specter-net ──→ detects threat ──→ phantom-veil ──→ quarantines memory
     ↑                                                    │
     └────────────── obsidian-core (policy) ←─────────────┘
                           │
cerebro ←── encrypted model storage ───→ phantom-veil
                           │
ironclad ←── artifact verification ───→ phantom-veil
```

| Component | Integration |
|-----------|-------------|
| [obsidian-labs](https://github.com/nicolas-beau/obsidian-labs) | Company & architecture docs |
| [specter-net](https://github.com/nicolas-beau/specter-net) | Threat events trigger quarantine |
| [cerebro](https://github.com/nicolas-beau/cerebro) | ML models stored encrypted |
| [ironclad](https://github.com/nicolas-beau/ironclad) | Build integrity verification |

## Quick Start

```bash
git clone https://github.com/nicolas-beau/phantom-veil.git
cd phantom-veil
pip install -r requirements.txt
make test
```

## Documentation

- [API Reference](docs/api-reference.md)
- [DMA Protection](docs/dma-protection.md)
- [Performance Tuning](docs/performance.md)
- [Security Hardening](docs/security-hardening.md)
- [Troubleshooting](docs/troubleshooting.md)

## License

Apache 2.0 — See [LICENSE](LICENSE)
