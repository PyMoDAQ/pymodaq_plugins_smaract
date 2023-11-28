from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main, DataActuatorType,\
    DataActuator  # common set of parameters for all actuators
from pymodaq.utils.daq_utils import ThreadCommand  # object used to send info back to the main thread
from pymodaq.utils.parameter import Parameter
from ..hardware.smaract.smaract import SmarAct
from ..hardware.smaract.smaract import get_controller_locators


class DAQ_Move_SmarActMCS_OpenLoop(DAQ_Move_base):
    """
    This plugin supports only SmarAct actuators (with or without sensor) in open loop operation. There is no
    referencing. It considers only moves as a number of steps.
    This plugin should be compatible with any actuator (linear, rotation, goniometer...) since it does not depend on a
    sensor type.
    We suppose to have one (or multiple) MCS controllers connected. With less than 9 channels each. If there is less
    channels the user should just ignore the other ones.
    PyMoDAQ version: 4.0.11
    OS: Windows 10
    Tested with a MCS controller and a STT optical mount.
    The SmarAct MCS installer should have been run before using this plugin: PTC and MCSConfiguration softwares should
    be installed.

    The size of each step can be tuned with the Amplitude parameter, but it seems like it is not something linear. For
    example for the STT mount we observed a kind of threshold: if Amplitude < 1000, the actuator does not move.
    The Frequency parameter is the number of steps done in a second. This should not be too high if the actuator is
    placed under vacuum.

    TODO: it should be possible to keep track of the sum of the number of steps the user has done in forward or
        backward directions. This is not implemented for now.
    """
    _controller_units = "step"
    _epsilon = 1
    # find controller locators
    controller_locators = get_controller_locators()

    is_multiaxes = True
    # we suppose to have a MCS controller (first generation) with up to 9 channels.
    axes_names = {'Axis 1': 0, 'Axis 2': 1, 'Axis 3': 2, 'Axis 4': 3, 'Axis 5': 4, 'Axis 6': 5, 'Axis 7': 6,
                  'Axis 8': 7, 'Axis 9': 8}

    params = [
        {
            "title": "Controller parameters",
            "name": "controller_parameters",
            "type": "group",
            "children": [
                {
                    "title": "Controller Name",
                    "name": "smaract_mcs",
                    "type": "str",
                    "value": "SmarAct MCS controller",
                    "readonly": True,
                },
                {
                    "title": "Controller locator",
                    "name": "controller_locator",
                    "type": "list",
                    "limits": controller_locators,
                },
            ],
        },
        {
             "title": "Open loop move parameters",
             "name": "open_loop_move_parameters",
             "type": "group",
             "children": [
                 {
                     "title": "Amplitude [0...+4095]",
                     "name": "step_amplitude",
                     "type": "int",
                     "value": 1000,
                 },
                 {
                     "title": "Frequency [1...+18,500] (Hz)",
                     "name": "step_frequency",
                     "type": "int",
                     "value": 1000,
                 },
             ],
        },
    ] + comon_parameters_fun(is_multiaxes, axes_names, epsilon=_epsilon)

    def ini_attributes(self):
        self.controller: SmarAct = None

    def ini_stage(self, controller=None):
        """Initialize the controller and stages (axes) with given parameters.

        Parameters
        ----------
        controller (object): custom object of a PyMoDAQ plugin (Slave case). None if only one actuator by controller
        (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        self.controller = self.ini_stage_init(controller, SmarAct())

        if self.settings.child('multiaxes', 'multi_status').value() == "Master":
            self.controller.init_communication(
                    self.settings["controller_parameters", "controller_locator"])
        info = 'SmarAct stage initialized'
        initialized = True

        return info, initialized

    def close(self):
        """Close the communication with the MCS controller.
        """
        self.controller.close_communication()
        self.controller = None

    def get_actuator_value(self):
        """Get the current position from the hardware with scaling conversion.

        This plugin considers only open-loop operation so there is no value for the actuator position. We return 0.0.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        pos = DataActuator(data=self.current_value)
        pos = self.get_position_with_scaling(pos)
        return pos

    def move_abs(self, value: DataActuator):
        """Move the actuator to the absolute target defined by value.

        This plugin considers only relative moves, thus this method is not implemented.

        Parameters
        ----------
        value: (float) value of the absolute target positioning.
        """
        self.emit_status(ThreadCommand('Update_Status', [
            'This plugin considers only relative moves, the method "move_abs" is not implemented.']))
        pass

    def move_rel(self, value: DataActuator):
        """Move the actuator to the relative target actuator value defined by value.

        Parameters
        ----------
        value: (float?) float or DataActuator?
        """
        self.controller.step_move(
            self.settings["multiaxes", "axis"],
            int(value),
            self.settings["open_loop_move_parameters", "step_amplitude"],
            self.settings["open_loop_move_parameters", "step_frequency"],
            )

    def move_home(self):
        """Move to home and reset position to zero.
        """
        self.emit_status(ThreadCommand('Update_Status', [
            'This plugin considers only relative moves, the method "move_home" is not implemented.']))
        pass

    def stop_motion(self):
        """
        See Also
        --------
        DAQ_Move_base.move_done
        """

        self.controller.stop(self.settings["multiaxes", "axis"])

        self.move_done()

        self.emit_status(ThreadCommand('Update_Status', [
            'The movement has been aborted.']))


if __name__ == "__main__":
    main(__file__, init=True)
