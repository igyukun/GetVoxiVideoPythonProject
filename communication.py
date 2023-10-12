import serial


# Calculates SCD detector or video engine (e.g. VOxI) command checksum
def calculate_checksum():

    # command including header, OpCode, data block size and the data block itself
    command = 'aa 16 85 04 00 1f 00 00 00'
    # split the command string into individual bytes
    com_hex = command.split()
    # sum of all bytes in decimal scale
    sum_dec = 0

    for i in range(len(com_hex)):
        # iterate through the list of bytes and calculate the sum
        sum_dec = int(com_hex[i], 16) + sum_dec

    # calculate the checksum and represent it as an upper case Hex string without leading '0x'
    checksum = format((~(sum_dec % 256) + 1 + 256), 'X')

    # printout the results to the console
    print(f"checksum byte: {checksum}")
    print(f"Full command: {command} {checksum}")


def sendSerialCommand(port, baudrate, command):
    """
    sendSerialCommand receives a serial connection parameters and writes a bytearray command to the port using 'serial' package
    :param port:        'COMX' for Windows or something like '/dev/ttyUSB0' for Linux
    :param baudrate:    Communication baud rate as defined in the VOXI configuration (default is 115200)
    :param command:     VOXI Command represented as bytearray
    :return:
    """
    serialPort = serial.Serial(port=port, baudrate=baudrate, bytesize=8, write_timeout=2, timeout=2, stopbits=serial.STOPBITS_ONE, parity=serial.PARITY_NONE)
    serialPort.write (command)

    commandReply = ''  # Used to hold data coming over UART
    serialPort.flush()
    while 1:
        commandReply = serialPort.readline()
        # Wait until there is data waiting in the serial buffer
        if serialPort.in_waiting > 0:

            # Read data out of the buffer until a carraige return / new line is found


            # Print the contents of the serial data
            if commandReply == '':
                serialPort.close()
                return "ERROR: NUC operation failed!"
        else:
            break

    serialPort.close()

def createNUCcmd ():
    packet = bytearray()
    packet.append(0xAA)
    packet.append(0x16)
    packet.append(0x85)
    packet.append(0x04)
    packet.append(0x00)
    packet.append(0x10)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0x00)
    packet.append(0xA7)
    return packet

if __name__ == '__main__':
    calculate_checksum()

