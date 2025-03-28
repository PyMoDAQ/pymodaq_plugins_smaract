import time
from typing import Optional, List

from pathlib import Path
import os



from pymodaq_plugins_smaract.hardware.smaract.scu import bindings


def get_devices():
    """
    Get devices ids and informations about them

    Returns
    -------
    list(int)
    list(SCUWrapper or SCULinear or SCURotation)
    """
    ids = bindings.GetAvailableDevices()
    ##ids = [ids]
    bindings.InitDevices(configuration=bindings.SYNCHRONOUS_COMMUNICATION)
    ptype = []

    for ind in enumerate(ids):
        rotation = False
        ind_channel = 0
        sensor = False

        while True:
            try:
                bindings.GetStatus_S(ids, ind_channel)
            except bindings.Error as e:
                # will fire an error if the ind_channel is invalid
                break
            try:
                sensor = bool(bindings.GetSensorPresent_S(ind, ind_channel))
            except bindings.Error as e:
                sensor = False
            if sensor:
                try:
                    bindings.GetAngle_S(ind,ind_channel)
                    rotation = True
                except bindings.Error:
                    rotation = False
            ind_channel += 1

        for ind_channel in range(ind_channel):
            ptype.append(SCUWrapper if not sensor else SCURotation if rotation else SCULinear)

    bindings.ReleaseDevices()

    return ids, ptype



class SCUWrapper:

    dev_type = 'stepper'
    units = 'steps'

    amplitude_limits = (150, 1001)
    frequency_limits = (1, 18501)
    steps_limits = (-30000, 30001)
    angle_limits = (-3599999, 3599999)


    def __init__(self):

        self.device_index: Optional[int] = None
        self.channel_index = 0
        self.hold_time = 10
        self._amplitude = 400    #between 150 and 1000
        self._frequency = 15000  #between 1 and 18500
        self._steps = 20000      #between -30000 and 30000



    @property
    def amplitude (self):
        """
        The amplitude should be defined in Volts, between 15V and 100V
        """
        return self._amplitude

    @amplitude.setter
    def amplitude(self, number : int):
        if isinstance(number, int) and 100 > number > 15 :
            self._amplitude = number * 10
            bindings.SetAmplitude_S(self.device_index, self.channel_index, self._amplitude)


    @property
    def frequency(self):
        """
        The frequency should be defined in Hertz, between 1Hz and 18500Hz
        """
        return self._frequency

    @frequency.setter
    def frequency(self, number: int):
        if isinstance(number, int) and 18500 > number > 1:
            self._frequency = number

    @property
    def steps(self):
        """
        The steps should be between -30000 and 30000
        """
        return self._steps

    @steps.setter
    def steps(self, number: int):
        if isinstance(number, int) and 30000 > number > -30000:
            self._steps = number
        else:
            self._steps=0


    def init_device (self, configuration=bindings.SYNCHRONOUS_COMMUNICATION) :
        bindings.InitDevices(configuration)


    def open(self, device_index: int, configuration=bindings.SYNCHRONOUS_COMMUNICATION) -> bool:
        config = configuration.value
        self.device_index = device_index
        try:
            error = bindings.InitDevices(config)
            return True
        except bindings.Error as e:
            print(str(e))
            return False

    def close(self):
        bindings.ReleaseDevices()

    def get_position(self) -> float:
        """
            Returns the current position of a positioner

            Parameters:
             - deviceIndex: Selects the device (zero-based)
             - channelIndex: Selects the channel (zero-based)

            Return value(s):
             - position: Buffer for the current position given in 1/10th micro
            meters
        """

        position = bindings.GetPosition_S(self.device_index, self.channel_index)

        return float(position / 10)

    def get_angle(self) -> float:
        """
            Returns the current angle of a positioner

            Parameters:
             - deviceIndex: Selects the device (zero-based)
             - channelIndex: Selects the channel (zero-based)

            Return value(s):
             - angle: Buffer for the current angle given in 1/10th milli degrees
             - revolution: Reserved for future use
            """
        angle = bindings.GetAngle_S(self.device_index, self.channel_index)
        return float(angle / 10)


    def move_home(self):
        """
            Starts the referencing procedure and moves the positioner to a known
            physical position

            Parameters:
             - deviceIndex: Selects the device (zero-based)
             - channelIndex: Selects the channel (zero-based)
             - holdTime: Time (in milliseconds) the position/angle is actively held
             after reaching the target
             - autoZero: Selects whether the current position is set to zero upon
            reaching the reference position
        """
        bindings.MoveToReference_S(self.device_index, self.channel_index, self.hold_time, autoZero=bindings.AUTO_ZERO)



    def amp(self):
        """
        Presets the target channel's amplitude

        Parameters:
         - deviceIndex: Selects the device (zero-based)
         - channelIndex: Selects the channel (zero-based)
         - amplitude: Amplitude in 1/10th Volts that should be preset
        """
        amplitude = self._amplitude
        bindings.SetAmplitude_S(self.device_index, self.channel_index, amplitude)


    def steps_move(self):
        """
        Performs a burst of steps with the given parameters

        Parameters:
         - deviceIndex: Selects the device (zero-based)
         - channelIndex: Selects the channel (zero-based)
         - steps: Number and direction of steps to perform
         - amplitude: Amplitude in 1/10th Volts that the steps are performed
        with
         - frequency: Frequency in Hz that the steps are performed with
        """
        amplitude = int(self.amplitude)
        bindings.MoveStep_S(self.device_index, self.channel_index, self._steps, amplitude, self._frequency)


    def stop(self):
        """Stop any ongoing movement of the positionner. This command also
            stops the hold position feature of closed-loop commands.

        Parameters
        ----------
        self.channel_index: unsigned int
        """

        bindings.Stop_S(self.device_index, self.channel_index)

