

from pymodaq.control_modules.move_utility_classes import (DAQ_Move_base, comon_parameters_fun, main,
                                                          DataActuatorType, DataActuator)
from pymodaq_plugins_smaract.hardware.mcs1.MCS1_wrapper import SmarActMCS1Wrapper, get_controller_locators


class DAQ_Move_SmarActMCS1(DAQ_Move_base):
    """
    This plugin supports only SmarAct LINEAR positionners (SLC type), with enabled sensors attached to them.
    We suppose to have one (or multiple) MCS controllers connected. With 3 channels (each).
    We suppose that the configuration of the controllers (sensor type etc) has been done via the SmarAct MCS
    Configuration software.
    Tested with one SLC-1740-S (closed loop with nanometer precision sensor) connected via a MCS-3S-EP-SDS15-TAB
    (sensor module) to a MCS-3D (or MCS-3C) controller on Windows 7 and Ubuntu.
    """
    _controller_units = "µm"
    _epsilon = 0.005 # µm. Precision tolerance for movement.
    controller_locators = get_controller_locators()

    is_multiaxes = True
    # we suppose to have a MCS controller with 3 channels (like the MCS-3D).
    axes_names= {'Axis 1': 0, 'Axis 2': 1, 'Axis 3': 2}
    # bounds corresponding to the SLC-24180
    min_bound = -61500  # µm
    max_bound = +61500  # µm
    offset = 0  # µm

    data_actuator_type = DataActuatorType.DataActuator

    params = [{'title': 'Controller Name:', 'name': 'device_name', 'type': 'str',
               'value': 'SmarAct MCS1 controller', 'readonly': True},
              {'title': 'Controller locator', 'name': 'controller_locator',
               'type': 'list', 'limits': controller_locators},
              ] + comon_parameters_fun(axis_names=axes_names, epsilon=_epsilon)

    def ini_attributes(self):
        self.controller: SmarActMCS1Wrapper = None
        self._base_resolution: list[int] = None
        self._base_units: list[str] = None

    def ini_stage(self, controller=None):
        """Initialize the controller and stages (axes) with given parameters.

        Parameters
        ----------
        controller (object): custom object of a PyMoDAQ plugin (Slave case).
            None if only one actuator by controller (Master case)

        Returns
        -------
        info: str
        initialized: bool
            False if initialization failed otherwise True
        """
        if self.is_master:
            self.controller = SmarActMCS1Wrapper()
            self.controller.open_communication(
                self.settings['controller_locator'])
        else:
            self.controller = controller

        # min and max bounds will depend on which positionner is plugged.
        # Anyway the bounds are secured by the library functions.
        self.settings.child("bounds", "is_bounds").setValue(True)
        self.settings.child("bounds", "min_bound").setValue(self.min_bound)
        self.settings.child("bounds", "max_bound").setValue(self.max_bound)
        self.settings.child("scaling", "use_scaling").setValue(True)
        self.settings.child("scaling", "offset").setValue(self.offset)

        initialized = True
        info = 'SmarAct stage initialized'
        return info, initialized

    def close(self):
        """Close the communication with the SmarAct controller.
        """
        self.controller.close_communication()
        self.controller = None

    def get_actuator_value(self) -> DataActuator:
        """Get the current position from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        pos = self.controller.get_position(self.axis_value)
        pos = DataActuator(data=pos, units='nm').units_as(self.axis_unit)
        pos = self.get_position_with_scaling(pos)
        # the position given by the controller is in nanometers, we convert in plugin units
        return pos

    def move_abs(self, value: DataActuator):
        """Move the actuator to the absolute target defined by value

        Parameters
        ----------
        value: (DataActuator object)
        """

        value = self.check_bound(value)  # if user checked bounds, the defined bounds are applied here
        self.target_value = value
        value = self.set_position_with_scaling(value)  # apply scaling if the user specified one
        value = int(value.units_as('nm').value())  # MCS1 controllers basic unit is nanometer
        self.controller.absolute_move(self.axis_value, value)

    def move_rel(self, value: DataActuator):
        """Move the actuator to the relative target actuator value defined by value

        Parameters
        ----------
        value: (DataActuator object)
        """
        value = self.check_bound(self.current_value + value) - self.current_value
        self.target_value = value + self.current_value
        # convert the user set position to the controller position if scaling
        # has been activated by user
        relative_move = self.set_position_with_scaling(value)

        # convert relative_move in nanometers (basic unit for MCS1 controllers)
        relative_move = int(relative_move.units_as('nm').value())

        self.controller.relative_move(self.axis_value, relative_move)

    def move_home(self):
        """Move to the physical reference and reset position to zero.
        """
        self.controller.find_reference(self.axis_value)

    def stop_motion(self):
        """Stop the actuator
        """
        self.controller.stop(self.axis_value)


if __name__ == "__main__":
    main(__file__, init=True)
