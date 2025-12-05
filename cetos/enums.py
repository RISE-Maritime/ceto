"""
Enumerations for vessel and engine types used in cetos.

This module defines type-safe enums for all categorical values used in vessel
and energy system analysis, providing IDE autocomplete and preventing typos.
"""

from enum import Enum


class VesselType(str, Enum):
    """Supported vessel types according to IMO Fourth GHG Study classification.

    Each vessel type has different characteristics affecting fuel consumption,
    auxiliary power requirements, and operational profiles.
    """

    BULK_CARRIER = "bulk_carrier"
    CHEMICAL_TANKER = "chemical_tanker"
    CONTAINER = "container"
    GENERAL_CARGO = "general_cargo"
    LIQUIFIED_GAS_TANKER = "liquified_gas_tanker"
    OIL_TANKER = "oil_tanker"
    OTHER_LIQUIDS_TANKER = "other_liquids_tanker"
    FERRY_PAX = "ferry-pax"
    CRUISE = "cruise"
    FERRY_ROPAX = "ferry-ropax"
    REFRIGERATED_CARGO = "refrigerated_cargo"
    RORO = "roro"
    VEHICLE = "vehicle"
    YACHT = "yacht"
    MISC_FISHING = "miscellaneous-fishing"
    SERVICE_TUG = "service-tug"
    OFFSHORE = "offshore"
    SERVICE_OTHER = "service-other"
    MISC_OTHER = "miscellaneous-other"


class FuelType(str, Enum):
    """Supported fuel types for marine engines.

    Each fuel type has different energy density, emission characteristics,
    and density values used in calculations.
    """

    HFO = "HFO"  # Heavy Fuel Oil
    MDO = "MDO"  # Marine Diesel Oil
    MeOH = "MeOH"  # Methanol
    LNG = "LNG"  # Liquefied Natural Gas


class EngineType(str, Enum):
    """Supported propulsion engine types.

    Engine types differ in speed, efficiency curves, and specific fuel
    consumption characteristics according to IMO Fourth GHG Study.
    """

    SSD = "SSD"  # Slow Speed Diesel
    MSD = "MSD"  # Medium Speed Diesel
    HSD = "HSD"  # High Speed Diesel
    LNG_OTTO_MS = "LNG-Otto-MS"  # LNG Otto Medium Speed
    LBSI = "LBSI"  # Lean Burn Spark Ignition
    GAS_TURBINE = "gas_turbine"
    STEAM_TURBINE = "steam_turbine"


class EngineAge(str, Enum):
    """Engine age categories for emission and efficiency standards.

    Different age categories have different specific fuel consumption
    characteristics based on technological improvements over time.
    """

    BEFORE_1984 = "before_1984"
    BETWEEN_1984_2000 = "1984-2000"
    AFTER_2000 = "after_2000"
