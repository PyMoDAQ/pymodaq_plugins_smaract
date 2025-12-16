# -*- coding: utf-8 -*-

import ctypes as ct

from pymodaq_utils.logger import set_logger, get_module_name

logger = set_logger(get_module_name(__file__))

try:
    from pymodaq_plugins_smaract.hardware.mcs1 import MCS1_bindings as bindings
except Exception as e:
    bindings = None
    logger.warning(f'Could not load Smaract MCS1 bindings: {str(e)}')



def get_controller_locators():
    """Get the locator (e.g. usb:id:3118167233) of the plugged MCS1 controller.

    Caution: if several controllers are plugged, the code probably needs to be updated.
    The 10-digit number corresponds to the serial number printed on the controller.

    Returns
    -------
    controller_locators : list of str
    """
    if bindings is None:
        return []

    outBuffer = ct.create_string_buffer(17)
    ioBufferSize = ct.c_ulong(18)
    status = bindings.SA_FindSystems('', outBuffer, ioBufferSize)

    if status != 0:
        raise Exception('SmarAct SA_FindSystems error')

    controller_locators = outBuffer[:18].decode("utf-8")

    if not controller_locators:
        logger.warning('No SmarAct MCS controller found')

    return [controller_locators]


class SmarActMCS1Wrapper(object):
    """The API documentation is in SmarAct MCS Programmers Guide.
    We suppose that the configuration of the controllers (sensor type etc) has been done via the SmarAct MCS
    Configuration software.
    We suppose to have some linear positionners (SLC type) with enabled sensors attached to them, connected to the
    channel 0 of the controller.
    Tested with SLC-1740-S (closed loop with nanometer precision sensor) connected to a MCS-3D or MCS-3C controller.
    """

    def __init__(self):
        super(SmarActMCS1Wrapper, self).__init__()

        self.controller_index = ''

    def open_communication(self, controller_locator):
        """Use the controller locator returned from get_controller_locator and return the system index attributed by
            FindSystems to refer to the controller.

        Parameters
        -------
        controller_locator:str
        """
        controller_index = ct.c_ulong()
        # we choose the synchronous communication mode
        options = 'sync'.encode('ascii')

        status = bindings.SA_OpenSystem(
            controller_index,
            controller_locator.encode('ascii'),
            options
        )

        if status != 0:
            raise Exception('SmarAct SA_OpenSystem failed')

        # return controller_index.value
        self.controller_index = controller_index.value

    def get_number_of_channels(self):
        """ Return the number of channels of the controller.

        Note that the number of channels does not represent the number positioners and/or end effectors that are
        currently connected to the system.

        Parameters
        -------
        controller_index:str

        Returns
        -------
        numberOfChannels.value:unsigned int
        """
        numberOfChannels = ct.c_ulong()

        status = bindings.SA_GetNumberOfChannels(
            ct.c_ulong(self.controller_index),
            numberOfChannels
        )

        if status != 0:
            self.close_communication()
            raise Exception('SmarAct SA_GetNumberOfChannels failed')

        return numberOfChannels.value

    def close_communication(self):
        """
            Close the communication with the controller.
        """
        status = bindings.SA_CloseSystem(
            ct.c_ulong(self.controller_index)
        )

        if status != 0:
            raise Exception(f'SmarAct SA_CloseSystem failed with error {status}')

    def get_position(self, channel_index):
        """
            Return the current position of the positioner connected to the channel indexed by channel_index
            (starts at 0) in nanometers.

        Parameters
        ----------
        channel_index:unsigned int

        Returns
        -------
        position.value:signed int
        """

        position = ct.c_int32()

        status = bindings.SA_GetPosition_S(
            ct.c_ulong(self.controller_index),
            ct.c_ulong(channel_index),
            position
        )

        if status != 0:
            self.close_communication()
            raise Exception('SmarAct SA_GetPosition failed')

        return position.value

    def find_reference(self, channel_index):
        """Find the physical zero reference of the positioner (starting in the forward direction) and reset the
        position to zero.

        Parameters
        ----------
        channel_index:unsigned int
        """

        # with direction = 0 search for reference starts in the forward
        # direction
        direction = 0
        # hold time = 60,000 ms corresponds to infinite holding
        hold_time = 60000
        # auto zero = 1 will reset the position to zero after reaching
        # the reference mark
        auto_zero = 1

        status = bindings.SA_FindReferenceMark_S(
            ct.c_ulong(self.controller_index),
            ct.c_ulong(channel_index),
            ct.c_ulong(direction),
            ct.c_ulong(hold_time),
            ct.c_ulong(auto_zero)
        )

        if status != 0:
            self.close_communication()
            raise Exception('SmarAct SA_FindReferenceMark failed')

        print('The positionner is referenced !')

    def relative_move(self, channel_index, relative_position):
        """Execute a relative move in nanometers.

        If a mechanical end stop is detected while the command is in execution, the movement will be aborted
        (without notice).

        Parameters
        ----------
        channel_index:unsigned int
        relative_position:signed int
        """

        # hold time = 60,000 ms corresponds to infinite holding
        hold_time = 60000

        status = bindings.SA_GotoPositionRelative_S(
            ct.c_ulong(self.controller_index),
            ct.c_ulong(channel_index),
            ct.c_long(relative_position),
            ct.c_ulong(hold_time)
        )

        if status != 0:
            self.close_communication()
            raise Exception('SmarAct SA_GotoPositionRelative failed')

    def absolute_move(self, channel_index, absolute_position):
        """Go to an absolute position in nanometers.

        If a mechanical end stop is detected while the command is in execution, the movement will be aborted
        (without notice).

        Parameters
        ----------
        channel_index:unsigned int
        absolute_position:signed int
        """

        # hold time = 60,000 ms corresponds to infinite holding
        hold_time = 60000

        status = bindings.SA_GotoPositionAbsolute_S(
            ct.c_ulong(self.controller_index),
            ct.c_ulong(channel_index),
            ct.c_long(absolute_position),
            ct.c_ulong(hold_time)
        )

        if status != 0:
            self.close_communication()
            raise Exception('SmarAct SA_GotoPositionAbsolute failed')

    def stop(self, channel_index):
        """ Stop any ongoing movement of the positionner.

        This command also stops the hold position feature of closed-loop commands.

        Parameters
        ----------
        channel_index:unsigned int
        """

        status = bindings.SA_Stop_S(
            ct.c_ulong(self.controller_index),
            ct.c_ulong(channel_index)
        )

        if status != 0:
            self.close_communication()
            raise Exception('SmarAct SA_Stop failed')
