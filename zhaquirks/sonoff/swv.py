"""Sonoff SWV - Zigbee smart water valve."""

from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import QuirkBuilder
import zigpy.types as t
from zigpy.zcl.foundation import BaseAttributeDefs, ZCLAttributeDef


class ValveState(t.enum8):
    """Water valve state."""

    Normal = 0
    Water_Shortage = 1
    Water_Leakage = 2
    Water_Shortage_And_Leakage = 3


class EwelinkCluster(CustomCluster):
    """Ewelink specific cluster."""

    cluster_id = 0xFC11

    class AttributeDefs(BaseAttributeDefs):
        """Attribute definitions."""

        water_valve_state = ZCLAttributeDef(
            id=0x500C,
            type=ValveState,
        )

    @property
    def _is_manuf_specific(self):
        return False


def is_water_shortage(valve_state: ValveState) -> bool:
    """Check if the valve state indicates water shortage."""
    return valve_state in {
        ValveState.Water_Shortage,
        ValveState.Water_Shortage_And_Leakage,
    }


def is_water_leakage(valve_state: ValveState) -> bool:
    """Check if the valve state indicates water leakage."""
    return valve_state in {
        ValveState.Water_Leakage,
        ValveState.Water_Shortage_And_Leakage,
    }


(
    QuirkBuilder("SONOFF", "SWV")
    .replaces(EwelinkCluster)
    .binary_sensor(
            EwelinkCluster.AttributeDefs.water_valve_state.name,
            EwelinkCluster.cluster_id,
            translation_key="water_shortage",
            fallback_name="Water Shortage",
            unique_id_suffix="water_shortage",
            attribute_converter=is_water_shortage,
        )
    .binary_sensor(
            EwelinkCluster.AttributeDefs.water_valve_state.name,
            EwelinkCluster.cluster_id,
            translation_key="water_leakage",
            fallback_name="Water Leakage",
            unique_id_suffix="water_leakage",
            attribute_converter=is_water_leakage,
        )
    .add_to_registry()
)  # fmt: skip
