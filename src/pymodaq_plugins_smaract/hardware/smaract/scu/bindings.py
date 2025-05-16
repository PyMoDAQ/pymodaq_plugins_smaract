#######################################################################
# Copyright (c) 2023 SmarAct GmbH
#
# THIS  SOFTWARE, DOCUMENTS, FILES AND INFORMATION ARE PROVIDED 'AS IS'
# WITHOUT WARRANTY OF ANY KIND, EITHER EXPRESSED OR IMPLIED, INCLUDING,
# BUT  NOT  LIMITED  TO, THE  IMPLIED  WARRANTIES  OF MERCHANTABILITY,
# FITNESS FOR A PURPOSE, OR THE WARRANTY OF NON - INFRINGEMENT.
# THE  ENTIRE  RISK  ARISING OUT OF USE OR PERFORMANCE OF THIS SOFTWARE
# REMAINS WITH YOU.
# IN  NO  EVENT  SHALL  THE  SMARACT  GMBH  BE  LIABLE  FOR ANY DIRECT,
# INDIRECT, SPECIAL, INCIDENTAL, CONSEQUENTIAL OR OTHER DAMAGES ARISING
# OUT OF THE USE OR INABILITY TO USE THIS SOFTWARE.
#
# Generated on 2023-12-22 08:28 +0100
#

"""
Python bindings for SCU3DControl
(C) SmarAct GmbH
Refer to the SmarAct EULA for licensing
SCU Python API
"""

from cffi import FFI
import enum
import sys

assert sys.version_info >= (3, 4), "Python v3.4 or higher is required"
apigen_version = (1, 8, 1)
api_version = (1, 5, 16)


def __initBindings(libName):
    global ffi, lib
    ffi = FFI()
    ffi.cdef("""
typedef unsigned int SA_PACKET_TYPE;
typedef unsigned int SA_INDEX;
struct SA_packet{ SA_PACKET_TYPE packetType; SA_INDEX channelIndex; unsigned int data1; int data2; int data3;};
typedef struct SA_packet SA_PACKET;
typedef unsigned int SA_STATUS;
SA_STATUS SA_GetDLLVersion(unsigned int *version);
SA_STATUS SA_GetAvailableDevices(unsigned int *idList, unsigned int *idListSize);
SA_STATUS SA_AddDeviceToInitDevicesList(unsigned int deviceId);
SA_STATUS SA_ClearInitDevicesList();
SA_STATUS SA_InitDevices(unsigned int configuration);
SA_STATUS SA_ReleaseDevices();
SA_STATUS SA_GetNumberOfDevices(unsigned int *number);
SA_STATUS SA_GetDeviceID(SA_INDEX deviceIndex, unsigned int *deviceId);
SA_STATUS SA_GetDeviceFirmwareVersion(SA_INDEX deviceIndex, unsigned int *version);
SA_STATUS SA_SetClosedLoopMaxFrequency_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int frequency);
SA_STATUS SA_GetClosedLoopMaxFrequency_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int *frequency);
SA_STATUS SA_SetZero_S(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_GetSensorPresent_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int *present);
SA_STATUS SA_SetSensorType_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int type);
SA_STATUS SA_GetSensorType_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int *type);
SA_STATUS SA_SetPositionerAlignment_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int alignment, unsigned int forwardAmplitude, unsigned int backwardAmplitude);
SA_STATUS SA_GetPositionerAlignment_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int *alignment, unsigned int *forwardAmplitude, unsigned int *backwardAmplitude);
SA_STATUS SA_SetSafeDirection_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int direction);
SA_STATUS SA_GetSafeDirection_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int *direction);
SA_STATUS SA_SetScale_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int scale, unsigned int inverted);
SA_STATUS SA_GetScale_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int *scale, unsigned int *inverted);
SA_STATUS SA_SetChannelProperty_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int key, int value);
SA_STATUS SA_GetChannelProperty_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int key, int *value);
SA_STATUS SA_SetSystemProperty_S(SA_INDEX deviceIndex, int key, int value);
SA_STATUS SA_GetSystemProperty_S(SA_INDEX deviceIndex, int key, int *value);
SA_STATUS SA_MoveStep_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int steps, unsigned int amplitude, unsigned int frequency);
SA_STATUS SA_SetAmplitude_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int amplitude);
SA_STATUS SA_MovePositionAbsolute_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int position, unsigned int holdTime);
SA_STATUS SA_MovePositionRelative_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int diff, unsigned int holdTime);
SA_STATUS SA_MoveAngleAbsolute_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int angle, int revolution, unsigned int holdTime);
SA_STATUS SA_MoveAngleRelative_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int angleDiff, int revolutionDiff, unsigned int holdTime);
SA_STATUS SA_CalibrateSensor_S(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_MoveToReference_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int holdTime, unsigned int autoZero);
SA_STATUS SA_MoveToEndStop_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int direction, unsigned int holdTime, unsigned int autoZero);
SA_STATUS SA_Stop_S(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_GetStatus_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int *status);
SA_STATUS SA_GetAmplitude_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int *amplitude);
SA_STATUS SA_GetPosition_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int *position);
SA_STATUS SA_GetAngle_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, int *angle, int *revolution);
SA_STATUS SA_GetPhysicalPositionKnown_S(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int *known);
SA_STATUS SA_SetClosedLoopMaxFrequency_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int frequency);
SA_STATUS SA_GetClosedLoopMaxFrequency_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_SetZero_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_GetSensorPresent_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_SetSensorType_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int type);
SA_STATUS SA_GetSensorType_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_SetPositionerAlignment_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int alignment, unsigned int forwardAmplitude, unsigned int backwardAmplitude);
SA_STATUS SA_GetPositionerAlignment_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_SetSafeDirection_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int direction);
SA_STATUS SA_GetSafeDirection_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_SetScale_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, int scale, unsigned int inverted);
SA_STATUS SA_GetScale_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_SetReportOnComplete_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int report);
SA_STATUS SA_SetChannelProperty_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, int key, int value);
SA_STATUS SA_GetChannelProperty_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, int key);
SA_STATUS SA_SetSystemProperty_A(SA_INDEX deviceIndex, int key, int value);
SA_STATUS SA_GetSystemProperty_A(SA_INDEX deviceIndex, int key);
SA_STATUS SA_MoveStep_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, int steps, unsigned int amplitude, unsigned int frequency);
SA_STATUS SA_SetAmplitude_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int amplitude);
SA_STATUS SA_MovePositionAbsolute_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, int position, unsigned int holdTime);
SA_STATUS SA_MovePositionRelative_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, int diff, unsigned int holdTime);
SA_STATUS SA_MoveAngleAbsolute_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, int angle, int revolution, unsigned int holdTime);
SA_STATUS SA_MoveAngleRelative_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, int angleDiff, int revolutionDiff, unsigned int holdTime);
SA_STATUS SA_CalibrateSensor_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_MoveToReference_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int holdTime, unsigned int autoZero);
SA_STATUS SA_MoveToEndStop_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int direction, unsigned int holdTime, unsigned int autoZero);
SA_STATUS SA_Stop_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_GetStatus_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_GetAmplitude_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_GetPosition_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_GetAngle_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_GetPhysicalPositionKnown_A(SA_INDEX deviceIndex, SA_INDEX channelIndex);
SA_STATUS SA_SetReceiveNotification_A(SA_INDEX deviceIndex, void *event);
SA_STATUS SA_ReceiveNextPacket_A(SA_INDEX deviceIndex, unsigned int timeout, SA_PACKET *packet);
SA_STATUS SA_ReceiveNextPacketIfChannel_A(SA_INDEX deviceIndex, SA_INDEX channelIndex, unsigned int timeout, SA_PACKET *packet);
SA_STATUS SA_LookAtNextPacket_A(SA_INDEX deviceIndex, unsigned int timeout, SA_PACKET *packet);
SA_STATUS SA_DiscardPacket_A(SA_INDEX deviceIndex);
""")
    lib = ffi.dlopen(libName)


