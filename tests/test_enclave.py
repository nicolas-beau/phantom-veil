"""Tests for secure enclave interface."""
import pytest
from phantom_veil.enclave import SecureEnclave, EnclaveConfig

class TestSecureEnclave:
    def setup_method(self):
        self.enclave = SecureEnclave(EnclaveConfig(memory_size=64*1024*1024))

    def test_create(self):
        eid = self.enclave.create()
        assert eid is not None
        assert len(eid) == 16

    def test_attach(self):
        eid = self.enclave.create()
        enclave2 = SecureEnclave()
        assert enclave2.attach(eid) is True

    def test_seal_unseal(self):
        self.enclave.create()
        self.enclave.attach(self.enclave.enclave_id)
        self.enclave.seal("key1", b"secret_data")
        assert self.enclave.unseal("key1") == b"secret_data"

    def test_destroy_wipes_sealed_data(self):
        self.enclave.create()
        self.enclave.attach(self.enclave.enclave_id)
        self.enclave.seal("key1", b"secret")
        self.enclave.destroy()
        assert self.enclave.unseal("key1") is None
