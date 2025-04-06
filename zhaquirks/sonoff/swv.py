"""Sonoff SWV - Zigbee smart water valve."""

import asyncio
import typing

from zigpy.quirks import CustomCluster
from zigpy.quirks.v2 import QuirkBuilder, ReportingConfig
from zigpy.quirks.v2.homeassistant.binary_sensor import BinarySensorDeviceClass
import zigpy.types as t
from zigpy.zcl import foundation
from zigpy.zcl.foundation import BaseAttributeDefs, ZCLAttributeDef

from zhaquirks import NoReplyMixin


class ValveState(t.enum8):
    """Water valve state."""

    Normal = 0
    Water_Shortage = 1
    Water_Leakage = 2
    Water_Shortage_And_Leakage = 3


class CustomSonoffCluster(CustomCluster):
    """Custom Sonoff cluster."""

    cluster_id = 0xFC11
    manufacturer_id_override: t.uint16_t = foundation.ZCLHeader.NO_MANUFACTURER_ID

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

    async def command(
        self,
        command_id: foundation.GeneralCommand | int | t.uint8_t,
        *args,
        manufacturer: int | t.uint16_t | None = None,
        expect_reply: bool = True,
        tsn: int | t.uint8_t | None = None,
        **kwargs: typing.Any,
    ) -> typing.Coroutine:
        """Send a command to the device.

        If on_time == 0 it keeps the normal On command (0x01)
        If on_time != 0 it sends a on_with_timed_off (0x42), with the on_time numbers of seconds sets in the attribute

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
        await self.endpoint.on_off.read_attributes(["on_off"])


def is_water_shortage(valve_state: ValveState) -> bool:
    """Check if the valve state indicates water shortage."""
    return bool(valve_state & ValveState.Water_Shortage)


def is_water_leakage(valve_state: ValveState) -> bool:
    """Check if the valve state indicates water leakage."""
    return bool(valve_state & ValveState.Water_Leakage)


(
    QuirkBuilder("SONOFF", "SWV")
    .replaces(CustomSonoffCluster)
    .binary_sensor(
        CustomSonoffCluster.AttributeDefs.water_valve_state.name,
        CustomSonoffCluster.cluster_id,
        device_class=BinarySensorDeviceClass.MOISTURE,
        attribute_converter=lambda x: x & ValveState.Water_Leakage,
        unique_id_suffix="water_leak_status",
        reporting_config=ReportingConfig(
            min_interval=30, max_interval=900, reportable_change=1
        ),
        translation_key="water_leak",
        fallback_name="Water leak",
    )
    .binary_sensor(
        CustomSonoffCluster.AttributeDefs.water_valve_state.name,
        CustomSonoffCluster.cluster_id,
        device_class=BinarySensorDeviceClass.PROBLEM,
        attribute_converter=lambda x: x & ValveState.Water_Shortage,
        unique_id_suffix="water_supply_status",
        translation_key="water_supply",
        fallback_name="Water supply",
    )
    .add_to_registry()
)
