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

def __initFfiApiGenCachedTypes():
    global _ffiApiGenCachedTypes
    _ffiApiGenCachedTypes = [
        ffi.typeof("struct SA_packet *"),
        ffi.typeof("unsigned int *"),
        ffi.typeof("unsigned int []"),
        ffi.typeof("int *"),
        ffi.typeof("SA_PACKET *")]


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

class SmarActSCUWrapper:

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

