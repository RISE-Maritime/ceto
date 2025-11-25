"""
Pinning tests for ceto.ais_adapter module.

These tests capture the complete output behavior of vessel and voyage data
estimation from AIS messages. They serve as a safety net during refactoring.
"""

from datetime import datetime

import pytest

from ceto.ais_adapter import guesstimate_vessel_data, guesstimate_voyage_data


def _to_json_serializable(obj):
    """
    Convert tuples to lists for JSON serialization compatibility.
    pytest-pinned stores results as JSON, which converts tuples to lists.
    """
    if isinstance(obj, tuple):
        return [_to_json_serializable(item) for item in obj]
    elif isinstance(obj, list):
        return [_to_json_serializable(item) for item in obj]
    elif isinstance(obj, dict):
        return {key: _to_json_serializable(value) for key, value in obj.items()}
    else:
        return obj


@pytest.mark.parametrize(
    "ship_type,to_bow,to_stern,to_port,to_starboard,speed,draught,lat,lon,scenario_name",
    [
        # Ferry passenger
        (60, 20, 20, 5, 5, 12, 2.8, 56.0, 12.0, "ferry_pax"),
        # Oil tanker
        (80, 150, 50, 15, 15, 14, 12, 57.0, 11.0, "oil_tanker"),
        # General cargo
        (70, 100, 50, 11, 12, 16, 8.5, 58.0, 12.5, "general_cargo"),
        # Container ship
        (70, 200, 50, 20, 22, 18, 10, 55.5, 13.0, "container"),
        # Fishing vessel
        (30, 15, 10, 4, 4, 8, 3.5, 56.5, 11.5, "fishing"),
        # Service tug
        (52, 15, 10, 5, 5, 10, 4, 57.5, 12.0, "tug"),
        # RoPax ferry
        (61, 120, 60, 14, 14, 20, 6.5, 58.5, 13.5, "ropax"),
    ],
)
def test_guesstimate_vessel_data_pinned(
    ship_type,
    to_bow,
    to_stern,
    to_port,
    to_starboard,
    speed,
    draught,
    lat,
    lon,
    scenario_name,
    pinned,
):
    """
    Pin complete vessel data estimations from AIS data.

    Captures the full vessel_data dictionary including:
    - Vessel dimensions (length, beam, design_draft, design_speed)
    - Propulsion system (engine power, type, fuel type, age, number of engines)
    - Vessel classification (type, size, double_ended)

    Tests various vessel types to ensure comprehensive coverage.
    """
    result = guesstimate_vessel_data(
        type_of_ship_and_cargo_type=ship_type,
        dim_a=to_bow,
        dim_b=to_stern,
        dim_c=to_port,
        dim_d=to_starboard,
        speed=speed,
        draft=draught,
        latitude=lat,
        longitude=lon,
    )
    assert result == pinned


@pytest.mark.parametrize(
    "lat1,lon1,lat2,lon2,draft1,draft2,speed1,speed2,hours_elapsed,design_speed,design_draft,scenario_name",
    [
        # Short coastal trip
        (56.0, 12.0, 56.1, 12.1, 2.8, 2.8, 12, 12, 2, 13.5, 2.84, "short_coastal"),
        # Medium voyage with draft change
        (57.0, 11.0, 57.5, 12.0, 12, 10, 14, 14, 10, 15, 12, "medium_draft_change"),
        # Long voyage
        (58.0, 12.0, 60.0, 15.0, 8.5, 7.0, 16, 16, 50, 18, 8.5, "long_voyage"),
        # Maneuvering scenario (slow speeds)
        (56.5, 11.5, 56.52, 11.55, 3.5, 3.5, 5, 6, 0.5, 10, 3.5, "maneuvering"),
        # At berth to at sea
        (57.5, 12.0, 58.0, 13.0, 6.5, 6.5, 0, 20, 5, 22, 6.5, "berth_to_sea"),
        # Anchored to maneuvering to at sea
        (55.0, 10.0, 55.5, 11.0, 7, 7, 0, 15, 8, 16, 7, "complex_ops"),
    ],
)
def test_guesstimate_voyage_data_pinned(
    lat1,
    lon1,
    lat2,
    lon2,
    draft1,
    draft2,
    speed1,
    speed2,
    hours_elapsed,
    design_speed,
    design_draft,
    scenario_name,
    pinned,
):
    """
    Pin complete voyage data estimations from AIS waypoints.

    Captures the full voyage_profile dictionary including:
    - time_anchored
    - time_at_berth
    - legs_manoeuvring (list of tuples with distance, speed, draft)
    - legs_at_sea (list of tuples with distance, speed, draft)

    Tests various voyage scenarios including:
    - Short coastal trips
    - Long voyages
    - Draft changes (cargo loading/unloading)
    - Maneuvering operations
    - Transitions between operational states
    """
    time1 = datetime.fromtimestamp(0)
    time2 = datetime.fromtimestamp(hours_elapsed * 3600)

    result = guesstimate_voyage_data(
        lat1,
        lon1,
        lat2,
        lon2,
        draft1,
        draft2,
        speed1,
        speed2,
        time1,
        time2,
        design_speed,
        design_draft,
    )
    # Convert tuples in legs_manoeuvring and legs_at_sea to lists for JSON compatibility
    result = _to_json_serializable(result)
    assert result == pinned


def test_guesstimate_vessel_data_minimum_dimensions_pinned(pinned):
    """Pin vessel data estimation for minimum viable dimensions."""
    result = guesstimate_vessel_data(
        type_of_ship_and_cargo_type=90,  # Other type
        dim_a=10,
        dim_b=5,
        dim_c=2,
        dim_d=2,
        speed=5,
        draft=2,
        latitude=56.0,
        longitude=12.0,
    )
    assert result == pinned


def test_guesstimate_vessel_data_large_dimensions_pinned(pinned):
    """Pin vessel data estimation for large vessel dimensions."""
    result = guesstimate_vessel_data(
        type_of_ship_and_cargo_type=80,  # Tanker
        dim_a=250,
        dim_b=50,
        dim_c=25,
        dim_d=25,
        speed=15,
        draft=15,
        latitude=57.0,
        longitude=11.0,
    )
    assert result == pinned


def test_guesstimate_voyage_data_stationary_vessel_pinned(pinned):
    """Pin voyage data for stationary vessel (no movement)."""
    time1 = datetime.fromtimestamp(0)
    time2 = datetime.fromtimestamp(10 * 3600)  # 10 hours

    result = guesstimate_voyage_data(
        latitude_1=56.0,
        longitude_1=12.0,
        latitude_2=56.0,
        longitude_2=12.0,
        draft_1=7,
        draft_2=7,
        speed_1=0,
        speed_2=0,
        time_1=time1,
        time_2=time2,
        design_speed=15,
        design_draft=7,
    )
    result = _to_json_serializable(result)
    assert result == pinned


def test_guesstimate_voyage_data_different_positions_zero_speed_pinned(pinned):
    """Pin voyage data for vessel at different positions but zero speed (drifting/current)."""
    time1 = datetime.fromtimestamp(0)
    time2 = datetime.fromtimestamp(5 * 3600)  # 5 hours

    result = guesstimate_voyage_data(
        latitude_1=56.0,
        longitude_1=12.0,
        latitude_2=56.05,
        longitude_2=12.05,
        draft_1=8,
        draft_2=8,
        speed_1=0,
        speed_2=0,
        time_1=time1,
        time_2=time2,
        design_speed=16,
        design_draft=8,
    )
    result = _to_json_serializable(result)
    assert result == pinned
