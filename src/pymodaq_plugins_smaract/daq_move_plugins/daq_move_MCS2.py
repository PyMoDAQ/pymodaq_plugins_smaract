

from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun,
                                                          main, DataActuatorType, DataActuator)  # common set of parameters for all actuators
from pymodaq_utils.utils import ThreadCommand, getLineInfo

from pymodaq_gui.parameter import Parameter
from pymodaq_data import Unit

from pymodaq_plugins_smaract.hardware.MCS2_wrapper import SmarActMCS2Wrapper, get_controller_locators


controller_locators = get_controller_locators()


class DAQ_Move_MCS2(DAQ_Move_base):
    """This plugin handles SmarAct MCS2 controller with positioners with the
    S option (which means that an encoder is present and give a feedback on the
    current position).

    If you use the first version of MCS controller use the daq_move_SmarActMCS
    plugin.

    The SmarAct MCS2 installer should be executed for this plugin to work.
    We suppose that the configuration of the controller and the positioners
    (sensor type…) has been done via the SmarAct MCS2ServiceTool software.

    If the controller is not switched on, the plugin will not be suggested in
    the list in the GUI of the daq_move.

    It has been tested on Windows 10, with SLC positioner type with enabled
    sensors.
    """

    is_multiaxes = True
    axis_names= {'Axis 1': 0, 'Axis 2': 1, 'Axis 3': 2}

    _controller_units = {'Axis 1': 'um', 'Axis 2': 'um', 'Axis 3': 'um'}  #may be changed at initialization
    _epsilon = {'Axis 1': 0.005, 'Axis 2': 0.005, 'Axis 3': 0.005}  # in _controller_units  precision tolerance for movement

    data_actuator_type = DataActuatorType.DataActuator

    params = [{'title': 'Controller Name:', 'name': 'device_name', 'type': 'str',
               'value': 'SmarAct MCS2 controller', 'readonly': True},
              {'title': 'Controller locator', 'name': 'controller_locator',
               'type': 'list', 'limits': controller_locators},
              ] + comon_parameters_fun(axis_names=axis_names, epsilon=_epsilon)

    def ini_attributes(self):
        self.controller: SmarActMCS2Wrapper = None
        self._base_resolution: list[int] = None
        self._base_units: list[str] = None

    def get_actuator_value(self) -> DataActuator:
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        pos = self.controller.get_position(self.axis_value)
        pos = 10**(self._base_resolution[self.axis_value]) * pos
        pos = DataActuator(data=pos, units=self._base_units[self.axis_value]).units_as(self.axis_unit)
        pos = self.get_position_with_scaling(pos)
        # the position given by the controller is in picometers, we convert in plugin units
        return pos

    def close(self):
        """Close the communication with the MCS2 controller.
        """
        self.controller.close_communication()
        self.controller = None

    def commit_settings(self, param: Parameter):
        """
            | Activate any parameter changes on the hardware.
            |
            | Called after a param_tree_changed signal from DAQ_Move_main.
        # Unused

        """

    def ini_stage(self, controller=None):
        """Actuator communication initialization

        Parameters
        ----------
        controller: (object)
            custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        if self.is_master:
            self.controller = SmarActMCS2Wrapper()
            self.controller.open_communication(
                self.settings['controller_locator'])
        else:
            self.controller = controller

        self.settings.child('device_name').setValue(self.controller.get_device_name())

        units = []
        base_resolution = []
        for ind_channel in range(self.controller.get_number_of_channels()):
            units.append(self.controller.get_units(ind_channel))
            base_resolution.append(self.controller.get_base_resolution(ind_channel))

        self.axis_units = dict(zip(self.axis_names.keys(),
                                   [self._reduce_unit(unit) for unit in units]))
        self._base_units = units
        self._base_resolution = base_resolution

        initialized = True
        info = "Smaract stage initialized"
        return info, initialized

    @staticmethod
    def _reduce_unit(unit: str) -> str:
        """ make use of easier to use units compared to base ones"""
        if Unit(unit).is_compatible_with('m'):
            return 'um'
        else:
            return unit

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """
        value = self.check_bound(value)  # if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one
        value = int(value.units_as(self._base_units[self.axis_value]).value() * 10**(-self._base_resolution[self.axis_value]))
        self.controller.absolute_move(self.axis_value, value)

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        value = self.set_position_relative_with_scaling(value)

        # convert relative_move in base unit and base resolution
        value = int(value.units_as(self._base_units[self.axis_value]).value() * 10**(-self._base_resolution[self.axis_value]))

        self.controller.relative_move(self.axis_value, value)

    def move_home(self):
        """Move to the physical reference and reset position to 0
        """
        self.controller.find_reference(self.axis_value)

    def stop_motion(self):
        """Stop the actuator and emits move_done signal"""
        self.controller.stop(self.axis_value)



if __name__ == '__main__':
    main(__file__, init=True)
