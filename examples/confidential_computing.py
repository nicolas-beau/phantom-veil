"""Confidential computing with secure enclaves."""
from phantom_veil.enclave import SecureEnclave, EnclaveConfig

# Create enclave with 256MB memory
enclave = SecureEnclave(EnclaveConfig(memory_size=256*1024*1024))
eid = enclave.create()
enclave.attach(eid)

# Seal sensitive data
enclave.seal("api_key", b"sk-very-secret-key-12345")
enclave.seal("private_key", b"-----BEGIN PRIVATE KEY-----\nMIIE...")

# Run computation inside enclave
result = enclave.run(
    code=b"def process(data): return encrypt(data)",
    data=b"sensitive_input_data"
)

# Get attestation report
report = enclave.get_report()
print(f"Enclave: {report.enclave_id}")
print(f"Measurement: {report.measurement[:32]}...")

# Cleanup
enclave.destroy()
print("Enclave destroyed, all sealed data wiped")
