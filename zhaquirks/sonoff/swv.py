"""Sonoff SWV - Zigbee smart water valve."""

from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import QuirkBuilder
import zigpy.types as t
from zigpy.zcl import foundation
from zigpy.zcl.foundation import BaseAttributeDefs, ZCLAttributeDef
from zigpy.zcl.clusters.general import OnOff
from zhaquirks import NoReplyMixin
from homeassistant.components.number import NumberDeviceClass
import typing
import asyncio


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

        on_time = ZCLAttributeDef(
            id=0x5011,
            type=t.uint16_t,
        )

    @property
    def _is_manuf_specific(self):
        return False


class SwvOnOff(NoReplyMixin, CustomCluster, OnOff):
    """SWV On Off Cluster."""

    cluster_id = OnOff.cluster_id
    cmd_values = OnOff.commands_by_name.values()

    """
    Send a command to the device.

    Args:
        command_id (foundation.GeneralCommand | int | t.uint8_t): The ID of the command to send.
        *args: Additional arguments for the command.
        manufacturer (int | t.uint16_t | None, optional): The manufacturer ID. Defaults to None.
        expect_reply (bool, optional): Whether to expect a reply from the device. Defaults to True.
        tsn (int | t.uint8_t | None, optional): The transaction sequence number. Defaults to None.
        **kwargs (typing.Any): Additional keyword arguments for the command.

    Returns:
        typing.Coroutine: A coroutine that sends the command and waits for the response.
    """

    async def command(
        self,
        command_id: foundation.GeneralCommand | int | t.uint8_t,
        *args,
        manufacturer: int | t.uint16_t | None = None,
        expect_reply: bool = True,
        tsn: int | t.uint8_t | None = None,
        **kwargs: typing.Any,
    ) -> typing.Coroutine:
        command = self.server_commands[command_id]

        if manufacturer is None and (
            self._is_manuf_specific or command.is_manufacturer_specific
        ):
            manufacturer = self._manufacturer_id
        if command_id == 0x01:
            base_cluster = self.endpoint.in_clusters[EwelinkCluster.cluster_id]
            on_time_value = base_cluster.get(EwelinkCluster.AttributeDefs.on_time.id)
            if on_time_value is not None and on_time_value != 0:
                command = self.server_commands[0x42]  # on_with_timed_off
                kwargs["on_off_control"] = 0x00
                kwargs["on_time"] = on_time_value
                kwargs["off_wait_time"] = 1
                self.create_catching_task(self._turn_off_later(on_time_value))

        return await self.request(
            False,
            command.id,
            command.schema,
            *args,
            manufacturer=manufacturer,
            expect_reply=expect_reply,
            tsn=tsn,
            **kwargs,
        )

    async def _turn_off_later(self, delay):
        """We are not receiving the auto off event, so we force an update."""
        await asyncio.sleep(delay + 1)
        # self._update_attribute(self.AttributeDefs.on_off.id, False)
        await self.endpoint.on_off.read_attributes(["on_off"])


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
    .replaces(SwvOnOff)
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
    .number(
            EwelinkCluster.AttributeDefs.on_time.name,
            EwelinkCluster.cluster_id,
            translation_key="auto_close_time",
            fallback_name="Auto Close Time",
            unique_id_suffix="auto_close_time",
            min_value=0,
            max_value=3600,
            device_class=NumberDeviceClass.DURATION,
        )
    .add_to_registry()
)  # fmt: skip
