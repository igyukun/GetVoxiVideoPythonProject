import serial


def create_voxi_command(command_string):
    """
    Reseive the string command, calculate the checksum and create the bytearray ready to be written onto the serial port
    :param command_string: the command including header, OpCode, data block size and the data block itself in a string representation, where each byte is separated by whitespaces.
                           e.g. "aa 16 85 04 00 1f 00 00 00"
    :return: bytearray, including the hex formatted command with the calculated checksum
    """

    # split the command string into individual bytes
    command_list = command_string.split()
    # sum of all bytes in decimal scale
    sum_dec = 0
    # create an empty bytearray
    command_byte_array = bytearray()

    for i in range(len(command_list)):
        # iterate through the list of bytes and calculate the sum
        sum_dec = int(command_list[i], 16) + sum_dec
        # append each byte to the byte array
        command_byte_array.append(int('0x'+command_list[i],16))

    # calculate the checksum and represent it as an upper case Hex string without leading '0x'
    checksum = format((~(sum_dec % 256) + 1 + 256), 'x')
    # append the checksum to the byte array
    command_byte_array.append(int('0x'+ checksum, 16))
    # printout the results to the console
    print(f"checksum byte: {checksum}")
    print(f"Full command: {command_byte_array}")

    return command_byte_array

def send_serial_command(port, baudrate, command):
    """
    sendSerialCommand receives a serial connection parameters and writes a bytearray command to the port using 'serial' package
    :param port:        'COMX' for Windows, e.g. 'COM4'
                        device name for Linux, e.g: '/dev/ttyUSB0'
    :param baudrate:    Communication baud rate as defined in the VOXI configuration (default is 115200)
    :param command:     VOXI Command represented as bytearray
    :return:
    """
    #open the communication
    serialPort = serial.Serial(port=port, baudrate=baudrate, bytesize=8, write_timeout=2, timeout=2, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
    # write the command onto the port
    serialPort.write (create_voxi_command((command)))
    #close the port
    serialPort.close()


if __name__ == '__main__':

    command = 'aa 16 85 04 00 1f 00 00 00'
    send_serial_command('COM4',115200, command)
