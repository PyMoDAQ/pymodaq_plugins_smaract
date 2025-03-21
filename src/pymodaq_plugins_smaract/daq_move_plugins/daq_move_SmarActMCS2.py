

from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun,
                                                          main, DataActuatorType, DataActuator)  # common set of parameters for all actuators
from pymodaq_utils.utils import ThreadCommand, getLineInfo

from pymodaq_gui.parameter import Parameter

from pymodaq_plugins_smaract.hardware.smaract.smaract_MCS2_wrapper import SmarActMCS2Wrapper
from pymodaq_plugins_smaract.hardware.smaract.smaract_MCS2_wrapper import get_controller_locators


"""This plugin handles SmarAct MCS2 controller with LINEAR positioners with the
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

class DAQ_Move_SmarActMCS2(DAQ_Move_base):
    """
        =============== ==============
        **Attributes**    **Type**
        *params*          dictionnary
        =============== ==============
    """
    _controller_units = 'µm'
    controller_locators = get_controller_locators()
    is_multiaxes = True  # we suppose a have a MCS2 controller with a sensor
    # module for 3 channels (stages).

    axis_names= {'Axis 1': 0, 'Axis 2': 1, 'Axis 3': 2}  # be careful that the channel index starts at 0
    # and not at 1 has is done in MCS2ServiceTool

    data_actuator_type = DataActuatorType.DataActuator

    _epsilon = 0.005 # µm   precision tolerance for movement


    params = [
                 {'title': 'group parameter:',
                  'name': 'group_parameter',
                  'type': 'group',
                  'children': [
                     {'title': 'Controller Name:',
                      'name': 'smaract_mcs2',
                      'type': 'str',
                      'value': 'SmarAct MCS2 controller',
                      'readonly': True},
                     {'title': 'Controller locator',
                      'name': 'controller_locator', 'type': 'list',
                      'limits': controller_locators},
                  ]}
                ] + comon_parameters_fun(axis_names=axis_names, epsilon=_epsilon)

    def ini_attributes(self):
        self.controller: SmarActMCS2Wrapper = None

    def get_actuator_value(self) -> DataActuator:
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        pos = self.controller.get_position(self.axis_value)
        pos = DataActuator(data=pos, units='pm').units_as(self.axis_unit)
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
            self.controller.init_communication(
                self.settings['group_parameter', 'controller_locator'])
        else:
            self.controller = controller


        initialized = True
        info = "Smaract stage initialized"
        return info, initialized

    def move_abs(self, value: DataActuator):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)  # if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one
        value = int(value.units_as('pm').value())
        self.controller.absolute_move(self.axis_value, value)

    def move_rel(self, value: DataActuator):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        relative_move = self.set_position_relative_with_scaling(value)

        # convert relative_move in picometers
        relative_move = int(relative_move.units_as('pm').value())

        self.controller.relative_move(self.axis_value, relative_move)

    def move_home(self):
        """Move to the physical reference and reset position to 0
        """
        self.controller.find_reference(self.axis_value)

    def stop_motion(self):
        """Stop the actuator and emits move_done signal"""
        self.controller.stop(self.axis_value)



if __name__ == '__main__':
    main(__file__, init=True)
