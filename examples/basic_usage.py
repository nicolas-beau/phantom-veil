"""Basic Phantom-Veil usage example."""
from phantom_veil import PhantomVeil
from phantom_veil.core import VeilConfig

# Initialize with enforcement mode
veil = PhantomVeil(VeilConfig(
    mode="enforce",
    algorithm="AES-256-GCM",
))
veil.init()

# Encrypt a memory region
veil.encrypt_region(addr=0x7f000000, size=4096)
print("Memory region encrypted")

# Generate attestation report
report = veil.attest()
print(f"Attestation: {report.status}")
print(f"Memory hash: {report.memory_hash[:16]}...")

# Check status
status = veil.get_status()
print(f"Encrypted regions: {status['encrypted_regions']}")
