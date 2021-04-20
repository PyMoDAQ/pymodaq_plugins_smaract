from pymodaq.daq_move.utility_classes import DAQ_Move_base  # base class
from pymodaq.daq_move.utility_classes import comon_parameters  # common set of
# parameters for all actuators
from pymodaq.daq_utils.daq_utils import ThreadCommand, getLineInfo  # object
# used to send info back to the main thread
from easydict import EasyDict as edict  # type of dict
from ..hardware.smaract.smaract_MCS2_wrapper import SmarActMCS2Wrapper
from ..hardware.smaract.smaract_MCS2_wrapper import get_controller_locators

"""This plugin handles SmarAct MCS2 controller with LINEAR positioners with the
    S option (which means that an encoder is present and give a feedback on the
    current position).
    If you use the first version of MCS controller use the daq_move_SmarActMCS
    plugin.
    The SmarAct MCS2 installer should be executed for this plugin to work.
    We suppose that the configuration of the controller and the positioners
    (sensor type…) has been done via the SmarAct MCS2ServiceTool software.

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
    stage_names = [0, 1, 2]  # be careful that the channel index starts at 0
    # and not at 1 has is done in MCS2ServiceTool
    min_bound = -61500  # µm
    max_bound = +61500  # µm
    # bounds corresponding to the SLC-24180
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
                      'values': controller_locators},
                  ]},
                 # parameters not specific to the plugin ######################
                 {'title': 'MultiAxes:',
                  'name': 'multiaxes',
                  'type': 'group',
                  'visible': is_multiaxes,
                  'children': [
                     {'title': 'is Multiaxes:',
                      'name': 'ismultiaxes',
                      'type': 'bool',
                      'value': is_multiaxes,
                      'default': False},
                     {'title': 'Status:',
                      'name': 'multi_status',
                      'type': 'list',
                      'value': 'Master',
                      'values': ['Master', 'Slave']},
                     {'title': 'Axis:',
                      'name': 'axis',
                      'type': 'list',
                      'values': stage_names},
                  ]}
                 ##############################################################
             ] + comon_parameters

    def __init__(self, parent=None, params_state=None):
        """Initialize the the class

        Parameters
        ----------
        parent (caller object of this plugin): see DAQ_Move_main.DAQ_Move_stage
        params_state (list of dicts): saved state of the plugins parameters
            list
        """
        super().__init__(parent, params_state)
        self.controller = None
        self.settings.child('epsilon').setValue(0.005)  # this means that we
        # tolerate an error of 5 nanometers on the target position

    def check_position(self):
        """Get the current position from the hardware with scaling conversion.

        Returns
        -------
        float: The position obtained after scaling conversion.
        """
        position = self.controller.get_position(
            self.settings.child('multiaxes', 'axis').value()
        )
        position = float(position) / 1e6  # the position given by the
        # controller is in picometers, we convert in micrometers
        position = self.get_position_with_scaling(position)  # convert position
        # if scaling options have been used, mandatory here

        self.current_position = position

        self.emit_status(ThreadCommand('check_position', [position]))
        return position

    def close(self):
        """Close the communication with the MCS2 controller.
        """
        self.controller.close_communication()
        self.controller = None

    def commit_settings(self, param):
        """
            | Activate any parameter changes on the hardware.
            |
            | Called after a param_tree_changed signal from DAQ_Move_main.

        ## TODO for your custom plugin
        if param.name() == "a_parameter_you've_added_in_self.params":
           self.controller.your_method_to_apply_this_param_change()
        elif ...
        ##
        """

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
            # initialize the stage and its controller status
            # controller is an object that may be passed to other instances of
            # DAQ_Move_Mock in case of one controller controlling
            # multiactuators (or detector)

            self.status.update(edict(
                info="", controller=None, initialized=False
            ))

            # check whether this stage is controlled by a multiaxe controller
            # (to be defined for each plugin)
            # if multiaxes then init the controller here if Master state
            # otherwise use external controller
            if self.settings.child('multiaxes',
                                   'ismultiaxes').value() \
                    and self.settings.child('multiaxes',
                                   'multi_status').value() == "Slave":
                if controller is None:
                    raise Exception('No controller has been defined externally'
                                    ' while this axe is a slave one')
                else:
                    self.controller = controller
            else:  # Master stage
                self.controller = SmarActMCS2Wrapper()
                self.controller.init_communication(
                    self.settings.child('group_parameter',
                                        'controller_locator').value())

            # min and max bounds will depend on which positionner is plugged.
            # Anyway the bounds are secured by the library functions.
            self.settings.child('bounds', 'is_bounds').setValue(True)
            self.settings.child('bounds', 'min_bound').setValue(self.min_bound)
            self.settings.child('bounds', 'max_bound').setValue(self.max_bound)
            self.settings.child('scaling', 'use_scaling').setValue(True)
            self.settings.child('scaling', 'offset').setValue(self.offset)

            self.status.info = "Stage initialized !"
            self.status.controller = self.controller
            self.status.initialized = True
            return self.status

        except Exception as e:
            self.emit_status(ThreadCommand('Update_Status',
                                           [getLineInfo() + str(e), 'log']))
            self.status.info = getLineInfo() + str(e)
            self.status.initialized = False
            return self.status

    def move_Abs(self, position):
        """ Move the actuator to the absolute target defined by position

        Parameters
        ----------
        position: (float) value of the absolute target positioning
        """

        position = self.check_bound(position)  # if user checked bounds,
        # the defined bounds are applied here
        position = self.set_position_with_scaling(position)  # apply scaling if
        # the user specified one

        position = int(position*1e6)  # convert position in picometers
        self.controller.absolute_move(
            self.settings.child('multiaxes', 'axis').value(), position)

        self.target_position = position
        self.poll_moving()  # start a loop to poll the current actuator value
        # and compare it with target position
        print(self.current_position)

    def move_Rel(self, position):
        """ Move the actuator to the relative target actuator value defined by
        position

        Parameters
        ----------
        position: (float) value of the relative distance to travel in
            micrometers
        """
        position = (self.check_bound(self.current_position+ position)
                    - self.current_position)
        self.target_position = position + self.current_position

        position = int(position*1e6)  # convert position in picometers
        self.controller.relative_move(
            self.settings.child('multiaxes', 'axis').value(), position)

        self.poll_moving()

    def move_Home(self):
        """Move to the physical reference and reset position to 0
        """
        self.controller.find_reference(
            self.settings.child('multiaxes', 'axis').value())
        self.emit_status(ThreadCommand('Update_Status',
                                       ['The positioner has been referenced']))

    def stop_motion(self):
        """Stop the current motion even if the target has not been reached
        """
        self.controller.stop(self.settings.child('multiaxes', 'axis').value())
        self.emit_status(ThreadCommand('Update_Status',
                                       ['The positioner has been stopped']))
        self.move_done()  # to let the interface know the actuator stopped

