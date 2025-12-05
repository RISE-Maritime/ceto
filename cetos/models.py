"""
Data models for vessel analysis.

This module defines dataclasses for all vessel, voyage, and result types
used throughout cetos. All models include validation and comprehensive
documentation.
"""

from dataclasses import dataclass, field
from typing import List, Literal, Optional

from cetos.enums import VesselType, FuelType, EngineType, EngineAge


@dataclass
class VoyageLeg:
    """A single leg of a voyage with distance, speed, and draft.

    Attributes:
        distance: Distance traveled in nautical miles (must be > 0)
        speed: Speed in knots (must be > 0)
        draft: Vessel draft in meters (must be > 0)

    Example:
        >>> leg = VoyageLeg(distance=10.5, speed=12.0, draft=2.8)
        >>> leg.distance
        10.5
    """

    distance: float
    speed: float
    draft: float

    def __post_init__(self):
        """Validate leg parameters after initialization."""
        if self.distance < 0:
            raise ValueError(
                f"distance must be >= 0, got {self.distance}"
            )
        if self.speed <= 0:
            raise ValueError(
                f"speed must be > 0, got {self.speed}"
            )
        if self.draft <= 0:
            raise ValueError(
                f"draft must be > 0, got {self.draft}"
            )


@dataclass
class VesselData:
    """Complete vessel characteristics for fuel and energy consumption analysis.

    All dimensions are validated on creation to match IMO Fourth GHG Study
    acceptable ranges. This ensures all downstream calculations receive
    valid inputs.

    Attributes:
        length: Vessel length in meters (5.0-450.0)
        beam: Vessel beam (width) in meters (1.5-70.0)
        design_speed: Design speed in knots (1.0-50.0)
        design_draft: Design draft in meters (0.1-25.0)
        double_ended: Whether vessel can operate in both directions
        number_of_propulsion_engines: Number of propulsion engines (1-4)
        propulsion_engine_power: Power per engine in kW (5-60,000)
        propulsion_engine_type: Type of propulsion engine
        propulsion_engine_age: Age category affecting efficiency
        propulsion_engine_fuel_type: Type of fuel used
        type: Vessel type classification
        size: Gross tonnage, deadweight, or cubic meters. Required for
            most vessel types, optional for yacht, service-tug,
            miscellaneous-fishing, offshore, service-other, miscellaneous-other

    Example:
        >>> from cetos.models import VesselData
        >>> from cetos.enums import VesselType, FuelType, EngineType, EngineAge
        >>>
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
    """

    length: float
    beam: float
    design_speed: float
    design_draft: float
    double_ended: bool
    number_of_propulsion_engines: Literal[1, 2, 3, 4]
    propulsion_engine_power: float
    propulsion_engine_type: EngineType
    propulsion_engine_age: EngineAge
    propulsion_engine_fuel_type: FuelType
    type: VesselType
    size: Optional[float] = None

    def __post_init__(self):
        """Validate all vessel parameters after initialization."""
        self._validate_range("length", self.length, 5.0, 450.0)
        self._validate_range("beam", self.beam, 1.5, 70.0)
        self._validate_range("design_speed", self.design_speed, 1.0, 50.0)
        self._validate_range("design_draft", self.design_draft, 0.1, 25.0)
        self._validate_range(
            "propulsion_engine_power",
            self.propulsion_engine_power,
            5,
            60_000
        )

        if self.size is not None:
            self._validate_range("size", self.size, 0, 500_000)

    @staticmethod
    def _validate_range(
        name: str,
        value: float,
        min_val: float,
        max_val: float
    ) -> None:
        """Validate that a numeric value is within acceptable range.

        Args:
            name: Parameter name for error messages
            value: Value to validate
            min_val: Minimum acceptable value (inclusive)
            max_val: Maximum acceptable value (inclusive)

        Raises:
            ValueError: If value is outside the acceptable range
        """
        if not min_val <= value <= max_val:
            raise ValueError(
                f"{name} must be between {min_val} and {max_val}, got {value}"
            )


