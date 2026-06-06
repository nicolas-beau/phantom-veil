# Troubleshooting Guide

## Common Issues

### 1. "IOMMU not available"

**Symptom**: DMA guard fails to initialize
**Solution**:
```bash
# Check if IOMMU is enabled
dmesg | grep -i iommu
# If not, enable in GRUB
echo 'GRUB_CMDLINE_LINUX="amd_iommu=on iommu=pt"' >> /etc/default/grub
update-grub && reboot
```

### 2. "Hardware AES not detected"

**Symptom**: Encryption engine uses software fallback
**Solution**:
```bash
# Check for AES-NI support
grep -o aes /proc/cpuinfo | head -1
# If missing, CPU doesn't support hardware AES
```

### 3. "Key rotation failed"

**Symptom**: Key rotation returns False
**Solution**: Check secure processor status:
```bash
cat /sys/kernel/security/phantom/psp_status
```

### 4. "Quarantine not working"

**Symptom**: Processes not isolated after threat event
**Check**:
- Mode is set to `enforce` (not `detect`/`audit`)
- specter-net integration is enabled
- Confidence threshold is met

### 5. "High memory overhead"

**Symptom**: System uses more RAM than expected
**Explanation**: Each encrypted page has metadata overhead (~64 bytes)
**Solution**: Encrypt only sensitive regions, not entire memory

## Diagnostic Commands

```bash
# Check Phantom-Veil status
curl localhost:9090/status

# View metrics
curl localhost:9090/metrics

# Check audit log
tail -f /var/log/phantom-veil/audit.jsonl

# Verify attestation
python3 -c "from phantom_veil import PhantomVeil; v = PhantomVeil(); v.init(); print(v.attest())"
```
