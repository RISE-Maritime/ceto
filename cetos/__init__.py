"""cetos - Vessel performance analysis tools.

This package provides tools for analyzing vessel performance, estimating
fuel consumption, and evaluating energy systems for maritime vessels based
on IMO Fourth GHG Study 2020 methodologies.

Example:
    >>> from cetos import (
    ...     VesselData, VoyageProfile, VoyageLeg,
    ...     VesselType, FuelType, EngineType, EngineAge,
    ...     estimate_fuel_consumption
    ... )
    >>>
    >>> # Define a ferry vessel
    >>> ferry = VesselData(
    ...     length=39.8,
    ...     beam=10.46,
    ...     design_speed=13.5,
    ...     design_draft=2.84,
    ...     double_ended=False,
    ...     number_of_propulsion_engines=4,
    ...     propulsion_engine_power=330,
    ...     propulsion_engine_type=EngineType.MSD,
    ...     propulsion_engine_age=EngineAge.AFTER_2000,
    ...     propulsion_engine_fuel_type=FuelType.MDO,
    ...     type=VesselType.FERRY_PAX,
    ...     size=686,
    ... )
    >>>
    >>> # Define a voyage
    >>> voyage = VoyageProfile(
    ...     time_anchored=10.0,
    ...     time_at_berth=10.0,
    ...     legs_manoeuvring=[VoyageLeg(10, 10, 6)],
    ...     legs_at_sea=[VoyageLeg(30, 10, 6), VoyageLeg(30, 10, 6)],
    ... )
    >>>
    >>> # Estimate fuel consumption
    >>> result = estimate_fuel_consumption(ferry, voyage)
    >>> print(f"Total: {result.total_kg:.2f} kg")
"""

# Core data models
from cetos.models import (
    VesselData,
    VoyageProfile,
    VoyageLeg,
    FuelConsumptionResult,
    FuelConsumptionBreakdown,
    EnergyConsumptionResult,
    EnergyConsumptionBreakdown,
    ReferenceValues,
    EnergySystemResult,
)

# Enumerations
from cetos.enums import (
    VesselType,
    FuelType,
    EngineType,
    EngineAge,
)

# Main fuel consumption functions
from cetos.imo import (
    estimate_fuel_consumption,
    calculate_fuel_volume,
    calculate_fuel_mass,
)

# Version
try:
    from cetos._version import __version__
except ImportError:
    __version__ = "unknown"

__all__ = [
    # Data models
    "VesselData",
    "VoyageProfile",
    "VoyageLeg",
    "FuelConsumptionResult",
    "FuelConsumptionBreakdown",
    "EnergyConsumptionResult",
    "EnergyConsumptionBreakdown",
    "ReferenceValues",
    "EnergySystemResult",
    # Enumerations
    "VesselType",
    "FuelType",
    "EngineType",
    "EngineAge",
    # Main functions
    "estimate_fuel_consumption",
    "calculate_fuel_volume",
    "calculate_fuel_mass",
    # Version
    "__version__",
]
