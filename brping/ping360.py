#!/usr/bin/env python

# Ping1D.py
# A device API for the Blue Robotics Ping1D echosounder

# ~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!
# THIS IS AN AUTOGENERATED FILE
# DO NOT EDIT
# ~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!~!

from brping import pingmessage
import serial
import time
from device import PingDevice
import definitions

class Ping360(PingDevice):

    ##
    # @brief Get a device_data message from the device\n
    # Message description:\n
    # This message is used to communicate the current sonar state. If the data field is populated, the other fields indicate the sonar state when the data was captured. The time taken before the response to the command is sent depends on the difference between the last angle scanned and the new angle in the parameters as well as the number of samples and sample interval (range). To allow for the worst case reponse time the command timeout should be set to 4000 msec.
    #
    # @return None if there is no reply from the device, otherwise a dictionary with the following keys:\n
    # mode: Operating mode (1 for Ping360)\n
    # gain_setting: Analog gain setting (0 = low, 1 = normal, 2 = high)\n
    # angle: Units: gradian; Head angle\n
    # transmit_duration: Units: microsecond; Acoustic transmission duration (1~1000 microseconds)\n
    # sample_period: Time interval between individual signal intensity samples in 25nsec increments (80 to 40000 == 2 microseconds to 1000 microseconds)\n
    # transmit_frequency: Units: kHz; Acoustic operating frequency. Frequency range is 500kHz to 1000kHz, however it is only practical to use say 650kHz to 850kHz due to the narrow bandwidth of the acoustic receiver.\n
    # number_of_samples: Number of samples per reflected signal\n
    # data: 8 bit binary data array representing sonar echo strength\n
    def get_device_data(self):
        if self.request(definitions.PING360_DEVICE_DATA) is None:
            return None
        data = ({
            "mode": self._mode,  # Operating mode (1 for Ping360)
            "gain_setting": self._gain_setting,  # Analog gain setting (0 = low, 1 = normal, 2 = high)
            "angle": self._angle,  # Units: gradian; Head angle
            "transmit_duration": self._transmit_duration,  # Units: microsecond; Acoustic transmission duration (1~1000 microseconds)
            "sample_period": self._sample_period,  # Time interval between individual signal intensity samples in 25nsec increments (80 to 40000 == 2 microseconds to 1000 microseconds)
            "transmit_frequency": self._transmit_frequency,  # Units: kHz; Acoustic operating frequency. Frequency range is 500kHz to 1000kHz, however it is only practical to use say 650kHz to 850kHz due to the narrow bandwidth of the acoustic receiver.
            "number_of_samples": self._number_of_samples,  # Number of samples per reflected signal
            "data": self._data,  # 8 bit binary data array representing sonar echo strength
        })
        return Ping1Ddata

    ##
    # @brief Send a set_device_id message to the device\n
    # Message description:\n
    # Change the device id\n
    # Send the message to write the device parameters, then read the values back from the device\n
    #
    # @param id - Device ID (1-254). 0 and 255 are reserved.
    # @param reserved - reserved
    #
    # @return If verify is False, True on successful communication with the device. If verify is False, True if the new device parameters are verified to have been written correctly. False otherwise (failure to read values back or on verification failure)
    def set_device_id(self, id, reserved, verify=True):
        m = pingmessage.PingMessage(definitions.PING360_SET_DEVICE_ID)
        m.id = id
        m.reserved = reserved
        m.pack_msg_data()
        self.write(m.msg_data)
        if self.request(definitions.PING360_DEVICE_ID) is None:
            return False
        # Read back the data and check that changes have been applied
        if (verify
                and (self._id != id or self._reserved != reserved)):
            return False
        return True  # success        m.id = id
        m.reserved = reserved
        m.pack_msg_data()
        self.write(m.msg_data)


    def control_reset(self, bootloader, reserved):
        m = pingmessage.PingMessage(definitions.PING360_RESET)
        m.bootloader = bootloader
        m.reserved = reserved
        m.pack_msg_data()
        self.write(m.msg_data) 

    def control_transducer(self, mode, gain_setting, angle, transmit_duration, sample_period, transmit_frequency, number_of_samples, transmit, reserved):
        m = pingmessage.PingMessage(definitions.PING360_TRANSDUCER)
        m.mode = mode
        m.gain_setting = gain_setting
        m.angle = angle
        m.transmit_duration = transmit_duration
        m.sample_period = sample_period
        m.transmit_frequency = transmit_frequency
        m.number_of_samples = number_of_samples
        m.transmit = transmit
        m.reserved = reserved
        m.pack_msg_data()
        self.write(m.msg_data)
        return self.wait_message(definitions.PING360_DEVICE_DATA, 4.0)

    def transmit(self):
        return self.control_transducer(
            self.mode,
            self.gain_setting,
            self.angle,
            self.transmit_duration,
            self.sample_period,
            self.transmit_frequency,
            self.number_of_samples,
            1,
            0
        )

    def transmitAngle(self, angle):
        self.angle = angle
        return self.transmit()

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ping python library example.")
    parser.add_argument('--device', action="store", required=True, type=str, help="Ping device port.")
    parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate.")
    args = parser.parse_args()

    p = Ping360(args.device, args.baudrate)

    print("Initialized: %s" % p.initialize())
    print("\ntesting get_device_data")
    result = p.get_device_data()
    print("  " + str(result))
    print("  > > pass: %s < <" % (result is not None))


    p.mode = 1
    p.gain_setting = 0
    p.angle = 0
    p.transmit_duration = 100
    p.sample_period = 80
    p.transmit_frequency = 740
    p.number_of_samples = 200

    p.transmit()

    for x in range(400):
        print(p.transmitAngle(x))

    print(p)
