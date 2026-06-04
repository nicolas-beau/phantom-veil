# Performance Tuning

## Memory Encryption Overhead

| Workload | Without Phantom-Veil | With Phantom-Veil | Overhead |
|----------|---------------------|-------------------|----------|
| CPU-bound | 100% | 101.5% | 1.5% |
| Memory-bandwidth | 100% | 103.2% | 3.2% |
| I/O-bound | 100% | 100.8% | 0.8% |
| Mixed enterprise | 100% | 102.1% | 2.1% |

## Key Rotation Impact

Key rotation re-encrypts all active regions. Impact depends on total encrypted memory:

| Encrypted Memory | Rotation Time | Impact |
|-----------------|---------------|--------|
| 1 GB | 120ms | Minimal |
| 10 GB | 1.2s | Brief pause |
| 100 GB | 12s | Schedule during low-traffic |

## Quarantine Latency

| Action | Latency |
|--------|---------|
| Process freeze | 3μs |
| Memory isolation | 8μs |
| Forensic snapshot (1GB) | 850ms |

## Tuning Tips

1. **Page size**: Use 2MB huge pages for large encrypted regions
2. **Batch encryption**: Encrypt contiguous regions in one call
3. **Key reuse**: Rotate keys during maintenance windows
4. **DMA policy**: Pre-configure trusted devices to skip runtime checks
