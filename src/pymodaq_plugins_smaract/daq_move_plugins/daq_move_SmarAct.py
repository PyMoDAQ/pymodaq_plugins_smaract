from typing import Union

from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, main, comon_parameters_fun
from pymodaq.utils.daq_utils import ThreadCommand
from easydict import EasyDict as edict
from instrumental import instrument, list_instruments
from instrumental.drivers.motion._smaract.scu import SCU, SCULinear, SCURotation, Q_


psets = list_instruments(module='motion._smaract')
psets_str = [f"Dev. Id{pset['id']} channel {pset['index']}" for pset in psets]


class DAQ_Move_SmarAct(DAQ_Move_base):
    """

    """
    _controller_units = ""
    _epsilon = 0.002
    # find controller locators

    is_multiaxes = False
    stage_names = []

    params = [
                 {'title': 'Device', 'name': 'device', 'type': 'list', 'limits': psets_str},
                 {'title': 'Frequency (Hz)', 'name': 'frequency', 'type': 'int', 'value': 450},
                 {'title': 'Amplitude (V)', 'name': 'amplitude', 'type': 'int', 'value': 100},
                 {'title': 'Max Frequency (Hz)', 'name': 'maxfreq', 'type': 'int', 'value': 18500},
    ] + comon_parameters_fun(is_multiaxes, epsilon=_epsilon)
    ##########################################################

    def ini_attributes(self):
        self.controller: Union[SCU, SCULinear, SCURotation] = None
        self.settings.child("epsilon").setValue(0.002)

    def commit_settings(self, param):
        if param.name() == 'amplitude':
            self.controller.amplitude = Q_(param.value(), units='V')
        elif param.name() == 'frequency':
            self.controller.frequency = Q_(param.value(), 'Hz')

        elif param.name() == 'maxfreq':
            self.controller.max_frequency = Q_(param.value(), 'Hz')
            self.settings.child('maxfreq').setValue(self.controller.max_frequency.m_as('Hz'))

    def ini_stage(self, controller=None):
        """Initialize the controller and stages (axes) with given parameters.

        """
        index = self.settings.child('device').opts['limits'].index(self.settings['device'])
        self.ini_stage_init(controller, instrument(psets[index]))

        self.settings.child('units').setValue(self.controller.units)
        self.settings.child('amplitude').setOpts(limits=list(self.controller.amplitude_limits.m_as('V')))
        self.settings.child('frequency').setOpts(limits=list(self.controller.frequency_limits.m_as('Hz')))
        self.settings.child('amplitude').setValue(self.controller.amplitude.m_as('V'))
        self.settings.child('frequency').setValue(self.controller.frequency.m_as('Hz'))
        if not isinstance(self.controller, SCU):
            self.settings.child('maxfreq').setValue(self.controller.max_frequency.m_as('Hz'))

        info = ''
        initialized = True

        return info, initialized

    def close(self):
        """Close the communication with the SmarAct controller.
        """
        self.controller.close()
        self.controller = None

    def get_actuator_value(self):
        """Get the current position from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        position = self.controller.check_position().magnitude
        # convert position if scaling options have been used, mandatory here
        position = self.get_position_with_scaling(position)
        #position = self.target_position
        self.current_position = position

        self.emit_status(ThreadCommand("check_position", [position]))

        return position

    def move_abs(self, position):
        """Move to an absolute position

        Parameters
        ----------
        position: float
        """
        # limit position if bounds options has been selected and if position is
        # out of them
        position = self.check_bound(position)
        self.target_position = position
        # convert the user set position to the controller position if scaling
        # has been activated by user
        position = self.set_position_with_scaling(position)

        self.controller.move_to(Q_(position, self.settings['units']), 'abs')

    def move_rel(self, position):
        """Move to a relative position

        Parameters
        ----------
        position: float
        """
        position = (self.check_bound(self.current_position + position) - self.current_position)
        self.target_position = position + self.current_position
        position = self.set_position_relative_with_scaling(position)

        self.controller.move_to(Q_(position, self.settings['units']), 'rel')

    def move_home(self):
        """Move to home and reset position to zero.
        """
        self.controller.move_home()
        self.get_actuator_value()

    def stop_motion(self):
        """
        """
        self.controller.stop()
        self.move_done()


if __name__ == "__main__":
    main(__file__)