class SCULinear(SCUWrapper):

    units ="µm"


    def move_rel(self, relative_move_value):
        """Execute a relative move in microns.
            If a mechanical end stop is detected while the command is in
            execution, the movement will be aborted (without notice).

        Parameters
        ----------
        self.channel_index: unsigned int
        relative_move_value: signed int. Relative distance in picometer.
        """

        diff = 10
        bindings.MovePositionRelative_S(self.device_index, self.channel_index,diff, self.hold_time)


    def move_abs(self, absolute_move_micron):
        """Go to an absolute position in microns.
            If a mechanical end stop is detected while the command is in
            execution, the movement will be aborted (without notice).

        Parameters
        ----------
        self.channel_index: unsigned int
        absolute_move_micron: float
            Absolute position in microns
        """
        position = int(absolute_move_micron * 10)
        bindings.MovePositionAbsolute_S(self.device_index, self.channel_index, position, self.hold_time)

class SCURotation(SCUWrapper):

    units = "milli deg"

    def move_abs_rot(self,absolute_move_degrees):
        """
            Instructs a positioner to move to a specific angle using closed-loop
            control

            Parameters:
             - deviceIndex: Selects the device (zero-based)
             - channelIndex: Selects the channel (zero-based)
             - angle: Absolute angle to move to in 1/10th milli degrees
             - revolution: Reserved for future use
             - holdTime: Time (in milliseconds) the angle is actively held after
            reaching the target
            """
        angle = int(absolute_move_degrees * 10)
        revolution = 0
        bindings.MoveAngleAbsolute_S(self.device_index, self.channel_index, angle, revolution, self.hold_time)

    def move_rel_rot(self, rel_move_degrees):
        """
            Instructs a positioner to move to an angle relative to its current
            angle using closed-loop control

            Parameters:
             - deviceIndex: Selects the device (zero-based)
             - channelIndex: Selects the channel (zero-based)
             - angleDiff: Relative angle difference to move in 1/10th milli degrees

             - revolutionDiff: Reserved for future use
             - holdTime: Time (in milliseconds) the angle is actively held after
            reaching the target
            """
        angle = int(rel_move_degrees * 10)
        revolution=0
        bindings.MoveAngleRelative_S(self.device_index, self.channel_index, angle, revolution, self.hold_time)





if __name__ == '__main__':


    ids = get_devices()

    wrapper = SCULinear()

    connect_to = 722998302
    device_index = ids.index(connect_to)

    wrapper.open(device_index)
    try:
        #channel = wrapper.get_number_of_channels()

        wrapper.move_home()

        time.sleep(2)

        #wrapper.absolute_move(1500)

        print(wrapper.get_position())


    except Exception as e:
        print(e)
    finally:
        wrapper.close()



