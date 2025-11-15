"""
Pinning tests for ceto.imo module.

These tests capture the complete output behavior of fuel and energy consumption
calculations for various vessel types and voyage profiles. They serve as a safety
net during refactoring by detecting any unintended changes in calculation results.
"""

import pytest
from ceto.imo import estimate_fuel_consumption, estimate_energy_consumption

from tests.fixtures import (
    FERRY_PAX_VESSEL,
    FERRY_PAX_DAILY_VOYAGE,
    OIL_TANKER_VESSEL,
    OIL_TANKER_LONG_VOYAGE,
    GENERAL_CARGO_VESSEL,
    GENERAL_CARGO_MEDIUM_VOYAGE,
    OFFSHORE_VESSEL,
    OFFSHORE_SHORT_VOYAGE,
    ROPAX_VESSEL,
    ROPAX_FREQUENT_VOYAGE,
    MINIMAL_VOYAGE,
    COMPLEX_VOYAGE,
)


@pytest.mark.parametrize(
    "vessel_data,voyage_profile,scenario_name",
    [
        (FERRY_PAX_VESSEL, FERRY_PAX_DAILY_VOYAGE, "ferry_pax_daily"),
        (OIL_TANKER_VESSEL, OIL_TANKER_LONG_VOYAGE, "oil_tanker_long"),
        (GENERAL_CARGO_VESSEL, GENERAL_CARGO_MEDIUM_VOYAGE, "general_cargo_medium"),
        (OFFSHORE_VESSEL, OFFSHORE_SHORT_VOYAGE, "offshore_short"),
        (ROPAX_VESSEL, ROPAX_FREQUENT_VOYAGE, "ropax_frequent"),
    ],
)
def test_estimate_fuel_consumption_pinned(
    vessel_data, voyage_profile, scenario_name, pinned
):
    """
    Pin complete fuel consumption outputs for different vessel types and voyage profiles.

    This captures the full nested dictionary output including:
    - total_kg
    - at_berth (auxiliary_engines_kg, steam_boilers_kg)
    - anchored (auxiliary_engines_kg, steam_boilers_kg)
    - manoeuvring (propulsion_engines_kg, auxiliary_engines_kg, steam_boilers_kg)
    - at_sea (propulsion_engines_kg, auxiliary_engines_kg, steam_boilers_kg)
    """
    result = estimate_fuel_consumption(vessel_data, voyage_profile)
    assert result == pinned


@pytest.mark.parametrize(
    "vessel_data,voyage_profile,scenario_name",
    [
        (FERRY_PAX_VESSEL, FERRY_PAX_DAILY_VOYAGE, "ferry_pax_daily"),
        (OIL_TANKER_VESSEL, OIL_TANKER_LONG_VOYAGE, "oil_tanker_long"),
        (GENERAL_CARGO_VESSEL, GENERAL_CARGO_MEDIUM_VOYAGE, "general_cargo_medium"),
        (OFFSHORE_VESSEL, OFFSHORE_SHORT_VOYAGE, "offshore_short"),
        (ROPAX_VESSEL, ROPAX_FREQUENT_VOYAGE, "ropax_frequent"),
    ],
)
def test_estimate_energy_consumption_pinned(
    vessel_data, voyage_profile, scenario_name, pinned
):
    """
    Pin complete energy consumption outputs for different vessel types and voyage profiles.

    This captures energy consumption in kWh including maximum required power.
    """
    result = estimate_energy_consumption(
        vessel_data, voyage_profile, include_steam_boilers=False, limit_7_percent=False
    )
    assert result == pinned


def test_estimate_fuel_consumption_minimal_voyage_pinned(pinned):
    """Pin fuel consumption for minimal voyage (edge case)."""
    result = estimate_fuel_consumption(FERRY_PAX_VESSEL, MINIMAL_VOYAGE)
    assert result == pinned


def test_estimate_fuel_consumption_complex_voyage_pinned(pinned):
    """Pin fuel consumption for complex multi-leg voyage."""
    result = estimate_fuel_consumption(GENERAL_CARGO_VESSEL, COMPLEX_VOYAGE)
    assert result == pinned


def test_estimate_energy_consumption_with_steam_boilers_pinned(pinned):
    """Pin energy consumption including steam boilers."""
    result = estimate_energy_consumption(
        OIL_TANKER_VESSEL,
        OIL_TANKER_LONG_VOYAGE,
        include_steam_boilers=True,
        limit_7_percent=False,
    )
    assert result == pinned


def test_estimate_energy_consumption_with_7_percent_limit_pinned(pinned):
    """Pin energy consumption with 7% power limit applied."""
    result = estimate_energy_consumption(
        GENERAL_CARGO_VESSEL,
        GENERAL_CARGO_MEDIUM_VOYAGE,
        include_steam_boilers=False,
        limit_7_percent=True,
    )
    assert result == pinned


def test_estimate_fuel_consumption_offshore_vessel_pinned(pinned):
    """Pin fuel consumption for offshore vessel (size=None handling)."""
    result = estimate_fuel_consumption(OFFSHORE_VESSEL, OFFSHORE_SHORT_VOYAGE)
    assert result == pinned


def test_estimate_fuel_consumption_double_ended_ferry_pinned(pinned):
    """Pin fuel consumption for double-ended RoPax ferry."""
    result = estimate_fuel_consumption(ROPAX_VESSEL, ROPAX_FREQUENT_VOYAGE)
    assert result == pinned
