import random
import time
import socket
import struct
import hashlib

ipAddress = '127.0.0.1'
port = 1337
responsePort = 1338
def delayGenerator(typeOfDelay, packetData=None):
    if typeOfDelay == 1:
        prob = random.choice([0, 0, 1, 1, 0, 0])
        if prob == 1:
            time.sleep(0.01)
            print("[DELAY] Network Loss has occured!")
            return(1)
        else:
            return(0)
    elif typeOfDelay == 2:
        prob = random.choice([0, 1, 0, 0, 0, 0])
        if prob == 1:
            time.sleep(0.01)
            print("[DELAY] Network Delay has occured!")
        else:
            print("[SUCCESS] Packet Sent")
    elif typeOfDelay == 3:
        prob = random.choice([0, 0, 1, 0, 1, 0])
        if prob == 1:
            time.sleep(0.01)
            print("[DELAY] The packet's checksum has been corrupted!")
            return (b'Checksum Corrupt')
        else:
            return (packetData)


# Creating & binding a socket for receiving packets
rcvrSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
rcvrSocket.bind((ipAddress, port))

print("[INFO] Listening for incoming connections on port {0}".format(port))

dataUnpacker = struct.Struct("I I 8s 32s")

responsePacker = struct.Struct('I I 32s')

while True:
    print("")
    print("########################################################")

    # Creating a socket for sending packets
    rspndrSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    data, addr = rcvrSocket.recvfrom(1024)
    thisPacket = dataUnpacker.unpack(data)

    # Display the received packet's data
    SEQ = thisPacket[1]

    print("Received packet data from client")
    print("ACK:", thisPacket[0])
    print("SEQ:", thisPacket[1])
    print("Checksum:", thisPacket[3])

    # Generate a checksum for the received packet
    values = (thisPacket[0], thisPacket[1], delayGenerator(3, thisPacket[2]))
    dataPacker = struct.Struct('I I 8s')
    convertedData = dataPacker.pack(*values)
    checkSum = bytes(hashlib.md5(convertedData).hexdigest(), encoding="UTF-8")

    if thisPacket[3] == checkSum:
        print("The checksum is correct!")
        if thisPacket[1] == 1:
            SEQ = 0
        else:
            SEQ = 1

        values = (thisPacket[0], SEQ)
        checksumPacker = struct.Struct('I I')
        checksumConverted = checksumPacker.pack(*values)
        checkSum = bytes(hashlib.md5(
            checksumConverted).hexdigest(), encoding="UTF-8")

        responseRaw = (thisPacket[0], SEQ, checkSum)
        responsePacket = responsePacker.pack(*responseRaw)

        delayGenerator(2)  # Randomly generate network delay
        delayGenerator(1)  # Randomly generate network loss delay
        rspndrSocket.sendto(responsePacket, (ipAddress, responsePort))
        rspndrSocket.close()

    else:
        print("The checksum is incorrect!")
        if thisPacket[0] == 1:
            ACK = 0
        else:
            ACK = 1

        print("Sending an acknowledgement to inform the sender that the packet is corrupt")
        values = (ACK, SEQ)
        checksumPacker = struct.Struct('I I')
        checksumConverted = checksumPacker.pack(*values)
        checkSum = bytes(hashlib.md5(
            checksumConverted).hexdigest(), encoding="UTF-8")

        # Create a response packet
        responseVal = (ACK, SEQ, checkSum)
        responsePacket = responsePacker.pack(*responseVal)

        delayGenerator(2)  # Randomly generate network delay
        delayGenerator(1)  # Randomly generate network loss delay

        rspndrSocket.sendto(responsePacket, (ipAddress, responsePort))
        rspndrSocket.close()
