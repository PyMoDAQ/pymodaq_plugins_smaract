from pymodaq.control_modules.move_utility_classes import DAQ_Move_base, comon_parameters_fun, main
from pymodaq_plugins_smaract.hardware.smaract.smaract import SmarAct, get_controller_locators


class DAQ_Move_SmarActMCS(DAQ_Move_base):
    """
    This plugin supports only SmarAct LINEAR positionners (SLC type), with
    enabled sensors attached to them.
    We suppose to have one (or multiple) MCS controllers connected. With 3
    channels (each).
    We suppose that the configuration of the controllers (sensor type etc) has
    been done via the SmarAct MCS Configuration software.
    Tested with one SLC-1740-S (closed loop with nanometer precision sensor)
    connected via a MCS-3S-EP-SDS15-TAB (sensor module) to a MCS-3D (or MCS-3C)
    controller on Windows 7.
    """
    _controller_units = "µm"
    _epsilon = 0.002
    # find controller locators
    controller_locators = get_controller_locators()

    is_multiaxes = True
    # we suppose to have a MCS controller with 3 channels (like the MCS-3D).
    axes_names= {'Axis 1': 0, 'Axis 2': 1, 'Axis 3': 2}
    # bounds corresponding to the SLC-24180
    min_bound = -61500  # µm
    max_bound = +61500  # µm
    offset = 0  # µm

    params = [
        {
            "title": "group parameter:",
            "name": "group_parameter",
            "type": "group",
            "children": [
                {
                    "title": "Controller Name:",
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
    ] + comon_parameters_fun(is_multiaxes, axes_names, epsilon=_epsilon)
    ##########################################################

    def ini_attributes(self):
        self.controller: SmarAct = None

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
        self.controller = self.ini_stage_init(controller, SmarAct())

        if self.settings.child('multiaxes', 'multi_status').value() == "Master":
            self.controller.init_communication(
                    self.settings["group_parameter", "controller_locator"])
        # min and max bounds will depend on which positionner is plugged.
        # Anyway the bounds are secured by the library functions.
        self.settings.child("bounds", "is_bounds").setValue(True)
        self.settings.child("bounds", "min_bound").setValue(self.min_bound)
        self.settings.child("bounds", "max_bound").setValue(self.max_bound)
        self.settings.child("scaling", "use_scaling").setValue(True)
        self.settings.child("scaling", "offset").setValue(self.offset)
        info = ''
        initialized = True

        return info, initialized

    def close(self):
        """Close the communication with the SmarAct controller.
        """
        self.controller.close_communication()
        self.controller = None

    def get_actuator_value(self):
        """Get the current position from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        position = self.controller.get_position(self.settings["multiaxes", "axis"])

        # the position given by the controller is in nanometers, we convert in
        # micrometers
        position = float(position) / 1e3

        # convert position if scaling options have been used, mandatory here
        position = self.get_position_with_scaling(position)
        self.current_position = position
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

        # we convert position in nm
        position = int(position * 1e3)

        # the SmarAct controller asks for nanometers
        self.controller.absolute_move(self.settings["multiaxes", "axis"], position)

    def move_rel(self, position):
        """Move to a relative position

        Parameters
        ----------
        position: float
        """
        # limit position if bounds options has been selected and if position is
        # out of them
        position = (
            self.check_bound(self.current_position + position)
            - self.current_position)
        self.target_position = position + self.current_position
        # convert the user set position to the controller position if scaling
        # has been activated by user
        position = self.set_position_with_scaling(position)

        # we convert position in nm
        position = int(position * 1e3)

        # the SmarAct controller asks for nanometers
        self.controller.relative_move(self.settings["multiaxes", "axis"], position)

    def move_home(self):
        """Move to home and reset position to zero.
        """

        self.controller.find_reference(self.settings["multiaxes", "axis"])

    def stop_motion(self):
        """
        See Also
        --------
        DAQ_Move_base.move_done
        """

        self.controller.stop(self.settings["multiaxes", "axis"])

        self.move_done()


if __name__ == "__main__":
    main(__file__, init=True)