class Error(Exception):
    def __init__(self, func, code, arguments):
        self.func = func
        self.code = code
        self.arguments = arguments

    def __str__(self):
        return "{} returned {} with arguments {}".format(self.func, self.code, self.arguments)


class packet:
    """
    Members:
     - packetType
     - channelIndex
     - data1
     - data2
     - data3

    """
    __slots__ = ['packetType', 'channelIndex', 'data1', 'data2', 'data3', 'cHandle']

    def __init__(self, packetType, channelIndex, data1, data2, data3, cHandle=None):
        if packetType is not None:
            self.packetType = packetType
        if channelIndex is not None:
            self.channelIndex = channelIndex
        if data1 is not None:
            self.data1 = data1
        if data2 is not None:
            self.data2 = data2
        if data3 is not None:
            self.data3 = data3
        self.cHandle = cHandle

    def __getattr__(self, attr):
        if self.cHandle is not None:
            value = getattr(self.cHandle, attr)
            retValue = value
            setattr(self, attr, retValue)
            return retValue
        else:
            raise AttributeError(f"packet has no attribute: {attr}")

    def asFFI(self):
        return ffi.new(_ffiApiGenCachedTypes[0],
                       {'packetType': self.packetType, 'channelIndex': self.channelIndex, 'data1': self.data1,
                        'data2': self.data2, 'data3': self.data3})


def GetDLLVersion():
    """
    Returns the version code of the library

    Return value(s):
     - version: Library Version
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetDLLVersion(local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetDLLVersion", local_1, {})
    return local_0[0]


def GetAvailableDevices(idListSize=256):
    """
    Returns a list of available device IDs

    Parameters:
     - idListSize = 256: Length of the buffer to allocate

    Return value(s):
     - idList: Buffer for device IDs
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[2], idListSize)
    local_1 = ffi.new(_ffiApiGenCachedTypes[1], idListSize)
    local_2 = lib.SA_GetAvailableDevices(local_0, local_1)
    if local_2 != ErrorCode.OK.value:
        raise Error("GetAvailableDevices", local_2, {})
    return ffi.unpack(local_0, local_1[0])


def AddDeviceToInitDevicesList(deviceId):
    """
    Used to acquire one or more specific devices

    Parameters:
     - deviceId: ID that is to be acquired
    """
    local_0 = lib.SA_AddDeviceToInitDevicesList(deviceId)
    if local_0 != ErrorCode.OK.value:
        raise Error("AddDeviceToInitDevicesList", local_0, {"deviceId": deviceId})


def ClearInitDevicesList():
    """
    Clears the device initialization list
    """
    local_0 = lib.SA_ClearInitDevicesList()
    if local_0 != ErrorCode.OK.value:
        raise Error("ClearInitDevicesList", local_0, {})


def InitDevices(configuration):
    """
    Global initialization function to acquire all devices available in the
    DevicesList

    Parameters:
     - configuration: Selection between synchronous and asynchronous
    communication mode
    """
    local_0 = lib.SA_InitDevices(configuration)
    if local_0 != ErrorCode.OK.value:
        raise Error("InitDevices", local_0, {"configuration": configuration})


def ReleaseDevices():
    """
    Release all previously acquired devices (should be called before the
    application closes)
    """
    local_0 = lib.SA_ReleaseDevices()
    if local_0 != ErrorCode.OK.value:
        raise Error("ReleaseDevices", local_0, {})


