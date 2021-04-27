# -*- coding: utf-8 -*-

import ctypes
import os
import re

"""The API documentation is in SmarAct MCS2 Programmers Guide, which should be
   in the same folder as this file.
    
    Prerequisites
    -------------
    We suppose that the configuration of the channels of the controller (sensor
type etc) has been done via the SmarAct MCS2ServiceTool software.
    We suppose to have some linear positionners (SLC type) with sensors
(S option).

    Tested with:
    - positioner: SLC24180s
    - sensor type: MCS2-S-0001
    - controller: MCS2 in closed loop, positioner type = SL...S1SS (300)
"""

# The SmarActCTL.dll should also be in the current folder, but also
# SmarActCTL.lib, SmarActIO.dll, SmarActSI.dll, SmarActSI.lib
# The CDLL function asks for the full path
dir_path = os.path.dirname(os.path.realpath(__file__))
smaract_dll = ctypes.CDLL(os.path.join(dir_path, "SmarActCTL.dll"))


def get_controller_locators():
    """Get the controller locator of the plugged MCS2 controllers.

    e.g. usb:sn:00000667
    The 8-digit number corresponds to the serial number printed on the device.

    Returns
    -------
    controller_locators : list of str
    """
    ioListSize = 4096
    options = ctypes.c_char()
    outList = (' ' * ioListSize).encode()
    ioListSize = ctypes.c_ulong(ioListSize)

    status = smaract_dll.SA_CTL_FindDevices(
        ctypes.byref(options),
        outList,
        ctypes.byref(ioListSize)
    )

    if status != 0:
        raise Exception('SmarAct SA_CTL_FindDevices error')

    controller_locators = re.findall("usb:sn:MCS2-[0-9]*", outList.decode())

    if not controller_locators:
        raise Exception('SmarActMCS2Wrapper: No controller found !')

    return controller_locators


