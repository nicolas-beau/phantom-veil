"""Configuration management for Phantom-Veil."""
import os
import yaml
import logging
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger("phantom-veil.config")

DEFAULT_CONFIG = {
    "phantom-veil": {
        "mode": "enforce",
        "algorithm": "AES-256-GCM",
        "key_rotation_interval": 86400,
        "quarantine_on_threat": True,
        "attestation_interval": 300,
        "dma_protection": True,
        "log_level": "info",
    },
    "integrations": {
        "specter_net": {
            "enabled": True,
            "event_endpoint": "localhost:9090",
            "auto_quarantine_threshold": 0.85,
        },
        "cerebro": {
            "enabled": True,
            "encrypted_model_store": True,
        },
        "obsidian_core": {
            "enabled": True,
            "policy_endpoint": "localhost:8443",
        },
    },
    "hardware": {
        "iommu_enabled": True,
        "secure_processor": "auto",
        "memory_encryption": True,
    },
}

class Config:
    """Phantom-Veil configuration manager."""

    def __init__(self, config_path: Optional[str] = None):
        self.config_path = config_path or os.environ.get("PHANTOM_CONFIG", "config/phantom-veil.yaml")
        self.data: Dict[str, Any] = DEFAULT_CONFIG.copy()

    def load(self) -> Dict[str, Any]:
        """Load configuration from YAML file."""
        path = Path(self.config_path)
        if path.exists():
            with open(path) as f:
                user_config = yaml.safe_load(f) or {}
            self._deep_merge(self.data, user_config)
            logger.info(f"Config loaded from {self.config_path}")
        else:
            logger.info("Using default configuration")
        return self.data

    def save(self):
        """Save current configuration to file."""
        path = Path(self.config_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        with open(path, 'w') as f:
            yaml.dump(self.data, f, default_flow_style=False)
        logger.info(f"Config saved to {self.config_path}")

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value by dot-notation key."""
        keys = key.split(".")
        val = self.data
        for k in keys:
            if isinstance(val, dict) and k in val:
                val = val[k]
            else:
                return default
        return val

    def set(self, key: str, value: Any):
        """Set config value by dot-notation key."""
        keys = key.split(".")
        d = self.data
        for k in keys[:-1]:
            d = d.setdefault(k, {})
        d[keys[-1]] = value

    def _deep_merge(self, base: dict, override: dict):
        """Deep merge override into base."""
        for k, v in override.items():
            if k in base and isinstance(base[k], dict) and isinstance(v, dict):
                self._deep_merge(base[k], v)
            else:
                base[k] = v