def GetNumberOfDevices():
    """
    Returns number of devices that that have been acquired by
    SA_InitDevices

    Return value(s):
     - number: Buffer for number of acquired devices
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetNumberOfDevices(local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetNumberOfDevices", local_1, {})
    return local_0[0]


def GetDeviceID(deviceIndex):
    """
    Returns the ID of an acquired device

    Parameters:
     - deviceIndex: Selects the device (zero-based)

    Return value(s):
     - deviceId: Buffer for the corresponding device ID
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetDeviceID(deviceIndex, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetDeviceID", local_1, {"deviceIndex": deviceIndex})
    return local_0[0]


def GetDeviceFirmwareVersion(deviceIndex):
    """
    Returns the firmware version of a device

    Parameters:
     - deviceIndex: Selects the device (zero-based)

    Return value(s):
     - version: Buffer for the device's firmware version
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetDeviceFirmwareVersion(deviceIndex, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetDeviceFirmwareVersion", local_1, {"deviceIndex": deviceIndex})
    return local_0[0]


def SetClosedLoopMaxFrequency_S(deviceIndex, channelIndex, frequency):
    """
    Defines the maximum frequency used for closed-loop movements

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - frequency: Maximum driving frequency in Hz
    """
    local_0 = lib.SA_SetClosedLoopMaxFrequency_S(deviceIndex, channelIndex, frequency)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetClosedLoopMaxFrequency_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "frequency": frequency})


def GetClosedLoopMaxFrequency_S(deviceIndex, channelIndex):
    """
    Returns the currently configured maximum frequency used for closed-loop
     movements

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)

    Return value(s):
     - frequency: Buffer for the maximum driving frequency in Hz
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetClosedLoopMaxFrequency_S(deviceIndex, channelIndex, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetClosedLoopMaxFrequency_S", local_1, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})
    return local_0[0]


def SetZero_S(deviceIndex, channelIndex):
    """
    Defines the current position as the zero position

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_SetZero_S(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetZero_S", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def GetSensorPresent_S(deviceIndex, channelIndex):
    """
    Returns whether a positioner is equipped with a sensor or not

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)

    Return value(s):
     - present: Buffer for the information whether a sensor is available
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetSensorPresent_S(deviceIndex, channelIndex, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetSensorPresent_S", local_1, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})
    return local_0[0]


def SetSensorType_S(deviceIndex, channelIndex, type):
    """
    Configures the type of positioner connected to a channel

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - type: Type of the positioner
    """
    local_0 = lib.SA_SetSensorType_S(deviceIndex, channelIndex, type)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetSensorType_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "type": type})


def GetSensorType_S(deviceIndex, channelIndex):
    """
    Returns the type of positioner for the given channel

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)

    Return value(s):
     - type: Buffer for the currently configured positioner type
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetSensorType_S(deviceIndex, channelIndex, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetSensorType_S", local_1, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})
    return local_0[0]


def SetPositionerAlignment_S(deviceIndex, channelIndex, alignment, forwardAmplitude=0, backwardAmplitude=0):
    """
    Sets advanced properties for vertically aligned positioners that carry
    high loads

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - alignment: Specifies the alignment (horizontal or vertical)
     - forwardAmplitude = 0: Step amplitude used for forward movements in
    vertical mode
     - backwardAmplitude = 0: Step amplitude used for backward movements in
     vertical mode
    """
    local_0 = lib.SA_SetPositionerAlignment_S(deviceIndex, channelIndex, alignment, forwardAmplitude, backwardAmplitude)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetPositionerAlignment_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "alignment": alignment,
                     "forwardAmplitude": forwardAmplitude, "backwardAmplitude": backwardAmplitude})


def GetPositionerAlignment_S(deviceIndex, channelIndex, alignment):
    """
    Returns current alignment settings

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - alignment

    Return value(s):
     - forwardAmplitude: Buffer for the currently configured step amplitude
     used for forward movements in vertical mode
     - backwardAmplitude: Buffer for the currently configured step
    amplitude used for backward movements in vertical mode
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = ffi.new(_ffiApiGenCachedTypes[1])
    local_2 = lib.SA_GetPositionerAlignment_S(deviceIndex, channelIndex, alignment, local_0, local_1)
    if local_2 != ErrorCode.OK.value:
        raise Error("GetPositionerAlignment_S", local_2,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "alignment": alignment})
    return local_0[0], local_1[0]


def SetSafeDirection_S(deviceIndex, channelIndex, direction):
    """
    Configures the safe direction

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - direction: Specifies the safe direction
    """
    local_0 = lib.SA_SetSafeDirection_S(deviceIndex, channelIndex, direction)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetSafeDirection_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "direction": direction})


def GetSafeDirection_S(deviceIndex, channelIndex, direction):
    """
    Returns the current safe direction

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - direction
    """
    local_0 = lib.SA_GetSafeDirection_S(deviceIndex, channelIndex, direction)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetSafeDirection_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "direction": direction})


def SetScale_S(deviceIndex, channelIndex, scale, inverted):
    """
    Configures the logical scale

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - scale: Scale shift relative to the positioner's physical scale
     - inverted: Scale inversion
    """
    local_0 = lib.SA_SetScale_S(deviceIndex, channelIndex, scale, inverted)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetScale_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "scale": scale, "inverted": inverted})


