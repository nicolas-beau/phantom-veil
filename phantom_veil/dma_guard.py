"""DMA protection and IOMMU enforcement."""
import logging
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

logger = logging.getLogger("phantom-veil.dma")

class DeviceTrustLevel(Enum):
    TRUSTED = "trusted"
    RESTRICTED = "restricted"
    BLOCKED = "blocked"

@dataclass
class DMADevice:
    device_id: str
    bus_address: str
    trust_level: DeviceTrustLevel
    iommu_group: int
    allowed_regions: List[tuple]  # (addr, size)

class DMAGuard:
    """IOMMU-based DMA protection for external device access."""

    def __init__(self):
        self.devices: Dict[str, DMADevice] = {}
        self.policies: Dict[str, dict] = {}

    def register_device(self, device_id: str, bus_address: str, trust_level: DeviceTrustLevel) -> bool:
        """Register a DMA device with trust level."""
        device = DMADevice(
            device_id=device_id,
            bus_address=bus_address,
            trust_level=trust_level,
            iommu_group=self._get_iommu_group(bus_address),
            allowed_regions=[],
        )
        self.devices[device_id] = device
        logger.info(f"DMA device registered: {device_id} ({trust_level.value})")
        return True

    def set_policy(self, device_id: str, policy: dict) -> bool:
        """Set DMA access policy for a device."""
        if device_id not in self.devices:
            return False
        self.policies[device_id] = policy
        logger.info(f"DMA policy set for {device_id}: {policy}")
        return True

    def check_access(self, device_id: str, addr: int, size: int) -> bool:
        """Check if a DMA access should be allowed."""
        if device_id not in self.devices:
            logger.warning(f"Unknown device {device_id} — blocked")
            return False

        device = self.devices[device_id]
        if device.trust_level == DeviceTrustLevel.BLOCKED:
            logger.warning(f"Blocked DMA from {device_id}")
            return False

        # Check if address is in allowed regions
        for region_addr, region_size in device.allowed_regions:
            if region_addr <= addr < region_addr + region_size:
                return True

        if device.trust_level == DeviceTrustLevel.RESTRICTED:
            logger.warning(f"Restricted DMA from {device_id} to 0x{addr:x}")
            return False

        return True

    def add_allowed_region(self, device_id: str, addr: int, size: int) -> bool:
        """Add an allowed DMA region for a device."""
        if device_id not in self.devices:
            return False
        self.devices[device_id].allowed_regions.append((addr, size))
        return True

    def _get_iommu_group(self, bus_address: str) -> int:
        """Get IOMMU group for a device."""
        # In production: read from /sys/kernel/iommu_groups/
        return hash(bus_address) % 256

    def get_status(self) -> dict:
        """Get DMA guard status."""
        return {
            "devices": len(self.devices),
            "trusted": sum(1 for d in self.devices.values() if d.trust_level == DeviceTrustLevel.TRUSTED),
            "restricted": sum(1 for d in self.devices.values() if d.trust_level == DeviceTrustLevel.RESTRICTED),
            "blocked": sum(1 for d in self.devices.values() if d.trust_level == DeviceTrustLevel.BLOCKED),
        }
