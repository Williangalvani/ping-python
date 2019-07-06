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
import definitions


class PingDevice(object):

    def __init__(self, device_name, baudrate=115200):
        if device_name is None:
            print("Device name is required")
            return

        try:
            print("Opening %s at %d bps" % (device_name, baudrate))

            ## Serial object for device communication
            self.iodev = serial.Serial(device_name, baudrate)
            self.iodev.timeout = 1
            self.iodev.send_break()
            self.iodev.write("U".encode("utf-8"))

        except Exception as e:
            print("Failed to open the given serial port")
            print("\t", e)
            exit(1)

        ## A helper class to take care of decoding the input stream
        self.parser = pingmessage.PingParser()

        ## device id of this Ping1D object, used for dst_device_id in outgoing messages
        self.my_id = 255

    ##
    # @brief Consume rx buffer data until a new message is successfully decoded
    #
    # @return A new PingMessage: as soon as a message is parsed (there may be data remaining in the buffer to be parsed, thus requiring subsequent calls to read())
    # @return None: if the buffer is empty and no message has been parsed
    def read(self):
        while self.iodev.in_waiting:
            b = self.iodev.read()

            if self.parser.parse_byte(ord(b)) == pingmessage.PingParser.NEW_MESSAGE:
                self.handle_message(self.parser.rx_msg)
                return self.parser.rx_msg
        return None

    ##
    # @brief Write data to device
    #
    # @param data: bytearray to write to device
    #
    # @return Number of bytes written
    def write(self, data):
        return self.iodev.write(data)

    ##
    # @brief Make sure there is a device on and read some initial data
    #
    # @return True if the device replies with expected data, False otherwise
    def initialize(self):
        return True

    ##
    # @brief Request the given message ID
    #
    # @param m_id: The message ID to request from the device
    # @param timeout: The time in seconds to wait for the device to send
    # the requested message before timing out and returning
    #
    # @return PingMessage: the device reply if it is received within timeout period, None otherwise
    #
    # @todo handle nack to exit without blocking
    def request(self, m_id, timeout=0.5):
        msg = pingmessage.PingMessage(definitions.COMMON_GENERAL_REQUEST)
        msg.requested_id = m_id
        msg.pack_msg_data()
        self.write(msg.msg_data)
        return self.wait_message(m_id, timeout)

    ##
    # @brief Wait until we receive a message from the device with the desired message_id for timeout seconds
    #
    # @param message_id: The message id to wait to receive from the device
    # @param timeout: The timeout period in seconds to wait
    #
    # @return PingMessage: the message from the device if it is received within timeout period, None otherwise
    def wait_message(self, message_id, timeout=0.5):
        tstart = time.time()
        while time.time() < tstart + timeout:
            msg = self.read()
            if msg is not None:
                if msg.message_id == message_id:
                    return msg
        return None

    ##
    # @brief Handle an incoming messge from the device.
    # Extract message fields into self attributes.
    #
    # @param msg: the PingMessage to handle.
    def handle_message(self, msg):
        if msg.message_id in pingmessage.payload_dict:
            for attr in pingmessage.payload_dict[msg.message_id]["field_names"]:
                setattr(self, "_" + attr, getattr(msg, attr))
        else:
            print("Unrecognized message: %d", msg)

    ##
    # @brief Dump object into string representation.
    #
    # @return string: a string representation of the object
    def __repr__(self):
        representation = "---------------------------------------------------------\n~Ping1D Object~"

        attrs = vars(self)
        for attr in sorted(attrs):
            try:
                if attr != 'iodev':
                    representation += "\n  - " + attr + "(hex): " + str([hex(item) for item in getattr(self, attr)])
                if attr != 'data':
                    representation += "\n  - " + attr + "(string): " + str(getattr(self, attr))
            # TODO: Better filter this exception
            except:
                representation += "\n  - " + attr + ": " + str(getattr(self, attr))
        return representation

    ##
    # @brief Get a device_information message from the device\n
    # Message description:\n
    # Device information
    #
    # @return None if there is no reply from the device, otherwise a dictionary with the following keys:\n
    # device_type: Device type. 0: Unknown; 1: Ping Echosounder; 2: Ping360\n
    # device_revision: device-specific hardware revision\n
    # firmware_version_major: Firmware version major number.\n
    # firmware_version_minor: Firmware version minor number.\n
    # firmware_version_patch: Firmware version patch number.\n
    # reserved: reserved\n
    def get_device_information(self):
        if self.request(pingmessage.PING1D_DEVICE_INFORMATION) is None:
            return None
        data = ({
            "device_type": self._device_type,  # Device type. 0: Unknown; 1: Ping Echosounder; 2: Ping360
            "device_revision": self._device_revision,  # device-specific hardware revision
            "firmware_version_major": self._firmware_version_major,  # Firmware version major number.
            "firmware_version_minor": self._firmware_version_minor,  # Firmware version minor number.
            "firmware_version_patch": self._firmware_version_patch,  # Firmware version patch number.
            "reserved": self._reserved,  # reserved
        })
        return data

    ##
    # @brief Get a protocol_version message from the device\n
    # Message description:\n
    # The protocol version
    #
    # @return None if there is no reply from the device, otherwise a dictionary with the following keys:\n
    # version_major: Protocol version major number.\n
    # version_minor: Protocol version minor number.\n
    # version_patch: Protocol version patch number.\n
    # reserved: reserved\n
    def get_protocol_version(self):
        if self.request(pingmessage.PING1D_PROTOCOL_VERSION) is None:
            return None
        data = ({
            "version_major": self._version_major,  # Protocol version major number.
            "version_minor": self._version_minor,  # Protocol version minor number.
            "version_patch": self._version_patch,  # Protocol version patch number.
            "reserved": self._reserved,  # reserved
        })
        return data


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Ping python library example.")
    parser.add_argument('--device', action="store", required=True, type=str, help="Ping device port.")
    parser.add_argument('--baudrate', action="store", type=int, default=115200, help="Ping device baudrate.")
    args = parser.parse_args()

    p = PingDevice(args.device, args.baudrate)

    print("Initialized: %s" % p.initialize())

    print("\ntesting get_device_information")
    result = p.get_device_information()
    print("  " + str(result))
    print("  > > pass: %s < <" % (result is not None))

    print("\ntesting get_protocol_version")
    result = p.get_protocol_version()
    print("  " + str(result))
    print("  > > pass: %s < <" % (result is not None))

    
    print(p)
