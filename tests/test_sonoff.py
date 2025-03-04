from unittest.mock import ANY, AsyncMock, MagicMock

import pytest
from zigpy.zcl.foundation import Status

from zhaquirks.sonoff.swv import (
    EwelinkCluster,
    SwvOnOff,
    ValveState,
    is_water_leakage,
    is_water_shortage,
)


@pytest.mark.parametrize(
    "valve_state, expected",
    [
        (ValveState.Normal, False),
        (ValveState.Water_Shortage, True),
        (ValveState.Water_Leakage, False),
        (ValveState.Water_Shortage_And_Leakage, True),
    ],
)
def test_is_water_shortage(valve_state, expected):
    """Test water shortage detection."""
    assert is_water_shortage(valve_state) == expected


@pytest.mark.parametrize(
    "valve_state, expected",
    [
        (ValveState.Normal, False),
        (ValveState.Water_Shortage, False),
        (ValveState.Water_Leakage, True),
        (ValveState.Water_Shortage_And_Leakage, True),
    ],
)
def test_is_water_leakage(valve_state, expected):
    """Test water leakage detection."""
    assert is_water_leakage(valve_state) == expected


@pytest.mark.asyncio
async def test_ewelink_cluster_attributes():
    """Test that EwelinkCluster attributes are correctly set."""
    cluster = EwelinkCluster(None, 1)

    assert hasattr(cluster.AttributeDefs, "water_valve_state")
    assert hasattr(cluster.AttributeDefs, "on_time")

    assert cluster.AttributeDefs.water_valve_state.id == 0x500C
    assert cluster.AttributeDefs.on_time.id == 0x5011


@pytest.mark.asyncio
async def test_swv_on_off_command():
    """Test SwvOnOff command method with different on_time values."""
    endpoint_mock = MagicMock()
    cluster = SwvOnOff(endpoint_mock, 1)
    cluster.server_commands = {0x01: MagicMock(id=0x01), 0x42: MagicMock(id=0x42)}
    cluster.request = AsyncMock(return_value=Status.SUCCESS)

    # Mock EwelinkCluster and its on_time attribute
    ewelink_cluster = MagicMock()
    ewelink_cluster.get = MagicMock(return_value=10)
    endpoint_mock.in_clusters = {EwelinkCluster.cluster_id: ewelink_cluster}

    # Command 0x01 with non-zero on_time should use 0x42 (on_with_timed_off)
    result = await cluster.command(0x01)
    assert result == Status.SUCCESS
    cluster.request.assert_called_with(
        False,
        0x42,  # on_with_timed_off
        cluster.server_commands[0x42].schema,
        manufacturer=ANY,
        expect_reply=True,
        tsn=None,
        on_off_control=0x00,
        on_time=10,
        off_wait_time=1,
    )

    # Command 0x01 with on_time = 0 should remain 0x01 (normal On command)
    ewelink_cluster.get.return_value = 0
    result = await cluster.command(0x01)
    assert result == Status.SUCCESS
    cluster.request.assert_called_with(
        False,
        0x01,  # normal On command
        cluster.server_commands[0x01].schema,
        manufacturer=ANY,
        expect_reply=True,
        tsn=None,
    )


@pytest.mark.asyncio
async def test_turn_off_later():
    """Test that _turn_off_later waits for the correct delay before updating the attribute."""
    endpoint_mock = MagicMock()
    cluster = SwvOnOff(endpoint_mock, 1)
    cluster.endpoint.on_off = MagicMock()
    cluster.endpoint.on_off.read_attributes = AsyncMock()

    delay = 5
    await cluster._turn_off_later(delay)

    # Ensure sleep was called for the expected duration
    cluster.endpoint.on_off.read_attributes.assert_called_with(["on_off"])