def GetScale_S(deviceIndex, channelIndex):
    """
    Returns the logical scale configuration

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)

    Return value(s):
     - scale: Buffer for the currently configured scale offset
     - inverted: Buffer for the currently configured scale inversion
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[3])
    local_1 = ffi.new(_ffiApiGenCachedTypes[1])
    local_2 = lib.SA_GetScale_S(deviceIndex, channelIndex, local_0, local_1)
    if local_2 != ErrorCode.OK.value:
        raise Error("GetScale_S", local_2, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})
    return local_0[0], local_1[0]


def SetChannelProperty_S(deviceIndex, channelIndex, key, value):
    """
    Sets a channel specific property depending on the given key

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - key: Target property
     - value: Desired value
    """
    local_0 = lib.SA_SetChannelProperty_S(deviceIndex, channelIndex, key, value)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetChannelProperty_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "key": key, "value": value})


def GetChannelProperty_S(deviceIndex, channelIndex, key):
    """
    Returns a channel specific property depending on the given key

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - key: Target property

    Return value(s):
     - value: Buffer for the property value@
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[3])
    local_1 = lib.SA_GetChannelProperty_S(deviceIndex, channelIndex, key, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetChannelProperty_S", local_1,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "key": key})
    return local_0[0]


def SetSystemProperty_S(deviceIndex, key, value):
    """
    Sets a system specific property depending on the given key

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - key: Target property
     - value: Desired value
    """
    local_0 = lib.SA_SetSystemProperty_S(deviceIndex, key, value)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetSystemProperty_S", local_0, {"deviceIndex": deviceIndex, "key": key, "value": value})


def GetSystemProperty_S(deviceIndex, key):
    """
    Returns a system specific property depending on the given key

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - key: Target property

    Return value(s):
     - value: Buffer for the property value
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[3])
    local_1 = lib.SA_GetSystemProperty_S(deviceIndex, key, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetSystemProperty_S", local_1, {"deviceIndex": deviceIndex, "key": key})
    return local_0[0]


def MoveStep_S(deviceIndex, channelIndex, steps, amplitude, frequency):
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
    local_0 = lib.SA_MoveStep_S(deviceIndex, channelIndex, steps, amplitude, frequency)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveStep_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "steps": steps, "amplitude": amplitude,
                     "frequency": frequency})


def SetAmplitude_S(deviceIndex, channelIndex, amplitude):
    """
    Presets the target channel's amplitude

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - amplitude: Amplitude in 1/10th Volts that should be preset
    """
    local_0 = lib.SA_SetAmplitude_S(deviceIndex, channelIndex, amplitude)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetAmplitude_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "amplitude": amplitude})


def MovePositionAbsolute_S(deviceIndex, channelIndex, position, holdTime):
    """
    Instructs a positioner to move to a specific position using closed-loop
     control

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - position: Absolute position to move to in 1/10th micro meters
     - holdTime: Time (in milliseconds) the position is actively held after
     reaching the target
    """
    local_0 = lib.SA_MovePositionAbsolute_S(deviceIndex, channelIndex, position, holdTime)
    if local_0 != ErrorCode.OK.value:
        raise Error("MovePositionAbsolute_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "position": position,
                     "holdTime": holdTime})


def MovePositionRelative_S(deviceIndex, channelIndex, diff, holdTime):
    """
    Instructs a positioner to move to a position relative to its current
    position using closed-loop control

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - diff: Relative position difference to move in 1/10th micro meters
     - holdTime: Time (in milliseconds) the position is actively held after
     reaching the target
    """
    local_0 = lib.SA_MovePositionRelative_S(deviceIndex, channelIndex, diff, holdTime)
    if local_0 != ErrorCode.OK.value:
        raise Error("MovePositionRelative_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "diff": diff, "holdTime": holdTime})


def MoveAngleAbsolute_S(deviceIndex, channelIndex, angle, revolution, holdTime):
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
    local_0 = lib.SA_MoveAngleAbsolute_S(deviceIndex, channelIndex, angle, revolution, holdTime)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveAngleAbsolute_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "angle": angle, "revolution": revolution,
                     "holdTime": holdTime})


def MoveAngleRelative_S(deviceIndex, channelIndex, angleDiff, revolutionDiff, holdTime):
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
    local_0 = lib.SA_MoveAngleRelative_S(deviceIndex, channelIndex, angleDiff, revolutionDiff, holdTime)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveAngleRelative_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "angleDiff": angleDiff,
                     "revolutionDiff": revolutionDiff, "holdTime": holdTime})


def CalibrateSensor_S(deviceIndex, channelIndex):
    """
    Starts the calibration procedure

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_CalibrateSensor_S(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("CalibrateSensor_S", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def MoveToReference_S(deviceIndex, channelIndex, holdTime, autoZero):
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
    local_0 = lib.SA_MoveToReference_S(deviceIndex, channelIndex, holdTime, autoZero)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveToReference_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "holdTime": holdTime,
                     "autoZero": autoZero})


def MoveToEndStop_S(deviceIndex, channelIndex, direction, holdTime, autoZero):
    """
    Moves the positioner to a mechanical end stop

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - direction: Specifies the movement direction
     - holdTime: Time (in milliseconds) the position/angle is actively held
     after reaching the end stop
     - autoZero: Selects whether the current positions is set to zero upon
    reaching the end stop
    """
    local_0 = lib.SA_MoveToEndStop_S(deviceIndex, channelIndex, direction, holdTime, autoZero)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveToEndStop_S", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "direction": direction,
                     "holdTime": holdTime, "autoZero": autoZero})


def Stop_S(deviceIndex, channelIndex):
    """
    Stops any ongoing movement of a positioner

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_Stop_S(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("Stop_S", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def GetStatus_S(deviceIndex, channelIndex):
    """
    Returns the current movement status of a positioner

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)

    Return value(s):
     - status: Buffer for the current status
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetStatus_S(deviceIndex, channelIndex, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetStatus_S", local_1, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})
    return local_0[0]


def GetAmplitude_S(deviceIndex, channelIndex):
    """
    Returns the currently configured step amplitude

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)

    Return value(s):
     - amplitude: Buffer for the current amplitude
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetAmplitude_S(deviceIndex, channelIndex, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetAmplitude_S", local_1, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})
    return local_0[0]


def GetPosition_S(deviceIndex, channelIndex):
    """
    Returns the current position of a positioner

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)

    Return value(s):
     - position: Buffer for the current position given in 1/10th micro
    meters
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[3])
    local_1 = lib.SA_GetPosition_S(deviceIndex, channelIndex, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetPosition_S", local_1, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})
    return local_0[0]


def GetAngle_S(deviceIndex, channelIndex):
    """
    Returns the current angle of a positioner

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)

    Return value(s):
     - angle: Buffer for the current angle given in 1/10th milli degrees
     - revolution: Reserved for future use
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[3])
    local_1 = ffi.new(_ffiApiGenCachedTypes[3])
    local_2 = lib.SA_GetAngle_S(deviceIndex, channelIndex, local_0, local_1)
    if local_2 != ErrorCode.OK.value:
        raise Error("GetAngle_S", local_2, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})
    return local_0[0], local_1[0]


def GetPhysicalPositionKnown_S(deviceIndex, channelIndex):
    """
    Returns whether the positioner "knows" its physical position (has been
    referenced)

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)

    Return value(s):
     - known: Buffer for the physical position known state
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[1])
    local_1 = lib.SA_GetPhysicalPositionKnown_S(deviceIndex, channelIndex, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("GetPhysicalPositionKnown_S", local_1, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})
    return local_0[0]


