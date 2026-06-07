# Phantom-Veil Examples

## Running Examples

```bash
# Set Python path
export PYTHONPATH=/path/to/phantom-veil

# Basic usage
python examples/basic_usage.py

# Threat response simulation
python examples/threat_response.py

# Confidential computing
python examples/confidential_computing.py
```

## Integration with Other Components

- **specter-net**: Sends threat events that trigger quarantine
- **cerebro**: Stores ML models in encrypted memory
- **ironclad**: Verifies build artifact integrity
- **obsidian-core**: Orchestrates policies across all components
