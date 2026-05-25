# DMA Protection

## Overview

DMA (Direct Memory Access) attacks allow external devices to read/write 
system memory without CPU involvement. Phantom-Veil's DMA Guard uses 
IOMMU to enforce strict access policies.

## Threat Model

| Attack Vector | Risk | Mitigation |
|---------------|------|------------|
| Thunderbolt DMA | Critical | IOMMU + device attestation |
| PCIe hot-plug | High | Device registration required |
| USB DMA | Medium | Blocked by default |
| FireWire DMA | Critical | Interface disabled |

## Configuration

```yaml
hardware:
  iommu_enabled: true
  dma_policies:
    - device_pattern: "pci:0000:01:*"
      trust: trusted
    - device_pattern: "usb:*"
      trust: blocked
```

## Integration with specter-net

When specter-net detects unauthorized DMA activity, phantom-veil 
automatically isolates the target memory region and alerts the operator.
