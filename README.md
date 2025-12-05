# cetos

[![CI](https://github.com/RISE-Maritime/cetos/workflows/CI%20checks/badge.svg)](https://github.com/RISE-Maritime/cetos/actions)
[![PyPI](https://img.shields.io/pypi/v/cetos)](https://pypi.org/project/cetos/)
[![Python Version](https://img.shields.io/pypi/pyversions/cetos)](https://pypi.org/project/cetos/)
[![License](https://img.shields.io/github/license/RISE-Maritime/cetos)](https://github.com/RISE-Maritime/cetos/blob/main/LICENSE)

Open-source tools for analyzing vessel data.

## Overview

cetos provides tools for analyzing vessel performance, estimating fuel consumption, and evaluating energy systems for maritime vessels. It implements methodologies from the IMO Fourth GHG Study 2020.

### Features

- **Fuel Consumption Estimation**: Calculate vessel fuel consumption based on IMO methodologies
- **Energy System Analysis**: Analyze batteries, hydrogen systems, and hybrid propulsion
- **AIS Data Processing**: Convert AIS data to voyage profiles
- **Multiple Vessel Types**: Support for various vessel types (ferries, container ships, tankers, etc.)

## Installation

Install cetos using pip:

```bash
pip install cetos
```

## Quick Start

```python
from cetos import (
    VesselData,
    VoyageProfile,
    VoyageLeg,
    VesselType,
    FuelType,
    EngineType,
    EngineAge,
    estimate_fuel_consumption,
)

# Define vessel characteristics
ferry = VesselData(
    length=39.8,  # meters
    beam=10.46,  # meters
    design_speed=13.5,  # knots
    design_draft=2.84,  # meters
    double_ended=False,
    number_of_propulsion_engines=4,
    propulsion_engine_power=330,  # kW per engine
    propulsion_engine_type=EngineType.MSD,
    propulsion_engine_age=EngineAge.AFTER_2000,
    propulsion_engine_fuel_type=FuelType.MDO,
    type=VesselType.FERRY_PAX,
    size=686,  # GT
)

# Define voyage profile
voyage = VoyageProfile(
    time_anchored=10.0,  # hours
    time_at_berth=10.0,  # hours
    legs_manoeuvring=[
        VoyageLeg(distance=10, speed=10, draft=6),  # distance (nm), speed (kn), draft (m)
    ],
    legs_at_sea=[
        VoyageLeg(distance=30, speed=10, draft=6),
        VoyageLeg(distance=30, speed=10, draft=6),
    ],
)

# Estimate fuel consumption
result = estimate_fuel_consumption(ferry, voyage)

# Access results with type-safe attributes
print(f"Total fuel consumption: {result.total_kg:.2f} kg")
print(f"At sea consumption: {result.at_sea.subtotal_kg:.2f} kg")
print(f"Average efficiency: {result.at_sea.average_fuel_consumption_l_per_nm:.2f} L/nm")
```

### Why the New API?

The modernized API provides:

- **Type safety**: IDE autocomplete and static type checking catch errors before runtime
- **Self-documenting**: Enum values show all valid options (try typing `VesselType.` in your IDE!)
- **Validation**: Errors caught on object creation, not deep in calculations
- **Reusability**: Define a vessel once, analyze multiple voyages
- **Professional**: Clean, modern Python following current best practices

```python
# Analyze the same vessel on different routes
short_voyage = VoyageProfile(
    time_anchored=0.5,
    time_at_berth=2.0,
    legs_at_sea=[VoyageLeg(10, 12, 2.8)],
)

long_voyage = VoyageProfile(
    time_anchored=1.0,
    time_at_berth=3.0,
    legs_at_sea=[VoyageLeg(50, 13, 2.8)],
)

# Same vessel, different voyages - clean and reusable!
result_short = estimate_fuel_consumption(ferry, short_voyage)
result_long = estimate_fuel_consumption(ferry, long_voyage)

print(f"Short route: {result_short.total_kg:.2f} kg")
print(f"Long route: {result_long.total_kg:.2f} kg")
```

## Modules

### IMO Module (`cetos.imo`)
Functions for estimating vessel fuel consumption based on IMO Fourth GHG Study 2020 methodologies.

### Energy Systems (`cetos.energy_systems`)
Tools for analyzing vessel energy systems including batteries, hydrogen, and internal combustion engines.

### AIS Adapter (`cetos.ais_adapter`)
Process AIS (Automatic Identification System) data and convert it to voyage profiles.

### Analysis (`cetos.analysis`)
Additional analysis tools for vessel performance evaluation.

## Development

### Quick Setup with uv (Recommended)

[uv](https://github.com/astral-sh/uv) is a fast Python package installer and resolver:

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/RISE-Maritime/cetos.git
cd cetos

# Create virtual environment and install dependencies
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv pip install -e ".[dev]"
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/RISE-Maritime/cetos.git
cd cetos

# Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

### Using Dev Containers

This repository includes a dev container configuration for VS Code. Simply open the repository in VS Code and select "Reopen in Container" when prompted.

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
ruff check --fix .
```

## Contributing

Contributions are welcome!

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## References

[1] IMO. Fourth IMO GHG Study 2020. International Maritime Organization.

## Contact

- **Issues**: [GitHub Issues](https://github.com/RISE-Maritime/cetos/issues)
- **Discussions**: [GitHub Discussions](https://github.com/RISE-Maritime/cetos/discussions)

