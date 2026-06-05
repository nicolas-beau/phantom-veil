# Security Hardening Checklist

## System Configuration

- [ ] Enable IOMMU in BIOS (`amd_iommu=on`)
- [ ] Enable SMEP and SMAP in kernel config
- [ ] Disable unnecessary DMA-capable interfaces (Thunderbolt, FireWire)
- [ ] Enable kernel lockdown mode
- [ ] Set `kernel.kptr_restrict=2`
- [ ] Enable `CONFIG_STATIC_USERMODESHELF`

## Phantom-Veil Configuration

- [ ] Set mode to `enforce` (not `detect`)
- [ ] Enable key rotation (interval ≤ 24h)
- [ ] Configure specter-net integration
- [ ] Set quarantine threshold to ≥ 0.85 confidence
- [ ] Enable audit logging
- [ ] Configure log forwarding to SIEM

## Network

- [ ] Bind management API to localhost only
- [ ] Enable TLS 1.3 for all API endpoints
- [ ] Use mTLS for component-to-component communication
- [ ] Firewall rules: allow only required ports

## Monitoring

- [ ] Prometheus metrics endpoint secured
- [ ] Alert on attestation failures
- [ ] Alert on key rotation failures
- [ ] Monitor quarantine count for anomalies

## Compliance

- [ ] Audit log retention ≥ 90 days
- [ ] Hash chain verification scheduled daily
- [ ] Key material never logged
- [ ] Attestation reports archived