@dataclass
class VoyageProfile:
    """Voyage profile describing vessel operations over a time period.

    A voyage profile captures all operational states: time at berth, time
    anchored, maneuvering legs (near port), and at-sea legs (open water).
    Each leg specifies distance, speed, and draft.

    Attributes:
        time_anchored: Time spent anchored in hours (0-8760)
        time_at_berth: Time spent at berth in hours (0-8760)
        legs_manoeuvring: List of maneuvering legs near port
        legs_at_sea: List of at-sea legs in open water

    Example:
        >>> from cetos.models import VoyageProfile, VoyageLeg
        >>>
        >>> voyage = VoyageProfile(
        ...     time_anchored=10.0,
        ...     time_at_berth=10.0,
        ...     legs_manoeuvring=[VoyageLeg(10, 10, 6)],
        ...     legs_at_sea=[
        ...         VoyageLeg(30, 10, 6),
        ...         VoyageLeg(30, 10, 6),
        ...     ],
        ... )
    """

    time_anchored: float
    time_at_berth: float
    legs_manoeuvring: List[VoyageLeg] = field(default_factory=list)
    legs_at_sea: List[VoyageLeg] = field(default_factory=list)

    def __post_init__(self):
        """Validate time values after initialization."""
        max_hours = 24 * 365  # One year
        if not 0 <= self.time_anchored <= max_hours:
            raise ValueError(
                f"time_anchored must be 0-{max_hours} hours, "
                f"got {self.time_anchored}"
            )
        if not 0 <= self.time_at_berth <= max_hours:
            raise ValueError(
                f"time_at_berth must be 0-{max_hours} hours, "
                f"got {self.time_at_berth}"
            )


@dataclass(frozen=True)
class FuelConsumptionBreakdown:
    """Fuel consumption breakdown for a single operation mode.

    This structure captures consumption from different systems
    (propulsion, auxiliary, steam boilers) for one operational mode
    such as at-berth, anchored, maneuvering, or at-sea.

    Attributes:
        subtotal_kg: Total fuel consumed in this mode (kg)
        auxiliary_engines_kg: Fuel consumed by auxiliary engines (kg)
        propulsion_engines_kg: Fuel consumed by propulsion engines (kg),
            0.0 for at-berth and anchored modes
        average_fuel_consumption_l_per_nm: Average consumption rate (L/nm),
            0.0 for stationary modes (at-berth, anchored)
        steam_boilers_kg: Fuel consumed by steam boilers (kg), if included
    """

    subtotal_kg: float
    auxiliary_engines_kg: float
    propulsion_engines_kg: float = 0.0
    average_fuel_consumption_l_per_nm: float = 0.0
    steam_boilers_kg: Optional[float] = None


@dataclass(frozen=True)
class FuelConsumptionResult:
    """Complete fuel consumption estimation result across all operation modes.

    Attributes:
        total_kg: Total fuel consumed across all operations (kg)
        at_berth: Consumption while berthed (auxiliary + boilers only)
        anchored: Consumption while anchored (auxiliary + boilers only)
        manoeuvring: Consumption during maneuvering (all systems)
        at_sea: Consumption during at-sea operations (all systems)

    Example:
        >>> result = estimate_fuel_consumption(vessel, voyage)
        >>> print(f"Total: {result.total_kg:.2f} kg")
        >>> print(f"At sea: {result.at_sea.subtotal_kg:.2f} kg")
        >>> print(f"Efficiency: {result.at_sea.average_fuel_consumption_l_per_nm:.2f} L/nm")
    """

    total_kg: float
    at_berth: FuelConsumptionBreakdown
    anchored: FuelConsumptionBreakdown
    manoeuvring: FuelConsumptionBreakdown
    at_sea: FuelConsumptionBreakdown


