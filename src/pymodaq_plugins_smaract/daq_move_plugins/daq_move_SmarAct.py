from pymodaq.daq_move.utility_classes import DAQ_Move_base, main
from pymodaq.daq_move.utility_classes import comon_parameters
from pymodaq.daq_utils.daq_utils import ThreadCommand
from easydict import EasyDict as edict
from instrumental import instrument, Q_, list_instruments

psets = list_instruments(module='motion._smaract')

psets_str = [f"Dev. Id{pset['id']} channel {pset['index']}" for pset in psets]



class DAQ_Move_SmarAct(DAQ_Move_base):
    """

    """
    _controller_units = ""

    # find controller locators


    is_multiaxes = False
    stage_names = []

    params = [
                 {'title': 'Device', 'name': 'device', 'type': 'list', 'limits': psets_str},
                 {'title': 'Frequency (Hz)', 'name': 'frequency', 'type': 'int', 'value': 450},
                 {'title': 'Amplitude (V)', 'name': 'amplitude', 'type': 'int', 'value': 100},
                 {'title': 'Max Frequency (Hz)', 'name': 'maxfreq', 'type': 'int', 'value': 18500},

        ##########################################################
        # the ones below should ALWAYS be present!!!
        {"title": "MultiAxes:", "name": "multiaxes", "type": "group", "visible": is_multiaxes, "children": [
            {"title": "is Multiaxes:", "name": "ismultiaxes", "type": "bool", "value": is_multiaxes},
            {"title": "Status:", "name": "multi_status", "type": "list", "value": "Master",
             "limits": ["Master", "Slave"],},
            {"title": "Axis:", "name": "axis", "type": "list", "limits": stage_names},
            ],},
    ] + comon_parameters
    ##########################################################

    def __init__(self, parent=None, params_state=None):
        super().__init__(parent, params_state)

        self.controller = None
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

        Parameters
        ----------
        controller (object): custom object of a PyMoDAQ plugin (Slave case).
            None if only one actuator by controller (Master case)

        Returns
        -------
        self.status: (edict) with initialization status: three fields:
            * info: (str)
            * controller: (object) initialized controller
            * initialized: (bool) False if initialization failed otherwise
                True
        """
        try:

            self.status.update(edict(
                info="", controller=None, initialized=False))

            # check whether this stage is controlled by a multiaxe controller
            # (to be defined for each plugin)
            # if multiaxes then init the controller here if Master state
            # otherwise use external controller
            if self.settings.child('multiaxes', 'ismultiaxes').value() \
                    and self.settings.child('multiaxes', 'multi_status').value() == "Slave":
                if controller is None:
                    raise Exception('No controller has been defined externally'
                                    ' while this axe is a slave one')
                else:
                    self.controller = controller
            else:  # Master stage
                index = self.settings.child('device').opts['limits'].index(self.settings.child('device').value())
                self.controller = instrument(psets[index])
                self.settings.child('units').setValue(self.controller.units)
                self.settings.child('amplitude').setOpts(limits=list(self.controller.amplitude_limits.m_as('V')))
                self.settings.child('frequency').setOpts(limits=list(self.controller.frequency_limits.m_as('Hz')))
                self.settings.child('amplitude').setValue(self.controller.amplitude.m_as('V'))
                self.settings.child('frequency').setValue(self.controller.frequency.m_as('Hz'))
                self.settings.child('maxfreq').setValue(self.controller.max_frequency.m_as('Hz'))

            self.status.controller = self.controller
            self.status.initialized = True

            return self.status

        except Exception as e:
            self.emit_status(ThreadCommand("Update_Status", [str(e), "log"]))
            self.status.info = str(e)
            self.status.initialized = False

            return self.status

    def close(self):
        """Close the communication with the SmarAct controller.
        """

        self.controller.close()
        self.controller = None

    def check_position(self):
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

    def move_Abs(self, position):
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


    def move_Rel(self, position):
        """Move to a relative position

        Parameters
        ----------
        position: float
        """
        position = (self.check_bound(self.current_position + position) - self.current_position)
        self.target_position = position + self.current_position
        position = self.set_position_relative_with_scaling(position)

        self.controller.move_to(Q_(position, self.settings['units']), 'rel')


    def move_Home(self):
        """Move to home and reset position to zero.
        """
        self.controller.move_home()
        self.check_position()

    def stop_motion(self):
        """
        """
        self.controller.stop()
        self.move_done()


if __name__ == "__main__":
    main(__file__)
