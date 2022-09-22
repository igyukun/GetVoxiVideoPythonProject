

# Calculates video engine (e.g. VOxI) command checksum
def calculate_checksum():

    # command including header, OpCode, data block size and the data block itself
    command = 'AA 16 85 04 00 10 00 00 00'
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
    print(f"checksum= {checksum}")
    print(f"Full command: {command} {checksum}")


calculate_checksum()