def SetClosedLoopMaxFrequency_A(deviceIndex, channelIndex, frequency):
    """
    Defines the maximum frequency used for closed-loop movements

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - frequency: Maximum driving frequency in Hz
    """
    local_0 = lib.SA_SetClosedLoopMaxFrequency_A(deviceIndex, channelIndex, frequency)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetClosedLoopMaxFrequency_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "frequency": frequency})


def GetClosedLoopMaxFrequency_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns the currently configured
    maximum frequency used for closed-loop movements

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetClosedLoopMaxFrequency_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetClosedLoopMaxFrequency_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def SetZero_A(deviceIndex, channelIndex):
    """
    Defines the current position as the zero position

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_SetZero_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetZero_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def GetSensorPresent_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns whether a positioner is
    equipped with a sensor or not

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetSensorPresent_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetSensorPresent_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def SetSensorType_A(deviceIndex, channelIndex, type):
    """
    Configures the type of positioner connected to a channel

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - type: Type of the positioner
    """
    local_0 = lib.SA_SetSensorType_A(deviceIndex, channelIndex, type)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetSensorType_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "type": type})


def GetSensorType_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns the current type of
    positioner

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetSensorType_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetSensorType_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def SetPositionerAlignment_A(deviceIndex, channelIndex, alignment, forwardAmplitude=0, backwardAmplitude=0):
    """
    Sets advanced properties for vertically aligned positioners that carry
    high loads

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - alignment: Specifies the alignment (horizontal or vertical)
     - forwardAmplitude = 0: Step amplitude used for forward movements in
    vertical mode
     - backwardAmplitude = 0: Step amplitude used for backward movements in
     vertical mode
    """
    local_0 = lib.SA_SetPositionerAlignment_A(deviceIndex, channelIndex, alignment, forwardAmplitude, backwardAmplitude)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetPositionerAlignment_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "alignment": alignment,
                     "forwardAmplitude": forwardAmplitude, "backwardAmplitude": backwardAmplitude})


def GetPositionerAlignment_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns the current alignment
    settings

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetPositionerAlignment_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetPositionerAlignment_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def SetSafeDirection_A(deviceIndex, channelIndex, direction):
    """
    Configures the safe direction

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - direction: Specifies the safe direction
    """
    local_0 = lib.SA_SetSafeDirection_A(deviceIndex, channelIndex, direction)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetSafeDirection_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "direction": direction})


def GetSafeDirection_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns the current safe direction

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetSafeDirection_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetSafeDirection_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def SetScale_A(deviceIndex, channelIndex, scale, inverted):
    """
    Configures the logical scale

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - scale: Scale shift relative to the positioner's physical scale
     - inverted: Scale inversion
    """
    local_0 = lib.SA_SetScale_A(deviceIndex, channelIndex, scale, inverted)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetScale_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "scale": scale, "inverted": inverted})


def GetScale_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns the current logical scale
    configuration

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetScale_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetScale_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def SetReportOnComplete_A(deviceIndex, channelIndex, report):
    """
    Defines whether or not to report completion of the last movement
    command

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - report: Enables/Disables Report On Complete
    """
    local_0 = lib.SA_SetReportOnComplete_A(deviceIndex, channelIndex, report)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetReportOnComplete_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "report": report})


def SetChannelProperty_A(deviceIndex, channelIndex, key, value):
    """
    Sets a channel specific property depending on the given key

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - key: Target property
     - value: Desired value
    """
    local_0 = lib.SA_SetChannelProperty_A(deviceIndex, channelIndex, key, value)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetChannelProperty_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "key": key, "value": value})


def GetChannelProperty_A(deviceIndex, channelIndex, key):
    """
    Sends a query to the channel that returns the selected property

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - key: Target property
    """
    local_0 = lib.SA_GetChannelProperty_A(deviceIndex, channelIndex, key)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetChannelProperty_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "key": key})


def SetSystemProperty_A(deviceIndex, key, value):
    """
    Sets a system specific property depending on the given key

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - key: Target property
     - value: Desired value
    """
    local_0 = lib.SA_SetSystemProperty_A(deviceIndex, key, value)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetSystemProperty_A", local_0, {"deviceIndex": deviceIndex, "key": key, "value": value})


def GetSystemProperty_A(deviceIndex, key):
    """
    Sends a query to the device that returns the selected property

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - key: Target property
    """
    local_0 = lib.SA_GetSystemProperty_A(deviceIndex, key)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetSystemProperty_A", local_0, {"deviceIndex": deviceIndex, "key": key})


def MoveStep_A(deviceIndex, channelIndex, steps, amplitude, frequency):
    """
    Performs a burst of steps with the given parameters

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - steps: Number and direction of steps to perform
     - amplitude: Amplitude that the steps are performed with
     - frequency: Frequency in Hz that the steps are performed with
    """
    local_0 = lib.SA_MoveStep_A(deviceIndex, channelIndex, steps, amplitude, frequency)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveStep_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "steps": steps, "amplitude": amplitude,
                     "frequency": frequency})


def SetAmplitude_A(deviceIndex, channelIndex, amplitude):
    """
    Presets the target channel's amplitude

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - amplitude: Amplitude in 1/10th Volts that should be preset
    """
    local_0 = lib.SA_SetAmplitude_A(deviceIndex, channelIndex, amplitude)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetAmplitude_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "amplitude": amplitude})


def MovePositionAbsolute_A(deviceIndex, channelIndex, position, holdTime):
    """
    Instructs a positioner to move to a specific position using closed-loop
     control

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - position: Absolute position to move to in 1/10th micro meters
     - holdTime: Time (in milliseconds) the position is actively held after
     reaching the target
    """
    local_0 = lib.SA_MovePositionAbsolute_A(deviceIndex, channelIndex, position, holdTime)
    if local_0 != ErrorCode.OK.value:
        raise Error("MovePositionAbsolute_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "position": position,
                     "holdTime": holdTime})


def MovePositionRelative_A(deviceIndex, channelIndex, diff, holdTime):
    """
    Instructs a positioner to move to a position relative to its current
    position using closed-loop control

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - diff: Relative position difference to move in 1/10th micro meters
     - holdTime: Time (in milliseconds) the position is actively held after
     reaching the target
    """
    local_0 = lib.SA_MovePositionRelative_A(deviceIndex, channelIndex, diff, holdTime)
    if local_0 != ErrorCode.OK.value:
        raise Error("MovePositionRelative_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "diff": diff, "holdTime": holdTime})


def MoveAngleAbsolute_A(deviceIndex, channelIndex, angle, revolution, holdTime):
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
    local_0 = lib.SA_MoveAngleAbsolute_A(deviceIndex, channelIndex, angle, revolution, holdTime)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveAngleAbsolute_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "angle": angle, "revolution": revolution,
                     "holdTime": holdTime})


def MoveAngleRelative_A(deviceIndex, channelIndex, angleDiff, revolutionDiff, holdTime):
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
    local_0 = lib.SA_MoveAngleRelative_A(deviceIndex, channelIndex, angleDiff, revolutionDiff, holdTime)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveAngleRelative_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "angleDiff": angleDiff,
                     "revolutionDiff": revolutionDiff, "holdTime": holdTime})


def CalibrateSensor_A(deviceIndex, channelIndex):
    """
    Starts the calibration procedure

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_CalibrateSensor_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("CalibrateSensor_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def MoveToReference_A(deviceIndex, channelIndex, holdTime, autoZero):
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
    local_0 = lib.SA_MoveToReference_A(deviceIndex, channelIndex, holdTime, autoZero)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveToReference_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "holdTime": holdTime,
                     "autoZero": autoZero})


