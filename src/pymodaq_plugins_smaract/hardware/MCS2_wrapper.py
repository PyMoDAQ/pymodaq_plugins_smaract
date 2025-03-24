# -*- coding: utf-8 -*-
import os
import re

from typing import Optional

import ctypes
from pymodaq_utils.logger import set_logger, get_module_name

logger = set_logger(get_module_name(__file__))

try:
    from pymodaq_plugins_smaract.hardware import MCS2_bindings as bindings
except Exception as e:
    bindings = None
    logger.warning(f'Could not load Smaract MCS2 bindings: {str(e)}')



def get_controller_locators():
    """Get the controller locator of the plugged MCS2 controllers.

    e.g. usb:sn:00000667
    The 8-digit number corresponds to the serial number printed on the device.

    Returns
    -------
    controller_locators : list of str
    """
    if bindings is None:
        return []
    try:
        devices = bindings.FindDevices()
    except bindings.Error as e:
        logger.warning('Smaract Library could not find any device')
        devices = []
    if not isinstance(devices, list):
        devices = [devices]
    return devices


class SmarActMCS2Wrapper:
    """The API documentation is in SmarAct MCS2 Programmers Guide, which is in the package docs folder

    Prerequisites
    -------------
    We suppose that the configuration of the channels of the controller (sensor type etc)
    has been done via the SmarAct MCS2ServiceTool software.


    It is up to the user to check for the positioner units and base resolution: in general picometer
    for a linear positioner or nano degree for a rotary one
    """


    def __init__(self):
        """ After initialization the program gives an unsigned int index to each
        controller that is connected.
        The plugin does not support multiple controllers management.
        """

        self.controller_index: Optional[int] = None

    def open_communication(self, controller_locator, configuration: str = ''):
        """Use the controller locator returned from get_controller_locator and
            return the system index attributed by the dll to refer to the
            controller.

        Parameters
        -------
        controller_locator: str
        configuration: str
            The configuration used to open the communication (unused)
        """
        self.controller_index = bindings.Open(controller_locator, config=configuration)

    def close_communication(self):
        """Close the communication with the controller.
        """
        bindings.Close(self.controller_index)

    def get_device_name(self) -> str:
        return bindings.GetProperty_s(self.controller_index, 0,
                                      bindings.Property.DEVICE_NAME)

    def get_number_of_channels(self):
        """ Return the number of channels of the controller.

        Note that the number of channels does not represent the number of positionners and/or
        end effectors that are currently connected to the system.

        Returns
        -------
        int: The number of channel the controller can handle
        """
        return bindings.GetProperty_i32(self.controller_index, 0,
                                        bindings.Property.NUMBER_OF_CHANNELS)

    def get_positionner_type(self, channel_index) -> str:
        """ Get the positionner type name"""

        return bindings.GetProperty_s(self.controller_index, channel_index,
                                      bindings.Property.POSITIONER_TYPE_NAME)

    def get_units(self, channel_index: int) -> str:
        """ Get the positionner units"""
        unit_enum_value = bindings.GetProperty_i32(self.controller_index, channel_index,
                                                   bindings.Property.POS_BASE_UNIT)
        unit = bindings.BaseUnit(unit_enum_value)
        if unit == bindings.BaseUnit.NONE:
            unit = None
        else:
            unit = str(unit.name).lower()
        return unit

    def get_base_resolution(self, channel_index: int) -> float:
        """ Get the channel base resolution

        See Also
        --------
        self.get_units
        """
        resolution_value = bindings.GetProperty_i32(self.controller_index, channel_index,
                                                    bindings.Property.POS_BASE_RESOLUTION)
        return resolution_value

    def get_position(self, channel_index: int):
        """Return the current position of the positionner connected to the channel
        indexed by channel_index (starts at 0) in picometers.

        Parameters
        ----------
        channel_index: int

        Returns
        -------
        int: The position in base units

        See Also:
        ---------
        self.get_units, self.get_base_resolution

        """
        position = bindings.GetProperty_i64(self.controller_index,
                                            channel_index,
                                            bindings.Property.POSITION)

        return position

    def find_reference(self, channel_index):
        """Find the physical zero reference of the positioner (starting in the forward direction)

        Reset the position to zero if configured as such (see configuration smaract tool)

        Here we suppose that the reference method has been configured with the MCS Configuration
        software for example.

        Parameters
        ----------
        channel_index: int
        """

        bindings.Reference(self.controller_index, channel_index)

    def absolute_move(self, channel_index, value: int):
        """Go to an absolute position in base units with base resolution.

        If a mechanical end stop is detected while the command is in execution,
        the movement will be aborted (without notice).

        Parameters
        ----------
        channel_index: int
        value: int
            The value expressed in base units and with base resolution (for instance 1e-12 meter)
        """
        bindings.SetProperty_i32(self.controller_index, channel_index,
                                 bindings.Property.MOVE_MODE,
                                 bindings.MoveMode.CL_ABSOLUTE)

        bindings.Move(self.controller_index, channel_index, int(value))

    def relative_move(self, channel_index, value: int):
        """Go to a relative position in base units with base resolution.

        If a mechanical end stop is detected while the command is in execution,
        the movement will be aborted (without notice).

        Parameters
        ----------
        channel_index: int
        value: int
            The value expressed in base units and with base resolution (for instance 1e-12 meter)
        """

        bindings.SetProperty_i32(self.controller_index, channel_index,
                                 bindings.Property.MOVE_MODE,
                                 bindings.MoveMode.CL_RELATIVE)

        bindings.Move(self.controller_index, channel_index, int(value))


    def stop(self, channel_index: int):
        """Stop any ongoing movement of the positionner. This command also
            stops the hold position feature of closed-loop commands.

        Parameters
        ----------
        channel_index: int
        """
        bindings.Stop(self.controller_index, channel_index)


if __name__ == '__main__':
    devices = get_controller_locators()

    wrapper = SmarActMCS2Wrapper()
    wrapper.open_communication(devices[0])
    nchannels = wrapper.get_number_of_channels()

    units = [wrapper.get_units(index) for index in range(nchannels)]
    base_resolution = [wrapper.get_base_resolution(index) for index in range(nchannels)]

    #wrapper.find_reference(0)

    wrapper.get_position(0)