class SmarActMCS2Wrapper:

    def __init__(self):
        super(SmarActMCS2Wrapper, self).__init__()

        # After initialization the program gives an unsigned int index to each
        # controller that is connected.
        # The plugin does not support multiple controllers management.
        self.controller_index = ''

    def init_communication(self, controller_locator):
        """Use the controller locator returned from get_controller_locator and
            return the system index attributed by the dll to refer to the
            controller.

        Parameters
        -------
        controller_locator: str
        """
        controller_index = ctypes.c_ulong()
        # we choose the synchronous communication mode
        # options = 'sync'.encode('ascii')

        status = smaract_dll.SA_CTL_Open(
            ctypes.byref(controller_index),
            controller_locator.encode('ascii'),
            ""
        )

        if status != 0:
            raise Exception('SmarActMCS2Wrapper: SmarAct SA_CTL_Open failed')

        self.controller_index = controller_index.value

    def get_number_of_channels(self):
        """
            Return the number of channels of the controller. Note that the
            number of channels does not represent the number positioners and/or
            end effectors that are currently connected to the system.

        Returns
        -------
        numberOfChannels.value: unsigned int
        """
        number_of_channels = ctypes.c_ulong()

        # The code 0x020F0017 corresponds to SA_CTL_PKEY_NUMBER_OF_CHANNELS has
        # been found in page 137 of the programmers guide
        status = smaract_dll.SA_CTL_GetProperty_i32(
            ctypes.c_ulong(self.controller_index),
            0,
            0x020F0017,
            ctypes.byref(number_of_channels),
            0)

        if status != 0:
            self.close_communication()
            raise Exception(
                'SmarActMCS2Wrapper: SmarAct API failed to get the number of'
                'channels')

        return number_of_channels.value

    def close_communication(self):
        """Close the communication with the controller.
        """
        status = smaract_dll.SA_CTL_Close(
            ctypes.c_ulong(self.controller_index)
        )

        if status != 0:
            raise Exception('SmarActMCS2Wrapper: SmarAct SA_CTL_Close failed')

    def get_position(self, channel_index):
        """Return the current position of the positioner connected to the
            channel indexed by channel_index (starts at 0) in picometers.

        Parameters
        ----------
        channel_index: unsigned int

        Returns
        -------
        position.value: signed int
        """

        position = ctypes.c_longlong()

        # The code 0x0305001D corresponds to SA_CTL_PKEY_POSITION has been
        # found in page 155 of the programmers guide
        status = smaract_dll.SA_CTL_GetProperty_i64(
            ctypes.c_ulong(self.controller_index),
            ctypes.c_ulong(channel_index),
            0x0305001D,
            ctypes.byref(position),
            0
        )

        if status != 0:
            self.close_communication()
            raise Exception('SmarActMCS2Wrapper: SmarAct API failed to get the'
                            ' position of the actuator')

        return position.value

    def find_reference(self, channel_index):
        """Find the physical zero reference of the positioner (starting in the
            forward direction) and reset the position to zero.
            Here we suppose that the reference method has been configured with
            the MCS Configuration software for example.

        Parameters
        ----------
        channel_index: unsigned int
        """

        status = smaract_dll.SA_CTL_Reference(
            ctypes.c_ulong(self.controller_index),
            ctypes.c_ulong(channel_index),
            0
        )

        if status != 0:
            self.close_communication()
            raise Exception(
                'SmarActMCS2Wrapper: SmarAct SA_CTL_Reference failed')

    def relative_move(self, channel_index, relative_move_value):
        """Execute a relative move in picometers.
            If a mechanical end stop is detected while the command is in
            execution, the movement will be aborted (without notice).

        Parameters
        ----------
        channel_index: unsigned int
        relative_move_value: signed int. Relative distance in picometer.
        """

        # To perform a relative movement it is necessary to configure the move
        # mode before.
        # The code 0x03050087 corresponds to SA_CTL_PKEY_MOVE_MODE has been
        # found in page 152 of the programmers guide.
        # Number 1 corresponds to a relative move (4th parameter). Found in
        # page 153 of the programmers guide.
        status = smaract_dll.SA_CTL_SetProperty_i32(
            ctypes.c_ulong(self.controller_index),
            ctypes.c_ulong(channel_index),
            0x03050087,
            1
        )

        if status != 0:
            self.close_communication()
            raise Exception(
                'SmarActMCS2Wrapper: SmarAct API failed to configure the'
                'relative move mode.'
            )

        status = smaract_dll.SA_CTL_Move(
            ctypes.c_ulong(self.controller_index),
            ctypes.c_ulong(channel_index),
            ctypes.c_longlong(relative_move_value),
            0
        )

        if status != 0:
            self.close_communication()
            raise Exception('SmarActMCS2Wrapper: SA_CTL_Move failed.')

    def absolute_move(self, channel_index, absolute_move_value):
        """Go to an absolute position in picometers.
            If a mechanical end stop is detected while the command is in
            execution, the movement will be aborted (without notice).

        Parameters
        ----------
        channel_index: unsigned int
        absolute_move_value: signed int. Absolute position in picometer.
        """

        # To perform an absolute movement it is necessary to configure the move
        # mode before.
        # The code 0x03050087 corresponds to SA_CTL_PKEY_MOVE_MODE has been
        # found in page 152 of the programmers guide.
        # Number 0 corresponds to an absolute move (4th parameter). Found in
        # page 153 of the programmers guide.
        status = smaract_dll.SA_CTL_SetProperty_i32(
            ctypes.c_ulong(self.controller_index),
            ctypes.c_ulong(channel_index),
            0x03050087,
            0
        )

        if status != 0:
            self.close_communication()
            raise Exception(
                'SmarActMCS2Wrapper: SmarAct API failed to configure the'
                'absolute move mode.'
            )

        status = smaract_dll.SA_CTL_Move(
            ctypes.c_ulong(self.controller_index),
            ctypes.c_ulong(channel_index),
            ctypes.c_longlong(absolute_move_value),
            0
        )

        if status != 0:
            self.close_communication()
            raise Exception(
                'SmarActMCS2Wrapper: SA_CTL_Move failed.')

    def stop(self, channel_index):
        """Stop any ongoing movement of the positionner. This command also
            stops the hold position feature of closed-loop commands.

        Parameters
        ----------
        channel_index: unsigned int
        """

        status = smaract_dll.SA_CTL_Stop(
            ctypes.c_ulong(self.controller_index),
            ctypes.c_ulong(channel_index),
            0
        )

        if status != 0:
            self.close_communication()
            raise Exception('SmarActMCS2Wrapper: SmarAct SA_CTL_Stop failed')