def MoveToEndStop_A(deviceIndex, channelIndex, direction, holdTime, autoZero):
    """
    Moves the positioner to a mechanical end stop

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - direction: Specifies the movement direction
     - holdTime: Time (in milliseconds) the position/angle is actively held
     after reaching the end stop
     - autoZero: Selects whether the current positions is set to zero upon
    reaching the end stop
    """
    local_0 = lib.SA_MoveToEndStop_A(deviceIndex, channelIndex, direction, holdTime, autoZero)
    if local_0 != ErrorCode.OK.value:
        raise Error("MoveToEndStop_A", local_0,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "direction": direction,
                     "holdTime": holdTime, "autoZero": autoZero})


def Stop_A(deviceIndex, channelIndex):
    """
    Stops any ongoing movement of a positioner

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_Stop_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("Stop_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def GetStatus_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns the current movement status

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetStatus_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetStatus_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def GetAmplitude_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns the current step amplitude

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetAmplitude_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetAmplitude_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def GetPosition_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns the current position

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetPosition_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetPosition_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def GetAngle_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns the current angle

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetAngle_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetAngle_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def GetPhysicalPositionKnown_A(deviceIndex, channelIndex):
    """
    Sends a query to the channel that returns whether the positioner
    "knows" its physical position (has been referenced)

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
    """
    local_0 = lib.SA_GetPhysicalPositionKnown_A(deviceIndex, channelIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("GetPhysicalPositionKnown_A", local_0, {"deviceIndex": deviceIndex, "channelIndex": channelIndex})


def SetReceiveNotification_A(deviceIndex, event):
    """
    Specifies an event used to inform the application when a data packet
    has been received

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - event
    """
    local_0 = lib.SA_SetReceiveNotification_A(deviceIndex, event)
    if local_0 != ErrorCode.OK.value:
        raise Error("SetReceiveNotification_A", local_0, {"deviceIndex": deviceIndex, "event": event})


def ReceiveNextPacket_A(deviceIndex, timeout):
    """
    Receives a data packet from the device

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - timeout: Specifies how long (in milliseconds) to wait for incoming
    data

    Return value(s):
     - packet: Buffer for the received data packet
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[4])
    local_1 = lib.SA_ReceiveNextPacket_A(deviceIndex, timeout, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("ReceiveNextPacket_A", local_1, {"deviceIndex": deviceIndex, "timeout": timeout})
    return packet(None, None, None, None, None, local_0)


def ReceiveNextPacketIfChannel_A(deviceIndex, channelIndex, timeout):
    """
    Receives a data packet for the given channel

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - channelIndex: Selects the channel (zero-based)
     - timeout: Specifies how long (in milliseconds) to wait for incoming
    data

    Return value(s):
     - packet: Buffer for the received data packet
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[4])
    local_1 = lib.SA_ReceiveNextPacketIfChannel_A(deviceIndex, channelIndex, timeout, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("ReceiveNextPacketIfChannel_A", local_1,
                    {"deviceIndex": deviceIndex, "channelIndex": channelIndex, "timeout": timeout})
    return packet(None, None, None, None, None, local_0)


def LookAtNextPacket_A(deviceIndex, timeout):
    """
    Receives a data packet from the device without actually consuming it

    Parameters:
     - deviceIndex: Selects the device (zero-based)
     - timeout: Specifies how long (in milliseconds) to wait for incoming
    data

    Return value(s):
     - packet: Buffer for the received data packet
    """
    local_0 = ffi.new(_ffiApiGenCachedTypes[4])
    local_1 = lib.SA_LookAtNextPacket_A(deviceIndex, timeout, local_0)
    if local_1 != ErrorCode.OK.value:
        raise Error("LookAtNextPacket_A", local_1, {"deviceIndex": deviceIndex, "timeout": timeout})
    return packet(None, None, None, None, None, local_0)


def DiscardPacket_A(deviceIndex):
    """
    Discards a received data packet

    Parameters:
     - deviceIndex: Selects the device (zero-based)
    """
    local_0 = lib.SA_DiscardPacket_A(deviceIndex)
    if local_0 != ErrorCode.OK.value:
        raise Error("DiscardPacket_A", local_0, {"deviceIndex": deviceIndex})


class ApiVersion(enum.IntEnum):
    MAJOR = 0x01
    MINOR = 0x05
    UPDATE = 0x10


class Global(enum.IntEnum):
    FALSE = 0x0
    TRUE = 0x1
    SYNCHRONOUS_COMMUNICATION = 0x0
    ASYNCHRONOUS_COMMUNICATION = 0x1
    HARDWARE_RESET = 0x2
    NO_REPORT_ON_COMPLETE = 0x0
    REPORT_ON_COMPLETE = 0x1
    BACKWARD_DIRECTION = 0x0
    FORWARD_DIRECTION = 0x1
    NO_AUTO_ZERO = 0x0
    AUTO_ZERO = 0x1
    NO_SENSOR_PRESENT = 0x0
    SENSOR_PRESENT = 0x1
    PHYSICAL_POSITION_UNKNOWN = 0x0
    PHYSICAL_POSITION_KNOWN = 0x1


FALSE = Global.FALSE
TRUE = Global.TRUE
SYNCHRONOUS_COMMUNICATION = Global.SYNCHRONOUS_COMMUNICATION
ASYNCHRONOUS_COMMUNICATION = Global.ASYNCHRONOUS_COMMUNICATION
HARDWARE_RESET = Global.HARDWARE_RESET
NO_REPORT_ON_COMPLETE = Global.NO_REPORT_ON_COMPLETE
REPORT_ON_COMPLETE = Global.REPORT_ON_COMPLETE
BACKWARD_DIRECTION = Global.BACKWARD_DIRECTION
FORWARD_DIRECTION = Global.FORWARD_DIRECTION
NO_AUTO_ZERO = Global.NO_AUTO_ZERO
AUTO_ZERO = Global.AUTO_ZERO
NO_SENSOR_PRESENT = Global.NO_SENSOR_PRESENT
SENSOR_PRESENT = Global.SENSOR_PRESENT
PHYSICAL_POSITION_UNKNOWN = Global.PHYSICAL_POSITION_UNKNOWN
PHYSICAL_POSITION_KNOWN = Global.PHYSICAL_POSITION_KNOWN


class ErrorCode(enum.IntEnum):
    OK = 0x00
    INITIALIZATION_ERROR = 0x01
    NOT_INITIALIZED_ERROR = 0x02
    NO_DEVICES_FOUND_ERROR = 0x03
    TOO_MANY_DEVICES_ERROR = 0x04
    INVALID_DEVICE_INDEX_ERROR = 0x05
    INVALID_CHANNEL_INDEX_ERROR = 0x06
    TRANSMIT_ERROR = 0x07
    WRITE_ERROR = 0x08
    INVALID_PARAMETER_ERROR = 0x09
    READ_ERROR = 0x0a
    INTERNAL_ERROR = 0x0c
    WRONG_MODE_ERROR = 0x0d
    PROTOCOL_ERROR = 0x0e
    TIMEOUT_ERROR = 0x0f
    NOTIFICATION_ALREADY_SET_ERROR = 0x10
    ID_LIST_TOO_SMALL_ERROR = 0x11
    DEVICE_ALREADY_ADDED_ERROR = 0x12
    DEVICE_NOT_FOUND_ERROR = 0x13
    INVALID_COMMAND_ERROR = 0x80
    COMMAND_NOT_SUPPORTED_ERROR = 0x81
    NO_SENSOR_PRESENT_ERROR = 0x82
    WRONG_SENSOR_TYPE_ERROR = 0x83
    END_STOP_REACHED_ERROR = 0x84
    COMMAND_OVERRIDDEN_ERROR = 0x85
    HV_RANGE_ERROR = 0x86
    TEMP_OVERHEAT_ERROR = 0x87
    CALIBRATION_FAILED_ERROR = 0x88
    REFERENCING_FAILED_ERROR = 0x89
    NOT_PROCESSABLE_ERROR = 0x8a
    OTHER_ERROR = 0xff


class PacketType(enum.IntEnum):
    NO_PACKET = 0x00
    ERROR_PACKET = 0x01
    POSITION_PACKET = 0x02
    ANGLE_PACKET = 0x03
    COMPLETED_PACKET = 0x04
    STATUS_PACKET = 0x05
    CLOSED_LOOP_FREQUENCY_PACKET = 0x06
    SENSOR_TYPE_PACKET = 0x07
    SENSOR_PRESENT_PACKET = 0x08
    AMPLITUDE_PACKET = 0x09
    POSITIONER_ALIGNMENT_PACKET = 0x0a
    SAFE_DIRECTION_PACKET = 0x0b
    SCALE_PACKET = 0x0c
    PHYSICAL_POSITION_KNOWN_PACKET = 0x0d
    CHANNEL_PROPERTY_PACKET = 0x0e
    SYSTEM_PROPERTY_PACKET = 0x0f
    INVALID_PACKET = 0xff


class StatusCode(enum.IntEnum):
    STOPPED = 0x0
    SETTING_AMPLITUDE = 0x1
    MOVING = 0x2
    TARGETING = 0x3
    HOLDING = 0x4
    CALIBRATING = 0x5
    MOVING_TO_REFERENCE = 0x6


class SensorType(enum.IntEnum):
    M_SENSOR_TYPE = 0x01
    GA_SENSOR_TYPE = 0x02
    GB_SENSOR_TYPE = 0x03
    GC_SENSOR_TYPE = 0x04
    GD_SENSOR_TYPE = 0x05
    GE_SENSOR_TYPE = 0x06
    RA_SENSOR_TYPE = 0x07
    GF_SENSOR_TYPE = 0x08
    RB_SENSOR_TYPE = 0x09
    SR36M_SENSOR_TYPE = 0x0a
    SR36ME_SENSOR_TYPE = 0x0b
    SR50M_SENSOR_TYPE = 0x0c
    SR50ME_SENSOR_TYPE = 0x0d
    MM50_SENSOR_TYPE = 0x0e
    G935M_SENSOR_TYPE = 0x0f
    MD_SENSOR_TYPE = 0x10
    TT254_SENSOR_TYPE = 0x11
    LC_SENSOR_TYPE = 0x12
    LR_SENSOR_TYPE = 0x13
    LCD_SENSOR_TYPE = 0x14
    L_SENSOR_TYPE = 0x15
    LD_SENSOR_TYPE = 0x16
    LE_SENSOR_TYPE = 0x17
    LED_SENSOR_TYPE = 0x18
    SL_S1I1E1_POSITIONER_TYPE = 0x19
    SL_D1I1E1_POSITIONER_TYPE = 0x1a
    SL_S1I2E2_POSITIONER_TYPE = 0x1b
    SL_D1I2E2_POSITIONER_TYPE = 0x1c
    ST_S1I1E2_POSITIONER_TYPE = 0x1d
    ST_S1I2E2_POSITIONER_TYPE = 0x25
    SG_D1L1S_POSITIONER_TYPE = 0x1e
    SG_D1L1E_POSITIONER_TYPE = 0x1f
    SG_D1L2S_POSITIONER_TYPE = 0x20
    SG_D1L2E_POSITIONER_TYPE = 0x21
    SG_D1M1E_POSITIONER_TYPE = 0x22
    SG_D1M2E_POSITIONER_TYPE = 0x23
    SI_S1L1S_POSITIONER_TYPE = 0x24
    SR_T5L3S_POSITIONER_TYPE = 0x26
    SI_S1L4E_POSITIONER_TYPE = 0x27
    SI_S1L1E_POSITIONER_TYPE = 0x28
    SI_S1L3E_POSITIONER_TYPE = 0x29
    NO_SENSOR_TYPE = 0x00
    L180_SENSOR_TYPE = 0x01
    G180R435_SENSOR_TYPE = 0x02
    G180R560_SENSOR_TYPE = 0x03
    G50R85_SENSOR_TYPE = 0x04


class Alignment(enum.IntEnum):
    HORIZONTAL = 0x0
    VERTICAL = 0x1


class MovementType(enum.IntEnum):
    LINEAR = 0x0
    ROTARY = 0x1
    GONIOMETER = 0x2


class SystemProperty(enum.IntEnum):
    INTERNAL_TEMPERATURE = 0x1
    INTERNAL_VOLTAGE = 0x2
    HARDWARE_VERSION_CODE = 0x3


class ChannelProperty(enum.IntEnum):
    TARGET_REACHED_THRESHOLD = 0x03
    KP = 0x05
    KPD = 0x06
    DEFAULT_MAX_CLOSED_LOOP_FREQUENCY = 0x0f
    ADVANCED_STEPPING_MODE_ENABLED = 0x15
    MOVEMENT_TYPE = 0x19


import platform

__initBindings("SCU3DControl.dll" if platform.system() == "Windows" else ("lib" + "SCU3DControl".lower() + ".so"))


def __initFfiApiGenCachedTypes():
    global _ffiApiGenCachedTypes
    _ffiApiGenCachedTypes = [
        ffi.typeof("struct SA_packet *"),
        ffi.typeof("unsigned int *"),
        ffi.typeof("unsigned int []"),
        ffi.typeof("int *"),
        ffi.typeof("SA_PACKET *")]


__initFfiApiGenCachedTypes()
__all__ = ["api_version", "apigen_version", "Error", "packet", "GetDLLVersion", "GetAvailableDevices",
           "AddDeviceToInitDevicesList", "ClearInitDevicesList", "InitDevices", "ReleaseDevices", "GetNumberOfDevices",
           "GetDeviceID", "GetDeviceFirmwareVersion", "SetClosedLoopMaxFrequency_S", "GetClosedLoopMaxFrequency_S",
           "SetZero_S", "GetSensorPresent_S", "SetSensorType_S", "GetSensorType_S", "SetPositionerAlignment_S",
           "GetPositionerAlignment_S", "SetSafeDirection_S", "GetSafeDirection_S", "SetScale_S", "GetScale_S",
           "SetChannelProperty_S", "GetChannelProperty_S", "SetSystemProperty_S", "GetSystemProperty_S", "MoveStep_S",
           "SetAmplitude_S", "MovePositionAbsolute_S", "MovePositionRelative_S", "MoveAngleAbsolute_S",
           "MoveAngleRelative_S", "CalibrateSensor_S", "MoveToReference_S", "MoveToEndStop_S", "Stop_S", "GetStatus_S",
           "GetAmplitude_S", "GetPosition_S", "GetAngle_S", "GetPhysicalPositionKnown_S", "SetClosedLoopMaxFrequency_A",
           "GetClosedLoopMaxFrequency_A", "SetZero_A", "GetSensorPresent_A", "SetSensorType_A", "GetSensorType_A",
           "SetPositionerAlignment_A", "GetPositionerAlignment_A", "SetSafeDirection_A", "GetSafeDirection_A",
           "SetScale_A", "GetScale_A", "SetReportOnComplete_A", "SetChannelProperty_A", "GetChannelProperty_A",
           "SetSystemProperty_A", "GetSystemProperty_A", "MoveStep_A", "SetAmplitude_A", "MovePositionAbsolute_A",
           "MovePositionRelative_A", "MoveAngleAbsolute_A", "MoveAngleRelative_A", "CalibrateSensor_A",
           "MoveToReference_A", "MoveToEndStop_A", "Stop_A", "GetStatus_A", "GetAmplitude_A", "GetPosition_A",
           "GetAngle_A", "GetPhysicalPositionKnown_A", "SetReceiveNotification_A", "ReceiveNextPacket_A",
           "ReceiveNextPacketIfChannel_A", "LookAtNextPacket_A", "DiscardPacket_A", "ApiVersion", "FALSE", "TRUE",
           "SYNCHRONOUS_COMMUNICATION", "ASYNCHRONOUS_COMMUNICATION", "HARDWARE_RESET", "NO_REPORT_ON_COMPLETE",
           "REPORT_ON_COMPLETE", "BACKWARD_DIRECTION", "FORWARD_DIRECTION", "NO_AUTO_ZERO", "AUTO_ZERO",
           "NO_SENSOR_PRESENT", "SENSOR_PRESENT", "PHYSICAL_POSITION_UNKNOWN", "PHYSICAL_POSITION_KNOWN", "ErrorCode",
           "PacketType", "StatusCode", "SensorType", "Alignment", "MovementType", "SystemProperty", "ChannelProperty"]
