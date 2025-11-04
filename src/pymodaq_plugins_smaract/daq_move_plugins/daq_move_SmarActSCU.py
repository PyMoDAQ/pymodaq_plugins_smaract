
from typing import Union, List, Dict

from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, main, comon_parameters_fun, DataActuatorType
from pymodaq.utils.daq_utils import ThreadCommand
from easydict import EasyDict as edict

from pymodaq_plugins_smaract.hardware.smaract.scu.scu_wrapper import (get_devices, SCUType, SCUWrapper,
                                                                      SCULinear, SCURotation)

from pymodaq.utils.data import DataActuator

psets: list[SCUType] = get_devices()
psets_str = [f"Dev. Id{pset.device_id} channel {pset.channel} ({pset.scu_type.__name__})" for pset in psets]


class DAQ_Move_SmarActSCU(DAQ_Move_base):
    """

    """
    _controller_units = ""
    _epsilon = 2
    # find controller locators

    is_multiaxes = True
    _axis_names = ['1']

    data_actuator_type = DataActuatorType.DataActuator

    params = [
                 {'title': 'Device', 'name': 'device', 'type': 'list','limits': psets_str},
                 {'title': 'Frequency (Hz)', 'name': 'frequency', 'type': 'int', 'value': 1000, 'limits': SCUWrapper.frequency_limits},
                 {'title': 'Amplitude (V)', 'name': 'amplitude', 'type': 'int', 'value': 100, 'limits':SCUWrapper.amplitude_limits},
    ] + comon_parameters_fun(is_multiaxes=is_multiaxes, axis_names=_axis_names, epsilon=_epsilon)
    ##########################################################

    def ini_attributes(self):
        self.controller: Union[SCUWrapper, SCULinear, SCURotation] = None
        self.settings.child("epsilon").setValue(2)

    def commit_settings(self, param):
        if param.name() == 'amplitude':
            self.controller.amplitude = param.value()
        elif param.name() == 'frequency':
            self.controller.frequency = param.value()

    def ini_stage(self, controller=None):
        """Initialize the controller and stages (axes) with given parameters.

        """
        index = self.settings.child('device').opts['limits'].index(self.settings['device'])
        if self.is_master:
            self.controller = psets[index].scu_type()
            self.controller.open(index)
            self.controller.amplitude = self.settings['amplitude']
            self.controller.frequency = self.settings['frequency']

        else:
            self.controller = controller

        self.axis_unit = self.controller.units

        info = ''
        initialized = True

        return info, initialized

    def close(self):
        """
        Close the communication with the SmarAct controller.
        """
        self.controller.close()

    def get_actuator_value(self):
        """
        Get the current position from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        position = DataActuator(data=self.controller.get_position(), units=self.axis_unit)
        # convert position if scaling options have been used, mandatory here
        position = self.get_position_with_scaling(position)
        #position = self.target_position
        self.current_position = position
        return position

    def move_abs(self, position):
        """
        Move to an absolute position

        Parameters:
        ----------
         - position: float
        """
        # limit position if bounds options has been selected and if position is
        # out of them
        position = self.check_bound(position)
        self.target_position = position
        # convert the user set position to the controller position if scaling
        # has been activated by user
        position = self.set_position_with_scaling(position)

        self.controller.move_abs(position.value())

    def move_rel(self, position):
        """
        Move to a relative position

        Parameters:
        ----------
         - position: float
        """
        position = (self.check_bound(self.current_position + position) - self.current_position)
        self.target_position = position + self.current_position
        position = self.set_position_relative_with_scaling(position)

        self.controller.move_rel(position.value())

    def move_home(self):
        """
        Move to home and reset position to zero.
        """
        self.controller.move_home()
        self.get_actuator_value()

    def stop_motion(self):
        """
        Stop any ongoing movement of the positionner.
        """
        self.controller.stop()
        self.move_done()


if __name__ == "__main__":
    main(__file__, init=False)
