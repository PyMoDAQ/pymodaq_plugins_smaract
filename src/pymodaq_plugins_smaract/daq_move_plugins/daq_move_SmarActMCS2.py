from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main  # common set of parameters for all actuators
from pymodaq.daq_utils.daq_utils import ThreadCommand, getLineInfo  # object used to send info back to the main thread
from pymodaq.daq_utils.parameter import Parameter
from ..hardware.smaract.smaract_MCS2_wrapper import SmarActMCS2Wrapper
from ..hardware.smaract.smaract_MCS2_wrapper import get_controller_locators
from pymodaq.daq_utils.config import Config
config = Config()

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

    axes_names = ['0', '1', '2']  # be careful that the channel index starts at 0
    # and not at 1 has is done in MCS2ServiceTool

    # bounds corresponding to the SLC-24180. Will be used at default if user doesn't provide other ones.
    min_bound = -61500  # µm
    max_bound = +61500  # µm

    offset = 0  # µm

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
                ] + comon_parameters_fun(is_multiaxes, axes_names)

    def ini_attributes(self):
        self.controller: SmarActMCS2Wrapper = None

    def get_actuator_value(self):
        """Get the current value from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        pos = self.controller.get_position(
            self.settings.child('multiaxes', 'axis').value())
        pos = float(pos) / 1e6  # the position given by the
        # controller is in picometers, we convert in micrometers
        pos = self.get_position_with_scaling(pos)
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

        self.ini_stage_init(old_controller=controller,
                            new_controller=SmarActMCS2Wrapper())

        # min and max bounds will depend on which positionner is plugged.
        # In case the user hasn't specified different values in the preset,
        # we add default values for convenience
        if self.settings.child('epsilon').value() == config('actuator', 'epsilon_default'):
            self.settings.child('epsilon').setValue(0.005)  # this means that we
            # tolerate an error of 5 nanometers on the target position

        self.settings.child('bounds', 'is_bounds').setValue(True)
        if self.settings.child('bounds', 'min_bound').value() == 0:
            self.settings.child('bounds', 'min_bound').setValue(self.min_bound)

        if self.settings.child('bounds', 'max_bound').value() == 1:
            self.settings.child('bounds', 'max_bound').setValue(self.max_bound)

        try:
            self.controller.init_communication(
                self.settings.child('group_parameter',
                                    'controller_locator').value())
            initialized = True
        except:
            initialized = False

        info = "Smaract stage initialized"
        return info, initialized

    def move_abs(self, value):
        """ Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (float) value of the absolute target positioning
        """

        value = self.check_bound(value)  # if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one
        value = int(value * 1e6)
        self.controller.absolute_move(
            self.settings.child('multiaxes', 'axis').value(), value)
        self.emit_status(ThreadCommand('Update_Status', [f'Moving to {value}']))

    def move_rel(self, value):
        """ Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (float) value of the relative target positioning
        """
        value = self.check_bound(self.current_position + value) - self.current_position
        self.target_value = value + self.current_position
        relative_move = self.set_position_relative_with_scaling(value)

        # convert relative_move in picometers
        relative_move = int(relative_move*1e6)

        self.controller.relative_move(
            self.settings.child('multiaxes', 'axis').value(),
            relative_move)
        self.emit_status(ThreadCommand('Update_Status', [f'Moving to {self.target_value}']))

    def move_home(self):
        """Move to the physical reference and reset position to 0
        """
        self.controller.find_reference(
            self.settings.child('multiaxes', 'axis').value())
        self.emit_status(ThreadCommand('Update_Status',
                                       ['The positioner has been referenced']))

    def stop_motion(self):
        """Stop the actuator and emits move_done signal"""
        self.controller.stop(self.settings.child('multiaxes', 'axis').value())
        self.emit_status(ThreadCommand('Update_Status',
                                       ['The positioner has been stopped']))


if __name__ == '__main__':
    main(__file__)