@dataclass(frozen=True)
class EnergyConsumptionBreakdown:
    """Energy consumption breakdown for a single operation mode.

    Similar to FuelConsumptionBreakdown but for energy (kWh) rather
    than fuel mass.

    Attributes:
        subtotal_kwh: Total energy consumed in this mode (kWh)
        auxiliary_engines_kwh: Energy from auxiliary engines (kWh)
        propulsion_engines_kwh: Energy from propulsion engines (kWh)
        steam_boilers_kwh: Energy from steam boilers (kWh), if included
    """

    subtotal_kwh: float
    auxiliary_engines_kwh: float
    propulsion_engines_kwh: float
    steam_boilers_kwh: Optional[float] = None


@dataclass(frozen=True)
class EnergyConsumptionResult:
    """Complete energy consumption estimation result.

    Attributes:
        total_kwh: Total energy consumed across all operations (kWh)
        at_berth: Energy consumption while berthed
        anchored: Energy consumption while anchored
        manoeuvring: Energy consumption during maneuvering
        at_sea: Energy consumption during at-sea operations
    """

    total_kwh: float
    at_berth: EnergyConsumptionBreakdown
    anchored: EnergyConsumptionBreakdown
    manoeuvring: EnergyConsumptionBreakdown
    at_sea: EnergyConsumptionBreakdown


@dataclass(frozen=True)
class ReferenceValues:
    """Reference values for energy system component specifications.

    These values define the characteristics of reference components
    (fuel cells, batteries, hydrogen tanks) used for scaling energy
    system estimates.

    Default values correspond to:
    - Fuel cell: PowerCellution 100 (https://powercellgroup.com/)
    - Battery: Corvus Orca Energy (https://corvusenergy.com/)
    - H2 tank: Hexagon Purus Type 4

    Attributes:
        reference_fuel_cell_volume_m3: Fuel cell volume (m³)
        reference_fuel_cell_weight_kg: Fuel cell weight (kg)
        reference_fuel_cell_power_kw: Fuel cell power (kW)
        reference_fuel_cell_efficiency_pct: Fuel cell efficiency (%)
        reference_battery_pack_volume_m3: Battery pack volume (m³)
        reference_battery_pack_weight_kg: Battery pack weight (kg)
        reference_battery_pack_capacity_kwh: Battery capacity (kWh)
        reference_battery_pack_depth_of_discharge_pct: Max discharge depth (%)
        reference_hydrogen_gas_tank_volume_m3: H2 tank volume (m³)
        reference_hydrogen_gas_tank_capacity_kg: H2 storage capacity (kg)
        reference_hydrogen_gas_tank_weight_kg: H2 tank weight (kg)
    """

    reference_fuel_cell_volume_m3: float = 0.730 * 0.9 * 2.2
    reference_fuel_cell_weight_kg: float = 1070
    reference_fuel_cell_power_kw: float = 185
    reference_fuel_cell_efficiency_pct: float = 45
    reference_battery_pack_volume_m3: float = 2.241 * 0.865 * 0.738
    reference_battery_pack_weight_kg: float = 1628
    reference_battery_pack_capacity_kwh: float = 124
    reference_battery_pack_depth_of_discharge_pct: float = 80
    reference_hydrogen_gas_tank_volume_m3: float = 1.033
    reference_hydrogen_gas_tank_capacity_kg: float = 18.4
    reference_hydrogen_gas_tank_weight_kg: float = 272


@dataclass(frozen=True)
class EnergySystemComponent:
    """Details of a single energy system component.

    Attributes:
        weight_kg: Component weight (kg)
        volume_m3: Component volume (m³)
        power_kw: Component power rating (kW), if applicable
        capacity_kwh: Energy capacity (kWh), if applicable
        capacity_kg: Mass capacity (kg), if applicable (e.g., H2 storage)
    """

    weight_kg: float
    volume_m3: float
    power_kw: Optional[float] = None
    capacity_kwh: Optional[float] = None
    capacity_kg: Optional[float] = None


@dataclass(frozen=True)
class EnergySystemResult:
    """Complete energy system estimation result.

    Attributes:
        total_weight_kg: Total system weight (kg)
        total_volume_m3: Total system volume (m³)
        details: Dictionary with component-level details
    """

    total_weight_kg: float
    total_volume_m3: float
    details: dict  # Component breakdown
