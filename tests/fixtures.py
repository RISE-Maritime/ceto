"""
Test fixtures for pinning tests.

This module contains realistic vessel and voyage profiles for different vessel types
to be used in comprehensive pinning tests.
"""

from cetos import (
    VesselData,
    VoyageProfile,
    VoyageLeg,
    VesselType,
    FuelType,
    EngineType,
    EngineAge,
)

# Ferry Passenger Vessel
FERRY_PAX_VESSEL = VesselData(
    length=39.8,
    beam=10.46,
    design_speed=13.5,
    design_draft=2.84,
    double_ended=False,
    number_of_propulsion_engines=4,
    propulsion_engine_power=330,
    propulsion_engine_type=EngineType.MSD,
    propulsion_engine_age=EngineAge.AFTER_2000,
    propulsion_engine_fuel_type=FuelType.MDO,
    type=VesselType.FERRY_PAX,
    size=686,
)

FERRY_PAX_DAILY_VOYAGE = VoyageProfile(
    time_anchored=0.5,
    time_at_berth=2.0,
    legs_manoeuvring=[
        VoyageLeg(0.5, 5, 2.8),
        VoyageLeg(0.5, 5, 2.8),
    ],
    legs_at_sea=[
        VoyageLeg(10, 12, 2.8),
        VoyageLeg(10, 12, 2.8),
    ],
)

# Oil Tanker
OIL_TANKER_VESSEL = VesselData(
    length=200,
    beam=30,
    design_speed=15,
    design_draft=12,
    double_ended=False,
    number_of_propulsion_engines=1,
    propulsion_engine_power=8_000,
    propulsion_engine_type=EngineType.SSD,
    propulsion_engine_age=EngineAge.AFTER_2000,
    propulsion_engine_fuel_type=FuelType.HFO,
    type=VesselType.OIL_TANKER,
    size=50_000,
)

OIL_TANKER_LONG_VOYAGE = VoyageProfile(
    time_anchored=10.0,
    time_at_berth=24.0,
    legs_manoeuvring=[
        VoyageLeg(2, 8, 12),
        VoyageLeg(2, 8, 10),
    ],
    legs_at_sea=[
        VoyageLeg(500, 14, 12),
        VoyageLeg(500, 14, 10),
    ],
)

# General Cargo Vessel
GENERAL_CARGO_VESSEL = VesselData(
    length=150,
    beam=23,
    design_speed=18,
    design_draft=8.5,
    double_ended=False,
    number_of_propulsion_engines=1,
    propulsion_engine_power=5_000,
    propulsion_engine_type=EngineType.MSD,
    propulsion_engine_age=EngineAge.AFTER_2000,
    propulsion_engine_fuel_type=FuelType.MDO,
    type=VesselType.GENERAL_CARGO,
    size=15_000,
)

GENERAL_CARGO_MEDIUM_VOYAGE = VoyageProfile(
    time_anchored=5.0,
    time_at_berth=12.0,
    legs_manoeuvring=[
        VoyageLeg(1.5, 6, 8.5),
        VoyageLeg(1.5, 6, 7.0),
    ],
    legs_at_sea=[
        VoyageLeg(200, 16, 8.5),
        VoyageLeg(200, 16, 7.0),
    ],
)

# Offshore Supply Vessel
OFFSHORE_VESSEL = VesselData(
    length=100,
    beam=20,
    design_speed=10,
    design_draft=7,
    double_ended=False,
    number_of_propulsion_engines=1,
    propulsion_engine_power=1_000,
    propulsion_engine_type=EngineType.MSD,
    propulsion_engine_age=EngineAge.AFTER_2000,
    propulsion_engine_fuel_type=FuelType.MDO,
    type=VesselType.OFFSHORE,
    size=None,
)

OFFSHORE_SHORT_VOYAGE = VoyageProfile(
    time_anchored=10.0,
    time_at_berth=10.0,
    legs_manoeuvring=[
        VoyageLeg(10, 10, 7),
    ],
    legs_at_sea=[
        VoyageLeg(10, 10, 7),
        VoyageLeg(20, 10, 6),
    ],
)

# RoRo Ferry
ROPAX_VESSEL = VesselData(
    length=180,
    beam=28,
    design_speed=22,
    design_draft=6.5,
    double_ended=True,
    number_of_propulsion_engines=4,
    propulsion_engine_power=2_500,
    propulsion_engine_type=EngineType.HSD,
    propulsion_engine_age=EngineAge.AFTER_2000,
    propulsion_engine_fuel_type=FuelType.MDO,
    type=VesselType.FERRY_ROPAX,
    size=25_000,
)

ROPAX_FREQUENT_VOYAGE = VoyageProfile(
    time_anchored=0.0,
    time_at_berth=4.0,
    legs_manoeuvring=[
        VoyageLeg(1, 8, 6.5),
        VoyageLeg(1, 8, 6.5),
        VoyageLeg(1, 8, 6.5),
        VoyageLeg(1, 8, 6.5),
    ],
    legs_at_sea=[
        VoyageLeg(50, 20, 6.5),
        VoyageLeg(50, 20, 6.5),
    ],
)

# Minimal voyage profile (edge case)
MINIMAL_VOYAGE = VoyageProfile(
    time_anchored=0.0,
    time_at_berth=1.0,
    legs_manoeuvring=[],
    legs_at_sea=[],
)

# Maximal complex voyage (stress test)
COMPLEX_VOYAGE = VoyageProfile(
    time_anchored=20.0,
    time_at_berth=30.0,
    legs_manoeuvring=[
        VoyageLeg(1, 5, 7),
        VoyageLeg(2, 6, 7),
        VoyageLeg(1, 4, 6.5),
    ],
    legs_at_sea=[
        VoyageLeg(100, 15, 8),
        VoyageLeg(150, 14, 7.5),
        VoyageLeg(200, 16, 7),
        VoyageLeg(100, 13, 6.5),
    ],
)

# AIS data samples for different vessel types
AIS_FERRY_PAX = {
    "ship_type": 60,  # Passenger ship
    "to_bow": 20,
    "to_stern": 20,
    "to_port": 5,
    "to_starboard": 5,
    "speed": 12,
    "draught": 2.8,
    "lat": 56.0,
    "lon": 12.0,
}

AIS_OIL_TANKER = {
    "ship_type": 80,  # Tanker
    "to_bow": 150,
    "to_stern": 50,
    "to_port": 15,
    "to_starboard": 15,
    "speed": 14,
    "draught": 12,
    "lat": 57.0,
    "lon": 11.0,
}

AIS_CARGO = {
    "ship_type": 70,  # Cargo
    "to_bow": 100,
    "to_stern": 50,
    "to_port": 11,
    "to_starboard": 12,
    "speed": 16,
    "draught": 8.5,
    "lat": 58.0,
    "lon": 12.5,
}
